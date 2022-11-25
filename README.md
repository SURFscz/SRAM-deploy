# SURF Research Access Management
![build status](https://github.com/SURFscz/SRAM-deploy/actions/workflows/main.yml/badge.svg)

The SURF Research Access Management (SRAM) project offers a Membership Management System
for research collaborations. It is a middleware solution for
researchers, which allows them to

- log in using credentials from their university, as well as support (international) 'guests';
- handle (Identity and) Access Management (IAM) for their collaborations;
- allow members of their collaborations easy access to services (like web
  applications, databases, storage solutions, compute facilities, etc.);

It is meant to be used in combination with a (SAML/OIDC) identity federation and proxy such as
[EduTEAMS](https://eduteams.org/), but can be used stand-alone in combination with a single OIDC OP.

More information can be obtained from <https://wiki.surfnet.nl/display/sram>.

## Technical
The SRAM is comprised of a number of open source components:

### SBS
SBS is the actual Membership Management UI.  See <https://github.com/SURFscz/SBS>.

### OpenLDAP
OpenLDAP is used to expose authorization information to services.

### pLSC (LDAP Synchronisation Connector)
pLSC is used to synchronize information from SBS to OpenLDAP.  See <https://github.com/SURFscz/plsc>.

## SRAM-deploy
This repository consists of an Ansible playbook to install a complete
SRAM-platform.

We support this on both Linux (tested on Ubuntu 20.04, experimental on
openSUSE Tumbleweed) and OSX/MacOS (tested on Big Sur).
The system is deployed to a number of docker containers.

To get started, do the following:

- install Docker (>=19.03) and Ansible (>=2.10)

    Ubuntu/Debian: `apt install ansible docker.io docker-compose`

    OpenSUSE Tumbleweed: `zypper install ansible docker docker-compose`

    MacOS: see
      <http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-on-mac-osx>
      and <https://docs.docker.com/docker-for-mac/>

- Install required ansible modules

    `ansible-galaxy install -r requirements.yml`

- Set up the containers and start the deploy:

    `./start-vm`

    This will boot 8 containers/VMs and run ansible to deploy SRAM to these 8 hosts.

- Alternatives:

    `./start-vm --skip-ansible`

    This will start the containers, and skip the deploy.

    `./start-vm --skip-vm [params]`

    This will skip the start of containers and deploy the software, [params] added to the ansible command.

- After the deploy finishes, you should be able to browse to
  <https://sbs.scz-vm.net> (accept certificate) and login using the default platform admin
  credentials `admin`/`admin`

