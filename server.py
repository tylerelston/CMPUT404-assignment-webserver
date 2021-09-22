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
        else:
            url = "www" + data[1].decode("utf-8") 
            print("URL:", url)
            if os.path.isdir(url) or os.path.isfile(url):
                if url.endswith("/"):
                    file = self.readFile(url + "index.html")
                    self.respond("200 OK", "html", file)
                else:
                    if not url.endswith("/") and not ".css" in url and not ".html" in url:
                        new = url.split("/")[-1] + "/"
                        self.respond("301 Moved Permanently", "", "", new)
                        return
                    file = self.readFile(url)
                    self.respond("200 OK", os.path.splitext(url)[-1].replace(".",""), file)
            else:
                print('404 Not Found')
                self.respond("404 Not Found")

    def readFile(self, path):
        file = open(path).read()
        print(file)
        return file

    def respond(self, code, contentType = "", file = "", location = ""):
        response = "HTTP/1.1 " + code + "\r\n"
        if contentType:
            response += "content-type: text/" + contentType + "\r\n"
        else:
            response += "content-type: application/octet-stream\r\n"
        if location:
            response += "location: " + location + "\r\n"
        response += "Connection: close\r\n"
        if file:
            response += "\r\n"
            response += file

        response += "\r\n"
        print("RESPONSE:")
        print(response)
        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
