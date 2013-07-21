#! /usr/bin/env bash

file=`dirname $0`/htmls/1.html

grep -oE 'href="product_detail.php\?id=\d+&typeid=\d+">[^<]+' $file | sed -n -E 's/^.*id=([[:digit:]]+)&typeid=([[:digit:]]+)">(.*)$/\1:\2:\3/p' > ~/dev/royalcanin/misc/product.lst
