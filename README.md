# LEDs-control
Control LEDs' brightness, speed and patterns with Python and Raspberry Pi

This is a Python program to controls a set of LEDs to display various patterns. 
It also interfaces with an analog-to-digital converter (ADS7830) to adjust the brightness and speed of the LED patterns.
Additionally, it utilizes a character LCD for displaying information about the currently active pattern and its settings.


**Purpose**
This program controls a set of PWM LEDs to display various patterns. 
The LED patterns can be changed by pressing a button. 
The brightness and speed of the patterns are adjustable via analog input from an ADS7830 converter. Information about the current pattern and its settings is displayed on an LCD.


**Dependencies**
Python 3
gpiozero library
rpi_lcd library
smbus library (for ADS7830)
Raspberry Pi hardware and Raspbian OS

**Functions**
safe_exit: Function to safely exit the script in response to a signal.
read_ads7830: Function to read analog input from the ADS7830.
show_pattern: Function to display LED patterns based on brightness and speed from ADS7830 input.
change_direction: Function to change the direction of LED pattern animation.
lcd_display: Function to update and display information on the LCD.
