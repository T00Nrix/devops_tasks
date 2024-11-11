
# DevOps Project Documentation

This repository contains a DevOps project that demonstrates the automation of building, testing, and deploying a simple Java application using various tools:
- Vagrant
- Ansible
- Docker 
- Jenkins (not done)
- Python scripts

## Table of Contents
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Vagrant Environment](#1-vagrant-environment)
  - [2. Building the Java Application](#2-building-the-java-application)
  - [3. Building and Running Docker Image](#3-building-and-running-docker-image)
  - [4. Automating with Scripts](#4-automating-with-scripts)
  - [5. Jenkins Pipeline Setup](#5-jenkins-pipeline-setup)
- [Scripts Explanation](#scripts-explanation)
  - [auto_build_all.py](#auto_build_allpy)
  - [jar_builder.py](#jar_builderpy)
  - [docker_builder.py](#docker_builderpy)
  - [auto_build.sh](#auto_build.sh)
- [Ansible Playbook](#ansible-playbook)
- [Light Checker](#light-checker)
- [Jenkins Pipeline](#jenkins-pipeline)
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
├── jenkins
│   └── Jenkinsfile
├── light_checker
│   ├── lightChecker.py
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
- Jenkins (for CI/CD pipeline) (not done)

## Setup Instructions

### 1. Vagrant Environment
The project uses Vagrant to create a reproducible virtual machine for the tasks using VirtualBox.

1. **Install Vagrant**: [Download Vagrant](https://www.vagrantup.com/downloads)
2. **Install VirtualBox**: [Download VirtualBox](https://www.virtualbox.org/)

**Important Note for ARM64 Mac Users**: VirtualBox does not support ARM64 Macs. You will need to set up the environment manually.

**Starting the VM**:
```bash
cd vagrant
vagrant up
```
This will download the base box of the VM and provision the image. It might take a few minutes.

**SSH into the VM**:
```bash
vagrant ssh
```

### 2. Building the Java Application
Navigate to the helloworld directory and build the application using Gradle.

```bash
cd helloworld
./gradlew clean build
```

### 3. Building and Running Docker Image

Build the Docker Image:

```bash
docker build -t helloworld_app .
```

Run the Docker Container:

```bash
docker run -d -p 8080:8080 --name helloworld_app_container helloworld_app
```

### 4. Automating with Scripts
The `scripts` directory contains Python scripts to automate various tasks.

Make sure the scripts are executable:

```bash
chmod +x scripts/*.py
```

### 5. Jenkins Pipeline Setup (not done...)
Jenkinsfile is provided in the `jenkins` directory.


Steps:
1. Install Jenkins
2. Install Required Plugins: Docker Pipeline Plugin, Ansible Plugin
3. Create a New Pipeline Job in Jenkins and configure SCM to point to your repository containing the Jenkinsfile.

## Scripts Explanation

### scripts/auto_build_all.py
Automates the setup and deployment process.

### scripts/jar_builder.py
Builds the Java application using Gradle and runs a lightweight test to verify the output.

### scripts/docker_builder.py
Simplifies building and running the Docker image for the application.

### vagrant/auto_build.sh
Will build for you environment

## Ansible Playbook
The Ansible playbook located at `ansible/playbook.yml` automates the provisioning of the application environment.

## Light Checker
The `light_checker` directory contains `lightChecker.py`, which determines whether the application should be running based on certain conditions.

## Jenkins Pipeline
The Jenkins pipeline automates the build, test, and deployment process.
(not done)

## Notes
- Configuration Files: Store all configurations in the configs directory in JSON format.
- Permissions: Ensure scripts have execution permissions.
- Some moment's can work not 100% correct.

## Conclusion
This project demonstrates the integration of various DevOps tools to automate the build, test, and deployment processes.