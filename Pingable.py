#!/usr/bin/env python3 

import argparse
import sys
from Package.Banner import *
class Run :
        def __init__(self):
            self.args_command()  
            self.control()
        def control(self):
           if self.args.network and not self.args.start and not self.args.end :
              from Package.Pingclass import  Discover_Network
              run = Discover_Network()
              exit()
           elif self.args.start and self.args.end :
              from Package.HostRange import RangeOfHosts
              run = RangeOfHosts()
              exit()
           elif self.args.Host :
                 from Package.OneHost import  Host_One
                 run = Host_One()
                 exit()
        def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser.add_argument( '-N',"--network"   ,metavar='' , action=None  ,help ="ping all Network ,IPaddress/subnet ")
              parser.add_argument( '-H',"--Host"      ,metavar='' , action=None  ,help ="Ping One Host Only ")
              parser.add_argument( '-O',"--output"    ,metavar='' , action=None  ,help ="output file report ")
              parser.add_argument( '-S',"--start"     ,metavar='' , action=None  ,help ="start of the range Ips ")
              parser.add_argument( '-E',"--end"       ,metavar='' , action=None  ,help ="end of the range ips ")

              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   print( Banner)
                   parser.print_help()
                   exit()

if __name__=="__main__":
   Run()

