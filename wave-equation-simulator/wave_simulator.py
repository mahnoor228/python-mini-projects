"""
Wave equation simulator — a vibrating drum skin.

Solves the damped 2D wave equation on a square grid with finite differences:

    u_tt + gamma * u_t = c^2 * (u_xx + u_yy)

with fixed (zero) edges, like a drum skin clamped to its rim. The skin is
"struck" with a Gaussian bump at the start, then the ripples spread, reflect
off the edges, interfere with each other, and slowly die away because of the
damping term.

Numerical scheme (explicit, second order in time and space):

    u_next = 2u - u_prev + r^2 * Laplacian(u) - gamma * dt * (u - u_prev)

where r = c * dt / dx is the Courant number. The scheme is stable when
r <= 1 / sqrt(2) in 2D (the CFL condition) — the default dt is chosen
well inside that limit.

Run it:
    python wave_simulator.py              # default: 300 steps, 80x80 grid
    python wave_simulator.py --steps 500 --damping 0.02

Outputs (in this folder):
    drum_animation.gif   — animated 3D surface of the vibrating skin
    drum_snapshots.png   — the skin at four moments in time
"""

import argparse

import matplotlib

matplotlib.use("Agg")  # headless: save figures, don't try to open a window
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter


def laplacian(u: np.ndarray) -> np.ndarray:
    """5-point discrete Laplacian of the interior of the grid."""
    lap = np.zeros_like(u)
    lap[1:-1, 1:-1] = (
        u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * u[1:-1, 1:-1]
    )
    return lap


def initial_condition(n: int) -> np.ndarray:
    """The "strike": a tall Gaussian bump in the centre plus a smaller
    off-centre one, so the ripples interfere instead of staying symmetric."""
    y, x = np.mgrid[0:n, 0:n]
    bump = lambda cx, cy, amp, sigma: amp * np.exp(
        -((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigma**2)
    )
    u = bump(n / 2, n / 2, 1.0, n / 12) + bump(n / 4, n * 3 / 4, 0.5, n / 16)
    u[0, :] = u[-1, :] = u[:, 0] = u[:, -1] = 0.0  # clamped rim
    return u


def simulate(n: int = 80, steps: int = 300, c: float = 1.0,
             damping: float = 0.01, dt: float = 0.4) -> list[np.ndarray]:
    """Run the simulation and return a snapshot of the skin every 5 steps.

    The Courant number r = c * dt / dx is 0.4 here (dx = 1), safely below
    the 2D stability limit of 1 / sqrt(2) ≈ 0.707.
    """
    r = c * dt  # dx = 1
    assert r <= 1 / np.sqrt(2), f"Unstable: Courant number {r:.2f} > 0.707"

    u = initial_condition(n)
    u_prev = u.copy()  # skin starts at rest: u_t = 0 at t = 0

    frames = [u.copy()]
    peak_amplitudes = [float(np.abs(u).max())]
    for _ in range(steps):
        u_next = 2 * u - u_prev + r**2 * laplacian(u) - damping * dt * (u - u_prev)
        u_next[0, :] = u_next[-1, :] = u_next[:, 0] = u_next[:, -1] = 0.0
        u_prev, u = u, u_next
        peak_amplitudes.append(float(np.abs(u).max()))
        if len(peak_amplitudes) % 5 == 0:
            frames.append(u.copy())

    print(f"Peak amplitude: {peak_amplitudes[0]:.3f} at t=0 "
          f"-> {peak_amplitudes[-1]:.3f} after {steps} steps "
          f"(damping {damping} drains the energy).")
    return frames


def plot_frame(ax, u: np.ndarray, title: str) -> None:
    """Draw one 3D surface view of the skin."""
    n = u.shape[0]
    # Plot every 2nd grid point: identical shape, ~4x faster to draw.
    x, y = np.meshgrid(np.arange(0, n, 2), np.arange(0, n, 2))
    ax.plot_surface(x, y, u[::2, ::2], cmap="viridis", linewidth=0,
                    antialiased=False)
    ax.set_zlim(-1.1, 1.1)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("height")
    ax.view_init(elev=28, azim=-120)


def save_animation(frames: list[np.ndarray], path: str) -> None:
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    writer = PillowWriter(fps=12)

    with writer.saving(fig, path, dpi=90):
        for i, u in enumerate(frames):
            ax.clear()
            plot_frame(ax, u, f"Vibrating drum skin — frame {i + 1}/{len(frames)}")
            writer.grab_frame()
    plt.close(fig)
    print(f"Saved animation: {path} ({len(frames)} frames)")


def save_snapshots(frames: list[np.ndarray], path: str) -> None:
    picks = [0, len(frames) // 3, 2 * len(frames) // 3, len(frames) - 1]
    fig = plt.figure(figsize=(10, 9))
    for k, idx in enumerate(picks):
        ax = fig.add_subplot(2, 2, k + 1, projection="3d")
        plot_frame(ax, frames[idx], f"Frame {idx + 1} of {len(frames)}")
    fig.suptitle("Damped wave equation — the drum skin over time", fontsize=13)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    print(f"Saved snapshots: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate a vibrating drum skin.")
    parser.add_argument("--grid", type=int, default=80, help="grid size (default 80)")
    parser.add_argument("--steps", type=int, default=300, help="time steps (default 300)")
    parser.add_argument("--damping", type=float, default=0.01,
                        help="damping coefficient (default 0.01)")
    args = parser.parse_args()

    frames = simulate(n=args.grid, steps=args.steps, damping=args.damping)
    save_animation(frames, "drum_animation.gif")
    save_snapshots(frames, "drum_snapshots.png")
    print("Done.")


if __name__ == "__main__":
    main()
