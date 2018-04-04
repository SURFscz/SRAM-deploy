# -*- mode: ruby -*- vi:ft=ruby:sw=4:ts=4:expandtab:

# Vagrant boxes location has changed
Vagrant::DEFAULT_SERVER_URL.replace('https://vagrantcloud.com')

# Generate a single new ssh key to use for all VMs
# By default, vagrant generates a key for each VM, but put is in a
# provider-dependent location.  Here, we want to support both vbox and
# libvirt, and there is no way to tell ansible to look for the key in two
# locations.  So, we just do this by hand...
require 'vagrant/util/keypair'
env = Vagrant::Environment.new()
sshkeypriv = Pathname.new(env.local_data_path) + 'id_rsa'
sshkeypub  = Pathname.new(env.local_data_path) + 'id_rsa.pub'
if ARGV[0] == "up"  and  ( !sshkeypriv.exist?  or  !sshkeypub.exist? )
    # see https://github.com/mitchellh/vagrant/blob/master/plugins/communicators/ssh/communicator.rb#L183-L193
    puts "Generating new ssh key to use"
    pub, priv, openssh = Vagrant::Util::Keypair.create
    sshkeypriv.open("w+").write(priv)
    sshkeypub.open("w+").write(openssh)

    File.chmod(0600,sshkeypriv)
end

ENV['COMPOSE_PROJECT_NAME']="scz"

