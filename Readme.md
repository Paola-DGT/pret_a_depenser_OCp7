
# OC Project 7
# Readme
This repo uses pre-commit hooks, bandit security checks and pylint.
## Data Science ML Stack
In this Exercise I set up a Machine Learning stack with dashboard and prediction 
capabilities. The stack is composed of a FastAPI backend, a Streamlit front with simple
authentication. The app with the chosen model is automatically deployed after every
merge commit on main branch. In a close future evidently will be added for model
deviation tests.

The application is deployed to a EC2-like instance (server) by ssh.
Ansible might be added later but right now this is the simplest version that makes the
work.
