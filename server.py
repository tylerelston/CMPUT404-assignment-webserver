#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        data = self.request.recv(1024).strip()
        print('#######################################')
        print(data)
        self.parse(data.split())

    def parse(self, data):
        if data[0].decode("utf-8") != "GET":
            print("405 Method Not Allowed")
            self.respond("405 Method Not Allowed")

        url = "www" + data[1].decode("utf-8") 
        print("URL:", url)
        if os.path.isdir(url) or os.path.isfile(url):
            print('is dir!')
            if data[1].decode("utf-8") == "/":
                print(' root')
                file = self.readFile(url + "index.html")
                self.respond("200 OK", file)
            else:
                print(' not root!')
                file = self.readFile(url)
                self.respond("200 OK", file)
        else:
            print('404 Not Found')
            self.respond("404 Not Found")

    def readFile(self, path):
        file = open(path).read()
        print(file)
        return file

    def respond(self, code, file = ""):
        response = "HTTP/1.1 "
        response += code + "\r\n"
        response += file
        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
