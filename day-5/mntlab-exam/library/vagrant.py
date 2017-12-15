#!/usr/bin/python

import subprocess
import vagrant
from ansible.module_utils.basic import *


def main():

    args = {"path":
                {"required": True, "type": "str"},
            "state":
                {"default": "started",
                 "choices": ['started', 'stopped', 'destroyed'],
                 "type": 'str'}
            }

    module = AnsibleModule(argument_spec=args)
    
    v = vagrant.Vagrant(root=module.params['path'])

    result = {}
    output = {}

    filecheck = (subprocess.check_output('[ -f '+module.params['path']+'Vagrantfile ] && echo "Found" || echo "Not found"', shell=True)).split('\n')[0]
    if filecheck != "Found":
        module.fail_json(msg="No Vagrant file detected", meta=filecheck)

    if module.params["state"] == 'started':
        v.up()
        vagrant_status = (v.status())[0]
        if vagrant_status[1] == 'running':
            status = v.conf()
            result['Name'] = status['Host']
            result['Hostname'] = status['HostName']
            result['Port'] = status['Port']
            result['User'] = status['User']
            result['SSHKey'] = status['IdentityFile']
            result['State'] = 'running'
            result['OS'] = v.ssh(vagrant_status[0], "cat /etc/system-release")
            result['RAMsize'] = v.ssh(vagrant_status[0], "cat /proc/meminfo | grep MemTotal | awk '{print $2}'")
            output.update(result)
        else:
            module.exit_json(msg='VM isn\'t running', meta=vagrant_status)

        module.exit_json(changed=False, meta=output)

    elif module.params["state"] == 'stopped':
        v.halt()
        vagrant_status = (v.status())[0]
        #status = v.conf()
        result['Name'] = vagrant_status[0]
        result['State'] = vagrant_status[1]
        output.update(result)
        module.exit_json(changed=False, meta=output)

    else:
        v.destroy()
        vagrant_status = (v.status())[0]
        #status = v.conf()
        result['Name'] = vagrant_status[0]
        result['State'] = vagrant_status[1]
        output.update(result)
        module.exit_json(changed=False, meta=output)


if __name__ == '__main__':
    main()

