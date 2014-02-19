#!/usr/bin/python

import ncode
import BaseHTTPServer

HOST_NAME = 'example.com'
PORT_NUMBER = 9000
DEFAULT_WIDTH = 128

class NCodeHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
  def do_GET(s):
    message = ncode.get_message(s.path.strip("/"), DEFAULT_WIDTH)
    if len(message) == 0:
      message = ncode.get_message("welcometoncode", DEFAULT_WIDTH)
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<html><head><title>ncoded text</title></head>")
    s.wfile.write('<body bgcolor="#000000" text="#00ff00"><pre>%s</pre>' % message)
    s.wfile.write("</body></html>")

if __name__ == '__main__':
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), NCodeHandler)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
