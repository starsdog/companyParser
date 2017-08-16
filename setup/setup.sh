#!/bin/bash
sudo ansible-playbook -i "localhost," -c local package.yml

if [ ! -d '../credit_show' ]; then
    mkdir ../credit_show
fi

if [ ! -d '../mops_show' ]; then
    mkdir ../mops_show
fi

if [ ! -d '../xml' ]; then
    mkdir ../xml
fi

if [ ! -d '../json' ]; then
    mkdir ../json
fi

