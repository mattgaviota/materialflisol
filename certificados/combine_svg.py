#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
Require inkscape y ghostscript
"""

from codecs import open
from itertools import izip
from subprocess import Popen, PIPE, STDOUT
import csv
import locale
import os
import re
import sys
import tempfile


def basename(path):
    return os.path.splitext(os.path.basename(path))[0]

def which(command):
    return "".join(
        Popen(['which', command], stdout=PIPE).stdout.readlines()).strip()


def main():

    if len(sys.argv) != 3:
        print( """Se debe invocar el comando de esta manera:
            combinar svgfile csvfile""")
        return 1

    svgfile = sys.argv[1]
    csvfile = sys.argv[2]
    finalfile = "%s - %s.pdf" % (basename(svgfile), basename(csvfile))
    original = open(svgfile, "r", "utf8").read()

    need_fileds = [m.group(1) for m in re.finditer(r'%(.*?)%', original)]
    print(need_fileds)

    all_rows = [row for row in csv.reader(open(csvfile), delimiter=';')]
    header = [word.decode("utf8") for word in all_rows.pop(0)]
    all_rows = [[word.decode("utf8").title()
        for word in row] for row in all_rows]

    all_rows.sort()

    pdflist = []
    svglist = []

    try:
        locale.localeconv()['thousands_sep'] = '.'
    except locale.Error:
        print("Configue una localización compatible con el sistema")
        return 2


    print("Combinando campos, generando páginas")
    last = ""
    for fila in all_rows:
        registro = dict(izip(header, fila))

        svgfile = tempfile.mktemp(".svg")
        svglist.append(svgfile)
        pdffile = tempfile.mktemp(".pdf")
        pdflist.append(pdffile)

        copia = original
        for key, value in registro.iteritems():
            if value.isdigit():
                value = locale.format("%d", int(value), True)

            copia = copia.replace("%%%s%%" % key, value.strip())

        file = open(svgfile, "w", "utf8")
        file.write(copia)
        file.close()

        proc = Popen([which("inkscape"), '-zC', '-d', '180', '-A', pdffile,
            svgfile], stdout=PIPE)
        proc.wait()

        if proc.returncode != 0:
            return returncode

        now = round((float(len(pdflist)) / len(all_rows) * 100))
        if now != last:
            last = now
            sys.stdout.write("%2d%% " % now)
            sys.stdout.flush()

    print("\nCombinando, páginas en documento final")
    proc = Popen([which("gs"), "-q", "-dNOPAUSE", "-dBATCH",
        "-sDEVICE=pdfwrite", "-sOutputFile=%s" % finalfile] + pdflist)
    proc.wait()

    if proc.returncode != 0:
        return proc.returncode
    else:
        print("Generado el documento %s" % finalfile)


if __name__ == "__main__":
    exit(main())
