#!/usr/bin/env python3

import subprocess
import os
import sys
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

def run_autobuild(config):
    """
    Run the script to set up the vagrant environment
    :param config:
    :return:
    """
    autobuild_script = config['vagrant_autobuild_script']
    if not os.path.isfile(autobuild_script):
        logging.error(f"Autobuild script [NOT FOUND] in {autobuild_script}")
        return
    logging.info("Starting vagrant environment [SETUP]")
    result = subprocess.run(['bash', autobuild_script], cwd=os.path.dirname(autobuild_script))
    if result.returncode != 0:
        logging.error("[FAILED] to set up Vagrant environment.")
        return

def run_ansible_playbook(config):
    """
    Run the ansible playbook
    :param config:
    :return:
    """
    playbook_file = config['ansible_playbook']
    inventory_file = config['ansible_inventory']
    if not os.path.isfile(playbook_file):
        logging.error(f"Ansible playbook [NOT FOUND] in {playbook_file}")
        return
    logging.info("[RUNNING] ansible playbook")
    result = subprocess.run(['ansible-playbook', '-i', inventory_file, playbook_file])
    if result.returncode != 0:
        logging.error("[FAILED] execute ansible playbook.")
        return

def manage_docker_app(config):
    """
    Use lightChecker.py to determine the status
    :param config:
    :return:
    """
    light_checker_script = config['light_checker_script']
    if not os.path.isfile(light_checker_script):
        logging.error(f"lightChecker.py [NOT FOUND] {light_checker_script}")
        return
    logging.info("[RUNNING] lightChecker.py")
    result = subprocess.run(['python3', light_checker_script], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("[FAILED] to execute lightChecker.py.")
        logging.error(result.stderr)
        return
    status = result.stdout.strip()
    logging.info(f"Light Checker status: {status}")
    docker_app_name = config['docker_app_name']
    if status == 'ON':
        # Start the Docker application
        logging.info("Starting docker application...")
        result = subprocess.run(['docker', 'start', docker_app_name])
        if result.returncode != 0:
            logging.error("[FAILED] to start docker application.")
            logging.error(result.stderr)
    elif status == 'OFF':
        # Stop the Docker application
        logging.info("Stopping docker application...")
        result = subprocess.run(['docker', 'stop', docker_app_name])
        if result.returncode != 0:
            logging.error("[FAILED] to stop docker application.")
            logging.error(result.stderr)
    else:
        logging.warning(f"Unknown status '{status}' lightChecker.py.")

def main():
    config = load_config()
    if not config:
        return
    run_autobuild(config)
    run_ansible_playbook(config)
    manage_docker_app(config)

if __name__ == '__main__':
    main()
