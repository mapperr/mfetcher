#! /bin/bash

if [ $# -lt 3 ]; then
   echo "$0 <start> <end>"
   exit 1
fi

manga=$1
start=$2
end=$3

for chap in `seq -s " " $start $end`; do
   ./mfetcher.py fetch $manga $chap
done

