#!/usr/bin/python

import vagrant

v = vagrant.Vagrant()

#print v.status()

v.up()

result = {}
output = {}

vagrant_status = v.status()
print vagrant_status[0][0]

if vagrant_status[1] == 'running':
    status = v.conf(vm_name=x[0])

    vm = status['Host']
    hostname = status['HostName']
    port = status['Port']
    sec_key = status['IdentityFile']
    user = status['User']

    result[vm] = {}
    result[vm]['Hostname'] = hostname
    result[vm]['Port'] = port
    print result
    output.update(result)
print output[vm]
print output

