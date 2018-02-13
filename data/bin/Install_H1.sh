#!/bin/bash
# A script to install H1 binaries and required system files on an H1 system.
# Do NOT run with sudo or as root. For a new H1, use the f option to force replacement of
# files regardless of date.
# Example for new H1:
# $ ./Install_H1.sh f
#if [[ $#>0 && "$1" =~ [-?f] ]]
#then
  KEEP_NEWER=""
#else
#  KEEP_NEWER="--keep-newer-files"
#fi
#    Reset pulseaudio
rm -rf ~/.config/pulse
pulseaudio -k
sudo rm -fv /bin/cam_setting
rm -fv /home/ubuntu/Desktop/*
sudo rm -fv /etc/xdg/autostart/nvchrome.*
mkdir -pv /home/ubuntu/h1_exe_old
mkdir -pv /home/ubuntu/h1_exe
mv -fv /home/ubuntu/h1_exe/*manager /home/ubuntu/h1_exe_old
# Options for tar:
#   x extract
#   v verbose
#   P use absloute directory path structure (to install in root directory).
#   --keep-newer-files this means the script will only update old files.)
#   f H1.tgz specifies the source tar file.
sudo tar -xvPf /media/ubuntu/USB/cobanvideos/bin/H1.tgz  $KEEP_NEWER
sudo chown -R ubuntu:ubuntu /home/ubuntu
# settings
dconf load / </usr/share/CobanH1/dconfdump.txt
if [[ -x "/usr/share/dbus-1/services/org.freedesktop.Notifications.service" ]]
then
 sudo mv /usr/share/dbus-1/services/org.freedesktop.Notifications.service /usr/share/dbus-1/services/org.freedesktop.Notifications.service.disabled
fi
# Move original nautilus program aside and replace with a script from H1.tgz.
lineCount=$(wc -l /usr/bin/nautilus)
lineCount=${lineCount%%/*s}
var100=100
if (( lineCount > var100 ))
then
	sudo mv /usr/bin/nautilus /usr/bin/nautilus-original
fi
sudo ln -s /usr/bin/nautilus-x1 /usr/bin/nautilus 2>/dev/null

sudo usermod -a -G syslog,adm,video,audio,dialout,i2c,tty,input,netdev ubuntu
gsettings set org.gnome.settings-daemon.plugins.power button-power nothing
gsettings set org.gnome.nm-applet suppress-wireless-networks-available true
# Fix display configuration
xrandr --output DSI-0 --left-of HDMI-0
xrandr --output HDMI-0

