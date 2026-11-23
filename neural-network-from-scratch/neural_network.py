"""
Neural network from scratch — no deep-learning framework involved.

A small multilayer perceptron (64 -> 32 -> 10) written in pure NumPy:
forward pass, backprop, and mini-batch gradient descent are all coded by
hand here. scikit-learn is used ONLY to load the dataset — the network
itself never touches it.

Dataset: the classic handwritten digits (sklearn's `load_digits`) — 1,797
real 8x8 images of handwritten digits, 10 classes. Features are
standardised; the data is split 80/20 into train/test.

What it plots:
  * loss_curve.png       — training loss and test accuracy over epochs
  * loss_landscape.png   — the loss surface around the trained weights,
                           with the path gradient descent actually took
                           through it drawn on top
  * predictions.png      — a few test digits with predicted vs true labels

The loss landscape is drawn the way the literature does it: pick two random
directions in weight space, scale each layer's direction to the size of that
layer's trained weights, then evaluate the loss on a grid of
theta* + alpha * d1 + beta * d2. The gradient-descent path is the training
trajectory projected onto the same two directions.

Run it:
    python neural_network.py
    python neural_network.py --epochs 80 --hidden 48 --lr 0.05

Outputs (in this folder): loss_curve.png, loss_landscape.png, predictions.png
"""

import argparse

import matplotlib

matplotlib.use("Agg")  # headless: save figures, don't try to open a window
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0, x)


def softmax(z: np.ndarray) -> np.ndarray:
    z = z - z.max(axis=1, keepdims=True)  # numerical stability
    exp_z = np.exp(z)
    return exp_z / exp_z.sum(axis=1, keepdims=True)


class MLP:
    """Two-layer perceptron: input -> hidden (ReLU) -> output (softmax).

    All parameters live in one dict so they can be flattened into a single
    vector for the loss-landscape plot.
    """

    def __init__(self, n_in: int, n_hidden: int, n_out: int, seed: int = 0):
        rng = np.random.default_rng(seed)
        # He initialisation for the ReLU layer, small weights for the output.
        self.params = {
            "W1": rng.normal(0, np.sqrt(2 / n_in), (n_in, n_hidden)),
            "b1": np.zeros(n_hidden),
            "W2": rng.normal(0, np.sqrt(1 / n_hidden), (n_hidden, n_out)),
            "b2": np.zeros(n_out),
        }

    def forward(self, x: np.ndarray):
        """Return class probabilities, caching the intermediates for backprop."""
        z1 = x @ self.params["W1"] + self.params["b1"]
        a1 = relu(z1)
        z2 = a1 @ self.params["W2"] + self.params["b2"]
        return softmax(z2), (x, z1, a1)

    def loss_and_grads(self, x: np.ndarray, y_onehot: np.ndarray):
        """Cross-entropy loss and its gradients for one mini-batch."""
        n = len(x)
        probs, (x_in, z1, a1) = self.forward(x)
        loss = -np.log(probs[np.arange(n), y_onehot.argmax(axis=1)] + 1e-12).mean()

        dz2 = (probs - y_onehot) / n
        grads = {
            "W2": a1.T @ dz2,
            "b2": dz2.sum(axis=0),
        }
        da1 = dz2 @ self.params["W2"].T
        dz1 = da1 * (z1 > 0)
        grads["W1"] = x_in.T @ dz1
        grads["b1"] = dz1.sum(axis=0)
        return loss, grads

    def predict(self, x: np.ndarray) -> np.ndarray:
        probs, _ = self.forward(x)
        return probs.argmax(axis=1)

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        return float((self.predict(x) == y).mean())

    def flat_params(self) -> np.ndarray:
        return np.concatenate([self.params[k].ravel() for k in
                               ("W1", "b1", "W2", "b2")])

    def set_flat_params(self, vec: np.ndarray) -> None:
        i = 0
        for key in ("W1", "b1", "W2", "b2"):
            size = self.params[key].size
            self.params[key] = vec[i:i + size].reshape(self.params[key].shape)
            i += size


def train(model: MLP, x_train, y_train_onehot, epochs: int, batch_size: int,
          lr: float, seed: int = 0):
    """Mini-batch SGD. Returns the loss history and a parameter snapshot
    every 2 epochs (the trajectory gradient descent took)."""
    rng = np.random.default_rng(seed)
    n = len(x_train)
    history, trajectory = [], []
    for epoch in range(epochs):
        order = rng.permutation(n)
        epoch_loss = 0.0
        for start in range(0, n, batch_size):
            idx = order[start:start + batch_size]
            loss, grads = model.loss_and_grads(x_train[idx], y_train_onehot[idx])
            epoch_loss += loss * len(idx)
            for key in model.params:
                model.params[key] -= lr * grads[key]
        history.append(epoch_loss / n)
        if epoch % 2 == 0:
            trajectory.append(model.flat_params())
    trajectory.append(model.flat_params())
    return history, trajectory


