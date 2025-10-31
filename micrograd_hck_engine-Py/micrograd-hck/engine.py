# engine.py
"""
Lightweight scalar autograd engine (micrograd-inspired).

Core features:
- Value: scalar value with .data, .grad, autograd history and backward propagation
- Elementary ops: +, -, *, /, pow, exp, log, tanh, relu, sigmoid
- Topological backward pass
- Small helpers for working with lists of Values (tensor_sum, tensor_mean)

Design goals:
- Pedagogical: easy to read, well-commented
- Dependency-free (only stdlib: math, random)
- Safe numeric choices (small eps where needed)
- Works well as an educational baseline for building tiny neural nets
"""

from __future__ import annotations
from typing import Callable, List, Set, Tuple, Iterable, Optional
import math
import random

EPS = 1e-12  # small epsilon to improve numerical stability where needed


class Value:
    """
    Scalar value with autograd.

    Attributes:
      data: float (the scalar value)
      grad: float (accumulated gradient, d(output)/d(this node))
      _prev: set of parent Value nodes (inputs)
      _op: string label of operation creating this Value (for debugging/visualization)
      _backward: callable that populates parents' .grad from this node's .grad

    Usage:
      a = Value(2.0)
      b = Value(3.0)
      c = a * b + b
      c.backward()
      # now a.grad, b.grad filled
    """
    __slots__ = ("data", "grad", "_prev", "_op", "_backward", "label")

    def __init__(self, data: float, _children: Tuple['Value', ...] = (), _op: str = '', label: str = ''):
        self.data: float = float(data)
        self.grad: float = 0.0
        self._prev: Set[Value] = set(_children)
        self._op: str = _op
        # filled by each op to propagate gradients to parents
        self._backward: Callable[[], None] = lambda: None
        self.label: str = label

    def __repr__(self):
        return f"Value(data={self.data:.6f}, grad={self.grad:.6f}, op={self._op})"

    # -----------------------
    # Utility / conversion
    # -----------------------
    @staticmethod
    def _ensure_value(other) -> 'Value':
        return other if isinstance(other, Value) else Value(other)

    def detach(self) -> 'Value':
        """Return a new Value with same numeric data but no history."""
        return Value(self.data)

    def __float__(self):
        return float(self.data)

    # -----------------------
    # Arithmetic operators
    # -----------------------
    def __add__(self, other):
        other = self._ensure_value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            # d/dx (x+y) = 1, d/dy (x+y) = 1
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        out = Value(-self.data, (self,), 'neg')

        def _backward():
            self.grad += -1.0 * out.grad
        out._backward = _backward
        return out

    def __sub__(self, other):
        other = self._ensure_value(other)
        return self + (-other)

    def __rsub__(self, other):
        other = self._ensure_value(other)
        return other - self

    def __mul__(self, other):
        other = self._ensure_value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            # d/dx (x*y) = y, d/dy (x*y) = x
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        other = self._ensure_value(other)
        # x / y = x * y^{-1}
        return self * (other ** -1)

    def __rtruediv__(self, other):
        other = self._ensure_value(other)
        return other / self

    def __pow__(self, exponent):
        assert isinstance(exponent, (int, float)), "Only constant powers supported for simplicity"
        out = Value(self.data ** exponent, (self,), f'**{exponent}')

        def _backward():
            # handle zero/near-zero numerics gracefully
            if self.data == 0.0 and exponent - 1 < 0:
                # avoid infinite gradient for 0 ** negative
                grad_local = 0.0
            else:
                grad_local = exponent * (self.data ** (exponent - 1))
            self.grad += grad_local * out.grad
        out._backward = _backward
        return out

    # -----------------------
    # Elementary math
    # -----------------------
    def exp(self):
        out_data = math.exp(self.data)
        out = Value(out_data, (self,), 'exp')

        def _backward():
            # derivative of e^x is e^x
            self.grad += out_data * out.grad
        out._backward = _backward
        return out

    def log(self):
        # natural log with epsilon guard
        safe = self.data if self.data > EPS else EPS
        out = Value(math.log(safe), (self,), 'log')

        def _backward():
            self.grad += (1.0 / safe) * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), 'tanh')

        def _backward():
            self.grad += (1.0 - t * t) * out.grad
        out._backward = _backward
        return out

    def relu(self):
        out_data = self.data if self.data > 0 else 0.0
        out = Value(out_data, (self,), 'relu')

        def _backward():
            self.grad += (1.0 if self.data > 0 else 0.0) * out.grad
        out._backward = _backward
        return out

    def sigmoid(self):
        # implemented via composition for correctness (and automatic gradients)
        out = 1.0 / (1.0 + (-self).exp())
        out._op = 'sigmoid'
        return out

    # -----------------------
    # Backpropagation
    # -----------------------
    def backward(self):
        """
        Run reverse-mode autodiff.

        Builds topological order of the graph (DFS) then runs _backward in reverse.
        After this call, every node's .grad contains d(self)/d(node) where self is the
        original Value this method was called on.
        """
        topo: List[Value] = []
        visited: Set[Value] = set()

        def build(v: Value):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build(child)
                topo.append(v)

        build(self)

        # zero grads first (avoids accidental accumulation)
        for node in topo:
            node.grad = 0.0
        self.grad = 1.0

        for node in reversed(topo):
            node._backward()

# -----------------------
# Helpers (work with lists of Value)
# -----------------------
def tensor_sum(values: Iterable[Value]) -> Value:
    s = Value(0.0)
    for v in values:
        s = s + v
    return s

def tensor_mean(values: Iterable[Value]) -> Value:
    vals = list(values)
    if len(vals) == 0:
        return Value(0.0)
    return tensor_sum(vals) * (1.0 / len(vals))


# -----------------------
# Example quick test (toy regression)
# -----------------------
if __name__ == "__main__":
    # Simple sanity check: gradient of f(x,y) = (x*y) + y at x=2,y=3
    x = Value(2.0, label="x")
    y = Value(3.0, label="y")
    z = x * y + y
    z.backward()
    print("z:", z)
    print("dz/dx (should be y=3):", x.grad)
    print("dz/dy (should be x+1=3):", y.grad)
