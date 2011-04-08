#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from subprocess import Popen, PIPE
import ftplib

DB_FILE = "database.db"
USERS_FILE = "users.csv"

def get_database(password):
    server = ftplib.FTP("186.136.207.69")
    server.login("saltalug", password)
    server.retrbinary("RETR "
        "web2py/applications/flisol2011/databases/development.db",
        open(DB_FILE, "wb").write)
    return DB_FILE

def get_csv(database):
    commands = ('.mode csv\n.separator ";"\n.header on\n'
        'SELECT * FROM auth_user;\n')
    proc = Popen("sqlite3 %s" % database, stdin=PIPE, stdout=PIPE, shell=True)
    stdout, stderr = proc.communicate(input=commands)

    return stdout


def main():
    password = raw_input("Password: ")
    database = get_database(password)
    users = get_csv(database)
    file = open(USERS_FILE, "w")
    file.write(users)
    file.close()

if __name__ == "__main__":
    exit(main())
