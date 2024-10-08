import can
import struct
from datetime import datetime

def read_message(bus):
    msg = bus.recv()

    if msg is not None and not msg.is_error_frame:
        messsage = msg.data.hex()
        #print(f"Received: {msg.data.hex()} from id {msg.arbitration_id}")
        return msg.arbitration_id, messsage

    return None, None

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
        "BatteryVoltage,AirTemp,CoolantTemp,odd\n"
    )
    f.close()

    return fname

def append_to_file(f, data):
    line = ', '.join(map(str, data)) + '\n'
    f.write(line)

if __name__ == "__main__":
    import os 
    
    can_data = {}

    with can.Bus(channel = 'can0', interface = 'socketcan', bitrate = 1000000) as bus:
        try:
            while True:
                    can_id, hex_values = read_message(bus)
                    #print(can_id)
                    if hex_values is not None:  # Proceed only if hex_values is valid
                        first, second = hex_string_to_floats(hex_values)
                    if can_id not in can_data:
                        can_data[can_id] = []
                    can_data[can_id].extend([first,second])
                    print(can_id)
        except KeyboardInterrupt:      
            for id in can_data:
                print(id)
                for data in can_data[id]:
                    print(data) 
