#!/bin/sh

for file in *.svg; do
    basefile="$(basename $file .svg)"
    inkscape -f $file --export-png=$basefile.png --export-area-page --export-dpi=50
    inkscape -f $file --export-pdf=$basefile.pdf --export-area-page --export-dpi=200
done
