#!/usr/bin/env python
#encoding: utf-8 

import os, sys, traceback, logging, time, threading
from tkinter import *

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from logging import getLogger
from renv_device import RenvDevice, actionHandler, event

# host = "192.168.128.157:8080"
# host = "192.168.170.219:8080"
#host = "192.168.180.15:8080"
host = "localhost:8080"
typeId = "RENVROS.TEST.DEVICE6"
name = "renvros2-tester6"
version = "1.0.0"
device_uuid = None
deviceName = "DEVICE6"


logging.basicConfig(filename=__name__ + '.log',level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')

do_cancel = None
goto = None

class MyHandler(BaseHTTPRequestHandler):
    """
    Received the request as json, send the response as json
    please you edit the your processing
    """
    def do_GET(self):
        try:
            print('pwd', os.getcwd())
            path = self.path
            print('path:', path)
            if path == '/cancel':
                do_cancel()
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                response = { 'status' : 200,
                             'result' : { 'hoge' : 100,
                                          'bar' : 'bar' }
                }
                responseBody = json.dumps(response)
                self.wfile.write(responseBody.encode('utf-8'))
                return
            elif path.startswith('/goto/'):
                target = int(path[-1:])
                print('goto', target)
                goto(target)
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                response = { 'status' : 200,
                             'result' : { 'hoge' : 100,
                                          'bar' : 'bar' }
                }
                responseBody = json.dumps(response)
                self.wfile.write(responseBody.encode('utf-8'))
                return
                
            else:
                #super().do_GET()
                self.path = "index.html"
                f = open(self.path)
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(f.read().encode())
                f.close()
                
            #content_len=int(self.headers.get('content-length'))
            #requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))
            """
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)

            self.wfile.write(responseBody.encode('utf-8'))
            """
            ##Open the static file requested and send it
        except Exception as e:
            print("An error occured")
            print("The information of error is as following")
            print(type(e))
            print(e.args)
            print(e)
            response = { 'status' : 500,
                         'msg' : 'An error occured' }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)

            self.wfile.write(responseBody.encode('utf-8'))


class MyRenvDevice(RenvDevice):
    """
        My Renv Device
    """
    
    def __init__(self):
        """
        My Renv Device
        """
        RenvDevice.__init__(self, typeId, name, version, device_uuid, deviceName=deviceName, use_mta=False, logger=getLogger(__name__))
        paramInfo = self.buildParamInfo('flag', 'Int', 'If non zero, do cancel')
        self.cancel = lambda x, f=self.addCustomEvent('Cancel', 'Cancel Behavior', [paramInfo]): f(**{'flag': x})

        paramInfo = self.buildParamInfo('target', 'Int', 'Target Position index')
        self.goto = lambda x, f=self.addCustomEvent('GoTo', 'GoTo Behavior', [paramInfo]): f(**{'target': x})
        
        global do_cancel
        do_cancel = lambda rd=self: rd.cancel(1)
        global goto
        goto = lambda x, rd=self: rd.goto(x)
        pass
    
def on_button(rd):
    rd.cancel(1)

def main():
    try:
        rd = MyRenvDevice()
        print('Connecting...')
        rd.connect(host)
        th = threading.Thread(target=lambda rd=rd : rd.run_forever())
        th.start()

        #root = Tk()
        #button = Button(root, text = 'Cancel', command=lambda x=rd:on_button(x), width=40, height=40)
        #button.pack()
        #root.mainloop()
        #rd.stop_running()
        server_name='0.0.0.0'
        port=8000
    
        server = HTTPServer((server_name, port), MyHandler)
        server.serve_forever()
        
    except:
        traceback.print_exc()

    
if __name__ == '__main__':
    main()










