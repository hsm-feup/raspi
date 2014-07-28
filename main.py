#!/usr/bin/python

import time #sleep
import sys #exit
import signal #signal
import netServer
        
def signal_handler(signal, frame):
    app.exit()

class App():
    def main(self):
        signal.signal(signal.SIGINT, signal_handler)
        
        self.server = netServer.netServer()   
        self.server.onMsg = self.onMsg
        
        while True:
            time.sleep(.1)
    
    def onMsg(self, cmd):
        if cmd[0:3] == "log":
            self.server.log = True if cmd[3] == "1" else False       
        elif cmd[0] == "v":
            self.server.send("Raspi v1.0")
        
    def exit(self):
        print("\rYou pressed Ctrl+C!")
        self.server.exit()
        sys.exit(0)
        
if __name__ == '__main__':
    app = App()
    app.main()
    