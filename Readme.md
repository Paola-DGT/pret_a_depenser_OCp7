
# Readme
This repo uses pre-commit hooks, bandit security checks and pylint.
## Data Science ML Stack
In this Exercise I set up a Machine Learning stack with dashboard and prediction 
capabilities. The stack is composed of a FastAPI backend, a Streamlit front with simple
authentication and MLflow to package the model. The app with the chosen model is
automatically deployed after every merge commit on main branch. In a close future 
evidently will be added for model deviation tests.

The application is deployed to a EC2-like instance (server) by ssh.
Ansible might be added later but right now this is the simplest version that makes the
work.
    
# How to use this project:
## CI/CD
In order to configure CI/CD to perform tests and deploy the application when PRs are
merged on main you would have to set up the following required secrets on your repo 
settings:
- secrets.VM_KEY (ssh private key)
- secrets.VM_IP (public ip of the server for ssh connection)
- secrets.KNOWN_HOSTS (see below)
- secrets.SSH_USER (the ssh user of your instance)

First, create and add the ssh key that will be used by github actions to connect to 
your server and then add the *.pub key to the ssh authorized_keys on the server side.

The KNOWN_HOSTS have to be obtained by running this command on the server:

    ssh-keyscan -H <YOUR INSTANCE IP>

Paste the output of the command above into a github secret called KNOWN_HOSTS.

## Server(instance) Side Installation:
I assume you are familiar with IaaS offer of cloud providers such as AWS EC2, this 
example **does not** include resource creation and assumes you already have acces to a 
**LINUX** instance by ssh.

The target **linux** instance will have to have the following:
- a public IP
- a domain name (otherwise use your public IP)
- ssh access
- Nginx server,
- Python 3.10 or above,
- rsync,
- letsencrypt certbot (if domain name otherwise proceed with http only),
- systemd.

First start by creating one virtual environement for each python application at the 
desired destination path (in this example "/volume")

    cd /volume
    python -m venv gunicorn-venv
    python -m venv streamlit-venv
    python -m venv mlflow-server-venv

Then create the app root directory (in this example "/volume/p7svr") and copy the app 
files by running the following command at the **project root on the local machine**:

    rsync -rlpvi --delete --delete-during \
          --exclude-from=rsync-exclude \
          ./ $YOUR_SSH_USER@$YOUR_VM_IP:/volume/p7svr/

or simply clone the project under the app root destination path if your instance has
all setup to clone from your github repo: 
    
    cd /volume/p7svr
    git clone PROJECT_URL

After this, activate install the app on the **gunicorn and streamlit** venvs 

    cd /volume/
    source gunicorn-venv/bin/activate
    pip install -e p7svr/.
do the same for streamlit.

At this point if your CI/CD pipeline is working correctly the deploy script will take
care of the rest.

## Configuration:
- The file settings.py has to be modified accordingly to be compatible with your
infrastructure,
- All the systemd files on the _deployment_ folder have to be modified to match your 
destination file structure, 
- Modify nginx.conf file to add your domain name (or public ip) and configure http or
https,
- Modify reload_services.sh to match your project file structure and your system paths.

## MLFlow, how do I change model ?
If you work with MLflow to explore different models, data treatment or optimizations, you
will have a bunch of experiments with models that have been tuned for some specific task.
Once you are happy with the model you want to make available via the streamlit dashboad,
find the model on your MLflow files and copy it to the models folder on the project.
Then you can change the configuration variable LOGGED_MODEL to the path of your model
description.

## Streamlit dashboard simple auth
The dashboard is password protected to avoid all the internet to access it and saturate
your server, the user/passwords are set on the file auth_config.yaml, check out 
streamlit_authenticator documentation to know how to set user/passwords in that file
https://github.com/mkhorasani/Streamlit-Authenticator

## What to expect ?
If everything goes right you will have an app running and accessible on port 443 or 80
depending on your nginx configuration, the services that make all run will be in place
and restarted every time a deployment occurs, your app will be up-to-date with the last 
merge commit on your main branch.

## Whats next ?
From this point you are free to turn the example template onto what ever you want your 
ML app to be.
