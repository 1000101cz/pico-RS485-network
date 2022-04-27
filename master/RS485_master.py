import machine
import time
import _thread
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

uart1 = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5)) # Channel-1 | read
uart2 = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1)) # Channel-0 | write 

my_address = 255    # master
#my_address = 1      #slave1
#my_address = 2      #slave2
#my_address = 3      #slave3

I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(8), scl=machine.Pin(9), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

flag = 1
print('RS485 master')
time.sleep(0.1)
rxData = bytes()

nodes = False
number_of_devices = 0
slave1=False
slave2=False
slave3=False
slave1value = 0.0     # temperature
slave2value = False   # motion
slave3value = 0       # distance


def reset_values():
    global nodes
    nodes = False
    global number_of_devices
    number_of_devices = 0
    global slave1
    slave1 = False
    global slave2
    slave2 = False
    global slave3
    slave3 = False
    global slave1value
    slave1value = 0.0     # temperature
    global slave2value
    slave2value = False   # motion
    global slave3value
    slave3value = 0       # distance
    
def display_values_lcd(repeat):
    if (nodes):
        string1 = ">> no. nodes: %3d <<"%number_of_devices
    else:
        string1 = ">> no. nodes: NaN <<"
    
    if (slave1):
        string2 = "> temp: %3d.%02d C   <"%(int(slave1value),(slave1value*100)%100)
    else:
        string2 = "> temp:     NaN    <"
    
    if (slave2):
        if (slave2value):
            string3 = "> motion: yes      <"
        else:
            string3 = "> motion: no       <"
            
    else:
        string3 = "> motion:   NaN    <"
    
    if (slave3):
        string4 = "> distance: %3d cm <"%slave3value
    else:
        string4 = "> distance: NaN    <"
    
    print("         %02d"%repeat)
    print(">>>>>>>>>><<<<<<<<<<")
    print(string1)
    print(string2)
    print(string3)
    print(string4)
    print(">>>>>>>>>><<<<<<<<<<\n\n")
    print()
    
    lcd.move_to(0,0)
    lcd.putstr(string1)
    lcd.move_to(0,1)
    lcd.putstr(string2)
    lcd.move_to(0,2)
    lcd.putstr(string3)
    lcd.move_to(0,3)
    lcd.putstr(string4)

    
def second_thread():
    repeat = 1
    while True:
        circle_lenght_init() # request lenght of circle
        time.sleep(0.05)
        slave_data_request(1) # request temperature from slave1
        time.sleep(0.05)
        slave_data_request(2) # request motion from slave2
        time.sleep(0.05)
        slave_data_request(3) # request distance from slave3
        time.sleep(0.5)
        
        display_values_lcd(repeat) # display obtained values on lcd
        
        reset_values()
        repeat+=1
        
        time.sleep(5)



# master functions
def circle_lenght_init():
    txData = bytes([0,my_address,255,0,123])
    uart2.write(txData)


def slave_data_request(slave_number):
    txData = bytes([slave_number, my_address, 0, 0, 123])
    uart2.write(txData)
    
    
# start sending thread
_thread.start_new_thread(second_thread, ())


# receiving thread
while True:
    while uart1.any() > 0:
        rxData = uart1.read()
        if(flag == 1):
            time.sleep(0.05)
            flag=0
        if (rxData[0] == my_address):
            if (rxData[1] == 1):
                slave1 = True
                slave1value = rxData[2]-50 + rxData[3]/100
            elif (rxData[1] == 2):
                slave2 = True
                if (rxData[2] == 255):
                    slave2value = True
            elif (rxData[1] == 3):
                slave3 = True
                slave3value = rxData[2]
                
        elif (rxData[0] == 0 and rxData[1] == my_address and rxData[2] == 255):
            number_of_devices = rxData[3]
            nodes = True
        