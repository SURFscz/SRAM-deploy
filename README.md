# SURF Research Access Management
![build status](https://github.com/SURFscz/SRAM-deploy/actions/workflows/main.yml/badge.svg)
![build status](https://github.com/SURFscz/SRAM-deploy/actions/workflows/ci-runner.yml/badge.svg)

The SURF Research Access Management (SRAM) project offers a Membership Management System
for research collaborations. It is a middleware solution for
researchers, which allows them to

- log in using credentials from their university, as well as support (international) 'guests';
- handle (Identity and) Access Management (IAM) for their collaborations;
- allow members of their collaborations easy access to services (like web
  applications, databases, storage solutions, compute facilities, etc.);

It is meant to be used in combination with a (SAML/OIDC) identity federation and proxy such as
[EduTEAMS](https://eduteams.org/), but can be used stand-alone in combination with a single OIDC OP.

More information can be obtained from our [documentation](https://edu.nl/vw3jx).

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

### WARNING
The instructions below are meant to deploy a TEST, DEV or DEMO environment
and should never be used to deploy a PRODUCTION setup!

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

    ```
    ansible-galaxy install -r requirements.yml
    ansible-galaxy collection install -r requirements.yml
    ```

- Add the hardcoded docker hosts (from `./docker/hosts`) to your own `/etc/hosts` file:

  ```
  127.0.0.1   localhost
  ....
  ....
  ....
  
  # SURFnet SRAM
  172.20.1.24 cm.scz-vm.net sp-test.scz-vm.net comanage.scz-vm.net idp-test.scz-vm.net meta.scz-vm.net proxy.scz-vm.net ldap.scz-vm.net mdq.scz-vm.net oidc-test.scz-vm.net sbs.scz-vm.net
  172.20.1.24 google-test.scz-vm.net pam.scz-vm.net orcid-test.scz-vm.net ms-test.scz-vm.net oidc-op.scz-vm.net ldap1.scz-vm.net ldap2.scz-vm.net mailpit.scz-vm.net
  172.20.1.20 ldap1.vm.scz-vm.net
  172.20.1.21 ldap2.vm.scz-vm.net
  172.20.1.22 proxy.vm.scz-vm.net
  172.20.1.23 meta.vm.scz-vm.net
  172.20.1.24 lb.vm.scz-vm.net
  172.20.1.25 client.vm.scz-vm.net
  172.20.1.26 sandbox1.vm.scz-vm.net
  172.20.1.27 sbs.vm.scz-vm.net
  172.20.1.28 db.vm.scz-vm.net
  172.20.1.29 bhr.vm.scz-vm.net
  172.20.1.30 test.vm.scz-vm.net
  172.20.1.31 demo1.vm.scz-vm.net
  172.20.1.32 docker1.vm.scz-vm.net
  172.20.1.33 docker2.vm.scz-vm.net
  172.20.1.40 websso.scz-vm.net
  172.20.1.41 webssod.scz-vm.net
  172.20.1.99 mail.vm.scz-vm.net
  ```

- Set up the containers and start the deploy:

    `./start-vm`

    This will boot 8 containers and run ansible to deploy SRAM to these 8 hosts.

- Alternatives:

    `./start-vm --skip-ansible`

    This will start the containers, and skip the deploy.

    `./start-vm --skip-vm [params]`

    This will skip the start of containers and deploy the software, [params] added to the ansible command.

- After the deploy finishes, you should be able to browse to
  <https://sbs.scz-vm.net> (accept certificate) and login using the default platform admin
  credentials `admin`/`admin`

