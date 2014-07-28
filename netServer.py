from threading import Thread
import socket

def getLocalIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

def pchar(c):
    return c if ord(c)<127 and ord(c)>=32 else "."
    
def printMsg(msg):
    N = 16
    print("-" * (N*3 + N))
    for i, c in enumerate(msg):
        if i % N == 0:
            if i != 0: print(hex + char)
            hex = char = ""
        hex = hex + "{:0>2X} ".format(ord(c))
        char = char + pchar(c)           
    print(hex + "   " * (N-1 - i%N) + char)       
       
class netServer():
    def __init__(self, port=12345, parent=None):
        self.onMsg = None
        self.log = True
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # [Errno 98] Address already in use
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.bind(('', port))
        self.soc.listen(1)
        print("Listening at {}:{}".format(getLocalIP(), port))

        self._exit = False
        self.th = Thread(target=self._th_read)
        self.th.daemon = True
        self.th.start()

    def send(self, msg):
        try:
            self.conn.sendall(msg + "\r\n")
        except AttributeError:
            print("Not connected yet!")
        except socket.error:
            print("Lost connection!")
        
    def _th_read(self):
        while not self._exit:
            self.soc.settimeout(1)
            try:
                self.conn, addr = self.soc.accept()
            except socket.timeout:
                continue
            self.conn.settimeout(1)
            print("Connected from {}:{}".format(addr[0], addr[1]))
            self.conn.recv(1024) # empty receiving buffer
            buffer = ""
            while not self._exit:
                try:
                    str = self.conn.recv(1024)
                    if str == "":
                        print("Disconnected")
                        break # if conn lost get out!
                    buffer = buffer + str
                    while "\r\n" in buffer: # PuTTY send CR+LF per each "Enter" key
                        (cmd, buffer) = buffer.split("\r\n", 1)
                        if self.log: printMsg(cmd)
                        if self.onMsg and cmd<>"":
                            self.onMsg(cmd)                        
                except socket.timeout:
                    continue

    def exit(self):
        self._exit = True
        self.th.join()
        self.soc.close()
        