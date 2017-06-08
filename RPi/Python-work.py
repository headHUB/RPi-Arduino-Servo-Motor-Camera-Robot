import serial
import pygame

# allow multiple joysticks
joy = []

# Arduino USB port address (try "COM5" on Win32)
usbport = "/dev/ttyUSB0"

# define usb serial connection to Arduino
ser = serial.Serial(usbport, 9600)


# handle joystick event
def handleJoyEvent(e):
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 1):
            axis = "X"

        if (e.dict['axis'] == 0):
            axis = "Y"

        # if (e.dict['axis'] == 2):
        #   axis = "Throttle"

        # if (e.dict['axis'] == 3):
        #    axis = "Z"

        if (axis != "unknown"):
            str = "Axis: %s; Value: %f" % (axis, e.dict['value'])
            # uncomment to debug
            # output(str, e.dict['joy'])

            # Arduino joystick-servo hack
            if (axis == "X"):
                pos = e.dict['value']
                # convert joystick position to servo increment, 0-180
                move = round(pos * 90, 0)
                if (move < 0):
                    tiltServo = int(90 - abs(move))
                else:
                    tiltServo = int(move + 90)
                    # convert position to ASCII character
                    tiltServoPosition = chr(tiltServo)
                    # and send to Arduino over serial connection
                    ser.write(tiltServoPosition)
                    # uncomment to debug
                    # print servo, servoPosition
            if (axis == "Y"):
                pos = e.dict['value']
                # convert joystick position to servo increment, 0-180
                move = round(pos * 90, 0)
                if (move < 0):
                    servo = int(90 - abs(move))
                else:
                    servo = int(move + 90)
                # convert position to ASCII character
                servoPosition = chr(servo)
                # and send to Arduino over serial connection
                ser.write(servoPosition)
                # uncomment to debug
                # print servo, servoPosition

                # elif e.type == pygame.JOYBUTTONDOWN:
                #    str = "Button: %d" % (e.dict['button'])
                # uncomment to debug
                # output(str, e.dict['joy'])
                # Button 0 (trigger) to quit
    # if (e.dict['button'] == 0):
    #        print "Bye!\n"
    #        ser.close()
    #        quit()
    else:
        pass


# print the joystick position
def output(line, stick):
    print "Joystick: %d; %s" % (stick, line)


# wait for joystick input
def joystickControl():
    while True:
        e = pygame.event.wait()
        if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN):
            handleJoyEvent(e)


# main method
def main():
    # initialize pygame
    pygame.joystick.init()
    pygame.display.init()
    if not pygame.joystick.get_count():
        print "\nPlease connect a joystick and run again.\n"
        quit()
    print "\n%d joystick(s) detected." % pygame.joystick.get_count()
    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        print "Joystick %d: " % (i) + joy[i].get_name()
    print "Depress trigger (button 0) to quit.\n"

    # run joystick listener loop
    joystickControl()


# allow use as a module or standalone script
if __name__ == "__main__":
    main()
