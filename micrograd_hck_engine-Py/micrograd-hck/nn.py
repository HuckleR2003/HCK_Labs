# nn.py
"""
Small neural network building blocks that use engine.Value.

Contents:
- Parameter: alias of Value intended to be optimized (keeps code semantic)
- Module: base class for modules (parameters(), zero_grad())
- Linear: fully-connected layer implemented with scalar Values
- MLP: sequential MLP (list of Linears + activations)
- utility activations & stable_softmax

Design notes:
- This module retains scalar Value operations (no numpy) for pedagogical clarity.
- We keep weight initialization sensible (Xavier/He) to help training stability.
"""

from __future__ import annotations
from typing import List, Callable, Optional, Iterable
import math
import random

from engine import Value, tensor_sum, tensor_mean

# Parameter is a semantic alias; we may extend it later (requires_grad etc.)
Parameter = Value


# -----------------------
# Weight initializers
# -----------------------
def xavier_uniform(n_in: int, n_out: int) -> List[Parameter]:
    bound = math.sqrt(6.0 / (n_in + n_out))
    return [Parameter(random.uniform(-bound, bound)) for _ in range(n_in)]

def kaiming_uniform(n_in: int) -> List[Parameter]:
    bound = math.sqrt(2.0 / n_in)
    return [Parameter(random.uniform(-bound, bound)) for _ in range(n_in)]


# -----------------------
# Module base class
# -----------------------
class Module:
    def parameters(self) -> List[Parameter]:
        """Return a flat list of parameters (Parameter/Value) in this module."""
        return []

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0.0


# -----------------------
# Linear (fully connected) layer
# -----------------------
class Linear(Module):
    """
    Linear layer: out_i = sum_j W[i][j] * x[j] + b[i]

    We store weights as List[List[Parameter]] where weights[out][in].
    Bias is optional and default-initialized to zeros.
    """
    def __init__(self, in_features: int, out_features: int, bias: bool = True, initializer: Callable = xavier_uniform):
        self.in_features = in_features
        self.out_features = out_features
        # initialize per-row (each output neuron has its own weight vector)
        self.W: List[List[Parameter]] = [
            initializer(in_features, out_features) if initializer is xavier_uniform else initializer(in_features)
            for _ in range(out_features)
        ]
        # use zero biases by default
        self.b: Optional[List[Parameter]] = [Parameter(0.0) for _ in range(out_features)] if bias else None

    def __call__(self, x: List[Value]) -> List[Value]:
        if len(x) != self.in_features:
            raise ValueError(f"Linear expected input length {self.in_features}, got {len(x)}")
        out: List[Value] = []
        for i in range(self.out_features):
            # dot product (weights row dot x) + bias
            s = tensor_sum(w * xi for w, xi in zip(self.W[i], x))
            if self.b is not None:
                s = s + self.b[i]
            out.append(s)
        return out

    def parameters(self) -> List[Parameter]:
        params: List[Parameter] = []
        for row in self.W:
            params.extend(row)
        if self.b is not None:
            params.extend(self.b)
        return params


# -----------------------
# MLP (stacked Linear + activations)
# -----------------------
class MLP(Module):
    """
    Simple MLP. 'sizes' is sequence of layer sizes, e.g. [in_dim, h1, h2, out_dim].
    activation: 'tanh'|'relu'|'sigmoid'|'linear'
    final_activation: activation for last layer (default 'linear')
    """
    def __init__(self, sizes: List[int], activation: str = 'tanh', final_activation: str = 'linear'):
        assert len(sizes) >= 2, "sizes must have at least [in, out]"
        self.layers: List[Linear] = []
        self.activation = activation
        self.final_activation = final_activation

        # create layers
        for i in range(len(sizes) - 1):
            in_f, out_f = sizes[i], sizes[i + 1]
            # use kaiming for hidden (works well with relu/tanh), xavier for output
            init = kaiming_uniform if i < len(sizes) - 2 else xavier_uniform
            self.layers.append(Linear(in_f, out_f, bias=True, initializer=init))

    def __call__(self, x: List[Value]) -> List[Value]:
        out = x
        for idx, layer in enumerate(self.layers):
            out = layer(out)
            # choose activation
            act = self.final_activation if idx == len(self.layers) - 1 else self.activation
            if act == 'tanh':
                out = [v.tanh() for v in out]
            elif act == 'relu':
                out = [v.relu() for v in out]
            elif act == 'sigmoid':
                out = [v.sigmoid() for v in out]
            elif act == 'linear':
                pass
            else:
                raise ValueError(f"Unknown activation: {act}")
        return out

    def parameters(self) -> List[Parameter]:
        params: List[Parameter] = []
        for layer in self.layers:
            params.extend(layer.parameters())
        return params


# -----------------------
# Softmax (stable) - returns list of probabilities (Value)
# -----------------------
def stable_softmax(logits: List[Value]) -> List[Value]:
    """
    Numerically stable softmax:
      softmax(x)_i = exp(x_i - max(x)) / sum_j exp(x_j - max(x))
    Works with Value objects (builds computational graph).
    """
    if not logits:
        return []

    # find max by numeric comparison on .data (we keep max as Value from inputs so graph can use it)
    max_val = logits[0]
    for v in logits[1:]:
        max_val = max_val if max_val.data >= v.data else v

    exps = [(v - max_val).exp() for v in logits]
    denom = tensor_sum(exps)
    probs = [e / denom for e in exps]
    return probs


# -----------------------
# Convenience: convert floats to Value list
# -----------------------
def to_values(xs: Iterable[float]) -> List[Value]:
    return [Value(x) for x in xs]


# -----------------------
# Example usage (brief)
# -----------------------
if __name__ == "__main__":
    # tiny sanity check: MLP 2 -> 4 -> 1 on random input
    model = MLP([2, 4, 1], activation='tanh', final_activation='linear')
    x = to_values([0.5, -1.2])
    y = model(x)
    print("output (Value):", y)
    params = model.parameters()
    print("num params:", len(params))
