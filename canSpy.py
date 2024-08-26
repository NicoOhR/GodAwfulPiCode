import can

with can.Bus(interface='socketcan', channel='can0', bitrate=250000) as bus:
    print_listener = can.Printer(append=True)
    for msg in bus:    
        print_listener.on_message_received(msg)

