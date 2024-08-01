import can
import struct
from datetime import datetime

def read_message(bus):
    try:
        msg = bus.recv()

        if msg is not None:
            messsage = msg.data.hex()
            print(f"Received: {msg.data.hex()}")

    except KeyboardInterrupt:
        print("\n Stopped Reading From Bus")
        #bus does not close cleanly despite following line
        bus.close()

    return messsage

def hex_string_to_floats(hex_string):
    if len(hex_string) != 16:
        raise ValueError("Input hex string must contain exactly 16 characters representing 8 hex values.")
    hex_string1 = hex_string[:8]
    hex_string2 = hex_string[8:]
    
    def hex_to_float(h_string):
        hex_pairs = [h_string[i:i+2] for i in range(0, len(h_string), 2)]
        
        hex_values = [int(pair, 16) for pair in hex_pairs]
        
        float_value = struct.unpack('<f', struct.pack('<I', int(''.join(format(x, '08b') for x in hex_values), 2)))[0]
        
        return float_value
        
    float_value1 = hex_to_float(hex_string1)
    float_value2 = hex_to_float(hex_string2)
    
    return float_value1, float_value2

def create_file():
    fname = f"data_file_{datetime.now().strftime('%Y-%m-%d')}_{datetime.now().strftime('%H:%M:%S')}.csv"
    f = open(fname, "a")
    f.write(
        "Timestamp,Linpot1,Linpot2,Linpot3,Linpot4,AccX,AccY,AccZ,"
        "GyroX,GyroY,GyroZ,RPM,TPS,FuelOpenTime,IgnitionAngle,Barometer,"
        "MAP,Lambda,AnalogInput1,AnalogInput2,AnalogInput3,AnalogInput4,"
        "AnalogInput5,AnalogInput6,AnalogInput7,AnalogInput8,"
        "BatteryVoltage,AirTemp,CoolantTemp\n"
    )
    f.close()

    return fname

def append_to_file(fname, first, second, last):
    f = open(fname, "a")
    if last:
        f.write(f"{first}, {second} \n")
    else:
        f.write(f"{first}, {second}, ")


if __name__ == "__main__":

    bus = can.Bus(channel = 'can0', interface = 'socketcan', bitrate = 250000)
    
    fname = create_file()
    count = 0
    last = False
    while True:
        last = False
        for count in range(10):
            hex_values = read_message(bus)
            if hex_values == "ffffffffffffffff":
                fname = create_file() #creates one more file than needed at the end of the transmission, wont get better without explicit state
                break
            first, second = hex_string_to_floats(hex_values)
            if(count == 9):
                last = True
            append_to_file(fname, first, second, last)
        