domain = "scz-vm.net"
machines = {
    "m1" => {
        "name"      => "ldap",
        "ip"        => "172.20.1.20",
        "hostname"  => "ldap.vm.#{domain}",
        "limit"     => ['ldap'],
        "ports"     => [ '2222:22' ] },
    "m2" => {
        "name"      => "comanage",
        "ip"        => "172.20.1.21",
        "hostname"  => "comanage.vm.#{domain}",
        "limit"     => ['comanage'],
        "ports"     => [ '2322:22'] },
    "m3" => {
        "name"      => "proxy",
        "ip"        => "172.20.1.22",
        "hostname"  => "proxy.vm.#{domain}",
        "limit"     => ['proxy'],
        "ports"     => [ '2422:22' ] },
    "m4" => {
        "name"      => "meta",
        "ip"        => "172.20.1.23",
        "hostname"  => "meta.vm.#{domain}",
        "limit"     => ['meta'],
        "ports"     => [ '2522:22' ] },
    "m5" => {
        "name"      => "lb",
        "ip"        => "172.20.1.24",
        "hostname"  => "lb.vm.#{domain}",
        "limit"     => ['lb'],
        "ports"     => [ '2622:22','2680:80','2643:443', '2689:389', '2639:636' ] },
    "m6" => {
        "name"      => "client",
        "ip"        => "172.20.1.25",
        "hostname"  => "client.vm.#{domain}",
        "limit"     => ['client'],
        "ports"     => [ '2722:22' ] }
}

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    # Workaround for ttyname errors: https://stackoverflow.com/questions/40815349/
    config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
    config.ssh.private_key_path = [sshkeypriv,"~/.vagrant.d/insecure_private_key"]
    config.ssh.insert_key = false

    config.vm.synced_folder ".", "/vagrant", disabled: true

    # because docker does not require an image (and in fact, we want it provisioned
    # atop our current OS) we put box information inside the providers that actually
    # need to download the box
    config.vm.provider "virtualbox" do |vb, override|
        # being paranoid and all, we don't trust random updated images without
        # manually checking sha256sums against https://cloud.alioth.debian.org/vagrantboxes/
        # and vagrant, being stupid and all, refuses to check checksums for regular vargantcloud downloads
        # so we simply specify everything manually
        override.vm.box = "Debian 9 (Stretch)"
        override.vm.box_url = "https://vagrantcloud.com/debian/boxes/stretch64/versions/9.3.0/providers/virtualbox.box"
        override.vm.box_download_checksum_type = "sha256"
        override.vm.box_download_checksum = "22620dd2b655db09ea991d156353dac35969e798fe3d031638d7316a5f570989"

        # install a swap daemon (needed for php/composer)
        override.vm.provision "shell", inline: "sudo env DEBIAN_FRONTEND=noninteractive apt-get -qq -y install swapspace > /dev/null"

        vb.cpus = "1"
        vb.memory = "768"
    end
    config.vm.provider "libvirt" do |lv, override|
        # being paranoid and all, we don't trust random updated images without
        # manually checking sha256sums against https://cloud.alioth.debian.org/vagrantboxes/
        # and vagrant, being stupid and all, refuses to check checksums for regular vargantcloud downloads
        # so we simply specify everything manually
        override.vm.box = "Debian 9 (Stretch)"
        override.vm.box_url = "https://vagrantcloud.com/debian/boxes/stretch64/versions/9.3.0/providers/libvirt.box"
        override.vm.box_download_checksum_type = "sha256"
        override.vm.box_download_checksum = "33f9f97fa8a4bbf9828a2609b386a6696126ddc29be9e03656a22108c9e425f2"

        # install a swap daemon (needed for php/composer)
        override.vm.provision "shell", inline: "sudo env DEBIAN_FRONTEND=noninteractive apt-get -qq -y install swapspace > /dev/null"

        lv.cpus = "1"
        lv.memory = "768"
        lv.graphics_type = "spice"
        lv.video_type = "qxl"
    end

    # use a proxy on the VM host to cache deb packages for the VMs
    # to use this, install apt-cacher-ng on the host, and run
    # vagrant plugin install vagrant-proxyconf
    if Vagrant.has_plugin?("vagrant-proxyconf")
        config.apt_proxy.http = "http://172.20.1.1:3142/"
        config.proxy.no_proxy = "localhost,127.0.0.1,.#{domain}"
    end

    config.vm.provider "docker" do |dk, override|
        # create a docker client network
        Vagrant::Util::Subprocess.execute('bash','-c',
            "(docker network list | grep 'scznet') || \
              docker network create --attachable --driver bridge \
                --gateway 172.20.1.1 --subnet 172.20.1.0/24 scznet",
            :notify => [:stdout, :stderr]
        )
        # disable proxying
        override.proxy.enabled = false
    end

    # we add the key to authorized_keys instead of provisioning the entire file, to allow
    # vagrant to reprovision running boxes. In that case, both the vagrant key and the
    # generated key need to be allowed
    config.vm.provision "file", source: sshkeypub, destination: "~/.ssh/provision_key.pub"
    config.vm.provision :shell do |shell|
        shell.inline = "cat /home/vagrant/.ssh/provision_key.pub >> \
                        /home/vagrant/.ssh/authorized_keys; \
                        echo '' >> /home/vagrant/.ssh/authorized_keys"
    end

    N=machines.length
    (1..N).each do |machine_id|
        machine = machines["m#{machine_id}"]
        machinename = "#{machine['name']}"

        config.vm.define machinename, autostart: true do |m|
            m.vm.network :private_network, ip: machine["ip"]
            m.vm.hostname = machinename
            m.vm.provider "virtualbox" do |v|
                v.name = "SCZ #{machine['name']}"
            end

            m.vm.provider "docker" do |dk|
                dk.name = machinename
                dk.build_dir ="./docker"
                dk.build_args = ["-t", "scz" ]
                dk.remains_running = true
                dk.has_ssh = true
                create_args = [
                    "-d", "-t", "-i",
                    "--network", "scznet",
                    "--ip", "#{machine['ip']}",
                    # internal names (used for LB rerouting)
                    "--add-host", "#{machines['m1']['hostname']}:#{machines['m1']['ip']}",
                    "--add-host", "#{machines['m2']['hostname']}:#{machines['m2']['ip']}",
                    "--add-host", "#{machines['m3']['hostname']}:#{machines['m3']['ip']}",
                    "--add-host", "#{machines['m4']['hostname']}:#{machines['m4']['ip']}",
                    "--add-host", "#{machines['m5']['hostname']}:#{machines['m5']['ip']}",
                    "--add-host", "#{machines['m6']['hostname']}:#{machines['m6']['ip']}",
                    # (unused) interface for outgoing mail
                    "--add-host", "outgoing.#{domain}:172.20.1.1",
                    # add options to get systemd to run properly
                    "-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro",
                    "--tmpfs", "/run",
                    "--tmpfs", "/tmp:exec" # need exec for vagrant
                ]
                if machine['name'] == "lb"
                    # for the loadbalancer, make sure we point to the right hosts
                    create_args = create_args + [
                        "--add-host", "proxy.#{domain}:#{machines['m3']['ip']}",
                        "--add-host", "mdq.#{domain}:#{machines['m3']['ip']}",
                        "--add-host", "cm.#{domain}:#{machines['m3']['ip']}",
                        "--add-host", "comanage.#{domain}:#{machines['m2']['ip']}",
                        "--add-host", "ldap.#{domain}:#{machines['m1']['ip']}",
                        "--add-host", "meta.#{domain}:#{machines['m4']['ip']}",
                        "--add-host", "oidc-test.#{domain}:#{machines['m6']['ip']}",
                        "--add-host", "sp-test.#{domain}:#{machines['m6']['ip']}",
                        "--add-host", "idp-test.#{domain}:#{machines['m6']['ip']}"
                    ]
                else
                    # external interfaces are routed through the LB
                    create_args = create_args + [
                        "--add-host", "proxy.#{domain}:#{machines['m5']['ip']}",
                        "--add-host", "mdq.#{domain}:#{machines['m5']['ip']}",
                        "--add-host", "consent.#{domain}:#{machines['m5']['ip']}",
                        "--add-host", "comanage.#{domain}:#{machines['m5']['ip']}",
                        "--add-host", "ldap.#{domain}:#{machines['m5']['ip']}",
                        "--add-host", "meta.#{domain}:#{machines['m5']['ip']}",
                        "--add-host", "oidc-test.#{domain}:#{machines['m5']['ip']}",
                        "--add-host", "sp-test.#{domain}:#{machines['m5']['ip']}",
                        "--add-host", "idp-test.#{domain}:#{machines['m5']['ip']}",
                    ]
                end
                dk.create_args = create_args
            end

            ## obsolete; run start-vagrant instead
            # if machine_id == N
            #    m.vm.provision :ansible do |ansible|
            #        # Note: recent versions of Vagrant need this, but older
            #        # version choke on it
            #        #ansible.compatibility_mode = "2.0"
            #        ansible.playbook = "provision.yml"
            #        ansible.inventory_path = "./environments/vm/inventory"
            #        #ansible.verbose = 3
            #        #ansible.raw_arguments = "-vvv"
            #        ansible.limit = "comanage,ldap,proxy,meta,lb,client"
            #        #ansible.tags = "clients,comanage"
            #        ansible.extra_vars = {
            #            secrets_file: "environments/vm/secrets/all.yml",
            #        }
            #    end
            #end
        end
    end

    config.vm.provider "libvirt" do |lv,override|
        # workaround for Vagrant bug https://github.com/hashicorp/vagrant/issues/9592
        override.vm.provision :shell do |shell|
            shell.inline = "cd /etc/systemd/network && mv -v 99-dhcp.network 99Z-dhcp.network && systemctl restart systemd-networkd || true"
        end
    end

end
