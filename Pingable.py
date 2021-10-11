#!/usr/bin/env python3 
import argparse
import sys
class Run :
        def __init__(self):
            self.args_command()  
            self.control()
        def control(self):
           if self.args.network  :
              from Package.Pingclass import  Discover_Network
              run = Discover_Network()
              exit()
#           elif self.args.pingclass and self.args.strat :
#              from Package.Start_range import gi
           else:
             if self.args.Host :
                 from Package.OneHost import  Host_One
                 run = Host_One()
                 exit()
        def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser.add_argument( '-N',"--network"   ,metavar='' , action=None  ,help ="ping all Network ,IPaddress/subnet ")
              parser.add_argument( '-H',"--Host"   ,metavar='' , action=None  ,help ="Ping One Host Only ")
              parser.add_argument( '-O',"--output"   ,metavar='' , action=None  ,help ="out put file report ")
             # Parser.add_argument( '-R', 

              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()

if __name__=="__main__":
   Run()

