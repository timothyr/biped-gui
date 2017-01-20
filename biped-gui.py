from Tkinter import *
import serial

# Test the program without robot plugged in
TEST_WITHOUT_ROBOT_COMM = True

class Servo(object):
    def __init__(self, root, servoIndex, min, max, defaultPos):
        self.min = min
        self.max = max

        self.servoIndex = IntVar()
        self.servoIndex.set(servoIndex)

        self.defaultPos = defaultPos

        self.position = IntVar()
        self.position.set(self.defaultPos)
        
        # Create slider for new Servo Object
        self.slider = Scale(root, 
                            variable = self.position,
                            to = min, 
                            from_ = max, 
                            label = "Servo #" + str(servoIndex),
                            length = 200,
                            command = self.sliderUpdateCallback)

        
        if(servoIndex > 15):
            self.slider.grid(row = 2, column = servoIndex - 15)
        else:
            self.slider.grid(row = 1, column = servoIndex + 1)
        
    
    def sendUpdate(self, position, time):
        print "Servo #" + str(self.servoIndex.get()) + " = " + str(position) + " (time = " + str(time) + ")" 
        if TEST_WITHOUT_ROBOT_COMM == False:
            # Send command to servo controller
            ser.write(b'#' + str(self.servoIndex.get()) + 'P' + str(position) + 'T' + str(time) + '\r')

    def sliderUpdateCallback(self, position):
        self.sendUpdate(position, 0)

    def setPosRelative(self, position, time):
        newPos = self.position.get() + position
        self.position.set(newPos)
        self.slider.set(newPos)
        self.sendUpdate(self.position.get(), time)

    def getMin(self):
        return self.min

    def getMax(self):
        return self.max

# End of Servo Object class

# Main

def squatDown():
    servoLeft2.setPosRelative(1000,0)
    servoLeft3.setPosRelative(500,0)
    servoLeft4.setPosRelative(300,0)
    

root = Tk()
root.title("Biped Robot Control")

# Windows port name
port = 'COM3' 
# Linux (and Mac?) port name
#port = '/dev/ttyUSB0'

# Do not open a serial if TEST_WITHOUT_ROBOT_COMM is True
if TEST_WITHOUT_ROBOT_COMM == True:
    print """\nTEST_WITHOUT_ROBOT_COMM = True
Set to False to send data to servos.\n"""
else:
    ser = serial.Serial(port, 9600, timeout = 0)


# A slider for each servo
servoLeft0  = Servo(root,0,  500,2500, 1529)
servoLeft1  = Servo(root,2,  500,2500, 1353)
servoLeft2  = Servo(root,4,  500,2500, 1971)
servoLeft3  = Servo(root,6,  500,2500, 1206)
servoLeft4  = Servo(root,8,  500,2500, 1176)
servoLeft5  = Servo(root,10, 500,2500, 2324)

servoRight0 = Servo(root,16, 500,2500, 1588)
servoRight1 = Servo(root,18, 500,2500, 1176)
servoRight2 = Servo(root,20, 500,2500, 1882)
servoRight3 = Servo(root,22, 500,2500, 2030)
servoRight4 = Servo(root,24, 500,2500, 2147)
servoRight5 = Servo(root,26, 500,2500, 735)

# Left and Right labels
leftLabel = Label(root, text="Left")
rightLabel = Label(root, text="Right")

leftLabel.grid(row = 1, column = 0)
rightLabel.grid(row = 2, column = 0)

# Squat button
button = Button(root, text="Squat (unfinished)", command=squatDown)
button.grid(row = 0, column = 0)

root.mainloop()