FROM debian:stretch
MAINTAINER SURFnet <info@surfnet.nl>

ARG DEBIAN_FRONTEND=noninteractive
ARG RUNLEVEL=1
ENV TERM linux
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
ARG ssh_pub_key

# add the backports repository so we get the right version of systemd
ADD sources.list /etc/apt/sources.list

RUN echo "exit 0" > /usr/sbin/policy-rc.d

# clean out, update and install systemd from backports
#RUN apt-get update -y && apt-get dist-upgrade -y
RUN apt-get update -y
RUN apt-get -t stretch-backports install -y systemd

VOLUME [ "/sys/fs/cgroup", "/run", "/run/lock", "/tmp" ]
CMD ["/lib/systemd/systemd"]

# Install base tools: sshd, python
# RUN apt-get update
RUN apt-get install -y openssh-server python2.7 python3 python sudo locales
RUN update-locale
RUN systemctl enable ssh.service
RUN systemctl disable getty\@tty1.service

# sshd services in all containers
EXPOSE 22
# for LB
EXPOSE 443
EXPOSE 636
# for ldap
EXPOSE 389
# for comanage, proxy
EXPOSE 80
# for oidc,idp,sp
EXPOSE 81
EXPOSE 82
EXPOSE 83
# for proxy, consent, mdq
EXPOSE 8080
EXPOSE 8081
EXPOSE 8082

# Create and configure vagrant user
RUN useradd --create-home -s /bin/bash vagrant
WORKDIR /home/vagrant

# Configure SSH access
RUN mkdir -p /home/vagrant/.ssh
RUN echo "${ssh_pub_key}" >> /home/vagrant/.ssh/authorized_keys
RUN chown -R vagrant: /home/vagrant/.ssh
RUN echo -n 'vagrant:vagrant' | chpasswd

# Enable passwordless sudo for the "vagrant" user
RUN mkdir -p /etc/sudoers.d
RUN install -b -m 0440 /dev/null /etc/sudoers.d/vagrant
RUN echo 'vagrant ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/vagrant

# Clean up APT when done.
RUN apt-get clean -y && apt-get autoremove -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
