from flask import request
import RPi.GPIO as GPIO
from flask import Flask, render_template
from time import sleep
import sys
import os
import time
import RPi.GPIO as IO
import threading

IO.setwarnings(False)
IO.setmode(IO.BCM)

HexDigits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_TYPICAL = 2
BRIGHT_HIGHEST = 7
OUTPUT = IO.OUT
INPUT = IO.IN
LOW = IO.LOW
HIGH = IO.HIGH
count1 = 0
class TM1637:
	__doublePoint = False
	__Clkpin = 0
	__Datapin = 0
	__brightnes = BRIGHT_TYPICAL;
	__currentData = [0,0,0,0];
	
	def __init__( self, pinClock, pinData, brightnes ):
		self.__Clkpin = pinClock
		self.__Datapin = pinData
		self.__brightnes = brightnes;
		IO.setup(self.__Clkpin,OUTPUT)
		IO.setup(self.__Datapin,OUTPUT)
	# end  __init__

	def Clear(self):
		b = self.__brightnes;
		point = self.__doublePoint;
		self.__brightnes = 0;
		self.__doublePoint = False;
		data = [0x7F,0x7F,0x7F,0x7F];
		self.Show(data);
		self.__brightnes = b;				# restore saved brightnes
		self.__doublePoint = point;
	# end  Clear

	def Show( self, data ):
		for i in range(0,4):
			self.__currentData[i] = data[i];
		
		self.start();
		self.writeByte(ADDR_AUTO);
		self.stop();
		self.start();
		self.writeByte(STARTADDR);
		for i in range(0,4):
			self.writeByte(self.coding(data[i]));
		self.stop();
		self.start();
		self.writeByte(0x88 + self.__brightnes);
		self.stop();
	# end  Show

	def Show1(self, DigitNumber, data):	# show one Digit (number 0...3)
		if( DigitNumber < 0 or DigitNumber > 3):
			return;	# error
	
		self.__currentData[DigitNumber] = data;
		
		self.start();
		self.writeByte(ADDR_FIXED);
		self.stop();
		self.start();
		self.writeByte(STARTADDR | DigitNumber);
		self.writeByte(self.coding(data));
		self.stop();
		self.start();
		self.writeByte(0x88 + self.__brightnes);
		self.stop();
	# end  Show1
		
	def SetBrightnes(self, brightnes):		# brightnes 0...7
		if( brightnes > 7 ):
			brightnes = 7;
		elif( brightnes < 0 ):
			brightnes = 0;

		if( self.__brightnes != brightnes):
			self.__brightnes = brightnes;
			self.Show(self.__currentData);
		# end if
	# end  SetBrightnes

	def ShowDoublepoint(self, on):			# shows or hides the doublepoint
		if( self.__doublePoint != on):
			self.__doublePoint = on;
			self.Show(self.__currentData);
		# end if
	# end  ShowDoublepoint
			
	def writeByte( self, data ):
		for i in range(0,8):
			IO.output( self.__Clkpin, LOW)
			if(data & 0x01):
				IO.output( self.__Datapin, HIGH)
			else:
				IO.output( self.__Datapin, LOW)
			data = data >> 1
			IO.output( self.__Clkpin, HIGH)
		#endfor

		# wait for ACK
		IO.output( self.__Clkpin, LOW)
		IO.output( self.__Datapin, HIGH)
		IO.output( self.__Clkpin, HIGH)
		IO.setup(self.__Datapin, INPUT)
		
		while(IO.input(self.__Datapin)):
			#time.sleep(0.001)
			if( IO.input(self.__Datapin)):
				IO.setup(self.__Datapin, OUTPUT)
				IO.output( self.__Datapin, LOW)
				IO.setup(self.__Datapin, INPUT)
			#endif
		# endwhile            
		IO.setup(self.__Datapin, OUTPUT)
	# end writeByte
    
	def start(self):
		IO.output( self.__Clkpin, HIGH) # send start signal to TM1637
		IO.output( self.__Datapin, HIGH)
		IO.output( self.__Datapin, LOW) 
		IO.output( self.__Clkpin, LOW) 
	# end start
	
	def stop(self):
		IO.output( self.__Clkpin, LOW) 
		IO.output( self.__Datapin, LOW) 
		IO.output( self.__Clkpin, HIGH)
		IO.output( self.__Datapin, HIGH)
	# end stop
	
	def coding(self, data):
		if( self.__doublePoint ):
			pointData = 0x80
		else:
			pointData = 0;
		
		if(data == 0x7F):
			data = 0
		else:
			data = HexDigits[data] + pointData;
		return data
	# end coding
	
# end class TM1637
class myThread (threading.Thread):
    def __init__(self, threadID, name, tim):
        threading.Thread.__init__(self)
        self.paused= False
        self.pause_cond =threading.Condition(threading.Lock())
        self.threadID = threadID
        self.name = name
        self.tim = tim
    def run(self):
        timer(self.tim)
        
                        
                     
    
            
		

## =============================================================
# -----------  Test -------------
i = 0
anzeige = [0,0,0,0]

def timer(var):
    Display = TM1637(23,24,BRIGHT_TYPICAL)
    global count1
    global anzeige
    global i
    Display.Clear()
    print "8888  - Taste bitte"
    Display.Show(anzeige)
    while(count1>=0):
            
        anzeige[3] = i
        Display.Show(anzeige)
        time.sleep(1)
        print (i)
        i+=1
        if i==10:
            anzeige[2]+=1
            i=0
            if anzeige[2]==6:
                anzeige[1]+=1
                anzeige[2]=0
                if anzeige[1]==10 and anzeige[0] <(var/10):
                    anzeige[0]+=1
                    anzeige[1]=0
                else:
                    if anzeige[1] < (var%10):
                        pass
                    else:
                        Display.Clear()
                        break;
        
    #Display.ShowDoublepoint(True)
    #Display.SetBrightnes(4)




