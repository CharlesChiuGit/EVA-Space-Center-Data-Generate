import json
import math
import random
import time
import ntpath
from OpenGL.GL import *
from OpenGL.GLU import *
from config import *
import shutil
# Import Objloader & Pygame
from objloader import OBJ
import pygame
from pygame.constants import *
from pygame.locals import *
# Import from generate_dataset.py
from generate_dataset import set_viewport, set_light_property, set_filed_of_vision


def remove_filename_extension(base_name):
    file_name = os.path.splitext(base_name)[0]

    return file_name


def remove_extra_path(extra_path):
    image_name = extra_path.split('/')[-1]

    return image_name


def read_json(file_path):
    with open(file_path, 'r') as reader:
        data = json.loads(reader.read())

    return data.keys(), data


def path_leaf(path):
    head, tail = ntpath.split(path)

    return tail or ntpath.basename(head)


def find_defect_image_target_value(defect_image):
    label_path = os.path.join(PATH, 'target_' + TARGET_INDEX + '.json')
    with open(label_path, 'r') as reader:
        data = json.loads(reader.read())
    [c_x, c_y, c_z, p_x, p_y, p_z, u_x, u_y, u_z] = data[defect_image]['cartesian']

    return c_x, c_y, c_z, p_x, p_y, p_z, u_x, u_y, u_z


if __name__ == '__main__':
    # PYGAME
    pygame.init()
    srf = set_viewport(VIEWPORT[0], VIEWPORT[1])
    # LOAD OBJECT AFTER PYGAME INIT
    obj = OBJ(OBJECT, swapyz=True)
    clock = pygame.time.Clock()
    # set up OPENGL env
    light_position = (-40, 200, 100, 0.0)
    set_light_property(light_position)
    set_filed_of_vision(FOVY, VIEWPORT, Z_NEAR, Z_FAR)
    # create image
    sample_target = {}
    part_start = time.time()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Defect image cartesian coordinate parameters
    defect_image_with_png = remove_extra_path(DEFECT_IMAGE)
    defect_image = remove_filename_extension(defect_image_with_png)
    c_x, c_y, c_z, p_x, p_y, p_z, u_x, u_y, u_z = find_defect_image_target_value(defect_image)

    # take the shoot
    logging.info('Start regenerating defect image ' + defect_image)
    print(c_x, c_y, c_z, p_x, p_y, p_z, u_x, u_y, u_z)
    gluLookAt(c_x, c_y, c_z, p_x, p_y, p_z, u_x, u_y, u_z)
    glCallList(obj.gl_list)

    # Move old defect image to /home/eva/space_center/moon_8K/Regen_Image/defect_image/
    defect_path = shutil.move(DEFECT_IMAGE, DEFECT_PATH)
    logging.info('{} move to {}'.format(DEFECT_IMAGE, DEFECT_PATH))

    # SAVE regenerated image
    # srf2 = srf
    pygame.image.save(srf, os.path.join(PATCH_PATH, defect_image + '.png'))
    pygame.image.save(srf, DEFECT_IMAGE)
    logging.info('Finish creating defect image, time = {}'.format(time.time() - part_start))
