# micrograd - engine Py HCK
___A compact educational autograd engine, by Marcin "HuckleR" Firmuga (HCK)___

**Status:** Early development  
**Created:** 2025-10-26

## What is this?
A minimal, well-documented autograd engine implemented in plain Python + NumPy.
The goal is to *teach* how automatic differentiation works by implementing:
- scalar and tensor values with gradients,
- computational graph creation,
- backward propagation (reverse-mode AD),
- small MLP training example (from-scratch).

This repository is intentionally small and readable — suitable for code reviews and portfolio presentation.

## Motivation
Large frameworks hide the mechanics behind many layers. By building a minimal engine we:
- learn the core math behind backpropagation,
- get hands-on experience with numerical stability,
- improve intuition about gradients, shapes, and optimization loops.

## Project structure
│micrograd - engine Py HCK/
│
│
├── README.md - this file
├── CHANGELOG.md - project-specific changelog
│
├── src/
│ ├── engine.py - Value/Tensor class, op implementations, autograd core
│ ├── nn.py - small layers (Linear, ReLU, MLP)
│ └── optim.py - simple SGD/Adam implementations
│
├── notebooks/
│ └── demo.ipynb - step-by-step demo & visualizations
│
├── docs/
│ └── design_notes.md - design choices, math derivations, diagrams
│
├── tests/
│ └── test_engine.py - unit tests for core ops
│
├── data/
│ └── tiny_dataset.csv - toy dataset for examples (kept tiny for repo)
│
├── examples/
└── train_mlp.py - runnable example training a tiny MLP

__________________
│#################
│ License - Contact
│ MIT
├──── Marcin "HuckleR" Firmuga - HCK
│
├─ LinkedIn: https://www.linkedin.com/in/marcin-firmuga-a665471a3 
└─ Github: https://github.com/HuckleR2003