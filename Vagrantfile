# -*- mode: ruby -*- vi: set ft=ruby:sw=4:s=4:noexpandtab :

# Generate a single new ssh key to use for all VMs
# By default, vagrant generates a key for each VM, but put is in a
# provider-dependent location.  Here, we want to support both vbox and
# libvirt, and there is no way to tell ansible to look for the key in two
# locations.  So, we just do this bij hand...
require 'vagrant/util/keypair'
env = Vagrant::Environment.new()
sshkeypriv = Pathname.new(env.local_data_path) + 'sshid'
sshkeypub  = Pathname.new(env.local_data_path) + 'sshid.pub'
if ARGV[0] == "up"  and  ( !sshkeypriv.exist?  or  !sshkeypub.exist? )
	# see https://github.com/mitchellh/vagrant/blob/master/plugins/communicators/ssh/communicator.rb#L183-L193
	puts "Generating new ssh key to use"
	pub, priv, _ = Vagrant::Util::Keypair.create
	sshkeypriv.open("w+").write(priv)
	sshkeypub.open("w+").write(pub)
end


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

	config.ssh.insert_key = false
	config.vm.provision "file", source: sshkeypub, destination: "~/.ssh/authorized_keys"

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

	config.vm.define "lb" do |lb|
		lb.vm.network :private_network, ip: "172.20.1.20"
		lb.vm.hostname = "lb.scz.vnet"
	end
	config.vm.define "comanage" do |lb|
		lb.vm.network :private_network, ip: "172.20.1.21"
		lb.vm.hostname = "comanage.scz.vnet"
	end

end
