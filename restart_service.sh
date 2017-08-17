#!/bin/bash
user='ubuntu'
project_dir='/home/'$user'/companyParser'
if [ -f $project_dir'/service.pid' ]; then
    sudo kill -15 $(cat $project_dir/service.pid);
    sudo rm $project_dir'/service.pid';
fi

sudo $project_dir/project_env/uwsgi3 --ini $project_dir/project_config/uwsgi.ini
exit
