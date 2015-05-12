from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


def render_COM(skel):
    glPushMatrix()
    glColor3d(1.0, 0.0, 0.0)
    glTranslated(*skel.C)
    glutSolidSphere(0.05, 4, 2)
    glPopMatrix()


def render_point(x, color, size=0.05):
    glPushMatrix()
    glColor3d(*color)
    glTranslated(*x)
    glutSolidSphere(size, 4, 2)
    glPopMatrix()


def render_line(x, y, color):
    glPushMatrix()
    glColor3d(*color)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex3d(*x)
    glVertex3d(*y)
    glEnd()
    glPopMatrix()


def render_skeleton_shadow(skel):
    glPushMatrix()
    M_s = [1.0, 0.0, 0.0, 0.0,
           1.0, 0.0, -1.0, 0.0,
           0.0, 0.0, 1.0, 0.0,
           0.0, -0.001, 0.0, 1.0]
    glMultMatrixf(M_s)
    glColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_LIGHTING)
    skel.render_with_color(0.0, 0.0, 0.0)
    glEnable(GL_LIGHTING)
    glPopMatrix()


def render_floor(n, sz):
    glPushMatrix()
    glTranslated(0.0, -0.01, 0.0)
    glDisable(GL_LIGHTING)
    cnt = 0
    step = sz / float(n)
    glColor(0.86, 0.86, 0.76)
    for x in np.linspace(-0.5 * sz, 0.5 * sz, n, endpoint = False):
        for z in np.linspace(-0.5 * sz, 0.5 * sz, n, endpoint = False):
            x2 = x + step
            z2 = z + step

            glBegin(GL_POLYGON)
            glVertex([x, 0, z])
            glVertex([x, 0, z2])
            glVertex([x2, 0, z2])
            glVertex([x2, 0, z])
            glEnd()
            cnt += 1
        cnt += 1

    glEnable(GL_LIGHTING)
    glPopMatrix()


def render_chessboard(n, sz):
    glPushMatrix()
    glTranslated(0.0, -0.01, 0.0)
    glDisable(GL_LIGHTING)
    cnt = 0
    step = sz / float(n)
    for x in np.linspace(-0.5 * sz, 0.5 * sz, n, endpoint = False):
        for z in np.linspace(-0.5 * sz, 0.5 * sz, n, endpoint = False):
            x2 = x + step
            z2 = z + step
            if cnt % 2 == 0:
                glColor(0.2, 0.2, 0.2)
            else:
                glColor(0.8, 0.8, 0.8)

            glBegin(GL_POLYGON)
            glVertex([x, 0, z])
            glVertex([x, 0, z2])
            glVertex([x2, 0, z2])
            glVertex([x2, 0, z])
            glEnd()
            cnt += 1
        cnt += 1

    glEnable(GL_LIGHTING)
    glPopMatrix()


def render_trajectory(pts, color):
    glPushMatrix()
    glColor3d(*color)
    glLineWidth(2.0)
    # glBegin(GL_LINES)
    glBegin(GL_LINE_STRIP)
    for pt in pts:
        glVertex3d(*pt)
    glEnd()
    glPopMatrix()
