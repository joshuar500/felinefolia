import os
import digitalocean

# TODO: Somebody make this look pretty

# Create droplet
droplet = digitalocean.Droplet(token='2b63ea6b8711ce73ee616872c31b7e6dab2b2c1b1690e000b9b60e20f66c9d2e',
                               name='ff-staging.com',
                               region='sfo2',
                               size='s-1vcpu-1gb',
                               image='coreos-stable',
                               ssh_keys=['29:78:b3:d0:b7:40:d0:5f:05:f8:22:9c:16:f3:f8:f5'],
                               ipv6=False,
                               user_data=None,
                               private_networking=None,
                               backups=False)
droplet.create()

def check_is_complete():
  # Check if droplet is created
  actions = droplet.get_actions()
  for action in actions:
      # Wait for droplet to be completed
      action.wait()
      print('Droplet created.')
      
      # Load additional data for droplet after creation
      droplet.load()
      print(droplet.ip_address)
      os.environ['DROPLET_IP_ADDRESS'] = droplet.ip_address

try:
  check_is_complete()
except TimeoutError:
  print('Time out')
  pass