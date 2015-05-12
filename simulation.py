import logging
import math
import numpy as np
import pydart
from controller import Controller
import gltools
from motion import Motion
# from guppy import hpy


class Simulation(object):
    def __init__(self, step_activation=None):
        self.prefix = ''
        self.postfix = ''
        self.logger = logging.getLogger(__name__)
        logger = self.logger
        # Init pydart
        pydart.init()
        logger.info('pydart initialization OK')

        # Create world
        self.world = pydart.create_world(1.0 / 1000.0)
        self.world.add_skeleton("./data/sdf/ground.urdf", control=False)
        self.world.add_skeleton("./data/urdf/BioloidGP/BioloidGP.URDF")
        logger.info('pydart create_world OK: dt = %f' % self.world.dt)

        # Configure human
        self.skel = self.world.skels[1]
        for i, body in enumerate(self.skel.bodies):
            self.logger.info('%d: %s' % (i, body.name))
        for i, dof in enumerate(self.skel.dofs):
            self.logger.info('%d: %s' % (i, dof.name))

        # Create the controller
        self.skel.controller = Controller(self,
                                          self.skel,
                                          self.world.dt)

        # Create the motion
        self.motion = Motion(self.skel)

        logger.info('set the initial pose OK')
        self.reset()

    def reset(self):
        q = np.zeros(self.skel.ndofs)
        q[0] = -0.50 * math.pi
        q[4] = 0.294 + 0.0 / math.sqrt(2) * (10.0 / 9.0)
        q[5] = q[4]
        self.skel.q = q
        self.skel.qdot = np.zeros(self.skel.ndofs)

        self.skel.controller.reset()
        self.world.reset()
        self.logger.info('reset OK')

    def step(self):
        # Find the corresponding target pose
        wt = float(self.world.t)
        for i in range(len(self.motion)):
            t = self.motion.durations[i]
            q = self.motion.poses[i]
            wt -= t
            if wt < 0.0:
                self.skel.controller.qhat = q
                break

        self.world.step()

    def num_frames(self):
        return self.world.num_frames()

    def set_frame(self, idx):
        self.world.set_frame(idx)

    def render(self):
        # gltools.render_COM(self.skel)
        gltools.render_chessboard(10, 20.0)
        # gltools.render_floor(20, 40.0)
        gltools.render_skeleton_shadow(self.skel)
        self.skel.render()

    def contacts(self):
        return self.world.contacts()

    def key_pressed(self, key):
        self.logger.info('key pressed: [%s]' % key)

    def title(self, full=True):
        return 'BioloidGP app'
