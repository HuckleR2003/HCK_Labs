# optim.py
"""
Optimizers and losses operating on Parameter (Value) objects.

Includes:
- Loss base class, MSELoss, CrossEntropyLoss (simple)
- Optimizer base class, SGD (momentum optional), Adam (bias-corrected)
Notes:
- This is implemented to work with scalar Value parameters (micrograd-style).
- State is keyed by id(param) to avoid accidental issues with Value hashing.
"""

from __future__ import annotations
from typing import List, Dict, Tuple
import math

from engine import Value, tensor_mean, tensor_sum
from nn import Parameter, stable_softmax

# -----------------------
# Losses
# -----------------------
class Loss:
    def __call__(self, preds: List[Value], targets: List[float]) -> Value:
        raise NotImplementedError

class MSELoss(Loss):
    """Mean squared error: mean((pred - target)^2)"""
    def __call__(self, preds: List[Value], targets: List[float]) -> Value:
        assert len(preds) == len(targets)
        losses = [(p - Value(t)) ** 2 for p, t in zip(preds, targets)]
        return tensor_mean(losses)

class CrossEntropyLoss(Loss):
    """
    Cross-entropy for logits + one-hot target:
    - compute softmax of logits (stable_softmax)
    - return mean(-sum(target_i * log(prob_i)))
    For simplicity, expect 'targets' as one-hot list or index-based form has to be adapted.
    """
    def __call__(self, logits: List[Value], targets: List[float]) -> Value:
        # assume targets is list with same length, containing 1.0 for true class else 0.0
        probs = stable_softmax(logits)
        losses = []
        for p, t in zip(probs, targets):
            if t == 1.0:
                # -log(p) for the true class
                losses.append(-(p.log()))
        return tensor_mean(losses)


# -----------------------
# Optimizer base + implementations
# -----------------------
class Optimizer:
    def __init__(self, params: List[Parameter], lr: float = 1e-3):
        self.params = list(params)
        self.lr = lr

    def step(self):
        raise NotImplementedError

    def zero_grad(self):
        for p in self.params:
            p.grad = 0.0

    def set_parameters(self, params: List[Parameter]):
        self.params = list(params)


class SGD(Optimizer):
    """
    SGD with optional momentum and weight_decay.
    Velocity stored per-param (keyed by id).
    """
    def __init__(self, params: List[Parameter], lr: float = 1e-2, momentum: float = 0.0, weight_decay: float = 0.0):
        super().__init__(params, lr)
        self.momentum = momentum
        self.weight_decay = weight_decay
        # velocity keyed by id
        self._vel: Dict[int, float] = {id(p): 0.0 for p in self.params}

    def step(self):
        for p in self.params:
            g = p.grad
            if self.weight_decay:
                g = g + self.weight_decay * p.data
            if self.momentum:
                v = self._vel.get(id(p), 0.0)
                v_new = self.momentum * v - self.lr * g
                self._vel[id(p)] = v_new
                p.data += v_new
            else:
                p.data += -self.lr * g


class Adam(Optimizer):
    """
    Adam optimizer (bias-corrected).
    State per param keyed by id(param): m, v. Time step t is global.
    """
    def __init__(self, params: List[Parameter], lr: float = 1e-3, betas: Tuple[float, float] = (0.9, 0.999), eps: float = 1e-8, weight_decay: float = 0.0):
        super().__init__(params, lr)
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self._m: Dict[int, float] = {id(p): 0.0 for p in self.params}
        self._v: Dict[int, float] = {id(p): 0.0 for p in self.params}
        self._t: int = 0

    def step(self):
        self._t += 1
        for p in self.params:
            g = p.grad
            if self.weight_decay:
                g = g + self.weight_decay * p.data
            pid = id(p)
            m = self._m.get(pid, 0.0)
            v = self._v.get(pid, 0.0)
            m = self.beta1 * m + (1 - self.beta1) * g
            v = self.beta2 * v + (1 - self.beta2) * (g * g)
            self._m[pid] = m
            self._v[pid] = v
            # bias correction
            m_hat = m / (1 - self.beta1 ** self._t)
            v_hat = v / (1 - self.beta2 ** self._t)
            step = - self.lr * m_hat / (math.sqrt(v_hat) + self.eps)
            p.data += step
