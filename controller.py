import numpy as np
from numpy.linalg import inv
from jacobian_transpose import JTController


class Controller:
    """ Add damping force to the skeleton """
    def __init__(self, sim, skel, h):
        self.sim = sim
        self.h = h
        self.skel = skel

        # Spring-damper
        ndofs = self.skel.ndofs
        self.qhat = self.skel.q
        self.qdhat = np.zeros(ndofs)

        self.Kp = np.diagflat([0.0] * 6 + [60.0] * (ndofs - 6))
        self.Kd = np.diagflat([0.0] * 6 + [3.0] * (ndofs - 6))
        self.tau_lo = np.array([0.0] * 6 + [-1.0] * (ndofs - 6))
        self.tau_hi = np.array([0.0] * 6 + [1.0] * (ndofs - 6))

        # Jacobian transpose
        self.jt = JTController(self.skel)
        self.reset()

    def reset(self):
        pass

    def compute(self):
        skel = self.skel

        invM = inv(skel.M + self.Kd * self.h)
        p = -self.Kp.dot(skel.q + skel.qdot * self.h - self.qhat)
        d = -self.Kd.dot(skel.qdot - self.qdhat)
        qddot = invM.dot(-skel.c + p + d + skel.constraint_forces())
        tau = p + d - self.Kd.dot(qddot) * self.h

        # Make sure the first six are zero
        tau = np.maximum(tau, self.tau_lo)
        tau = np.minimum(tau, self.tau_hi)
        return tau
