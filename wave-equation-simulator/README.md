# Wave Equation Simulator

A vibrating drum skin, simulated from first principles. The skin starts with a
Gaussian "strike" and then ripples, reflects off the clamped rim, interferes
with itself, and slowly dies away through damping.

## The physics

The damped 2D wave equation:

```
u_tt + gamma * u_t = c^2 * (u_xx + u_yy)
```

solved with an explicit finite-difference scheme (second order in time and
space) on an 80×80 grid with fixed zero edges. The Courant number
`r = c * dt / dx = 0.4` sits safely below the 2D stability limit of
`1 / sqrt(2) ≈ 0.707` (the CFL condition).

This is a **numerical simulation**, not measured data — the "data" here is the
solution of a PDE.

## What it demonstrates

- Finite-difference methods for PDEs
- The CFL stability condition
- Wave reflection, interference, and damping
- 3D animation with Matplotlib

## How to run

```bash
pip install -r requirements.txt
python wave_simulator.py                 # defaults: 300 steps, 80x80 grid
python wave_simulator.py --steps 500 --damping 0.02
```

## Output

- `drum_animation.gif` — animated 3D surface of the vibrating skin
- `drum_snapshots.png` — the skin at four moments in time

The peak amplitude printed at the end shows the damping draining the energy
from the skin over time.
