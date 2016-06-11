import serial
import time
from serial.tools import list_ports
import random
import psutil
import wmi
import time

def main():

    ports = list(list_ports.comports())
    arduino_port = None

    print ports
    for port_id, port_name, port_address in ports:
            if 'arduino' in port_name.lower():
                    arduino_port = port_id

            

    if not arduino_port:
            raise Exception('arduino not detected')

    arduino_port = arduino_port[3:]
    arduino_port = int(arduino_port) - 1
    ser = serial.Serial(arduino_port)  

    counter = 0

    def bytesto(bytes, to, bsize=1024):
        a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
        r = float(bytes)
        for i in range(a[to]):
            r = r / bsize

        return(r)


    def get_cpu_info():

            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_usage = int(cpu_usage)
            
            return cpu_usage
               	
    while True:

            ram = psutil.virtual_memory()
            total_ram = bytesto(ram.total, 'g')
            used_ram = bytesto(ram.used, 'g')

            cpu_usage = get_cpu_info()
            
            lines = []

            total_processes = len(psutil.pids())
            
            lines.append('CPU: {0}%'.format(cpu_usage))
            lines.append('RAM: {0:.1f}/{1:.1f}GB'.format(used_ram, total_ram))
            lines.append('PROCESSES: {0}'.format(total_processes))
            
            message = ''
            
            for line in reversed(sorted(lines, key=len)):

                    if len(line) >= 10:
                            
                            message += line + ' ' * (20-len(line))
                                    
                    elif len(line) >= 5:
                            
                            message += line + ' ' * (10-len(line))

                    elif len(line) > 0:
                            
                            message += line + ' ' * (5-len(line))
            
            ser.write(message)
            counter += 1


while True:
    try:
        main()
    except Exception as e:
        with open(r"S:\scripts\error.log", "a") as w:
            w.write('{0}\r\n'.format(e))
        

    time.sleep(5)
    
    
