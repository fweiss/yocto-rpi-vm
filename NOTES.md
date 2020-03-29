List of targets (images):

cd ~/poky
ls meta*/recipes*/images/*.bb

directory structure:

/home/vagrant/
  build/
  sources/
     meta-openembedded/ <<git>>
     meta-rapsberrypi/ <<git>>
     poky/ <<git>>

/vagrant/ <<git>>
  boot/
  conf/
  root/
  scripts/
  *

/vagrant/
  build/
  sources/
     poky/ <linked <git>>
     meta-openembedded/ <<linked git>>
     meta-rapsberrypi/ <<linked git>>
     meta-rover/ <<git>>
       COPYING.MIT
       README
       conf/
         layer.conf
         
       
    
     