import sys
import os, os.path
# TODO: potentially rewrite to use argparse
# import argparse
import pathlib
import subprocess
import digitalocean
import errno

# TODO: Somebody make this look more pretty

# Create droplet on digital ocean
def create_droplet():
  droplet = digitalocean.Droplet(token='2b63ea6b8711ce73ee616872c31b7e6dab2b2c1b1690e000b9b60e20f66c9d2e',
                               name='ff-staging.com',
                               region='sfo2',
                               size='s-1vcpu-1gb',
                               image='coreos-stable',
                               ssh_keys=['29:78:b3:d0:b7:40:d0:5f:05:f8:22:9c:16:f3:f8:f5', '4a:11:e3:b9:7e:b1:3c:76:f2:80:22:28:67:15:82:45'],
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
      
      # this doesn't work
      # os.environ['DROPLET_IP_ADDRESS'] = droplet.ip_address
      
      # this does work but only good for same job in circleci
      # bash_cmd = 'echo \'export DROPLET_IP_ADDRESS="' + droplet.ip_address + '"\' >> $BASH_ENV'
      # subprocess.Popen(bash_cmd, shell=True)

      return droplet.ip_address

def save_ip_to_file(ip_address):
  path_to_save = pathlib.Path(__file__).parent / 'tmp'
  file_to_open = 'ip_address.txt'
  mkdir_p(path_to_save)
  with safe_open_w(path_to_save / file_to_open) as f:
    f.write(ip_address)

def get_ip_from_file():
  pass

def deploy_to_droplet(ip_address):
  pass

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

def main(argv):
  if argv[1] == 'create_droplet':
    try:
      droplet = create_droplet()
      ip_address = wait_for_ip(droplet)
      save_ip_to_file(ip_address)
    except TimeoutError:
      print('Creating droplet timed out')
  if argv[1] == 'deploy_to_staging':
    print('deploying to staging environment')
    

if __name__ == '__main__':
  main(sys.argv)