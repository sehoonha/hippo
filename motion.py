import logging
import numpy as np
from pydart import SkelVector
import gp


class Motion(object):
    def __init__(self, skel):
        self.logger = logging.getLogger(__name__)

        self.skel = skel
        self.poses = []
        self.durations = []

        q = SkelVector(skel.q, skel)

        self.initpose = q

        # The first pose
        self.add_pose(q, 0.5)

        # The second pose
        q['l_thigh'] += 0.7
        q['l_shin'] -= 1.0
        q['l_heel'] += 1.0
        self.add_pose(q, 0.4)

    def __len__(self):
        return len(self.durations)

    def add_pose(self, q, t):
        self.poses.append(np.array(q))
        self.durations.append(t)

    def export_mtn(self, output_filename):
        self.logger.info('export_mtn: %s' % output_filename)

        mm = gp.MotorMap()
        mm.load('data/urdf/BioloidGP/BioloidGPMotorMap.xml')
        self.logger.info('export_mtn: creating motormap OK')

        motion = gp.Motion(mm)
        motion.add_page('Init', [self.initpose], [1.0])
        motion.add_page('MyMotion', self.poses, self.durations)
        motion.fill_with_empty_pages()
        self.logger.info('export_mtn: creating motion OK')
        motion.save(output_filename)
        self.logger.info('export_mtn: save OK')
