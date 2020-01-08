# todo do this with yocto
groupadd i2c
chgrp i2c /dev/i2c-1
chmod g+rw /dev/i2c-1
useradd pi -G i2c
# usermod -a -G i2c pi
passwd pi
# passwd -d pi
