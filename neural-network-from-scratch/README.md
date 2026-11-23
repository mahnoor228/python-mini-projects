# Neural Network from Scratch

A small multilayer perceptron (64 → 32 → 10) written in **pure NumPy** —
forward pass, backprop, and mini-batch gradient descent are all coded by
hand. No PyTorch, no TensorFlow, no Keras.

scikit-learn is used **only to load the dataset**. The network itself never
touches it.

## The data

The classic handwritten digits dataset (`sklearn.datasets.load_digits`):
**1,797 real 8×8 images of handwritten digits**, 10 classes, split 80/20
into train/test (stratified). Features are standardised using the training
set only. Nothing is synthetic.

## The network

- Input: 64 pixels → hidden layer of 32 units (ReLU) → 10 outputs (softmax)
- Loss: cross-entropy, optimised with mini-batch SGD (batch 32, lr 0.1)
- He initialisation for the ReLU layer
- Default: 60 epochs, reaching roughly 95%+ test accuracy

## What the plots show

- `loss_curve.png` — training loss and test accuracy over epochs
- `loss_landscape.png` — the loss surface on a 2D slice through weight
  space around the trained weights, with the red line showing the actual
  path gradient descent took to get there. The slice is built the way the
  literature does it: two random directions, each layer's direction scaled
  to the norm of that layer's trained weights, then the loss evaluated on a
  grid of `theta* + alpha·d1 + beta·d2`.
- `predictions.png` — test digits with predicted vs true labels

## How to run

```bash
pip install -r requirements.txt
python neural_network.py
python neural_network.py --epochs 80 --hidden 48 --lr 0.05
```
