#!/usr/bin/env python3

import subprocess
import logging
import sys
import os

# logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s; %(levelname)s;  %(message)s'
)

def build_docker_image():
    """
    Build docker image
    """
    image_name = "helloworld_app"
    dockerfile_path = "../helloworld"

    try:
        logging.info(f"[BUILDING] docker img: {image_name}")
        result = subprocess.run(
            ["docker", "build", "-t", image_name, dockerfile_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logging.info(f"[SUCCESSFUL] docker img: {image_name}")
        else:
            logging.error(f"[FAILED] docker img: {image_name}")
            logging.error(result.stderr)
            return
    except Exception as e:
        logging.critical(f"[FAILED] {e}")
        return

def run_docker_container():
    """
    Run docker container
    """
    image_name = "helloworld_app"
    container_name = "helloworld_app_container"
    ports = ["8080:8080"]

    command = ["docker", "run", "-d"]
    for port in ports:
        command.extend(["-p", port])
    command.extend(["--name", container_name, image_name])

    try:
        logging.info(f"[RUNNING] docker container: {container_name}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"[SUCCESSFUL] docker container: {container_name}")
        else:
            logging.error(f"[FAILED] docker container: {container_name}")
            logging.error(result.stderr)
            return
    except Exception as e:
        logging.critical(f"[FAILED] {e}")
        return

def main():
    build_docker_image()
    run_docker_container()

if __name__ == '__main__':
    main()
