# DevOps Project Documentation

This repository contains a DevOps project that demonstrates the automation of building, testing, and deploying a simple Java application using various tools:
- Vagrant
- Ansible
- Docker
- GitHub Actions Pipeline
- Python scripts

## Table of Contents
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Vagrant Environment](#1-vagrant-environment)
  - [2. Automating with Scripts](#2-automating-with-scripts)
- [Scripts Explanation](#scripts-explanation)
  - [auto_build_all.py](#auto_build_allpy)
  - [jar_builder.py](#jar_builderpy)
  - [docker_builder.py](#docker_builderpy)
- [Ansible Playbook](#ansible-playbook)
- [Light Checker](#light-checker)
- [GitHub Actions Pipeline](#github-actions-pipeline)
- [Notes](#notes)
- [Conclusion](#conclusion)

## Project Structure

```
.
├── ansible
│   ├── inventory.ini
│   └── playbook.yml
├── configs
│   ├── config_jar_builder.json
│   └── config.json
├── helloworld
│   ├── build.gradle
│   ├── Dockerfile
│   ├── gradle
│   │   └── wrapper
│   │       ├── gradle-wrapper.jar
│   │       └── gradle-wrapper.properties
│   ├── gradlew
│   ├── gradlew.bat
│   ├── settings.gradle
│   └── src
│       └── main
│           ├── java
│           │   └── com
│           │       └── ilionx
│           │           └── helloworld
│           │               └── HelloworldApplication.java
│           └── resources
│               └── application.properties
├── light_checker
│   ├── lightChecker.py
│   ├── __pycache__
│   │   └── lightChecker.cpython-312.pyc
│   └── unitTestLightChecker.py
├── provisioning
│   └── asdf.yml
├── README.md
├── scripts
│   ├── auto_build_all.py
│   ├── docker_builder.py
│   └── jar_builder.py
└── vagrant
    ├── auto_build.sh
    └── Vagrantfile
```

## Prerequisites
**Operating System**: Linux or macOS (Windows users can use WSL)  
**Software Requirements**:
- Vagrant (version 2.4.x)
- VirtualBox (version 7.0.x)
- Ansible
- Docker
- Python 3
- Java (Temurin 21)
- Gradle
- GitHub Actions

## Setup Instructions

### 1. Vagrant Environment
The project uses Vagrant to create a reproducible virtual machine for the tasks using VirtualBox.

1. **Install Vagrant**: [Download Vagrant](https://www.vagrantup.com/downloads)
2. **Install VirtualBox**: [Download VirtualBox](https://www.virtualbox.org/)

**Important Note for ARM64 Mac Users**: VirtualBox does not support ARM64 Macs. You will need to set up the environment manually.

**Starting the VM**:

While the `auto_build_all.py` script manages the Vagrant VM automatically, you can also start it manually if needed:

```bash
cd vagrant

vagrant up
vagrant ssh
```

### 2. Automating with Scripts

The `scripts` directory contains Python scripts to automate various tasks.

The main script is `scripts/auto_build_all.py`, which serves as the central automation point for managing the entire project architecture. This script automates the setup and teardown of the environment based on the status provided by `lightChecker.py`.

**Execution**:

```bash
cd scripts
python3 auto_build_all.py
```

**Automated Execution**:

To ensure that the environment is managed automatically based on time or other conditions, you can set up a cron job to run the script periodically.

For example, to run the script every hour, add the following line to your crontab:

```cron
0 * * * * /usr/bin/python3 /path/to/scripts/auto_build_all.py
```

## Scripts Explanation

### scripts/auto_build_all.py

This is the main automation script that manages the entire project architecture.

#### Functionality:

- **Automatic Management**: Based on the status from `lightChecker.py`, it automatically brings up or tears down the project environment.
- **Vagrant Environment Control**: It starts or stops the Vagrant virtual machine.
- **Ansible Playbook Execution**: It runs the Ansible playbook to set up the environment within the Vagrant VM.
- **Docker Container Management**: It ensures that the Docker container is running or stopped as per the status.

#### How It Works:

- The script checks the status returned by `lightChecker.py`, which can be either `'ON'` or `'OFF'`.
  - **When `status` is `'OFF'`**:
    - This indicates that the working day is over, and external lights are turned on.
    - The script will:
      - **Start the Vagrant VM** if it's not already running.
      - **Run the Ansible playbook** to set up the environment.
      - **Ensure the Docker container is running**.
      - **This represents starting services that should run after work hours**, such as maintenance tasks or background jobs.
  - **When `status` is `'ON'`**:
    - This indicates that the working day is starting, and external lights are turned off.
    - The script will:
      - **Stop the Docker container** if it's running.
      - **Halt the Vagrant VM**.
      - **This represents stopping services during the working day**.

- **Repeated Execution**: Re-running the script or setting it up to run automatically (e.g., via a cron job) will ensure the environment is managed correctly based on the current status.

**Customization**:

- **Change the Application**: You can replace the contents of the `helloworld` application (the JAR file) with your own application.
- **Adjust Logic**: The logic within the scripts can be adjusted to fit your specific needs.
  - For example, you can modify the actions taken when the status is `'ON'` or `'OFF'`.

### scripts/jar_builder.py

Builds the Java application using Gradle and runs a lightweight test to verify the output. This is typically handled automatically within the `auto_build_all.py` script and the Ansible playbook.

### scripts/docker_builder.py

Simplifies building and running the Docker image for the application. This is also managed by the `auto_build_all.py` script and the Ansible playbook.

## Ansible Playbook

The Ansible playbook located at `ansible/playbook.yml` automates the provisioning of the application environment within the Vagrant VM. It installs all necessary dependencies, builds the application, and runs the Docker container.

## Light Checker

The `light_checker` directory contains `lightChecker.py`, which determines whether the application environment should be running based on the status of external lights (simulating the time of day).

### How It Works:

- **Purpose**: Simulates an external trigger (like a light sensor) to control the environment.

- **Logic**:

  - The `lightChecker.py` script returns a status of `'ON'` or `'OFF'` based on the time of day.

  - **When `status` is `'OFF'`**:
    - Indicates that external lights are turned **on** (it's nighttime).
    - The working day is **over**.
    - The script will:
      - **Start the Vagrant VM**.
      - **Run the Ansible playbook**.
      - **Start the Docker container**.
      - **This represents starting services that run after work hours**.

  - **When `status` is `'ON'`**:
    - Indicates that external lights are turned **off** (it's daytime).
    - The working day is **starting**.
    - The script will:
      - **Stop the Docker container**.
      - **Halt the Vagrant VM**.
      - **This represents stopping services during the working day**.

- **Customization**:
  - You can adjust the latitude and longitude in the script to match your location.
  - The logic can be modified to suit different conditions or triggers.

## GitHub Actions Pipeline

The GitHub Actions workflow automates the building and containerization of the Spring Boot application. The workflow ensures that every change pushed to the main branch or submitted via a pull request is automatically built into a Docker image, streamlining the development and deployment process.

### Steps:

1. **Checkout Repository**: Clones the repository code.
2. **Set up QEMU**: Enables cross-platform builds (optional for single architecture).
3. **Set up Docker Buildx**: Configures advanced Docker build capabilities.
4. **Cache Docker Layers**: Caches Docker layers to speed up future builds.
5. **Build Docker Image**: Builds the Docker image using the Dockerfile in the `helloworld` directory and tags it as `helloworld_app:latest`.
6. **List Docker Images**: Displays the built Docker images for verification.

## Notes

- **Configuration Files**: All configurations are stored in the `configs` directory in JSON format.
- **Permissions**: Ensure scripts have execution permissions.
- **Automated Execution**: You can set up the `auto_build_all.py` script to run automatically (e.g., via a cron job) to manage the environment without manual intervention.
- **Logic Customization**: The logic in `auto_build_all.py` and `lightChecker.py` can be customized to match your specific requirements regarding when services should run.

## Conclusion

This project demonstrates the integration of various DevOps tools to automate the build, test, and deployment processes. By using the `auto_build_all.py` script, you can automatically manage the project environment based on external conditions, providing a flexible and dynamic deployment solution.

**Note**: You can modify the application contents (e.g., replace the `helloworld` application with your own) and adjust the logic in the scripts to fit your specific use case.