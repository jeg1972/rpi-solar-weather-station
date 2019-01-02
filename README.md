# Raspberry Pi Based Solar Powered Weather Station 

Make these changes on the Raspberry Pi...

```
sudo vi /boot/config.txt
dtoverlay=w1-gpio
sudo reboot
sudo modprobe w1-gpio
sudo modprobe w1-therm
cd /sys/bus/w1/devices/
cd 28*
less w1_slave
```

Then run the *ds18b20.py* file.
