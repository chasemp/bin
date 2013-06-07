file {'/usr/local/bin/run':
      ensure  => present,
      mode => '0755',
      content => "#!/bin/bash
                  cd /vagrant/puppet
                  sudo ./localrun"
}
~>
exec{'run puppet update':
  command => "/usr/local/bin/run",
  logoutput => "on_failure"
}
~>
file {'/usr/local/bin/branch_me':
      ensure  => present,
      mode => '0755',
      content => "#!/bin/bash
                  cd /vagrant/puppet && git checkout -b `cat /etc/hostname`"
}
~>
exec{'create branch for vm':
  refreshonly => true,
  command => "/usr/local/bin/branch_me",
  logoutput => "on_failure"
}
->
file {'/usr/local/bin/user_setup':
      ensure  => present,
      mode => '0755',
      content => "#!/bin/bash
                  #drop user to root default
                  echo 'sudo -s' >> /home/vagrant/.bashrc
                  #drop root into puppet dir auto
                  echo 'cd /vagrant/puppet' >> /root/.bashrc
                  echo 'git branch' >> /root/.bashrc
                  echo 'ls' >> /root/.bashrc"
}
->
exec{'setup user stuff':
  command => "/usr/local/bin/user_setup",
  logoutput => "on_failure"
}
->
package { 'openssh-client': ensure => present }
->
package { 'git': ensure => present }
->
package { 'tree': ensure => present }
->
package { 'puppet': ensure => present }
->
package { 'runit': ensure => present }
->
package { 'apt-transport-https': ensure => present }
