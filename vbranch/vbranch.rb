#!/usr/bin/env ruby

#This is a quick script to spin up a vm based on a git branch

#Idea: you need a vm to test something locally in a branch. Why not do it all at once?
#./vbranch <branch_name>

require 'fileutils'
require 'net/http'
vagrant_dir = "<path_to_vagrant_stuff>"
testing_repo = "<path_to_testing_repo>
branch_name = ARGV[0]

now = Time.now
vconfig = <<-EOF
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|

  config.vm.customize [
  "modifyvm", :id,
  "--name", "#{branch_name}",
  "--memory", "256"
  ]

  config.vm.host_name = "#{branch_name}"
  config.ssh.forward_agent = true 
  config.vm.box = "debsqueeze"
  #config.vm.forward_port 80, 80
  #config.vm.forward_port 22, 2022
  config.vm.network :hostonly, "192.168.10.10"
  config.vm.share_folder "local_repo", "/repo", "#{testing_repo}"

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "manifests"
    puppet.manifest_file = "branch.pp"
  end
  #config.vm.boot_mode = :gui
end
  EOF

puts  "Creating vm for branch: " + branch_name
#puts vconfig

vbranch_dir = vagrant_dir + branch_name

FileUtils.mkdir_p(vbranch_dir)
FileUtils.cd(vbranch_dir, :verbose => true) 
FileUtils.cp_r(vagrant_dir + '/manifests', vbranch_dir)

# open and write to a file with ruby
open('Vagrantfile', 'w') { |f|
  f.puts vconfig
}

a = system('git clone <repo> -- hard coded change')

#Make sure node is picked up by puppet
manifest_add = <<-EOF
node #{branch_name} inherits default {
}
  EOF
# open and write to a file with ruby
open('puppet/manifests/site.pp', 'a') { |f|
  f.puts manifest_add
}

b = system('vagrant up')
#system('vagrant ssh -c "/usr/local/bin/run"')
c = system('vagrant status')
d = system('vagrant ssh')

if ARGV[0] == 'kill'
  puts 'kill'
  vagrant destroy -f
end

puts a
