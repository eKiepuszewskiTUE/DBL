import RPi.GPIO as GPIO
import time
from time import sleep
import board
import adafruit_tcs34725
import webcolors
import board, busio, time
import datetime
from adafruit_extended_bus import ExtendedI2C as I2C
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

i2c = I2C(3)
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=4, num_cols=20)

input1 = 23
input2 = 24
input3 = 26
input4 = 5 
enable1 = 4
enable2 = 6 

GPIO.setmode(GPIO.BCM)	# GPIO Numbering



counter = 0
GPIO.setup(input1 ,GPIO.OUT)  # Input 1
GPIO.setup(input2 ,GPIO.OUT) # Input 2
GPIO.setup(enable1 ,GPIO.OUT) # Enable 1
pwm1 = GPIO.PWM(enable1, 100)
pwm1.start(0)

GPIO.setup(input3, GPIO.OUT) # Input 3
GPIO.setup(input4, GPIO.OUT) # Input 4
GPIO.setup(enable2, GPIO.OUT) # Enable 2
pwm2 = GPIO.PWM(enable2, 100)
pwm2.start(0)

#pwm1.ChangeDutyCycle(100)
#pwm2.ChangeDutyCycle(100)

#GPIO.output(enable1, False)
#GPIO.output(enable2, False)

def pulse_width_modulation(pwm, motor):
    '''
    Changes the pulse width modulation of the motor.
    (changes the speed of the motor)
    
    Parameters
    ----------
    pwm : int, value between 0-100 for the pulse width
    
    motor : string, "1" for motor 1, "2" for motor 2, "both" for both motors
    '''
    if motor == 1:
        pwm1.ChangeDutyCycle(pwm)
    elif motor == 2:
        pwm2.ChangeDutyCycle(pwm)
    elif motor == "both":
        pwm1.ChangeDutyCycle(pwm)
        pwm2.ChangeDutyCycle(pwm)

def motor_spin(direction, motor):
    '''
    Can make the motor spin forward or backward. Independently of each other, or both at the same time.
    
    Parameters
    ----------
    direction : string, "forward" or "backward" forward for the the windmill motor is the direction that makes the windmill knock discs into our sorter.
                For the splitter motor, forward is the direction that makes the splitter move to the right.
    motor : string, "1" for motor 1, "2" for motor 2, "both" for both motors. Motor "1" is splitter motor, motor "2" is windmill motor.
    '''
    
    #print("tocim sa")
    if (direction == "forward" and motor == "both"):
        GPIO.output(input1, True)
        GPIO.output(input2, False)

        GPIO.output(input3, True)
        GPIO.output(input4, False)
        
        GPIO.output(enable1, True)
        GPIO.output(enable2, True)
        
    elif (direction == "backward" and motor == "both"):
        GPIO.output(input1, False)
        GPIO.output(input2, True)

        GPIO.output(input3, False)
        GPIO.output(input4, True)
        
        GPIO.output(enable1, True)
        GPIO.output(enable2, True)
        
    elif (direction == "forward" and motor == 1):
        GPIO.output(input1, True)
        GPIO.output(input2, False)
        
        GPIO.output(enable1, True)
    
    elif (direction == "backward" and motor == 1):
        GPIO.output(input1, False)
        GPIO.output(input2, True)
        
        GPIO.output(enable2, True)
        
    elif (direction == "forward" and motor == 2):
        GPIO.output(input3, True)
        GPIO.output(input4, False)

        GPIO.output(enable2, True)  
    elif (direction == "forward" and motor == 2):
        GPIO.output(input3, False)
        GPIO.output(input4, True)

        GPIO.output(enable2, True)  
    else:
        print("Invalid motor or direction.")

wall_position = 'left'


# Function to move the wall
def move_wall(position):
    '''
    Moves the wall to the left or right.
    
    Parameters
    ----------
    position : string, "left" or "right" depends on where you want the wall to move.
    '''
    global wall_position
    
    pulse_width_modulation(100, 1)
    if position == 'left' and wall_position != 'left':
        motor_spin("backward" ,1)
    if position == 'right' and wall_position != 'right':
        motor_spin("forward" ,1)
            
    
    wall_position = position
    
def hit_disk():
    '''
    Hits the disk of the conveyor belt.
    '''
    pulse_width_modulation(100, 2)
    motor_spin("forward", 2)
        
    
        
def cleanup():
    '''
    Cleans up the GPIO pins and channels.
    '''
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()


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
    if ((type(lux) is float) and type(prev_lux) is float and (prev_lux - lux >=50)) or lux is None:
        return True
    return False

def whatColorDisk(color_rgb):
    if color_rgb != "black":
        return "white"
    return "black"


def main():
    sensor = adafruit_tcs34725.TCS34725(board.I2C())
    sensor.gain = 60 # Change sensor gain to 1, 4, 16, or 60
    
    counter = 0
    lux = 0
    prev_lux = 0
    sorted_counter = 0
    
    while True:
        color = sensor.color
        color_rgb = sensor.color_rgb_bytes
        print(get_colour_name(color_rgb))      
        lcd.clear()
        print_text(0, 0, "Color: " + str(get_colour_name(color_rgb)[1]))
        
        # Read the color temperature and lux of the sensor too.
        temp = sensor.color_temperature
        prev_lux = lux
        lux = sensor.lux
        print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
        
        if (chceckIfDisk(lux, prev_lux)):
            counter += 1
            #if (whatColorDisk(str(get_colour_name(color_rgb)[1])) == "white"):
                #sleep(1.25)
            #treba mat logiku iba na kazdy stvrty disk aby sa registroval
            if counter % 4 == 1:
                sorted_counter += 1
                sense_disk_time = datetime.datetime.now()
                if (whatColorDisk(str(get_colour_name(color_rgb)[1])) == "black"):
                    move_wall("left")
                    print("som cierny a hybem stenu")
                else:
                    move_wall("right")
                    print("som biely a hybem stenu")

        try:
            if (datetime.datetime.now() - sense_disk_time).total_seconds() >= 0.75:
                hit_disk()
                del sense_disk_time 
                hit_time = datetime.datetime.now()
        except UnboundLocalError:
            pass
        
        try:
            if (datetime.datetime.now() - hit_time).total_seconds() >= 1.25:
                print("zastavujem koleso smrti")
                pulse_width_modulation(0,2)
                GPIO.output(enable2, False)
                del hit_time
        except UnboundLocalError:
            pass
        
        try:
            if (datetime.datetime.now() - sense_disk_time).total_seconds() > 0.45:
                pulse_width_modulation(0,1)
                GPIO.output(enable1, False)
        except UnboundLocalError:
            pass
            
        print_text(3,0, "Sorted disks: "+str(sorted_counter))
        print_text(1, 0, "Counter: " + str(counter))
        print(counter)

        print_text(2, 0, "Disk: " + str(whatColorDisk(str(get_colour_name(color_rgb)[1]))))
        print(whatColorDisk(str(get_colour_name(color_rgb)[1])))

        time.sleep(1)

if __name__ == "__main__":
    main()