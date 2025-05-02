FROM debian:bookworm AS scz-base
LABEL org.opencontainers.image.authors="SRAM team <sram-beheer@surf.nl>"

ARG DEBIAN_FRONTEND=noninteractive
ARG RUNLEVEL=1
ENV TERM=linux

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update -y                && \
    apt-get install -y                  \
        acl                             \
        apt-transport-https             \
        aptitude                        \
        bash                            \
        bash-completion                 \
        bzip2                           \
        ca-certificates                 \
        chrony                          \
        cloud-init                      \
        curl                            \
        dnsutils                        \
        git                             \
        gnupg2                          \
        locales-all                     \
        logrotate                       \
        lsof                            \
        needrestart                     \
        net-tools                       \
        netcat-openbsd                  \
        nullmailer                      \
        openssh-server                  \
        parted                          \
        python3                         \
        python3-apt                     \
        python3-setuptools              \
        python3-venv                    \
        rsyslog                         \
        sudo                            \
        tmpreaper                       \
        unzip                           \
        vim                             \
        wget                            \
        xz-utils                        \
        zstd                         && \
    apt-get purge -y isc-dhcp-client && \
    apt-get clean -y                 && \
    apt-get autoremove --purge -y    && \
    rm -rf /var/lib/apt/lists/*      && \
    rm -rf /tmp/* /var/tmp/*

RUN systemctl enable ssh.service                 && \
    systemctl disable systemd-timesyncd.service  && \
    echo "exit 0" > /usr/sbin/policy-rc.d

RUN systemctl disable getty@  && \
    systemctl disable getty.target  && \
    rm /lib/systemd/system/multi-user.target.wants/getty.target  && \
    rm /lib/systemd/system/getty.target.wants/getty-static.service

RUN useradd --create-home --shell /bin/bash --groups adm ansible        && \
    install -d -o ansible -m 0700 /home/ansible/.ssh  && \
    echo -n 'ansible:ansible' | chpasswd

RUN mkdir -p /etc/sudoers.d && install -b -m 0440 /dev/null /etc/sudoers.d/ansible  && \
    echo 'ansible ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/ansible

RUN /bin/echo -e '#!/bin/sh\ncp /tmp/authorized_keys ~ansible/.ssh\nchown ansible:ansible ~ansible/.ssh/authorized_keys' >> /etc/rc.local && \
    chmod 755 /etc/rc.local


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

STOPSIGNAL SIGRTMIN+3

CMD ["/lib/systemd/systemd"]

