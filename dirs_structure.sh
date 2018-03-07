#!/bin/bash
# Por el momento los paths donde trabajar estan definidos en el codigo
# y el codigo no hace verificacion si los mismos existen o no.
#
# es necesario en el root del proyecto crear files/brando y files/ohlala
# ademas en cada uno hay que crear el archivo vacio links.txt

mkdir -p files/brando
mkdir -p files/ohlala
touch files/brando/links.txt
touch files/ohlala/links.txt
