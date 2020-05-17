Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial32"
  config.disksize.size = '64GB'
  
  config.vm.provider "virtualbox" do |v|
  	v.memory = 4096
  	v.cpus = 4
  end

  config.vm.provision :chef_solo do |chef|
    chef.arguments = "--chef-license accept"
    chef.add_recipe 'yocto'
  end

end
