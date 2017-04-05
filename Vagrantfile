# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  #config.vm.network "forwarded_port", guest: 80, host: 8080,  host_ip: "127.0.0.1"
  # neo4j port
  config.vm.network "forwarded_port", guest: 7474, host: 7474,  host_ip: "127.0.0.1"
  # neo4j bolt port
  config.vm.network "forwarded_port", guest: 7687, host: 7687,  host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  #  config.vm.network "private_network", ip: "192.168.33.10"

  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
  end

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.verbose        = true
    ansible.install        = true
    ansible.limit          = "all"
    ansible.inventory_path = "inventory"
  end

end
