import machine, onewire, ds18x20, time, _thread

uart1 = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5)) # Channel-1 | read
uart2 = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1)) # Channel-0 | write 

ds_pin = machine.Pin(16)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()

#my_address = 255    # master
my_address = 1       #slave1
#my_address = 2      #slave2
#my_address = 3      #slave3

flag = 1
print('RS485 slave')
time.sleep(0.1)
rxData = bytes()
    

# slave functions
def circle_lenght_interact(master_address, current_lenght):
    txData = bytes([0,master_address,255,current_lenght+1,123])
    uart2.write(txData)
    #print("Circle lenght request captured and sent to next node")

def send_data(master_address):
    ds_sensor.convert_temp()
    temperature = 0
    for rom in roms:
        temperature = ds_sensor.read_temp(rom)
  
    data1 = int(temperature) + 50
    data2 = int(100*temperature % 100)
    
    txData = bytes([master_address,my_address,data1,data2,123])
    uart2.write(txData)
    print("Requested data sent to network")

def resend_packet(tx0,tx1,tx2,tx3,tx4):
    txData = bytes([tx0,tx1,tx2,tx3,tx4])
    uart2.write(txData)
    #print("Packet resent")




while True:
    
    while uart1.any() > 0:
        rxData = uart1.read()
        if(flag == 1):
            time.sleep(0.05)
            flag=0
            
        if (rxData[0] == my_address and rxData[2] == 0 and rxData[3] == 0): # data requested
            _thread.start_new_thread(send_data, ([rxData[1]]))  
        elif (rxData[0] == 0 and rxData[2] == 255): # circle lenght requested
            _thread.start_new_thread(circle_lenght_interact, ([rxData[1], rxData[3]]))
        else: # packet for another node
            _thread.start_new_thread(resend_packet, ([rxData[0], rxData[1], rxData[2], rxData[3], rxData[4]]))
        