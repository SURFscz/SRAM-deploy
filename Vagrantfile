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
  "m1" => { "name" => "ldap", "ip" => "172.20.1.20", "hostname" => "ldap.scz.vnet", "limit" => ['ldap'] },
  "m2" => { "name" => "comanage", "ip" => "172.20.1.21", "hostname" => "comanage.scz.vnet", "limit" => ['comanage'] },
  "m3" => { "name" => "proxy", "ip" => "172.20.1.22", "hostname" => "proxy.scz.vnet", "limit" => ['proxy'] },
  "m4" => { "name" => "meta", "ip" => "172.20.1.23", "hostname" => "meta.scz.vnet", "limit" => ['meta'] }
}

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    config.vm.box = "debian/stretch64"

    # being paranoid and all, we don't trust random updated images without
    # manually checking sha256sums against https://cloud.alioth.debian.org/vagrantboxes/
    config.vm.box_check_update = false
    config.vm.box_download_checksum_type = "sha256"
    config.vm.box_download_checksum = "ecd924aae99d1e029e795cb55775bb96aabb77ab122f3ab4d3655589fd5674cd"

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

    (1..N).each do |machine_id|
        machine = machines["m#{machine_id}"]
	    config.vm.define machine["name"] do |m|
		    m.vm.network :private_network, ip: machine["ip"]
		    m.vm.hostname = machine["hostname"]
		    m.vm.provider "virtualbox" do |v|
		        v.name = "SCZ #{machine['name']}"
		    end
            m.ssh.insert_key = false

            # we add the key to authorized_keys instead of provisioning the entire file, to allow
            # vagrant to reprovision running boxes. In that case, both the vagrant key and the
            # generated key need to be allowed
            config.vm.provision "file", source: sshkeypub, destination: "~/.ssh/provision_key.pub"
            config.vm.provision :shell do |shell|
                shell.inline = "cat /home/vagrant/.ssh/provision_key.pub >> \
                               /home/vagrant/.ssh/authorized_keys; \
                                echo '' >> /home/vagrant/.ssh/authorized_keys"
            end

            if machine_id == N
                m.vm.provision :ansible do |ansible|
                    # Disable default limit to connect to all the machines
                    ansible.limit = "all"
                    ansible.playbook = "provision.yml"
                    ansible.inventory_path = "./environments/vm/inventory"
#                    ansible.verbose = 3
#                    ansible.raw_arguments = "-vvv"
                    ansible.raw_ssh_args = ["-o IdentityFile=.vagrant/id_rsa"]
                    ansible.limit = "comanage,ldap,proxy,meta"
                    ansible.extra_vars = {
                        user: "vagrant",
                        secrets_file: "environments/vm/secrets/all.yml",
                    }
                end
            end
        end
    end
end
