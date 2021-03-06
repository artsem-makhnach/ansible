#!/usr/bin/bash

source $1

if [ -z "$url" || -z "$war" || -z "$username" || -z "$password" ]; then
	printf '{"failed": true, "msg": "missing required params"}'
	exit 1
fi

if [ "$url" == "None" ]; then
	printf '{"failed": true, "msg": "missing required params"}'
	exit 1
fi	

if [ ! -f "$war" ]; then
	printf '{"failed": true, "msg": "no war file path"}'
	exit 1
fi

curl --upload-file $war "http://$username:$password@192.168.1.2:8080/manager/text/deploy?path=/$url&update=true"

printf '{"changed": true, "msg": "deployed"}'
echo "Deployment time: $(date +"%T")" > deploy-info.txt
echo "Deploy User: arm" >> deploy-info.txt

exit 0
