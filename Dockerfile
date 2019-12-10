FROM debian:buster AS scz-base
MAINTAINER SURFnet <info@surfnet.nl>

ARG DEBIAN_FRONTEND=noninteractive
ARG RUNLEVEL=1
ENV TERM linux

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections  && \
    echo "deb http://ftp.de.debian.org/debian/ buster-backports main" >> /etc/apt/sources.list  && \
    apt update -y  && \
    apt install -y openssh-server python2.7 python3 python sudo locales python-setuptools && \
    apt clean -y && apt-get autoremove -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  && \
    update-locale  && \
    systemctl enable ssh.service  && \
    systemctl disable getty@  && \
    systemctl disable getty.target  && \
    rm /lib/systemd/system/multi-user.target.wants/getty.target  && \
    rm /lib/systemd/system/getty.target.wants/getty-static.service  && \
    systemctl disable systemd-timesyncd.service  && \
    echo "exit 0" > /usr/sbin/policy-rc.d  && \
    useradd --create-home -s /bin/bash ansible  && \
    install -d -o ansible -m 0700 /home/ansible/.ssh  && \
    echo -n 'ansible:ansible' | chpasswd  && \
    mkdir -p /etc/sudoers.d && install -b -m 0440 /dev/null /etc/sudoers.d/ansible  && \
    echo 'ansible ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/ansible

# sshd services in all containers
EXPOSE 22
# for LB
EXPOSE 443
EXPOSE 636
# for ldap
EXPOSE 389
EXPOSE 636
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

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/lib/systemd/systemd"]

