FROM debian:stretch as scz-base
MAINTAINER SURFnet <info@surfnet.nl>

ARG DEBIAN_FRONTEND=noninteractive
ARG RUNLEVEL=1
ENV TERM linux

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections  && \
    echo "deb http://ftp.de.debian.org/debian/ stretch-backports main" >> /etc/apt/sources.list  && \
    apt-get update -y  && \
    apt-get -t stretch-backports install -y systemd  && \
    apt-get install -y openssh-server python2.7 python3 python sudo locales  && \
    apt-get clean -y && apt-get autoremove -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  && \
    update-locale  && \
    systemctl enable ssh.service  && \
    systemctl disable getty@  && \
    systemctl disable getty.target  && \
    rm /lib/systemd/system/multi-user.target.wants/getty.target  && \
    rm /lib/systemd/system/getty.target.wants/getty-static.service  && \
    systemctl disable systemd-timesyncd.service  && \
    echo "exit 0" > /usr/sbin/policy-rc.d  && \
    useradd --create-home -s /bin/bash vagrant  && \
    install -d -o vagrant -m 0700 /home/vagrant/.ssh  && \
    echo -n 'vagrant:vagrant' | chpasswd  && \
    mkdir -p /etc/sudoers.d && install -b -m 0440 /dev/null /etc/sudoers.d/vagrant  && \
    echo 'vagrant ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/vagran

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

VOLUME [ "/sys/fs/cgroup", "/run", "/run/lock", "/tmp" ]
CMD ["/lib/systemd/systemd"]

FROM scz-base as scz
ARG ssh_pub_key
# save ssh public key; Note: this is the only thing that is different for the containers up until we run ansible
RUN echo "${ssh_pub_key}" >> /home/vagrant/.ssh/authorized_keys
