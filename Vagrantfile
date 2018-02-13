# -*- mode: ruby -*- vi: set ft=ruby:sw=4:s=4:expandtab :

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
        "hostname"  => "ldap.#{domain}",
        "limit"     => ['ldap'],
        "ports"     => [ '2222:22','2280:80','2243:443'] },
    "m2" => {
        "name"      => "comanage",
        "ip"        => "172.20.1.21",
        "hostname"  => "comanage.#{domain}",
        "limit"     => ['comanage'],
        "ports"     => [ '2322:22','2380:80','2343:443'] },
    "m3" => {
        "name"      => "proxy",
        "ip"        => "172.20.1.22",
        "hostname"  => "proxy.#{domain}",
        "limit"     => ['proxy'],
        "ports"     => [ '2422:22','2480:80','2443:443'] },
    "m4" => {
        "name"      => "meta",
        "ip"        => "172.20.1.23",
        "hostname"  => "meta.#{domain}",
        "limit"     => ['meta'],
        "ports"     => [ '2522:22','2580:80','2543:443'] },
    "m5" => {
        "name"      => "lb",
        "ip"        => "172.20.1.24",
        "hostname"  => "lb.#{domain}",
        "limit"     => ['lb'],
        "ports"     => [ '2622:22','2680:80','2643:443'] },
    "m6" => {
        "name"      => "client",
        "ip"        => "172.20.1.25",
        "hostname"  => "client.#{domain}",
        "limit"     => ['client'],
        "ports"     => [ '2722:22','2780:80','2743:443'] }
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
        override.vm.box = "debian/stretch64"
        # being paranoid and all, we don't trust random updated images without
        # manually checking sha256sums against https://cloud.alioth.debian.org/vagrantboxes/
        override.vm.box_check_update = false
        override.vm.box_download_checksum_type = "sha256"
        override.vm.box_download_checksum = "ecd924aae99d1e029e795cb55775bb96aabb77ab122f3ab4d3655589fd5674cd"

        # install a swap daemon (needer for php/composer, ao)
        override.vm.provision "shell", inline: "sudo env DEBIAN_FRONTEND=noninteractive apt-get -qq -y install swapspace > /dev/null"

        vb.cpus = "1"
        vb.memory = "768"
    end
    config.vm.provider "libvirt" do |lv, override|
        override.vm.box = "debian/stretch64"
        # being paranoid and all, we don't trust random updated images without
        # manually checking sha256sums against https://cloud.alioth.debian.org/vagrantboxes/
        override.vm.box_check_update = false
        override.vm.box_download_checksum_type = "sha256"
        override.vm.box_download_checksum = "ecd924aae99d1e029e795cb55775bb96aabb77ab122f3ab4d3655589fd5674cd"

        # install a swap daemon (needer for php/composer, ao)
        override.vm.provision "shell", inline: "sudo env DEBIAN_FRONTEND=noninteractive apt-get -qq -y install swapspace > /dev/null"

        lv.cpus = "1"
        lv.memory = "768"
        lv.graphics_type = "spice"
        lv.video_type = "qxl"
    end

    if Vagrant.has_plugin?("vagrant-cachier")
        config.cache.scope = :box
        config.cache.synced_folder_opts = {
            type: :rsync,
            owner: "_apt",
        }
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

        config.vm.define machine["name"], autostart: true do |m|
            m.vm.network :private_network, ip: machine["ip"]
            m.vm.hostname = machine["hostname"]
            m.vm.provider "virtualbox" do |v|
                v.name = "SCZ #{machine['name']}"
            end

            m.vm.provider "docker" do |dk|
                dk.name = machine['name']
                dk.build_dir ="./docker/#{machine['name']}"
                dk.build_args = ["-t", "scz:#{machine['name']}" ]
                dk.remains_running = false
                dk.has_ssh = false
            end

            if machine_id == N
                m.vm.provider "docker" do |dk|
                    dk.cmd = ["/usr/sbin/sshd", "-D" ]
                    dk.remains_running = true
                    dk.has_ssh = true
                    dk.compose = true
                    dk.compose_configuration = {
                        "services" => {
                            machines["m1"]["name"] => {
                                "build" => {
                                    "context" => "../../docker/#{machines['m1']['name']}"
                                },
                                "command" => ["/usr/sbin/sshd", "-D" ],
                                "image" => "scz:#{machines['m1']['name']}",
                                "hostname" => "#{machines['m1']['name']}.#{domain}",
                                "networks" => {
                                    "scznet" => {
                                        "ipv4_address" => machines["m1"]["ip"]
                                    }
                                }
                            },
                            machines["m2"]["name"] => {
                                "build" => {
                                    "context" => "../../docker/#{machines['m2']['name']}"
                                },
                                "command" => ["/usr/sbin/sshd", "-D" ],
                                "image" => "scz:#{machines['m2']['name']}",
                                "hostname" => "#{machines['m2']['name']}.#{domain}",
                                "networks" => {
                                    "scznet" => {
                                        "ipv4_address" => machines["m2"]["ip"]
                                    }
                                }
                            },
                            machines["m3"]["name"] => {
                                "build" => {
                                    "context" => "../../docker/#{machines['m3']['name']}"
                                },
                                "command" => ["/usr/sbin/sshd", "-D" ],
                                "image" => "scz:#{machines['m3']['name']}",
                                "hostname" => "#{machines['m3']['name']}.#{domain}",
                                "networks" => {
                                    "scznet" => {
                                        "ipv4_address" => machines["m3"]["ip"]
                                    }
                                }
                            },
                            machines["m4"]["name"] => {
                                "build" => {
                                    "context" => "../../docker/#{machines['m4']['name']}"
                                },
                                "command" => ["/usr/sbin/sshd", "-D" ],
                                "image" => "scz:#{machines['m4']['name']}",
                                "hostname" => "#{machines['m4']['name']}.#{domain}",
                                "networks" => {
                                    "scznet" => {
                                        "ipv4_address" => machines["m4"]["ip"]
                                    }
                                }
                            },
                            machines["m5"]["name"] => {
                                "build" => {
                                    "context" => "../../docker/#{machines['m5']['name']}"
                                },
                                "command" => ["/usr/sbin/sshd", "-D" ],
                                "image" => "scz:#{machines['m5']['name']}",
                                "hostname" => "#{machines['m5']['name']}.#{domain}",
                                "networks" => {
                                    "scznet" => {
                                        "ipv4_address" => machines["m5"]["ip"]
                                    }
                                }
                            },
                            machines["m6"]["name"] => {
                                "build" => {
                                    "context" => "../../docker/#{machines['m6']['name']}"
                                },
                                "command" => ["/usr/sbin/sshd", "-D" ],
                                "image" => "scz:#{machines['m6']['name']}",
                                "hostname" => "#{machines['m6']['name']}.#{domain}",
                                "networks" => {
                                    "scznet" => {
                                        "ipv4_address" => machines["m6"]["ip"]
                                    }
                                }
                            }
                        },
                        "networks" => {
                            "scznet" => {
                                "driver" => "bridge",
                                "ipam" => {
                                    "config" => [{
                                        "subnet" => "172.20.1.0/24",
                                        "gateway" => "172.20.1.1"
                                    }]
                                }
                            }
                        }
                    }
                end

                m.vm.provision :ansible do |ansible|
                    # Note: recent versions of Vagrant need this, but older
                    # version choke on it
                    #ansible.compatibility_mode = "2.0"
                    ansible.playbook = "provision.yml"
                    ansible.inventory_path = "./environments/vm/inventory"
                    #ansible.verbose = 3
                    #ansible.raw_arguments = "-vvv"
                    ansible.limit = "comanage,ldap,proxy,meta,lb,client"
                    #ansible.tags = "clients,comanage"
                    ansible.extra_vars = {
                        secrets_file: "environments/vm/secrets/all.yml",
                    }
                end
            end
        end
    end
end
