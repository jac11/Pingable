 #!/usr/bin/env python3
 
import os
import sys
import re
import argparse
import ipaddress
import socket 
import uuid
from subprocess import Popen, PIPE, check_output 
from Package.Banner import *
import subprocess 
import timeit,time


command_argv = str(" ".join(sys.argv))
start = timeit.default_timer()
Mac_Interface = ':'.join(re.findall('..', '%012x' % uuid.getnode())) 
Mac_Get = Mac_Interface[0:8].replace(":","").upper()
Macdb = open('Package/mac-vendor.txt', 'r')
Mac = Macdb.readlines()

try:
   host_name  = socket.gethostname() 
   host_ip    = str(check_output(['hostname', '--all-ip-addresses'],stderr=subprocess.PIPE)).\
   replace("b'","").replace("'","").replace("\\n","")
   if  host_ip in str(ipaddress.ip_network(self.args.network), strict=False):
       pass
   else:
        if  " " in host_ip : 
            host_ip = host_ip.split()       
            host_ip = host_ip[-1]
except Exception :
    if "/" in sys.argv[2]:
       host_ip = sys.argv[2][:-3]
    else:
       host_ip = sys.argv[2] 
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
             try:
               if self.args.network or (self.args.network and self.args.output) :
                   if "/" not in self.args.network:
                       print("\n"+"="*50+"\n"+"[*] Set the Subnet Netwotk...."+"\n"+"="*50+"\n")
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
                   print("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))
                   print("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))
                   print("[+] Number of hosts --------------|- " +  str(Hosts_range ))
                   print("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))
                   print("\n"+"="*50+"\n"+"[*] Host-discover-"+"\n"+"="*20+"\n")
                   if self.args.output:
                         printF  = ""
                         printF  += ("[+] "+ command_argv)+"\n"
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
                         printF  += ("\n"+"="*50+"\n"+"[*] Host-discover-"+"\n"+"="*20+"\n\n")
                         with open(self.args.output,"w+") as out_put:
                             out_put.write(Banner+"\n"+printF)
                           
                   scop   = "/"
                   Network  = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-2:]))
                   Hcount = 0
                   dcount = 0
                   for Host in Network .hosts():
                       Host = str(Host)
                       DisCover = Popen(["ping", "-w1",Host], stdout=PIPE)
                       output   = DisCover.communicate()[0]
                       respons  = DisCover.returncode                       
                       if respons == 0:
                           Hcount  +=1	
                           print("[+] HOST OnLine     --------------| ",Host)
                          
                           if self.args.output :
                             printF = str("[+] HOST OnLine     --------------|  " + Host).strip()
                             with  open (self.args.output,"a") as out_put :
                                 out_put.write(printF+"\n")
                           pid = Popen(["arp", "-n", Host], stdout=PIPE)
                           arp_host = pid.communicate()[0]
                           Mac = str(re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})",arp_host.decode('utf-8')))\
                           .replace("<re.Match object; span=(114, 131), match='",'').replace("'>",'')    
                           
                           if "None" in Mac and str(ipaddress.ip_address(Host)) ==  str(ipaddress.ip_address(host_ip)) :
                                  print("[*] Mac-Address     ..............|-",Mac_Interface)
                                  if self.args.output :
                                      printF = str("[*] Mac-Address     ..............|- "+Mac_Interface).strip()
                                      with open (self.args.output,'a') as out_put :
                                           out_put.write(str(printF+"\n"))
                                  interfaceMac = Mac_Interface[0:8].replace(":","").upper() 
                                 
                           elif "None" in Mac and str(ipaddress.ip_address(Host)) != str(ipaddress.ip_address(host_ip)) :                     
                                  print("[*] Mac-Address     ..............|- None")
                                  if self.args.output :
                                      printF = str("[*] Mac-Address     ..............|- None")
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
                               
                           if "None" in Mac and str(ipaddress.ip_address(Host)) ==  str(ipaddress.ip_address(host_ip)) : 
                                   print("[+] Mac-Vendor      --------------|  " +vendor)
                                   if  self.args.output :
                                        printF = str("[+] Mac-Vendor      --------------|  " +vendor).strip()
                                        with open(self.args.output ,"a") as out_put :
                                            out_put.write(str(printF+"\n"))
                                   
                           elif "None" in Mac and str(ipaddress.ip_address(Host)) != str(ipaddress.ip_address(host_ip)) :
                                   print("[+] Mac-Vendor      --------------|  None ")
                                   if  self.args.output :
                                        printF = str("[+] Mac-Vendor      --------------|  None")
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
                           dcount +=1
                           print("[+] TRY HOST        --------------| ",Host)
                           sys.stdout.write('\x1b[1A')
                           sys.stdout.write('\x1b[2K')
                   stop = timeit.default_timer()
                   sec = stop  - start
                   fix_time = time.gmtime(sec)
                   result = time.strftime("%H:%M:%S",fix_time)                
                  
                   print("\n[*] Scan-Result-\n"+"="*14+"\n")
                   print("[+] Total Hosts       --------------|- " +  str(Hosts_range))
                   print("[+] Active Hosts      --------------|- " +  str(Hcount))
                   print("[+] Inactive Hosts    --------------|- " +  str(dcount))  
                   print("[+] Run-Time          --------------|- " +  result) 
                   print(Banner) 
                   
                   if self.args.output:
                      printF = ""
                      printF += ("\n[*] SCAN RSULET-\n"+"="*14+"\n")+"\n"
                      printF += ("[+] Total Hosts       --------------|- " +  str(Hosts_range))+"\n"
                      printF += ("[+] Active Hosts      --------------|- " +  str(Hcount))+"\n"
                      printF += ("[+] Inactive Hosts    --------------|- " +  str(dcount))+"\n"
                      printF += ("[+] Run-Time          --------------|- " +  str(result))+"\n"
                      with open(self.args.output,'a') as out_put :
                          out_put.write(printF+Banner)
                        
             except Exception:
                    print("\n"+"="*50+"\n"+"[*] HOST (",self.args.network,")   -------------| ValueError"+"\n"+"="*50+"\n")
         except KeyboardInterrupt:
                print(Banner)
                if self.args.output:
                   with open(self.args.output,'a') as out_put :
                      out_put.write(Banner)
                
      def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser.add_argument( '-N',"--network"   ,metavar='' , action=None  )
              parser.add_argument( '-O',"--output"   ,metavar='' , action=None  )
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   Discover_Network()
 

