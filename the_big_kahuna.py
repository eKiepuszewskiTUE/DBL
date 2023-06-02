import threading
import time
import board
import adafruit_tcs34725
import webcolors
import board, busio, time
from adafruit_extended_bus import ExtendedI2C as I2C
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

i2c = I2C(3)
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=4, num_cols=20)

counter = 0

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]
 
def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def print_text(column, row, message):
    lcd.set_cursor_pos(column, row)
    lcd.print(message)

def chceckIfDisk(lux, prev_lux):
    print(type(lux))
    if (type(lux) == float):
        if (lux > 100 and prev_lux < 100):
            return True
        return False

def main():
    sensor = adafruit_tcs34725.TCS34725(board.I2C())
    sensor.gain = 60 # Change sensor gain to 1, 4, 16, or 60
    
    counter = 0
    lux = 0
    prev_lux = 0
    
    while True:
        color = sensor.color
        color_rgb = sensor.color_rgb_bytes
        print(get_colour_name(color_rgb))
        print_text(0, 0, "Color: " + str(get_colour_name(color_rgb)[1]))
        
        # Read the color temperature and lux of the sensor too.
        temp = sensor.color_temperature
        prev_lux = lux
        lux = sensor.lux
        print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
        
        if (chceckIfDisk(lux, prev_lux)):
            counter += 1

        print_text(1, 0, "Counter: " + str(counter))
        print(counter)

        # Delay for a second and repeat.
        time.sleep(0.1)
        lcd.clear()



if __name__ == "__main__":
    main()