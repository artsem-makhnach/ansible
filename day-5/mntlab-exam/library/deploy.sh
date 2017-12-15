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

curl --upload-file $war "http://$username:$password@127.0.0.1:8080/manager/text/deploy?path=/$url&update=true"

printf '{"changed": true, "msg": "deployed"}'
echo "Deployment time: $(date +"%T")" > /var/lib/tomcat/webapps/deploy-info.txt
echo "Deploy User: arm" >> /var/lib/tomcat/webapps/deploy-info.txt

exit 0
