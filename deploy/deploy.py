# TODO: Somebody make this look more pretty

import sys
import os
import os.path
# TODO: potentially rewrite to use argparse
# import argparse
import pathlib
import subprocess
import digitalocean
import paramiko
import socket
import traceback
import errno
import logging
from binascii import hexlify
import getpass

# Create droplet on digital ocean
def create_droplet():
    droplet = digitalocean.Droplet(token='2b63ea6b8711ce73ee616872c31b7e6dab2b2c1b1690e000b9b60e20f66c9d2e',
                                   name='ff-staging.com',
                                   region='sfo2',
                                   size='s-1vcpu-1gb',
                                   image='coreos-stable',
                                   ssh_keys=['29:78:b3:d0:b7:40:d0:5f:05:f8:22:9c:16:f3:f8:f5',
                                             '4a:11:e3:b9:7e:b1:3c:76:f2:80:22:28:67:15:82:45'],
                                   ipv6=False,
                                   user_data=None,
                                   private_networking=None,
                                   backups=False)
    droplet.create()
    return droplet


# Check if droplet is fully created
def wait_for_ip(droplet):
    # Check if droplet is created
    actions = droplet.get_actions()
    for action in actions:
        # Wait for droplet to be completed
        action.wait()
        print('Droplet created.')

        # Load additional data for droplet after creation
        droplet.load()
        print(droplet.ip_address)

        return droplet.ip_address


def save_ip_to_file(ip_address):
    # TODO: duplicate code
    path_to_save = pathlib.Path(__file__).parent / 'tmp'
    print(path_to_save)
    file_to_open = 'ip_address.txt'
    mkdir_p(path_to_save)
    with safe_open_w(path_to_save / file_to_open) as f:
        f.write(ip_address)


def get_ip_from_file():
    # TODO: duplicate code
    path_to_open = pathlib.Path(__file__).parent / 'tmp'
    file_to_open = 'ip_address.txt'
    with open(path_to_open / file_to_open, 'r') as f:
        ip_address = f.read()
        return ip_address


def deploy_to_droplet(client):
    print("*** Here we go!\n")

    source_dir = './'
    dest_dir = '/home/core'

    put(client, source_dir, dest_dir)

    (stdin, stdout, stderr) = client.exec_command('sudo bash /home/core/start.sh -s')
    stdout = stdout.readlines()
    print(stdout)


def add_to_hosts(ip_address):
    bash_command = 'ssh-keyscan -H {ip_address} >> ~/.ssh/known_hosts'
    process = subprocess.Popen(bash_command, shell=True)
    output, error = process.communicate()
    if error:
      print(error)
    else:
      print(output)


def connect_to_client(ip_address):
    hostname = ip_address
    port = 22
    username = 'core'
    password = ''

    try:
        client = paramiko.SSHClient()

        try:
            client.load_host_keys(
                os.path.expanduser("~/.ssh/known_hosts")
            )
        except IOError:
            try:
                client.load_host_keys(
                    os.path.expanduser("~/ssh/known_hosts")
                )
            except IOError:
                print("*** Unable to open host keys file")

        client.connect(hostname, port, username=username, password=password)
        return client

    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        logging.debug(e)
        traceback.print_exc()
        try:
            client.close()
        except:
            pass

    sys.exit(1)


# https://stackoverflow.com/questions/46005883/copying-directories-using-paramiko-sftp
def put(client, localpath, remotepath):

    sftp = client.open_sftp()

    # Create remote directory if it doesn't exist
    try:
        sftp.stat(remotepath)
    except FileNotFoundError:
        sftp.mkdir(remotepath)

    if os.path.isfile(localpath):
        # Obtain file name from local path & append to remote path
        # Returns a tuple (directory, filename)
        path = os.path.split(localpath)
        remote_filename = os.path.join(remotepath, path[1])
        print('  Copying %s' % remote_filename)
        sftp.put(localpath, remote_filename)

    elif os.path.isdir(localpath):
        if localpath.endswith('/'):
            for dirpath, dirnames, filenames in os.walk(localpath):
                # Change local dirpath to match remote path. Ex: local/dir/.. to remote/dir/...
                # remotedir = [local, dir1, dir2, ...]
                remotedir = dirpath.split('/')
                # remotedir = [/remote, dir1, dir2, ...]
                remotedir[0] = remotepath.rstrip('/')
                remotedir = '/'.join(remotedir)

                # Traverse into each child directory and create sub directory if it doesn't exist on remote host
                if dirnames:
                    for dirname in dirnames:
                        subdir = os.path.join(remotedir, dirname)

                        try:
                            sftp.stat(subdir)
                        except FileNotFoundError:
                            sftp.mkdir(subdir)

                for filename in filenames:
                    localdir = os.path.join(dirpath, filename)
                    remotefile = os.path.join(remotedir, filename)
                    print('  Copying %s' % localdir)
                    sftp.put(localdir, remotefile)
        else:
            # Create path /remote/local/dir1...
            p = os.path.join(remotepath, localpath)

            try:
                sftp.stat(p)
            except FileNotFoundError:
                sftp.mkdir(p)

            for dirpath, dirnames, filenames in os.walk(localpath):
                if dirnames:
                    for dirname in dirnames:
                        subdir = os.path.join(dirpath, dirname)
                        remotedir = os.path.join(remotepath, subdir)

                        try:
                            sftp.stat(remotedir)
                        except FileNotFoundError:
                            sftp.mkdir(remotedir)

                for filename in filenames:
                    local_filename = os.path.join(dirpath, filename)
                    remote_filename = os.path.join(remotepath, local_filename)
                    print(' Copying %s' % local_filename)
                    sftp.put(local_filename, remote_filename)
    else:
        print('File or directory not found.')


# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')


def main(argv):
    if argv[1] == 'deploy_to_staging':
        try:
            # print('Creating droplet...')
            # droplet = create_droplet()
            # ip_address = wait_for_ip(droplet)
            # save_ip_to_file(ip_address)
            print('Deploying to droplet...')
            add_to_hosts('167.99.161.25')
            client = connect_to_client('167.99.161.25')
            deploy_to_droplet(client)
            client.close()
            # deploy_to_droplet(ip_address)
        except TimeoutError:
            print('ERROR: Creating droplet timed out')


if __name__ == '__main__':
    main(sys.argv)
