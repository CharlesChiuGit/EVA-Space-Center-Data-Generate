# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import json
import math
import pygame
import random
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from config import *
# IMPORT OBJECT LOADER
from objloader import OBJ
from pygame.constants import *
from pygame.locals import *


def check_directory(directory):
    directory_path = os.path.join(PATH, directory)
    if not os.path.exists(directory_path):
        logging.info('Create directory {}'.format(directory))
        os.makedirs(directory_path)


def normalize(coord):
    temp = [0,0,0]
    temp[0] = coord[0]
    temp[1] = coord[1]
    temp[2] = coord[2]
    l = (temp[0]**2 + temp[1]**2 + temp[2]**2) ** 0.5
    temp[0] /= l
    temp[1] /= l
    temp[2] /= l
    return temp


def crossf(a,b):
    temp = [0,0,0]
    temp[0] = a[1]*b[2] - a[2]*b[1]
    temp[1] = a[2]*b[0] - a[0]*b[2]
    temp[2] = a[0]*b[1] - a[1]*b[0]
    return temp


def set_viewport(viewport_width, viewport_hight):
    """
    Set view port.
    :return: surface(PYGAME image)
    """
    logging.info('Start setting viewport')
    viewport = (viewport_width, viewport_hight)
    srf = pygame.display.set_mode(viewport, pygame.OPENGL | pygame.DOUBLEBUF)

    return srf


def set_light_property():
    """
    Set light poroperty.
    """
    logging.info('Start setting light property')
    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))


def set_filed_of_vision(fovy, viewport, zNear, zFar):
    """
    Set FOV.
    :param fovy: The field of view angle, in degrees, in the y direction.
    :param viewport:
    :param zNear: The distance from the viewer to the near clipping plane (always positive).
    :param zFar: The distance from the viewer to the far clipping plane (always positive).
    """
    logging.info('Start setting FOV')
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(fovy, width / float(height), zNear, zFar)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)


def ball_coordinates_to_cassette_coordinates(gamma, theta, phi):
    """
    In physics order: (gamma, theta, phi)
    Transfer Ball coordinates to Cassette coordinates.
    """
    x = gamma * math.sin(theta) * math.cos(phi)
    y = gamma * math.sin(theta) * math.sin(phi)
    z = gamma * math.cos(theta)

    return x, y, z


def set_camera_position(lower_bound, upper_bound):
    """
    Set camera position. c_gamma, c_theta, c_phi are sampled with random.uniform in their own range.
    """
    # c_gamma = random.uniform(lower_bound, upper_bound)
    # c_theta = math.acos(1 - 2 * random.uniform(0, 1))
    # c_phi = 2 * math.pi * random.uniform(0, 1)
    c_gamma = upper_bound
    c_theta, c_phi = 0, 0
    c_x, c_y, c_z = ball_coordinates_to_cassette_coordinates(c_gamma, c_theta, c_phi)

    return c_gamma, c_theta, c_phi, c_x, c_y, c_z


def set_optical_axis_look_at(moon_radius):
    """
    Set optical axis' end point. p_gamma, p_theta, p_phi are sampled with random.uniform in their own range.
    """
    # p_gamma = random.uniform(0, 0.5 * moon_radius)  # no influences
    p_gamma = 0
    p_theta = math.acos(1 - 2 * random.uniform(0, 1))
    p_phi = 2 * math.pi * random.uniform(0, 1)
    # p_theta, p_phi = 0.5*math.pi, math.pi
    p_x, p_y, p_z = ball_coordinates_to_cassette_coordinates(p_gamma, p_theta, p_phi)

    return p_gamma, p_theta, p_phi, p_x, p_y, p_z


def camera_direction(c_x, c_y, c_z, p_x, p_y, p_z):
    """
    Set direction of the camera.
    """
    forward = [0, 0, 0]
    up = [0, 0, 0]
    camera_position = [c_x, c_y, c_z]
    optical_axis_position = [p_x, p_y, p_z]
    for i in range(3):
        forward[i] = optical_axis_position[i] - camera_position[i]
        # up[i] = random.uniform(0, 1)
    up = [0, 1, 0]  # for Dataset_six_random

    norm_forward = normalize(forward)
    side = normalize(crossf(norm_forward, up))
    up = normalize(crossf(side, norm_forward))

    return up[0], up[1], up[2]


if __name__ == '__main__':
    # PYGAME
    pygame.init()
    srf = set_viewport(VIEWPORT[0], VIEWPORT[1])
    # LOAD OBJECT AFTER PYGAME INIT
    obj = OBJ(OBJECT, swapyz=True)
    clock = pygame.time.Clock()
    # set up OPENGL env
    set_light_property()
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded
    set_filed_of_vision(FOVY, VIEWPORT, Z_NEAR, Z_FAR)
    # create image
    for i in range(LEVEL_1_INDEX):
        sample_target = {}
        # sample_image = {}
        logging.info('Start creating Part_{}'.format(i))
        part_start = time.time()
        level_l_directory = '{}'.format(i)
        check_directory(level_l_directory)
        for j in range(LEVEL_2_INDEX):
            level_2_directory = os.path.join(level_l_directory, '{}_{}'.format(i, j))
            check_directory(level_2_directory)
            for k in range(IMAGE_INDEX):  # make 1000 images
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glLoadIdentity()

                # CAMERA location
                c_gamma, c_theta, c_phi, c_x, c_y, c_z = set_camera_position(LOWER_BOUND, UPPER_BOUND)
                # WHERE does camera look at
                p_gamma, p_theta, p_phi, p_x, p_y, p_z = set_optical_axis_look_at(MOON_RADIUS)
                # DIRECTION of camera
                u_x, u_y, u_z = camera_direction(c_x, c_y, c_z, p_x, p_y, p_z)
                # take the shoot
                gluLookAt(c_x, c_y, c_z, p_x, p_y, p_z, u_x, u_y, u_z)
                glCallList(obj.gl_list)

                # SAVE target and image
                img_name = DATASET_NAME + '_{}'.format((i * IMAGE_INDEX * LEVEL_2_INDEX) + (j * IMAGE_INDEX) + k)
                # sample_image[img_name] = img.tolist()
                sample_target[img_name] = {}
                sample_target[img_name]['spherical'] = [c_gamma, c_theta, c_phi, p_gamma, p_theta, p_phi, u_x, u_y, u_z]
                sample_target[img_name]['cartesian'] = [c_x, c_y, c_z, p_x, p_y, p_z, u_x, u_y, u_z]
                pygame.image.save(srf, os.path.join(PATH, level_2_directory, img_name + '.png'))

        logging.info('Finish creating Part_{}, time = {}'.format(i, (time.time() - part_start)))
        logging.info('Start saving target_{}'.format(i))
        with open(os.path.join(PATH, 'target_{}.json'.format(i)), 'a') as f:
            json.dump(sample_target, f)
        logging.info('Finish saving target_{}'.format(i))
