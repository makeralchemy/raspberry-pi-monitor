# raspberry pi monitor

## Overview
*monitor.py* is a Python program used to display Raspberry Pi system status on an Adafruit SSD1306 compatible display.
The program uses four lines on the display to show the hostname, IP address, CPU load, and memory usage.
On the far right of first line line, a heart icon blinks (aka a heart beat) to show that the Raspberry Pi is running and not hung or stopped.
When the program is terminated, the number of heart beats recorded from the time the program was started will be displayed.

This program was inspired by my building a Raspberry Pi cluster and wanting to have a way to to monitor the status of each Pi in the cluster on a set of small OLED displays
mounted on the top of the case for the Pi's.  The hardware includes a 128x64 pixel OLED display connected to each Raspberry Pi via I2C.  The displays are Adafruit SSD1306 compatible.

*monitor.py* was written for Python 2.7.x.

## Usage Instructions

*monitor.py* is intended to be executed from the command line, inside a shell script, or inside a boot script like *rc.local*.

### Command Line Usage:

    $ python monitor.py -h

    usage: monitor.py [-h] [-b HEARTBEAT]

    optional arguments
      -h, --help                   shows this help message and exit
      -b, --heartbeat HEARTBEAT    number of seconds between heart beats

### Command Line Examples
Start the monitor using the default of 0.25 seconds between heart beats

     $ python monitor.py

Start the monitor with 0.5 seconds between heart beats:

     $ python monitor.py -b 0.5

Start the monitor with 2 seconds between heart beats:

     $ python monitor.py --heartbeat 2

### Sample of displays

When running:

     Host: master
     IP: 192.168.1.128
     CPU Load: 0.50
     Mem: 361/927MB 38.94%

When stopped:

     Monitor stopped after
     3,422 heartbeats

## Installation Instructions

When configuring the Raspian on the Raspberry Pi using the command "sudo raspi-config", make sure to enable the I2C interface.

The following libraries may already be installed but these commands should be run anyways to ensure the libraries are there:

     sudo apt-get install python-dev
     sudo apt-get install -y python-imaging python-smbus i2c-tools

To install the required Adafruit libraries for SSD1306 based displays, run these commands:

     git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
     cd Adafruit_Python_SSD1306
     sudo python setup.py install

Create a directory for the monitor program:

     cd examples
     mkdir monitor

Install the monitor code:

     git clone https://github.com/makeralchemy/raspberry-pi-monitor

## License
This project is licensed under the MIT license.



