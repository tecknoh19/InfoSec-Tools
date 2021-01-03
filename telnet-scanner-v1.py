#!/usr/bin/python
from netaddr import *
from datetime import datetime
import socket, time, telnetlib, sys, os.path


# Set output log filename
#name_tag = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
log = "telnet-scan-log" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + ".txt"

# Define variables
start_ip = raw_input("Start IP: ") # Get start IP from user
end_ip = raw_input("End IP: ") # Get end IP from user
startTime = datetime.now() # Scan execution time counter start
port = 23 # Define port, in this case 23 for telnet
retry = 1 # number of times to retry on fail
delay = 2 # number of seconds for delay
ctimeout = 2 # number of seconds before connection attempt should time out

def intro(): 
    print " _____    _            _     _____"                                 
    print "|_   _|  | |          | |   /  ___|"                              
    print "  | | ___| |_ __   ___| |_  \ `--.  ___ __ _ _ __  _ __   ___ _ __  " 
    print "  | |/ _ \ | '_ \ / _ \ __|  `--. \/ __/ _` | '_ \| '_ \ / _ \ '__| " 
    print "  | |  __/ | | | |  __/ |_  /\__/ / (_| (_| | | | | | | |  __/ |   "   
    print "  \_/\___|_|_| |_|\___|\__| \____/ \___\__,_|_| |_|_| |_|\___|_|    "  
    #print "\n"
    print "Telnet Scanner v1: by tecknoh19"
    print "Scans provided IP range for telnet servers\n"                                                          
                                                                   
# Check for existing log file and create if missing
if not os.path.isfile(log):
    f = open(log, "a")
    f.write("\"Log Created\",\"Telnet Scanner Log: " + start_ip + " - " + end_ip+"\"" + "\n")
else:
    f = open(log, "a")

# IP address validation function
def check_ipv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
                   
    return True
    

intro()    

# Validate IP input
if check_ipv4(start_ip) == False:
    sys.exit("Invalid start IP.  Please try again.")
if check_ipv4(end_ip) == False:
    sys.exit("Invalid end IP. Please try again.")

# Generate IP range
try:
    gen = iter_iprange(start_ip,end_ip,step=1)
    ips = list(gen)
except:
    sys.exit("Could not initiate scan.  Ensure the provide IP addresses are valid and try again.")

# Loop through IP's and perform connection attempt    
try:
    for ip in ips:
        print "Checking " + str(ip)
        try:
            tn = telnetlib.Telnet(str(ip),port,ctimeout)            
            rdat =  tn.read_until(b'\r\r\n\r\n', timeout=ctimeout).decode('UTF-8')
            if rdat:
                f.write("\"" + str(ip) + "\",\"" + str(port) + "\"," + "\"" + rdat + "\"" + "\n")
                print "Connection established.  Log entry created.\n"
            else:
                print"Connection refused.\n"
        except Exception as e:
            print e.message
        print "\n"
        
except:
    exc_time = datetime.now() - startTime 
    comp = "Scan complete in " + str(exc_time) + " seconds."
    print comp
    f.close()