led1= 4
led2= 17
led3= 27
led4= 22
led5= 18
led6= 8
led7= 7
led8= 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)
GPIO.setup(led5, GPIO.OUT)
GPIO.setup(led6, GPIO.OUT)
GPIO.setup(led7, GPIO.OUT)
GPIO.setup(led8, GPIO.OUT)


GPIO.output(led1, True)
GPIO.output(led2, True)
GPIO.output(led3, True)
GPIO.output(led4, True)

GPIO.output(led5, True)
GPIO.output(led6, True)
GPIO.output(led7, True)
GPIO.output(led8, True)


def ssd1(i):
                if i == 1:
                        
                        GPIO.output(led1, True)
                        GPIO.output(led2, False)
                        GPIO.output(led3, False)
                        GPIO.output(led4, False)
                        
                if i == 2:
                
                        GPIO.output(led1, False)
                        GPIO.output(led2, True)
                        GPIO.output(led3, False)
                        GPIO.output(led4, False)

                if i == 3:
                                
                        GPIO.output(led1, True)
                        GPIO.output(led2, True)
                        GPIO.output(led3, False)
                        GPIO.output(led4, False)

                if i == 4:
                        
                        GPIO.output(led1, False)
                        GPIO.output(led2, False)
                        GPIO.output(led3, True)
                        GPIO.output(led4, False)

                if i == 5:
                
                        GPIO.output(led1, True)
                        GPIO.output(led2, False)
                        GPIO.output(led3, True)
                        GPIO.output(led4, False)

                if i == 6:
                        
                        GPIO.output(led1, False)
                        GPIO.output(led2, True)
                        GPIO.output(led3, True)
                        GPIO.output(led4, False)

                if i == 7:
                        
                        GPIO.output(led1, True)
                        GPIO.output(led2,  True)
                        GPIO.output(led3, True)
                        GPIO.output(led4, False)
                if i == 8:
                        
                        GPIO.output(led1, False)
                        GPIO.output(led2, False)
                        GPIO.output(led3, False)
                        GPIO.output(led4, True)

                if i == 9:
                        
                        GPIO.output(led1, True)
                        GPIO.output(led2, False)
                        GPIO.output(led3, False)
                        GPIO.output(led4, True)

                if i == 0:
                        GPIO.output(led1, False)
                        GPIO.output(led2, False)
                        GPIO.output(led3, False)
                        GPIO.output(led4, False)
def ssd2(j):
                if j == 1:
                        
                        GPIO.output(led5, True)
                        GPIO.output(led6, False)
                        GPIO.output(led7, False)
                        GPIO.output(led8, False)

                if j == 2:
                        
                        GPIO.output(led5, False)
                        GPIO.output(led6, True)
                        GPIO.output(led7, False)
                        GPIO.output(led8, False)


                if j == 3:
                        
                        GPIO.output(led5, True)
                        GPIO.output(led6, True)
                        GPIO.output(led7, False)
                        GPIO.output(led8, False)

                if j == 4:
                        
                        GPIO.output(led5, False)
                        GPIO.output(led6, False)
                        GPIO.output(led7, True)
                        GPIO.output(led8, False)
                        
                if j ==5:
                        
                        GPIO.output(led5, True)
                        GPIO.output(led6, False)
                        GPIO.output(led7, True)
                        GPIO.output(led8, False)

                if j == 6:
                        
                        GPIO.output(led5, False)
                        GPIO.output(led6, True)
                        GPIO.output(led7, True)
                        GPIO.output(led8, False)
                if j == 7:
                        
                        GPIO.output(led5, True)
                        GPIO.output(led6, True)
                        GPIO.output(led7, True)
                        GPIO.output(led8, False)

                if j == 8:
                        
                        GPIO.output(led5, False)
                        GPIO.output(led6, False)
                        GPIO.output(led7, False)
                        GPIO.output(led8, True)

                if j == 9:
                        
                        GPIO.output(led5, True)
                        GPIO.output(led6, False)
                        GPIO.output(led7, False)
                        GPIO.output(led8, True)

                if j == 0:
                        
                        GPIO.output(led5, False)
                        GPIO.output(led6, False)
                        GPIO.output(led7, False)
                        GPIO.output(led8, False)






# The GPIO pins for the Energenie modu

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/1/on/<score1>')
def on1(score1):
    
    i = int(score1)	
    ssd1(i)
    return render_template('index.html')

@app.route('/1/off/<score2>')
def off1(score2):
    
    j = int(score2)
    ssd2(j)
    return render_template('index.html')

@app.route('/ini/')
def ini():
    
    ssd2(0)	
    ssd1(0)
    global i
    global anzeige
    global count1
    i = 0
    anzeige = [0,0,0,0]
    count1 = -1
    return render_template('index.html')

@app.route('/tim/<time>')
def tim(time):
    global count1
    count1 = 0
    thread1= myThread(1,"t1",int(time))
    thread1.start()
    return render_template('index.html')

@app.route('/stop/')
def stop():
    global count1
    count1 = -1
    return render_template('index.html')

@app.route('/reset/')
def reset():
    global i
    global anzeige
    global count1
    anzeige=[0,0,0,0]
    i = 0
    count1 = -1
    timer(10)
    
    return render_template('index.html')

@app.route('/1/gameover/')
def gameover1():
    ssd1(0)
    ssd2(0)
    global i
    global anzeige
    global count1
    anzeige=[0,0,0,0]
    i = 0
    count1 = -1
    timer(10)
    
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')















    
