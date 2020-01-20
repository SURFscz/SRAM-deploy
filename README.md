# Science Collaboration Zone
[![Build Status](https://travis-ci.com/SURFscz/SCZ-deploy.svg?branch=travis-docker)](https://travis-ci.org/SURFscz/SCZ-deploy)


The Science Collaboration Zone (SCZ) project offers an Identity Management solution
for research collaborations.  It is a middleware solution for
researchers, which allows them to

- log in using credentials from their university, as well as support (international) 'guests';
- handle (Identity and) Access Management (IAM) for their collaborations;
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

### LSC (LDAP Synchronisation Connector)
<https://github.com/lsc-project>


## SCZ-deploy
This repository consists of an Ansible playbook to install a complete
SCZ-platform.  The easiest way to get started is using Vagrant, which will
create a number of VMs on your local machine, en run the Ansible playbook to
install the different components onto the VMs.

We support this on both Linux (tested on Ubuntu 17.10 and 18.04, experimental on
openSUSE Tumbleweed) and OSX/MacOS (tested on High Sierra).
You can either deploy to full VMs (libvirt/qemu and Virtualbox are supported), or to container (using docker).

We _strongly_ recommend using the container/docker-based deploy, because it requires much less resources (should run
easily on a dual core machine with 8GB memory). To deploy to VMs, we recommend a quad-core CPU and at least 16GB of
memory, as the script will create 6 VMs with 768MB of memory each.

To get started, do the following:

- install Vagrant (>=1.9) and Ansible (>=2.4.3)
    - Ubuntu/Debian: `apt install ansible vagrant`
    - OpenSUSE Tumbleweed: `zypper install ansible vagrant`
    - MacOS: see
      <http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-on-mac-osx>
      and <https://www.vagrantup.com/downloads.html>
- install either one of:
    - docker:
      - (Debian/Ubuntu): `sudo apt install docker-compose docker.io` and add yourself to the docker group:
        `adduser $(whoami) docker`
      - (openSUSE Tumbleweed): `sudo zypper install docker docker-compose` and if you want the docker deamon to start
        automatically: `sudo systemctl enable docker`.  Add yourself tot he docker group: `sudo usermod -a -G docker`
    - virtualbox:
      - (Debian/Ubuntu): `apt install virtualbox`
      - (openSUSE Tumbleweed): `zypper install virtualbox`
    - libvirt and qemu:
      - (Debian/Ubuntu): `apt install libvirt-daemon-system virt-manager gir1.2-spice-client-gtk-3.0 qemu qemu-kvm`
        and add your user to the libvirt group: `adduser $(whoami) libvirt`
- add the following entries to `/etc/hosts`:
    ```
    172.20.1.24 lb.vm.scz-vm.net oidc-test.scz-vm.net sp-test.scz-vm.net idp-test.scz-vm.net proxy.scz-vm.net mdq.scz-vm.net cm.scz-vm.net ldap.scz-vm.net meta.scz-vm.net sbs.scz-vm.net
    172.20.1.20 ldap.vm.scz-vm.net
    172.20.1.22 proxy.vm.scz-vm.net
    172.20.1.23 meta.vm.scz-vm.net
    172.20.1.25 client.vm.scz-vm.net
    172.20.1.26 sandbox1.vm.scz-vm.net
    172.20.1.27 sbs.vm.scz-vm.net
    ```
- set up the VMs and start the deploy:
    - docker (recommended): `./start-vm --provider docker`
    - libvirt: `./start-vm --provider libvirt`
    - virtualbox: `./start-vm --provider virtualbox`

    This will boot 8 containers/VMs and run ansible to deploy SCZ to these 8 hosts.

- when the deploy finishes, you should be able to browse to
  <https://sbs.scz-vm.net> and login using the default platform admin
  credentials `baas`/`baas`

