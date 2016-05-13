from gpiozero import LED

led1=LED(4)
led2=LED(17)
led3=LED(27)
led4=LED(22)
led5=LED(18)
led6=LED(23)
led7=LED(24)
led8=LED(25)

ledlist1=[led1,led2,led3,led4]
for i in range(0,4):
    ledlist1[i].on()#initialize all the led/gpio pins.

ledlist2=[led5,led6,led7,led8]
for i in range(0,4):
    ledlist2[i].on()

    
def show_num(x):
    lis=[0,0,0,0,0,0,0,0]
    i=0
    while(x>1):
        a=x%2;
        lis[i]=a
        i=i+1
        x=int(x/2)
    lis[i]=1
    
    for j in range(0,4):
        if lis[j]==1:
            ledlist1[j].off()
    for k in range(4,8):
        if lis[k]==1:
            ledlist2[k-4].off()   
         
 
var = input("Enter the number you want to be displayed :  ") #input

if int(var)>99:
    print("Error! Enter a number within the range.")
else:
    while(True):
        show_num(int(var))
