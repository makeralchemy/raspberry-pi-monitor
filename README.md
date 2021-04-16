# raspberry pi monitor

## Overview
*monitor.py* is a Python program used to display Raspberry Pi system status on an Adafruit SSD1306 compatible display.
The program uses four lines on the display to show the hostname, IP address, CPU load, and memory usage.
On the far right of first line line, a heart icon blinks (aka a heart beat) to show that the Raspberry Pi is running and not hung or stopped.
When the program is terminated, the number of heart beats recorded from the time the program was started will be displayed.

This program was inspired by my building a Raspberry Pi cluster and wanting to have a way to to monitor the status of each Pi in the cluster on a set of small OLED displays
mounted on the top of the case for the Pi's.  The hardware includes a 128x64 pixel OLED display connected to each Raspberry Pi via I2C.  The displays are Adafruit SSD1306 compatible.

*monitor.py* was written for Python 3.7.x.

## Usage Instructions

*monitor.py* is intended to be executed from the command line, inside a shell script, or inside a boot script like *rc.local*.

### Command Line Usage:

    $ python3 monitor.py -h

    usage: monitor.py [-h] [-b HEARTBEAT] [-f]

    optional arguments
      -h, --help                   shows this help message and exit
      -b, --heartbeat HEARTBEAT    number of seconds between heart beats
      -f, --freeze                 freeze the display when the program stops

### Command Line Examples
Start the monitor using the default of 0.25 seconds between heart beats. 
When the program stops, display the number of heart beats while the program was running.

     $ python3 monitor.py

Start the monitor with 0.5 seconds between heart beats.
When the program stops, display the number of heart beats while the program was running.

     $ python3 monitor.py -b 0.5

Start the monitor with 2 seconds between heart beats.
Freeze the display with the system information when the program is stopped:

     $ python3 monitor.py --freeze --heartbeat 2

Start the monitor with the default time between heart beats and freeze the display with
the system information when the program is stopped:

     $ python3 monitor.py -f

### Sample of displays

When running:

     Host: master
     IP: 192.168.1.128
     CPU Load: 0.50
     Mem: 361/927MB 38.94%

When stopped and the freeze option not specified:

     Monitor stopped after
     3,422 heartbeats

## Installation Instructions

Before installing the libraries, you should run the standard updates:

     sudo apt-get update
     sudo apt-get upgrade
     sudo pip3 install --upgrade setuptools
     
If the last command above doesn't work, try:

     sudo apt-get install python3-pip 
     
Adafruit provides a script to ensure the Raspberry Pi is correctly configured and installs the Blinka library. 
Blinka brings CircuitPython APIs and CircuitPython libraries to single board computers (SBCs) for cross platform portability.
It requires just a few commands to run. Most of it is installing the dependencies.     
     
     cd ~
     sudo pip3 install --upgrade adafruit-python-shell
     wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
     sudo python3 raspi-blinka.py

When configuring the Raspian on the Raspberry Pi using the command "sudo raspi-config", make sure to enable the I2C interface. 
More details on enabling and checking the I2C interface can be found at https://adafru.it/Deo.

Create a directory for the monitor program:

     cd examples
     mkdir monitor
     cd monitor

Install the monitor code:

     git clone https://github.com/makeralchemy/raspberry-pi-monitor

Make the program executable:

     chmod +x monitor.py

To make 'monitor.py' start upon boot, copy the service file into the systemd services directory:

     sudo cp monitor.service /etc/systemd/system/monitor.service

To start the monitoring service:

     sudo systemctl start monitor.service

To stop the monitoring service:

     sudo systemctl stop monitor.service

When you are satisfied that this starts and stops the monitoring program, it can be enabled to start automatically on reboot by using this command:

     sudo systemctl enable monitor.service

## License
This project is licensed under the MIT license.
