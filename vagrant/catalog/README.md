# Seminars R'Us
FSND project

This is a project for the Udacity Project: Item Catalog

# Requirement

Download and install the following according to your operating system
[Git](http://git-scm.com/downloads), 
[Virtual Box](https://www.virtualbox.org/wiki/Downloads), 
[Vagrant](https://www.vagrantup.com/downloads.html)

Fork the root of the project [here](https://github.com/trevordo/fullstack-nanodegree-vm)
clone the project to your local machine

# Setup

Run Git Bash
```sh

$ cd "/path_of_project/fullstack/vagrant/"

```
Setup a virtual machine on VirtualBox
```sh

$ vagrant up

```
log into virtual machine
```sh

$ vagrant ssh

```
# Usage

After logging into virtual machine


```sh
change path to tournament
$ cd /vagrant/catalog

Create the database by running the python file
$ python seminar_populate.py

Run webserver
$ python finalproject.py

Exit virtual machine and log off
```sh

$ exit

$ exit

```

# Seminar API JSON Department and Seminar

Departments 
.../Department/JSON

Seminars
.../Department/<"department.id">/seminar/JSON