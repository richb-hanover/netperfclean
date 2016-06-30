#! /bin/bash
#
# Concatenate all the kern.log files from last week into a single file
#

zcat /var/log/kern.log.7.gz > ~/kernlog.txt
zcat /var/log/kern.log.6.gz >> ~/kernlog.txt
zcat /var/log/kern.log.5.gz >> ~/kernlog.txt
zcat /var/log/kern.log.4.gz >> ~/kernlog.txt
zcat /var/log/kern.log.3.gz >> ~/kernlog.txt
zcat /var/log/kern.log.2.gz >> ~/kernlog.txt
cat /var/log/kern.log.1 >> ~/kernlog.txt
cat /var/log/kern.log >> ~/kernlog.txt
