#!/usr/bin/env python3

import os
import sys
import re
import argparse
import ipaddress
import socket 
import uuid
import requests
from subprocess import Popen, PIPE, check_output 
a = """
 ______ _                   _     _       
(_____ (_)                 | |   | |      
 _____) ) ____   ____  ____| | _ | | ____ 
|  ____/ |  _ \ / _  |/ _  | || \| |/ _  )
| |    | | | | ( ( | ( ( | | |_) ) ( (/ / 
|_|    |_|_| |_|\_|| |\_||_|____/|_|\____)
               (_____|by:jacstory                    
"""
print(a)
host_name  = socket.gethostname()
Mac_Interface = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
Mac_Get = Mac_Interface[0:8].replace(":","").upper()
Macdb = open('mac-vendor.txt', 'r')
Mac = Macdb.readlines()
count = 0
for line in Mac:
    line = line.strip()
    if Mac_Get in line  : 
       vandor = line[7:].replace("   ","") 
       break 
    elif Mac_Get not  in line  : 
           vandor = "UNKWON MAC" 
    count += 1
    
class Discover_Network():
          
          def __init__(self):
             self.args_command()
             self.Ping_command()            
                
          def Ping_command(self):
               if self.args.ping :
                   if "/" not in self.args.ping:
                       print("Plese set the subnet netwotk")
                       exit()
                   Network    = ipaddress.ip_network('{}'.format(self.args.ping), strict=False)
                   Network_ID = Network.network_address
                   SubNet     = Network.netmask
                   print("\n[*] HOST INFO-\n"+"="*14+"\n")
                   print("[+] Network-ID      --------------|-  " +  str(Network_ID))
                   print("[+] NetWork-Prefix  --------------|-  " +  self.args.ping[-2:])
                   print("[+] Subnet-Mask     --------------|-  " +  str(SubNet))
                   print("[+] HOST-IP         --------------|-  " +  self.args.ping[0:-3])
                   print("[+] Mac-ADDRESS     --------------|-  " +  Mac_Interface)
                   print("[+] Mac-Vandor      --------------|-  " +  vandor)
                   print("\n"+"="*50+'\n')
                   scop = "/"
                   NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.ping[-2:]))
                   for Host in NetworkID.hosts():
                       Host = str(Host)
                       DisCover = Popen(["ping", "-c1",Host], stdout=PIPE)
                       output   = DisCover.communicate()[0]
                       respons  = DisCover.returncode                       
                       if respons == 0:
                           print("[+] HOST OnLine  --------------| ",Host)
                           pid = Popen(["arp", "-n", Host], stdout=PIPE)
                           arp_host = pid.communicate()[0]
                           Mac = str(re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})",arp_host.decode('utf-8')))\
                           .replace("<re.Match object; span=(114, 131), match='",'').replace("'>",'')
                           
                           if "None" in Mac:
                                print("[*] Mac ADDRESS  ..............|-",Mac_Interface)
                                interfaceMac = Mac_Interface[0:8].replace(":","").upper() 
                                              
                           else:
                               print("[*] Mac ADDRESS  ..............|-",Mac)  
                           MacGET= Mac[0:8].replace(":","").upper()
                           Macdb = open('mac-vendor.txt', 'r')
                           MacFile = Macdb.readlines()
                           count = 0
                           for line in MacFile:
                              line = line.strip()
                              if MacGET in line  : 
                                 vandor1 = line[7:].replace("    ","")  
                                 break
                              elif MacGET not  in line:
                                    vandor1 = " UNKWON MAC" 
                              count += 1  
                           if "None" in Mac :
                                print("[+] Mac-Vandor   --------------|  " + vandor)
                           else: 
                                print("[+] Mac-Vandor   --------------| " + vandor1)               
                           print()
                       else:
                           print("[+] TRY HOST     --------------| ",Host)
                           sys.stdout.write('\x1b[1A')
                           sys.stdout.write('\x1b[2K')

          def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser = argparse.ArgumentParser(description="Example: ./PingHost.py -p 10.195.100.0/24  ")
              parser.add_argument( '-p',"--ping"   ,metavar='' , action=None  ,help ="Target ip address or name ")
              
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   Discover_Network()





