# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time
import sys
import argparse
import subprocess

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def monitor_stats(heart_beat):

    # Raspberry Pi pin configuration:

    # On the PiOLED the RST pin is not used
    RST = None

    # The following are only used with SPI:
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    # Beaglebone Black pin configuration:
    # RST = 'P9_12'
    # The following are only used with SPI:
    # DC = 'P9_15'
    # SPI_PORT = 1
    # SPI_DEVICE = 0

    # 128x32 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

    # 128x64 display with hardware I2C:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

    # You can change the I2C address by passing an i2c_address parameter like:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

    # Alternatively you can specify an explicit I2C bus number, for example
    # with the 128x32 display you would use:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

    # 128x32 display with hardware SPI:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC,
    #        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # 128x64 display with hardware SPI:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC,
    #        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # Alternatively you can specify a software SPI implementation by providing
    # digital GPIO pin numbers for all the required display pins.  For example
    # on a Raspberry Pi with the 128x32 display you might use:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25,
    #        cs=22)

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for
    # drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!

    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('Minecraftia.ttf', 8)

    # 'display_heart' will change from flip back and forth from true to false
    # during each loop in order to show the heart on the display - making it
    # blink on and off like the heart is beating.
    display_heart = True

    # the number of heart beats will be tracked and displayed on the display
    # when the program is stopped.
    heart_beats = 0

    # define the command that will be used to get the display info
    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    CMD_HOSTNAME = "hostname"
    CMD_IP_ADDR = "hostname -I | cut -d\' \' -f1"
    CMD_CPU_LOAD = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CMD_MEM_USAGE = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"

    try:

        while True:

            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, width, height), outline=0, fill=0)

            # Execute shell scripts to get system info
            HostName = subprocess.check_output(CMD_HOSTNAME, shell=True)
            IP = subprocess.check_output(CMD_IP_ADDR, shell=True)
            CPU = subprocess.check_output(CMD_CPU_LOAD, shell=True)
            MemUsage = subprocess.check_output(CMD_MEM_USAGE, shell=True)

            # draw a series of vertical lines to create the heart
            if display_heart:
                draw.line((120, 1, 120, 3), fill=255)
                draw.line((121, 0, 121, 4), fill=255)
                draw.line((122, 1, 122, 5), fill=255)
                draw.line((123, 2, 123, 6), fill=255)   # center of heart
                draw.line((124, 2, 124, 6), fill=255)   # center of heart
                draw.line((125, 1, 125, 5), fill=255)
                draw.line((126, 0, 126, 4), fill=255)
                draw.line((127, 1, 127, 3), fill=255)

                # increment the number of heart beats
                heart_beats += 1

            # if the heart was just drawn, don't display it in the next
            # loop, and visa versa
            display_heart = not display_heart

            # draw the text for hostname, IP address, CPU load, memory usage
            host_text = "Host: " + str(HostName.rstrip().ljust(13))
            draw.text((x, top), host_text, font=font, fill=255)
            ip_text = "IP: " + str(IP)
            draw.text((x, top+8), ip_text,  font=font, fill=255)
            draw.text((x, top+16), str(CPU), font=font, fill=255)
            draw.text((x, top+25), str(MemUsage),  font=font, fill=255)

            # display the image
            disp.image(image)
            disp.display()
            time.sleep(heart_beat)

    except KeyboardInterrupt:

        if heart_beats > 1000000:
            str_heartbeats = ">1,000,000"
        else:
            str_heartbeats = format(heart_beats, ',')
        str_heartbeats += " heartbeats"

        # blank the display
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # display the number of heartbeats since the program was started
        draw.text((x, top+8), "Monitor stopped after", font=font, fill=255)
        draw.text((x, top+16), str_heartbeats, font=font, fill=255)
        disp.image(image)
        disp.display()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--heartbeat", type=float, default=0.25,
                        help="number of seconds between heart beats")
    args = parser.parse_args()
    monitor_stats(args.heartbeat)
