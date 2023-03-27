#!/usr/bin/env bash

# exit when any command fails
set -e


function check_code_on_exit {
    test $? -eq 0 || echo "\"${last_command}\" command filed with exit code $?."
}

# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap check_code_on_exit EXIT

# set server specific variables -all paths absolute-
venvs=(gunicorn-venv streamlit-venv)          # venvs names
apps=(backend dashboard)                      # my app service names
app_root_path="/volume/p7svr"                 # app path on server
deploy_root_path="/volume/p7svr/deployment"   # deploy path on server
systemd_path="/etc/systemd/system"            # systemd path on server
nginx_conf_path="/etc/nginx"                  # nginx conf path on server

# copy nginx config
sudo cp -f $deploy_root_path/nginx.conf $nginx_conf_path/nginx.conf

echo "Nginx conf file copied"

# copy all unit files to systemd directory
for app in "${apps[@]}"; do
    sudo cp -f $deploy_root_path/$app.service $systemd_path/$app.service || exit 1
done

echo "App Unit files from $deploy_root_path/ were copied to $systemd_path/"

# reinstall app in venvs
echo "Re-installing virtual environements"

for venv in "${venvs[@]}"; do
    /volume/$venv/bin/python -m pip install --force-reinstall -e $app_root_path/. || exit 1
done

echo "Virtual environements succesfully installed !"

# reload daemon after file changes
sudo systemctl daemon-reload

echo "Systemd Daemon was reloaded"

apps+=(nginx)
# restart apps services
for app in "${apps[@]}"; do

    sudo systemctl restart $app.service || exit 100
done

echo "All apps and proxy were rebooted"

# check service status
for app in "${apps[@]}"; do
    sudo systemctl is-active --quiet $app.service || exit 200
done

echo "Reboot was successfull"
