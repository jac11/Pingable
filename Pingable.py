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



Banner = """
 ______ _                   _     _       
(_____ (_)                 | |   | |      
 _____) ) ____   ____  ____| | _ | | ____ 
|  ____/ |  _ \ / _  |/ _  | || \| |/ _  )
| |    | | | | ( ( | ( ( | | |_) ) ( (/ / 
|_|    |_|_| |_|\_|| |\_||_|____/|_|\____)
               (_____|by:jacstory                    
"""
print(Banner)


host_name  = socket.gethostname()

Mac_Interface = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

Mac_Get = Mac_Interface[0:8].replace(":","").upper()
Macdb = open('mac-vendor.txt', 'r')
Mac = Macdb.readlines()

count = 0
for line in Mac:
    line = line.strip()
    if Mac_Get in line  : 
       vendor = line[7:].strip() 
       break 
    elif Mac_Get not  in line  : 
          vendor = "Unknown-MAC" 
    count += 1
    
class Discover_Network():
          
          def __init__(self):
               self.args_command()
               self.Ping_command()            
                
          def Ping_command(self):
       
             try:
               if self.args.ping or (self.args.ping and self.args.output) :
                   if "/" not in self.args.ping:
                       print("Plese set the subnet netwotk")
                       exit()
                   Network    = ipaddress.ip_network('{}'.format(self.args.ping), strict=False)
                   Network_ID = Network.network_address
                   SubNet     = Network.netmask
                   print("\n[*] HOST INFO-\n"+"="*14+"\n")
                   print("[+] Network-ID      --------------|- " +  str(Network_ID))
                   print("[+] NetWork-Prefix  --------------|- " +  self.args.ping[-2:])
                   print("[+] Subnet-Mask     --------------|- " +  str(SubNet))
                   print("[+] HOST-IP         --------------|- " +  self.args.ping[0:-3])
                   print("[+] Mac-Address     --------------|- " +  Mac_Interface)
                   print("[+] Mac-Vendor      --------------|- " + vendor)
                   print("\n"+"="*50+'\n')
                   if self.args.output:
                     printF  = ""
                     printF  += ("\n[*] HOST INFO-\n"+"="*14+"\n")+"\n"
                     printF  += ("[+] Network-ID      --------------|- " +  str(Network_ID))+"\n"
                     printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.ping[-2:])+"\n"
                     printF  += ("[+] Subnet-Mask     --------------|- " +  str(SubNet))+"\n"
                     printF  += ("[+] HOST-IP         --------------|- " +  self.args.ping[0:-3])+"\n"
                     printF  += ("[+] Mac-Address     --------------|- " +  Mac_Interface)+"\n"
                     printF  += ("[+] Mac-Vendor      --------------|- " + vendor)+"\n"
                     printF  += ("\n"+"="*50+'\n')
                     with open(self.args.output,"w+") as out_put:
                         out_put.write(Banner+"\n"+printF)
                   scop   = "/"
                   NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.ping[-2:]))
                   for Host in NetworkID.hosts():
                       Host = str(Host)
                       DisCover = Popen(["ping", "-c1",Host], stdout=PIPE)
                       output   = DisCover.communicate()[0]
                       respons  = DisCover.returncode                       
                       if respons == 0:
                           print("[+] HOST OnLine     --------------| ",Host)
                           if self.args.output :
                             printF = str("[+] HOST OnLine     --------------|  " + Host).strip()
                             with  open (self.args.output,"a") as out_put :
                                 out_put.write(printF+"\n")
                           pid = Popen(["arp", "-n", Host], stdout=PIPE)
                           arp_host = pid.communicate()[0]
                           Mac = str(re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})",arp_host.decode('utf-8')))\
                           .replace("<re.Match object; span=(114, 131), match='",'').replace("'>",'')
                           
                           if "None" in Mac:
                                print("[*] Mac-Address     ..............|-",Mac_Interface)
                                if self.args.output :
                                   printF = str("[*] Mac-Address     ..............|- "+Mac_Interface).strip()
                                   with open (self.args.output,'a') as out_put :
                                          out_put.write(str(printF+"\n"))
                                interfaceMac = Mac_Interface[0:8].replace(":","").upper() 
                           else:
                                   print("[*] Mac-Address     ..............|-",Mac)
                                   if self.args.output :  
                                      printF = str("[*] Mac-Address     ..............|- "+Mac).strip()
                                      with open (self.args.output,'a') as out_put :
                                           out_put.write(str(printF+"\n"))
                           MacGET= Mac[0:8].replace(":","").upper()
                           Macdb = open('mac-vendor.txt', 'r')
                           MacFile = Macdb.readlines()
                           count = 0
                           for line in MacFile:
                              line = line.strip()
                              if MacGET in line  : 
                                 vendor1 = line[7:].replace("    ","")  
                                 break
                              elif MacGET not  in line:
                                   vendor1 = " Unknown-MAC" 
                              count += 1  
                           if "None" in Mac :
                                print("[+] Mac-Vendor      --------------|  " +vendor)
                                if  self.args.output :
                                    printF = str("[+] Mac-Vendor      --------------|  " +vendor).strip()
                                    with open(self.args.output ,"a") as out_put :
                                         out_put.write(str(printF+"\n"))
                           else: 
                                print("[+] Mac-Vendor      --------------| " +vendor1)
                                if self.args.output :    
                                    printF = str("[+] Mac-Vendor      --------------| " +vendor1).strip()
                                    with open(self.args.output ,"a") as out_put :
                                         out_put.write(str(printF+"\n"))           
                           print()
                           if self.args.output:
                              with open(self.args.output,"a") as out_put :
                                   out_put.write("\n")
                       else:
                           print("[+] TRY HOST        --------------| ",Host)
                           sys.stdout.write('\x1b[1A')
                           sys.stdout.write('\x1b[2K')
                   print(Banner) 
                   if self.args.output:
                      with open(self.args.output,'a') as out_put :
                          out_put.write(Banner) 
             except KeyboardInterrupt:
                print(Banner)
                if self.args.output:
                   with open(self.args.output,'a') as out_put :
                        out_put.write(Banner)
          def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser = argparse.ArgumentParser(description="Example: ./PingHost.py -p 10.195.100.0/24  ")
              parser.add_argument( '-p',"--ping"   ,metavar='' , action=None  ,help ="Target ip Address or name ")
              parser.add_argument( '-o',"--output"   ,metavar='' , action=None  ,help ="Target ip Address or name ")
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   Discover_Network()
