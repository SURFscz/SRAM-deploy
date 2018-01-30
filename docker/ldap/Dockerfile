FROM debian:stretch
LABEL maintainer="SURFnet <info@surfnet.nl>"
LABEL name=ldap

# Install base tools: sshd, python
RUN apt-get update
RUN apt-get install -y openssh-server python2.7 python3 python sudo

EXPOSE 22
EXPOSE 80
EXPOSE 389
EXPOSE 443
EXPOSE 636

RUN mkdir -p /var/run/sshd
RUN chmod 0755 /var/run/sshd

# Create and configure vagrant user
RUN useradd --create-home -s /bin/bash vagrant
WORKDIR /home/vagrant

# Configure SSH access
RUN mkdir -p /home/vagrant/.ssh
RUN echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key" > /home/vagrant/.ssh/authorized_keys
# RUN echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8M1AhJNqVuB3kdOt4WKnYryqIKow8Z1FTfFlsFXEIav6UdpoEixo6RhED2q2yGbhymg/onGpewc+AoHqN/lyzyE1EpbW4ubqhhvsZ8tcMChWcJmSAIgjweRo6wMfYk7bcPzYUV+V1iWOhIeMAtU9YsiySfbm+a7W9mKdYZgeNRaoqP7RAcXzQOh2O/Z3wgNJBjxcrCKoeBQcI9xSlPnAFFhlizwUZVmk+CmcJSojw0p0q+4AUOfTY7KhgQ9bGMgFIkauozv4tTc4KalzVqCgVRe9LwFaMtPBG2HP5Il/sjuo0r9lkeHVlejOd2HuXH6+uiLiC0V7R5H0z3Ygnz6oT vagrant" >> /home/vagrant/.ssh/authorized_keys
RUN chown -R vagrant: /home/vagrant/.ssh
RUN echo -n 'vagrant:vagrant' | chpasswd

# Enable passwordless sudo for the "vagrant" user
RUN mkdir -p /etc/sudoers.d
RUN install -b -m 0440 /dev/null /etc/sudoers.d/vagrant
RUN echo 'vagrant ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/vagrant

# Clean up APT when done.

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
