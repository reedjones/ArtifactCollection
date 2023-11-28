Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"  # Choose a base box that matches your production environment

  # Customize VM settings as needed
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 2
  end

  # Forward SSH agent to the VM (for key-based authentication)
  config.ssh.forward_agent = true

  # Define provisioning script
  config.vm.provision "shell", path: "deploy_vagrant.sh"
end