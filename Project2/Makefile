all:
	sudo sysctl net.ipv4.ip_forward=1	
	mkdir -p logfile
	sudo chmod +x mitm_attack pharm_attack mitm_parse.sh
	sudo iptables -t nat -F
	sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443	
	touch ~/.rnd
	openssl genrsa -out ca.key 4096
	openssl req -new -x509 -days 1826 -key ca.key -out ca.crt -subj '/C=TW/ST=TW/L=hsinchu/O=nycu/OU=nycu/CN=csc_project2/'
	
clean: 
	rm ~/.rnd
	rm -f logfile/*.log
	rm -f ca.crt ca.key
	sudo kill -9 `cat sslsplit.pid`
