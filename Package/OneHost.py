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
| |    |  | | | ( ( | ( ( | | |_) ) ( (/ / 
|_|    |_|_| |_|\_|| |\_||_|____/|_|\____)
               (_____|by:jacstory                    
"""
print(Banner)
 
 
host_name  = socket.gethostname()
 
Mac_Interface = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
 
Mac_Get = Mac_Interface[0:8].replace(":","").upper()
Macdb = open('Package/mac-vendor.txt', 'r')
Mac = Macdb.readlines()
host_name  = socket.gethostname()
host_ip   = check_output(['hostname', '--all-ip-addresses']).decode('utf8').replace('\n','')
count = 0
for line in Mac:
    line = line.strip()
    if Mac_Get in line  : 
       vendor = line[7:].strip() 
       break 
    elif Mac_Get not  in line  : 
          vendor = "Unknown-MAC" 
    count += 1
    
class Host_One():
          
          def __init__(self):
               self.args_command()
               self.Ping_command()            
                
          def Ping_command(self):
       
             try:
               if self.args.Host or (self.args.Host and self.args.output) :
                   Network     = ipaddress.ip_network('{}'.format(self.args.Host), strict=False)
                   Network_ID  = Network.network_address
                   SubNet      = Network.netmask
                   Hosts_range = Network.num_addresses - 2 
                   print("\n[*] HOST INFO-\n"+"="*14+"\n")
                   print("[+] HOST-IP         --------------|- " +  host_ip )
                   print("[+] Mac-Address     --------------|- " +  Mac_Interface)
                   print("[+] Mac-Vendor      --------------|- " + vendor)
                   print("\n[*] NETWORK INFO-\n"+"="*14+"\n")
                   print("[+] Network-ID      --------------|- " +  str(Network_ID))
                   print("[+] NetWork-Prefix  --------------|- " +  self.args.Host[-2:])
                   print("[+] Subnet-Mask     --------------|- " +  str(SubNet))
                   print("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))
                   print("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))
                   print("[+] Number of hosts --------------|- " +  str(Hosts_range ))
                   print("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))
                   print("\n"+"="*50+'\n')
                   if self.args.output:
                      printF  = ""
                      printF  += ("\n[*] HOST INFO-\n"+"="*14+"\n")+"\n"
                      printF  += ("[+] HOST-IP         --------------|- " +  host_ip)+"\n"
                      printF  += ("[+] Mac-Address     --------------|- " +  Mac_Interface)+"\n"
                      printF  += ("[+] Mac-Vendor      --------------|- " + vendor)+"\n"
                      printF  += ("\n[*] NETWIRK INFO-\n"+"="*14+"\n")+"\n"
                      printF  += ("[+] Network-ID      --------------|- " +  str(Network_ID))+"\n"
                      printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.Host[-2:])+"\n"
                      printF  += ("[+] Subnet-Mask     --------------|- " +  str(SubNet))+"\n"
                      printF  += ("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))+"\n"
                      printF  += ("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))+"\n"
                      printF  += ("[+] Number of hosts --------------|- " +  str(Hosts_range ))+"\n"
                      printF  += ("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))+"\n"
                      printF  += ("\n"+"="*50+'\n')
                      with open(self.args.output,"w+") as out_put:
                         out_put.write(Banner+"\n"+printF)
                   if "/"in self.args.Host:
                       Host = self.args.Host.replace(self.args.Host[-3:],"")
                   else:
                       Host = self.args.Host
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
                           Macdb = open('Package/mac-vendor.txt', 'r')
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
                           print("[*] HOST  (",Host,")   -------------| Not response !!")
                           
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
              parser.add_argument( '-O',"--output"   ,metavar='' , action=None  ,help ="Target ip Address or name ")
              parser.add_argument( '-H',"--Host"   ,metavar='' , action=None  ,help ="Target ip Address or name ")
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   Host_One()