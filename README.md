# Science Collaboration Zone
[![Build Status](https://travis-ci.org/SURFscz/SCZ-deploy.svg?branch=travis-docker)](https://travis-ci.org/SURFscz/SCZ-deploy)


The Science Collaboration Zone (SCZ) project offers ann Identity Management solution
for research collaborations.  It is a middleware solution for
researchers, which allows them to

- log in using credentials from their university;
- handle (Identity and Access Management (IAM) for their collaborations;
- allow members of their collaborations easy access to services (like web
  applications, databases, storage solutions, compute facilities, etc.);

More information can be obtained from <https://wiki.surfnet.nl/display/SCZ>.

## Technical

The SCZ is comprised of a number of existing, open source components:

### COmanage
<https://spaces.internet2.edu/display/COmanage>

### Satosa
<https://github.com/IdentityPython/SATOSA>

### Pyff
<https://github.com/leifj/pyFF>


## SCZ-deploy
This repository consists of an Ansible playbook to install a complete
SCZ-platform.  The easiest way to get started is using Vagrant, which will
create a number of VMs on your local machine, en run the Ansible playbook to
install the different components onto the VMs.

We support this on both Linux (tested on Ubuntu 17.10 and 18.04, experimental on
openSUSE Tumbleweed) and OSX/MacOS (tested on High Sierra).  For VM backends,
both libvirt/qemu and virtualbox are supported.  We are working on Docker
support, but this is currently broken (works on openSUSE Tumbleweed).

To get started, do the following:

- install Vagrant (>=1.9) and Ansible (>=2.4.3)
    - Ubuntu/Debian: `apt install ansible vagrant`
    - OpenSUSE Tumbleweed: `zypper install ansible vagrant`
    - MacOS: see
      <http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-on-mac-osx>
      and <https://www.vagrantup.com/downloads.html>
- install either one of:
    - virtualbox: `apt install virtualbox`
    - virtualbox (openSUSE Tumbleweed): `zypper install virtualbox`
    - libvirt and qemu: `apt install libvirt-daemon-system virt-manager
     gir1.2-spice-client-gtk-3.0 qemu qemu-kvm`
    - docker (openSUSE Tumbleweed): `sudo zypper install docker docker-compose` and
      if you want the docker deamon to start automatically: `sudo systemctl enable docker`
      If you are on a btrfs system and using snapshots (snapper for example),
      you might want to consider making `/var/lib/docker` a subvolume.
- (libvirt only) add your user to the libvirt group: `adduser $(whoami) libvirt`
- openSUSE Tumbleweed with docker: either use YaST, or `sudo usermod -a -G docker`
- add the following entries to `/etc/hosts`:
    ```
    172.20.1.24 lb.vm.scz-vm.net oidc-test.scz-vm.net sp-test.scz-vm.net idp-test.scz-vm.net proxy.scz-vm.net mdq.scz-vm.net cm.scz-vm.net comanage.scz-vm.net ldap.scz-vm.net meta.scz-vm.net
    172.20.1.20 ldap.vm.scz-vm.net
    172.20.1.21 comanage.vm.scz-vm.net
    172.20.1.22 proxy.vm.scz-vm.net
    172.20.1.23 meta.vm.scz-vm.net
    172.20.1.25 client.vm.scz-vm.net
    ```
- set up the VMs and start the deploy:
    - libvirt: `vagrant up --provider libvirt --no-provision` 
    - virtualbox: `vagrant up --provider virtualbox --no-provision`

    This will start 6 unprovisioned VMs (each requires 786MB of memory). In order to
    provision each of the, run `./start-vm` to start the provisioning the VMs with SCZ.

- when the deploy finishes, you should be able to browse to
  <https://comanage.scz-vm.net> and login using the default platform admin
  credentials `baas`/`baas`
