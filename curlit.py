#!/usr/bin/python

from ansible.module_utils.basic import *
from os.path import isfile
from urlparse import urlparse
import subprocess

def main() :
  module = AnsibleModule(
    argument_spec = dict(
      url = dict(required=True),
      dest = dict(required=True),
      mode = dict(required=False),
      owner = dict(required=False),
      group = dict(required=False)
    )
  )

  p = module.params
  dest = p['dest']
  url = p['url']

  changed = False
  if not isfile(dest) :
    changed = True
    command = ["curl", "-sL", "-o", dest, url]
    subprocess.check_call(command)
    if (p['owner']) :
      owner = p['owner']
      if (p['group']) : owner += ':' + p['group']
      subprocess.check_call(["chown", owner, dest])

    if (p['mode']) :
      subprocess.check_call(["chmod", p['mode'], dest])

  module.exit_json(changed=changed)

if __name__ == '__main__':
  main()
