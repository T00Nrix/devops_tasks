#!/usr/bin/env python3

import subprocess
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def load_config():
    """
     Load configurations from config.json file
    :return:
    """
    config_path = os.path.join('../configs', 'config.json')
    if not os.path.isfile(config_path):
        logging.error(f"Configuration file [NOT FOUND] in {config_path}")
        return None
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def get_light_checker_status(config):
    """
    Use lightChecker.py to determine the status
    :param config:
    :return: status ('ON' or 'OFF')
    """
    light_checker_script = os.path.join('..', 'light_checker', 'lightChecker.py')
    if not os.path.isfile(light_checker_script):
        logging.error(f"lightChecker.py [NOT FOUND] {light_checker_script}")
        return None
    logging.info("[RUNNING] lightChecker.py")
    result = subprocess.run(['python3', light_checker_script], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("[FAILED] to execute lightChecker.py.")
        logging.error(result.stderr)
        return None
    status = result.stdout.strip()
    logging.info(f"Light Checker status: {status}")
    return status

def is_vagrant_running():
    """
    Check if Vagrant is running
    :return: True if running, False otherwise
    """
    vagrant_dir = os.path.join('..', 'vagrant')
    result = subprocess.run(['vagrant', 'status', '--machine-readable'], cwd=vagrant_dir, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("[FAILED] to get Vagrant status.")
        return False
    for line in result.stdout.splitlines():
        if ',state,running' in line:
            return True
    return False

def  manage_docker_app():
    """
    Check if any Docker container is running inside Vagrant 
    :return: True if running, False otherwise
    """
    vagrant_dir = os.path.join('..', 'vagrant')
    docker_ps_command = 'docker ps -q'
    result = subprocess.run(['vagrant', 'ssh', '-c', docker_ps_command], cwd=vagrant_dir, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("[FAILED] to check Docker containers inside Vagrant.")
        logging.error(result.stderr)
        return False
    output = result.stdout.strip()
    if output:
        return True
    else:
        return False

def run_vagrant_up():
    """
    Run 'vagrant up' in the vagrant directory
    """
    vagrant_dir = os.path.join('..', 'vagrant')
    if not os.path.isdir(vagrant_dir):
        logging.error(f"Vagrant directory [NOT FOUND] in {vagrant_dir}")
        return False
    logging.info("Starting Vagrant environment [UP]")
    result = subprocess.run(['vagrant', 'up'], cwd=vagrant_dir)
    if result.returncode != 0:
        logging.error("[FAILED] to start Vagrant environment.")
        return False
    return True

def run_vagrant_halt():
    """
    Run 'vagrant halt' in the vagrant directory
    """
    vagrant_dir = os.path.join('..', 'vagrant')
    if not os.path.isdir(vagrant_dir):
        logging.error(f"Vagrant directory [NOT FOUND] in {vagrant_dir}")
        return False
    logging.info("Stopping Vagrant environment [HALT]")
    result = subprocess.run(['vagrant', 'halt'], cwd=vagrant_dir)
    if result.returncode != 0:
        logging.error("[FAILED] to stop Vagrant environment.")
        return False
    return True

def run_ansible_playbook():
    """
    Run the ansible playbook inside the Vagrant
    """
    vagrant_dir = os.path.join('..', 'vagrant')
    ansible_command = 'cd /home/vagrant/project/ansible && ansible-playbook -i inventory.ini playbook.yml'
    logging.info("[RUNNING] ansible playbook inside Vagrant")
    result = subprocess.run(['vagrant', 'ssh', '-c', ansible_command], cwd=vagrant_dir)
    if result.returncode != 0:
        logging.error("[FAILED] to execute ansible playbook inside Vagrant.")
        return False
    return True

def manage_vagrant_based_on_status(config):
    """
    Manage Vagrant and Docker based on lightChecker status
    :param config:
    :return:
    """
    status = get_light_checker_status(config)
    if status is None:
        return

    vagrant_running = is_vagrant_running()

    if status == 'OFF':
        # light off, working day is starting
        if not vagrant_running:
            logging.info("Vagrant is not running. Starting Vagrant ...")
            if run_vagrant_up():
                # start ansible playbook
                run_ansible_playbook()
        else:
            logging.info("Vagrant  is already running.")
            # check if Docker container is run?
            if not  manage_docker_app():
                logging.info("Docker container is not running. Running Ansible playbook to ensure environment is set up.")
                run_ansible_playbook()
            else:
                logging.info("Docker container is already running.")
    elif status == 'ON':
        # light on, working day finished
        if vagrant_running:
            logging.info("Vagrant  is running. Halting Vagrant ...")
            run_vagrant_halt()
        else:
            logging.info("Vagrant  is already halted.")
    else:
        logging.warning(f"[UNKNOWN STATUS] '{status}' from lightChecker.py.")

def main():
    config = load_config()
    if not config:
        return
    manage_vagrant_based_on_status(config)

if __name__ == '__main__':
    main()
