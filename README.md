# ProjectPIP
Pico I2C Peripheral

This project has a few examples of how you can use a Raspberry Pi Pico microcontroller as an I2C peripheral/responder/slave device. This allows building custom sensors or extending projects with extra ADC or Digital IO over an I2C buss using a Raspberry Pi Pico.

An example of a few ways this might be usefull:
 - ADC input to a Raspberry PI
 - High precession pulse timer
 - Dedicated PWM controller for servos

The examples in this project are written in MicroPython for the Raspberry PI Pico microcontroller

This project uses the I2C responder class from the following repo
https://github.com/epmoyer/I2CResponder
