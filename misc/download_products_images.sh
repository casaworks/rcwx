#! /usr/bin/env bash

rm -rf product_images
mkdir product_images

files=`egrep -o '[^"]*(jpg|png)' data.json`

for file in $files;do
	name=${file%.*}
	filename=`basename $file`
	extension=${filename##*.}
	md5name=`md5 -q -s $name`
	md5file=$md5name.$extension
	wget royal-canin.cn$file -O product_images/$md5file
done
