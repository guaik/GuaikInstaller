#!/usr/bin/python
import os
import getpass
from sys import argv

install = """
yum -y install epel-release
yum -y install wget
yum -y update
echo -e "[mongodb-org-3.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/3.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.2.asc
" > /etc/yum.repos.d/mongodb-org-3.2.repo
yum -y install mongodb-org
systemctl enable mongod.service
systemctl start mongod.service
"""

remove = """
systemctl stop mongod.service
yum -y remove mongodb-org
rm -rf /etc/yum.repos.d/mongodb-org-3.2.repo
rm -rf /etc/rc.d/init.d/mongod
"""


if __name__ == "__main__":
    if len(argv) < 2:
        exit()
    action = argv[1]
    print """
****************************************
* Guaik: https://bbs.guaik.org
****************************************
"""
    if action == "install":
        print "Start install......"
        os.system(install)
        print """
Install finish.
        """
    elif action == "remove":
        print "Start remove......"
        os.system(remove)
        print """
remove finish.
        """
