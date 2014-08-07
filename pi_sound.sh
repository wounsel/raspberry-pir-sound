#
#! /bin/sh
#! /etc/init.d/pi_sound

case "$1" in
  start)
    echo "Starting Raspberry Pi Sound Script"
    # run application you want to start
    sudo mount /dev/sda1 /mnt/usbdrive
    sudo python2 /mnt/usbdrive/pir_sound.py
    ;;
  stop)
    echo "Stopping Raspberry Pi Sound Script"
    # kill application you want to stop
    killall python2
    ;;
  *)
    echo "Usage: /etc/init.d/pi_sound {start|stop}"
    exit 1
    ;;
esac

exit 0


