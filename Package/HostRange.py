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
Macdb = open('Package/mac-vendor.txt', 'r')
Mac = Macdb.readlines()
host_name  = socket.gethostname()
host_ip    = check_output(['hostname', '--all-ip-addresses']).decode('utf8').replace('\n','')
count = 0
for line in Mac:
    line = line.strip()
    if Mac_Get in line  : 
       vendor = line[7:].strip() 
       break 
    elif Mac_Get not  in line  : 
          vendor = "Unknown-MAC" 
    count += 1
    
class RangeOfHosts :
          
          def __init__(self):
               self.args_command()
               self.Ping_Range()            
                
          def Ping_Range(self):
       
             try:
               if self.args.network or (self.args.network and self.args.output) :
                   if "/" not in self.args.network:
                       print("[*] Set the Subnet Netwotk....")
                       exit()
                   Network     = ipaddress.ip_network('{}'.format(self.args.network), strict=False)
                   Network_ID  = Network.network_address
                   SubNet      = Network.netmask
                   Hosts_range = Network.num_addresses - 2 
                   print("\n[*] HOST INFO-\n"+"="*14+"\n")
                   print("[+] HOST-IP         --------------|- " +  host_ip)
                   print("[+] Mac-Address     --------------|- " +  Mac_Interface)
                   print("[+] Mac-Vendor      --------------|- " + vendor)
                   print("\n[*] NETWORK INFO-\n"+"="*14+"\n")
                   print("[+] Network-ID      --------------|- " +  str(Network_ID))
                   print("[+] NetWork-Prefix  --------------|- " +  self.args.network[-2:])
                   print("[+] Subnet-Mask     --------------|- " +  str(SubNet))
                   print("[+] Frist ip        --------------|- " +  str([ x for x in Network.hosts()][0]))
                   print("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))
                   print("[+] Number of hosts --------------|- " +  str(Hosts_range ))
                   print("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))
                   print("\n[*] Range Host -\n"+"="*14)
                   print("[+] start-Host       --------------|- " + self.args.start)
                   print("[+] End-Host         --------------|- " +  self.args.end)
                   print("\n"+"="*50+'\n')
                   
                   if self.args.output:
                      printF  = ""
                      printF  += ("\n[*] HOST INFO-\n"+"="*14+"\n")+"\n"
                      printF  += ("[+] HOST-IP         --------------|- " +  host_ip)+"\n"
                      printF  += ("[+] Mac-Address     --------------|- " +  Mac_Interface)+"\n"
                      printF  += ("[+] Mac-Vendor      --------------|- " + vendor)+"\n"
                      printF  += ("\n[*] NETWIRK INFO-\n"+"="*14+"\n")+"\n"
                      printF  += ("[+] Network-ID      --------------|- " +  str(Network_ID))+"\n"
                      printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.network[-2:])+"\n"
                      printF  += ("[+] Subnet-Mask     --------------|- " +  str(SubNet))+"\n"
                      printF  += ("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))+"\n"
                      printF  += ("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))+"\n"
                      printF  += ("[+] Number of hosts --------------|- " +  str(Hosts_range ))+"\n"
                      printF  += ("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))+"\n"
                      printF  += ("\n[*] Range Host -\n"+"="*14)+"\n"
                      printF  += ("[+] start-Host       --------------|- " + self.args.start)+"\n"
                      printF  += ("[+] End-Host         --------------|- " +  self.args.end)+"\n"
                      printF  += ("\n"+"="*50+'\n\n')
                      with open(self.args.output,"w+") as out_put:
                         out_put.write(Banner+"\n"+printF)
                   scop   = "/"
                   NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-2:]))               
                   for Host_Num in range(int(self.args.start),int(self.args.end)) :
                       fix  = self.args.network
                       ip,sub = fix.split('/')
                       oct_ip = ip.split('.')
                       oct_ip.remove(oct_ip[3])
                       oct_ip.append(Host_Num)
                       Host = str(oct_ip).replace("['","").replace("'","").replace(",",".").replace("]","").replace(" ","")               
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
                           print("[+] TRY HOST        --------------| ",Host)
                           sys.stdout.write('\x1b[1A')
                           sys.stdout.write('\x1b[2K')
                   print("="*50+"\n"+Banner) 
                   if self.args.output:
                      with open(self.args.output,'a') as out_put :
                          out_put.write("="*50+"\n"+Banner) 
             except KeyboardInterrupt:
                print(Banner)
                if self.args.output:
                   with open(self.args.output,'a') as out_put :
                        out_put.write(Banner)
          def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser = argparse.ArgumentParser(description="Example: ./PingHost.py -p 10.195.100.0/24  ")
              parser.add_argument( '-N',"--network"   ,metavar='' , action=None  ,help ="ping all Network ,IPaddress/subnet ")
              parser.add_argument( '-S',"--start"   ,metavar='' , action=None  ,help ="ping all Network ,IPaddress/subnet ")
              parser.add_argument( '-O',"--output"   ,metavar='' , action=None  ,help ="Target ip Address or name ")
              parser.add_argument( '-E',"--end"   ,metavar='' , action=None  ,help ="Target ip Address or name ")
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   RangeOfHosts()



 
 
