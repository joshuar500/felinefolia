import sys
import os, os.path
# TODO: potentially rewrite to use argparse
# import argparse
import pathlib
import subprocess
import digitalocean
import paramiko
import traceback
import errno

UseGSSAPI = (
    paramiko.GSS_AUTH_AVAILABLE
)  # enable "gssapi-with-mic" authentication, if supported by your python installation
DoGSSAPIKeyExchange = (
    paramiko.GSS_AUTH_AVAILABLE
) # enable "gssapi-kex" key exchange, if supported by your python installation

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

def deploy_to_droplet(ip_address):
  hostname = ip_address
  port = 22
  username = 'coreos'

  try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    print("*** Connecting...")
    if not UseGSSAPI and not DoGSSAPIKeyExchange:
        client.connect(hostname, port, username)
    else:
        try:
            client.connect(
                hostname,
                port,
                username,
                gss_auth=UseGSSAPI,
                gss_kex=DoGSSAPIKeyExchange,
            )
        except Exception:
            # traceback.print_exc()
            # password = getpass.getpass(
            #     "Password for %s@%s: " % (username, hostname)
            # )
            client.connect(hostname, port, username)

    client.exec_command('echo im connected remotely')
    # chan = client.invoke_shell()
    # print(repr(client.get_transport()))
    # print("*** Here we go!\n")
    # interactive.interactive_shell(chan)
    # chan.close()
    client.close()

  except Exception as e:
      print("*** Caught exception: %s: %s" % (e.__class__, e))
      traceback.print_exc()
      try:
          client.close()
      except:
          pass
  sys.exit(1)

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
  if argv[1] == 'deploy_to_staging':
    try:
      print('Creating droplet...')
      droplet = create_droplet()
      ip_address = wait_for_ip(droplet)
      save_ip_to_file(ip_address)
      print('Deploying to droplet...')
      deploy_to_droplet(ip_address)
    except TimeoutError:
      print('ERROR: Creating droplet timed out')
    

if __name__ == '__main__':
  main(sys.argv)