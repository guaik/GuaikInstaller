#!/usr/bin/python
import os
import getpass
from sys import argv

install_rabbitmq = """
yum -y install epel-release
yum -y install erlang socat
yum -y install wget
yum -y update
mkdir rabbitmq
wget -P ./rabbitmq https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.10/rabbitmq-server-3.6.10-1.el7.noarch.rpm
rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
rpm -Uvh ./rabbitmq/rabbitmq-server-3.6.10-1.el7.noarch.rpm
rm -rf ./rabbitmq
"""

service_conf = """
systemctl start rabbitmq-server
systemctl enable rabbitmq-server
systemctl status rabbitmq-server
"""

firewall_conf = """
firewall-cmd --zone=public --permanent --add-port=4369/tcp
firewall-cmd --zone=public --permanent --add-port=25672/tcp
firewall-cmd --zone=public --permanent --add-port=5671-5672/tcp
firewall-cmd --zone=public --permanent --add-port=15672/tcp
firewall-cmd --zone=public --permanent --add-port=61613-61614/tcp
firewall-cmd --zone=public --permanent --add-port=1883/tcp
firewall-cmd --zone=public --permanent --add-port=8883/tcp
firewall-cmd --reload
setsebool -P nis_enabled 1
"""

rabbitmq_conf = """
username={}
passwd={}
mkdir /var/lib/rabbitmq/
rabbitmq-plugins enable rabbitmq_management
chown -R rabbitmq:rabbitmq /var/lib/rabbitmq/
rabbitmqctl add_user $username $passwd
rabbitmqctl set_user_tags $username administrator;
rabbitmqctl set_permissions -p / $username ".*" ".*" ".*"
"""

remove = """
yum -y remove rabbitmq-server
userdel rabbitmq
rm -rf /usr/lib/rabbitmq/
rm -rf /var/lib/rabbitmq/
firewall-cmd --zone=public --permanent --remove-port=4369/tcp
firewall-cmd --zone=public --permanent --remove-port=25672/tcp
firewall-cmd --zone=public --permanent --remove-port=5671-5672/tcp
firewall-cmd --zone=public --permanent --remove-port=15672/tcp
firewall-cmd --zone=public --permanent --remove-port=61613-61614/tcp
firewall-cmd --zone=public --permanent --remove-port=1883/tcp
firewall-cmd --zone=public --permanent --remove-port=8883/tcp
firewall-cmd --reload
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
        username = raw_input("Enter admin name:")
        passwd = getpass.getpass("Enter admin passwd:")
        os.system(install_rabbitmq)
        os.system(service_conf)
        os.system(firewall_conf)
        os.system(rabbitmq_conf.format(username,passwd))
        print """
Install finish.
[Admin website] http://host:15672/#/
        """
    elif action == "remove":
        print "Start remove......"
        os.system(remove)
        print """
remove finish.
        """
