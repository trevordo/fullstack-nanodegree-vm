# Tournament
FSND project

This is a project for the Udacity Tourament SQL databases

# Requirement

Download and install the following according to your operating system
[Git](http://git-scm.com/downloads), 
[Virtual Box](https://www.virtualbox.org/wiki/Downloads), 
[Vagrant](https://www.vagrantup.com/downloads.html)

fork the root of the project [here](https://github.com/trevordo/fullstack-nanodegree-vm)
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

change path to tournament
```sh

$ cd /vagrant/tournament

```

start Postgresql and import database
```sh

$ psql

$ \i tournament.sql

$ \q

```

Run unit test
```sh

$ python tournament_test.py

```

Exit virtual machine and log off
```sh

$ exit

$ exit

```