def loss_landscape(model: MLP, x_sub, y_sub_onehot, trajectory,
                   grid: int = 21, span: float = 1.0, seed: int = 1):
    """Evaluate the loss on a 2D slice through weight space around the
    trained weights, and project the training trajectory onto the same plane.

    Each layer's random direction is scaled to the norm of that layer's
    trained weights, so a step of 1.0 in either direction is a meaningful
    perturbation of the network (not dominated by one layer).
    """
    theta_star = model.flat_params()
    rng = np.random.default_rng(seed)
    directions = []
    for key in ("W1", "b1", "W2", "b2"):
        d = rng.normal(size=model.params[key].shape)
        d *= np.linalg.norm(model.params[key]) / (np.linalg.norm(d) + 1e-12)
        directions.append(d.ravel())
    d1 = np.concatenate(directions)
    rng2 = np.random.default_rng(seed + 1)
    directions = []
    for key in ("W1", "b1", "W2", "b2"):
        d = rng2.normal(size=model.params[key].shape)
        d *= np.linalg.norm(model.params[key]) / (np.linalg.norm(d) + 1e-12)
        directions.append(d.ravel())
    d2 = np.concatenate(directions)
    # Make the two directions orthogonal so the plot axes are independent.
    d2 = d2 - (d1 @ d2) / (d1 @ d1) * d1
    d2 *= np.linalg.norm(d1) / (np.linalg.norm(d2) + 1e-12)

    alphas = np.linspace(-span, span, grid)
    betas = np.linspace(-span, span, grid)
    surface = np.zeros((grid, grid))
    probe = MLP(64, model.params["W1"].shape[1], 10)  # same shape, reused
    for i, a in enumerate(alphas):
        for j, b in enumerate(betas):
            probe.set_flat_params(theta_star + a * d1 + b * d2)
            loss, _ = probe.loss_and_grads(x_sub, y_sub_onehot)
            surface[j, i] = loss

    path = np.array([[ (t - theta_star) @ d1, (t - theta_star) @ d2]
                     for t in trajectory])
    return alphas, betas, surface, path


def plot_loss_curve(history, snapshot_epochs, test_acc, path: str) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(history, lw=2)
    ax1.set_title("Training loss (cross-entropy)")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.grid(alpha=0.3)
    ax2.plot(snapshot_epochs, test_acc, lw=2, color="green")
    ax2.set_title("Test accuracy")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy")
    ax2.set_ylim(0.5, 1.0)
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"Saved: {path}")


def plot_landscape(alphas, betas, surface, path, out: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 7))
    levels = np.linspace(surface.min(), min(surface.max(), surface.min() + 2.0), 18)
    ax.contourf(alphas, betas, surface, levels=levels, cmap="viridis")
    ax.contour(alphas, betas, surface, levels=levels, colors="white",
               linewidths=0.4, alpha=0.5)
    ax.plot(path[:, 0], path[:, 1], "o-", color="red", ms=4, lw=1.5,
            label="gradient descent path")
    ax.plot(path[0, 0], path[0, 1], "o", color="white", ms=9, label="start")
    ax.plot(path[-1, 0], path[-1, 1], "*", color="yellow", ms=16, label="trained weights")
    ax.set_title("Loss landscape around the trained weights\n"
                 "(red: the path gradient descent took)")
    ax.set_xlabel("Random direction 1")
    ax.set_ylabel("Random direction 2")
    ax.legend(fontsize=9, loc="upper right")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"Saved: {out}")


def plot_predictions(x_test_raw, y_test, y_pred, path: str, n: int = 12) -> None:
    rng = np.random.default_rng(7)
    idx = rng.choice(len(x_test_raw), size=n, replace=False)
    fig, axes = plt.subplots(3, 4, figsize=(9, 8))
    for ax, i in zip(axes.ravel(), idx):
        ax.imshow(x_test_raw[i].reshape(8, 8), cmap="gray")
        correct = y_pred[i] == y_test[i]
        color = "green" if correct else "red"
        ax.set_title(f"pred {y_pred[i]}, true {y_test[i]}", color=color, fontsize=10)
        ax.axis("off")
    fig.suptitle("Test digits — predicted vs true label", fontsize=13)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"Saved: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a neural net from scratch.")
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--hidden", type=int, default=32)
    parser.add_argument("--lr", type=float, default=0.1)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    digits = load_digits()
    x_raw, y = digits.data, digits.target
    print(f"Dataset: sklearn digits — {len(x_raw)} real handwritten digit images "
          f"({x_raw.shape[1]} pixels each), {len(np.unique(y))} classes.")

    x_train_raw, x_test_raw, y_train, y_test = train_test_split(
        x_raw, y, test_size=0.2, random_state=42, stratify=y)
    # Standardise using the training set only.
    mean, std = x_train_raw.mean(axis=0), x_train_raw.std(axis=0) + 1e-8
    x_train = (x_train_raw - mean) / std
    x_test = (x_test_raw - mean) / std
    y_train_onehot = np.eye(10)[y_train]

    model = MLP(n_in=64, n_hidden=args.hidden, n_out=10)
    print(f"Network: 64 -> {args.hidden} (ReLU) -> 10 (softmax), "
          f"pure NumPy, {args.epochs} epochs of mini-batch SGD.")
    history, trajectory = train(model, x_train, y_train_onehot,
                                epochs=args.epochs, batch_size=args.batch_size,
                                lr=args.lr)
    test_acc_history = []
    # Test accuracy at each recorded trajectory point (every 2 epochs).
    probe = MLP(64, args.hidden, 10)
    snapshot_epochs = list(range(0, args.epochs, 2)) + [args.epochs - 1]
    for theta in trajectory:
        probe.set_flat_params(theta)
        test_acc_history.append(probe.accuracy(x_test, y_test))

    final_acc = model.accuracy(x_test, y_test)
    print(f"Final train loss: {history[-1]:.4f} "
          f"(started at {history[0]:.4f}); test accuracy: {final_acc:.1%}")

    plot_loss_curve(history, snapshot_epochs, test_acc_history, "loss_curve.png")

    # Loss landscape on a 500-sample subset (fast, still representative).
    rng = np.random.default_rng(0)
    sub = rng.choice(len(x_train), size=500, replace=False)
    alphas, betas, surface, path = loss_landscape(
        model, x_train[sub], y_train_onehot[sub], trajectory)
    plot_landscape(alphas, betas, surface, path, "loss_landscape.png")

    plot_predictions(x_test_raw, y_test, model.predict(x_test), "predictions.png")
    print("Done.")


if __name__ == "__main__":
    main()
