#!/bin/bash
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -C "reedjones760@yahoo.com"
    cat ~/.ssh/id_rsa.pub
fi
echo "ssh key \n"
cat ~/.ssh/id_rsa.pub
echo "ssh key \n"