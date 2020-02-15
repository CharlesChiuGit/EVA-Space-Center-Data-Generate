import paramiko
import json
import ntpath
import os
from config import *


# File operation related
def remove_filename_extension(file_name):
    base_name = os.path.splitext(file_name)[0]

    return base_name


def remove_extra_path(extra_path):
    file_name = extra_path.split('/')[-1]

    return file_name


def get_image_index(image_name):
    image_index = image_name.split('_')[-1]

    return image_index


def read_json(file_path):
    with open(file_path, 'r') as reader:
        data = json.loads(reader.read())

    return data.keys(), data


def path_leaf(path):
    head, tail = ntpath.split(path)

    return tail or ntpath.basename(head)


def check_directory(directory):
    directory_path = os.path.join(PATH, directory)
    if not os.path.exists(directory_path):
        logging.info('Create directory {}'.format(directory))
        os.makedirs(directory_path)


# SSH related
def send_command_to_remote_device(command_list):
    private_key = paramiko.RSAKey.from_private_key_file("/home/charleschiu/.ssh/eva_58")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("140.113.86.59", 22, "eva", pkey=private_key)
    for command in command_list:
        print("Executing {}".format(command))
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.readlines())
        print("Errors:")
        print(stderr.readlines())
    ssh.close()


def build_session(remote_ip, remote_user):
    private_key = paramiko.RSAKey.from_private_key_file("/home/charleschiu/.ssh/eva_58")
    transport = paramiko.Transport((remote_ip, 22))
    transport.connect(username=remote_user, pkey=private_key)
    sftp = paramiko.SFTPClient.from_transport(t)
    return transport, sftp


def upload_file_to_remote_device(remote_path, local_path):
    remote_ip, remote_user = "140.113.86.59", "eva"
    transport, sftp = build_session(remote_ip, remote_user)
    sftp.put(local_path, remote_path)
    transport.close()


def download_file_from_remote_device(remote_path, local_path):
    remote_ip, remote_user = "140.113.86.59", "eva"
    transport, sftp = build_session(remote_ip, remote_user)
    sftp.get(remote_path, local_path)
    transport.close()
