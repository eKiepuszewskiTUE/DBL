import RPi.GPIO as GPIO
from time import sleep

# Sets up the pins on the RPI as variables for easier manipulation
input1 = 23
input2 = 24
input3 = 26
input4 = 5 
enable1 = 4
enable2 = 6 

pwm1 = GPIO.PWM(enable1, 100)
pwm2 = GPIO.PWM(enable2, 100)


def motor_pin_setup():
    '''
    Sets up the pins on the RPI as outputs for the motor.
    '''
    GPIO.setmode(GPIO.BCM)	# GPIO Numbering
    GPIO.setup(input1 ,GPIO.OUT)  # Input 1
    GPIO.setup(input2 ,GPIO.OUT) # Input 2
    GPIO.setup(enable1 ,GPIO.OUT) # Enable 1
    pwm1.start(0)

    GPIO.setup(input3, GPIO.OUT) # Input 3
    GPIO.setup(input4, GPIO.OUT) # Input 4
    GPIO.setup(enable2, GPIO.OUT) # Enable 2
    pwm2.start(0)

def PulseWidthModulation(pwm, motor):
    '''
    Changes the pulse width modulation of the motor.
    (changes the speed of the motor)
    
    Parameters
    ----------
    pwm : int, value between 0-100 for the pulse width
    
    motor : string, "1" for motor 1, "2" for motor 2, "both" for both motors
    '''
    if motor == "1":
        pwm1.ChangeDutyCycle(pwm)
    elif motor == "2":
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
        
    elif (direction == "forward" and motor == "1"):
        GPIO.output(input1, True)
        GPIO.output(input2, False)
        
        GPIO.output(enable1, True)
    
    elif (direction == "backward" and motor == "1"):
        GPIO.output(input1, False)
        GPIO.output(input2, True)
        
        GPIO.output(enable2, True)
        
    elif (direction == "forward" and motor == "2"):
        GPIO.output(input3, True)
        GPIO.output(input4, False)

        GPIO.output(enable2, True)  
    elif (direction == "forward" and motor == "2"):
        GPIO.output(input3, False)
        GPIO.output(input4, True)

        GPIO.output(enable2, True)  
    else:
        print("Invalid motor")
        
def cleanup():
    '''
    Cleans up the GPIO pins and channels.
    '''
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
