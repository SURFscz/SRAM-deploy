# -*- mode: ruby -*- vi: set ft=ruby:sw=4:s=4:noexpandtab :

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

N=4
machines = {
  "m1" => {
    "name"      => "ldap",
    "ip"        => "172.20.1.20",
    "hostname"  => "ldap.scz.vnet",
    "limit"     => ['ldap'],
    "ports"     => [ '2222:22','2280:80','2243:443'] },
  "m2" => {
    "name"      => "comanage",
    "ip"        => "172.20.1.21",
    "hostname"  => "comanage.scz.vnet",
    "limit"     => ['comanage'],
    "ports"     => [ '2322:22','2380:80','2343:443'] },
  "m3" => {
    "name"      => "proxy",
    "ip"        => "172.20.1.22",
    "hostname"  => "proxy.scz.vnet",
    "limit"     => ['proxy'],
    "ports"     => [ '2422:22','2480:80','2443:443'] },
  "m4" => {
    "name"      => "meta",
    "ip"        => "172.20.1.23",
    "hostname"  => "meta.scz.vnet",
    "limit"     => ['meta'],
    "ports"     => [ '2522:22','2580:80','2543:443'] }
}

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    config.vm.synced_folder ".", "/vagrant", disabled: true
    #config.vm.box = "debian/stretch64"
    # being paranoid and all, we don't trust random updated images without
    # manually checking sha256sums against https://cloud.alioth.debian.org/vagrantboxes/
    #config.vm.box_check_update = false
    #config.vm.box_download_checksum_type = "sha256"
    #config.vm.box_download_checksum = "ecd924aae99d1e029e795cb55775bb96aabb77ab122f3ab4d3655589fd5674cd"

    # because docker does not require an image (and in fact, we want it provisioned
    # atop our current OS) we put box information inside the providers that actually
    # need to download the box
	config.vm.provider "virtualbox" do |vb|
		vb.cpus = "1"
		vb.memory = "512"
	end
	config.vm.provider "libvirt" do |lv|
		lv.cpus = "1"
		lv.memory = "512"
		lv.graphics_type = "spice"
		lv.video_type = "qxl"
	end
	config.vm.provider "docker" do |dk|
        # dk.image = "debian:stretch"
        # dk.ports = ['22:22', '80:80', '443:443']
        dk.build_dir = "./docker"
        dk.build_args = ["-t=scz"]
        dk.remains_running =true
        dk.has_ssh=true
        dk.cmd = ["/usr/bin/tail", "-f", "/dev/null" ]
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

#    machine1 = machines["m1"]
#    config.vm.define machine1["name"], autostart: true do |m|
#	    m.vm.network :private_network, ip: machine1["ip"]
#	    m.vm.hostname = machine1["hostname"]
#	    m.vm.provider "virtualbox" do |v|
#	        v.name = "SCZ #{machine1['name']}"
#	    end
#	    m.vm.provider "docker" do |dk|
#	        dk.name = machine1['name']
#	        dk.ports = machine1['ports']
#	    end
#       m.ssh.insert_key = false
#
#    end
#    machine2 = machines["m2"]
#    config.vm.define machine2["name"], autostart: true do |m|
#	    m.vm.network :private_network, ip: machine2["ip"]
#	    m.vm.hostname = machine2["hostname"]
#	    m.vm.provider "virtualbox" do |v|
#	        v.name = "SCZ #{machine2['name']}"
#	    end
#	    m.vm.provider "docker" do |dk|
#	        dk.name = machine2['name']
#	        dk.ports = machine2['ports']
#	    end
#       m.ssh.insert_key = false
#
#    end
#    machine3 = machines["m3"]
#    config.vm.define machine3["name"], autostart: true do |m|
#	    m.vm.network :private_network, ip: machine3["ip"]
#	    m.vm.hostname = machine3["hostname"]
#	    m.vm.provider "virtualbox" do |v|
#	        v.name = "SCZ #{machine3['name']}"
#	    end
#	    m.vm.provider "docker" do |dk|
#	        dk.name = machine3['name']
#	        dk.ports = machine3['ports']
#	    end
#        m.ssh.insert_key = false
#
#    end

    machine4 = machines["m4"]
    config.vm.define machine4["name"], autostart: true do |m|
	    m.vm.network :private_network, ip: machine4["ip"]
	    m.vm.hostname = machine4["hostname"]
	    m.vm.provider "virtualbox" do |v|
	        v.name = "SCZ #{machine4['name']}"
	    end
	    m.vm.provider "docker" do |dk|
	        dk.name = machine4['name']
	        dk.ports = machine4['ports']
	        dk.compose = true
	        dk.compose_configuration = {
                "networks" => {
                    "scznet" => {
                        "driver" => "bridge"
#                        "ipam" => {
#                            "config" => {
#                                "subnet" => "172.20.1.0/24",
#                                "ip_range" => "172.20.1.0/24",
#                                "gateway" =>  "172.20.1.1"	        
#	                         }
#	                     }
	                 }
	             }
	         }
	    end
        m.ssh.insert_key = false
        m.ssh.guest_port = 2522
        m.local_data_path = "docker"

        m.vm.provision :docker
        m.vm.provision :docker_compose do |dc|
            dc.yml = "/mnt/carn/raid/projects/surfnet/scz/SCZ-deploy/docker/docker-compose.yml"
        end

        m.vm.provision :ansible do |ansible|
            # Disable default limit to connect to all the machines
            ansible.limit = "all"
            ansible.playbook = "provision.yml"
            ansible.inventory_path = "./environments/vm/inventory"
#            ansible.verbose = 3
#            ansible.raw_arguments = "-vvv"
            ansible.raw_ssh_args = ["-o IdentityFile=.vagrant/id_rsa", "-D 2522"]
            ansible.limit = "comanage,ldap,proxy,meta"
            ansible.extra_vars = {
                user: "vagrant",
                secrets_file: "environments/vm/secrets/all.yml",
            }
        end
    end
end
