#!/bin/bash
while true; do
	ls -l logfile/*.log > /dev/null 2>&1
	if [ "$?" -eq "0" ]; then
		for file in logfile/*.log; do
			# echo "reading files: $file" 
			info=`cat $file | grep "logintoken="`
			if [ -n "$info" ]; then 
				username=`echo $info | awk 'BEGIN {FS="&"} {print $2}'`
				password=`echo $info | awk 'BEGIN {FS="&"} {print $3}'`
				echo_uname=`echo $username | awk 'BEGIN {FS="="} {print $2}'`
				echo_pwd=`echo $password | awk 'BEGIN {FS="="} {print $2}'`
				
				echo ""	
				echo "Username: $echo_uname"
				echo "Password: $echo_pwd"
				exit 0;
			fi
		done
	fi
	sleep 1;
done
