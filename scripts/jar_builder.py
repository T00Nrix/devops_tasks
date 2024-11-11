#!/usr/bin/env python3

import logging    # For logging steps
import sys        # For ending program | clearing screen
import json       # For working with config
import os         # For working with path
import subprocess # For running commands

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs/jar_builder_log.log",
    format='%(asctime)s; %(levelname)s;  %(message)s'
)

def load_config():
    """
    Load information from the config file.
    """
    path_config = os.path.join("../configs", "config_jar_builder.json")

    try:
        with open(path_config, "r") as config_file:  # Read config file
            logging.info(f"[LOADING] Config file from {path_config}")
            return json.load(config_file)
    except FileNotFoundError:
        logging.error(f"[NOT FOUND] Config file: {path_config}")
        return None

def build_jar(config):
    """
    Build the jar file with Gradle.
    :param config: config_jar_builder.json
    """
    if not config:
        logging.error("Configuration not loaded. Skipping build.")
        return

    project_dir = config["project_dir"]
    jar_name = config["jar_name"]
    jar_path = os.path.abspath(os.path.join(project_dir, "build", "libs", jar_name))

    try:
        logging.info(f"[STARTING] Building jar in path: {project_dir}")

        result = subprocess.run(
            config['build_command'],   # Use build command
            cwd=project_dir,           # Current working directory
            capture_output=True,       # Capture output
            text=True                  # Command output as string
        )

        if result.returncode == 0:  # Check if the process was successful
            logging.info(f"[SUCCESSFUL] Built jar: {jar_path}")
        else:
            logging.error(f"[FAILED] Building jar: {jar_path}")
            logging.error(result.stderr)
            return

    except Exception as e:
        logging.critical(f"[FAILED] {e}")
        return

def test_jar(config):
    """
    Runs a test to check the output of the jar.
    :param config: config_jar_builder.json
    """
    if not config:
        logging.error("Configuration not loaded. Skipping test.")
        return

    test_exp_value = config["test_exp_value"]
    jar_path = os.path.abspath(os.path.join(config["project_dir"], "build", "libs", config["jar_name"]))
    test_command = config["test_command"] + [jar_path]  # Create command for testing

    if not os.path.exists(jar_path):
        logging.critical(f"[FAILED] Test jar: {jar_path} - jar path does not exist")
        return

    try:
        logging.info(f"[STARTING] Testing jar: {jar_path}")

        result = subprocess.run(test_command, capture_output=True, text=True)

        if result.returncode != 0:
            logging.error(f"[FAILED] Running jar: {jar_path}")
            logging.error(result.stderr)
            return

        if test_exp_value in result.stdout:
            logging.info(f"[SUCCESSFUL] Testing jar: {jar_path}")
        else:
            logging.error(f"[FAILED] Testing jar: {jar_path}")
            logging.error("Expected output not found in jar output.")
            return

    except Exception as e:
        logging.error(f"[FAILED] Run jar: {e}")
        return

if __name__ == '__main__':
    conf = load_config()  # Prevent double check

    build_jar(conf)
    test_jar(conf)
