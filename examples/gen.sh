#!/bin/bash

records=$(($1))

for n in `seq 1 $records` ; do
    s=`date +%s`
    m=$(($RANDOM%10000))
    p=$(($RANDOM%10))
    st=$(($s - $m))
    en=$(($s + $p))

    echo "$st, $en"
done
