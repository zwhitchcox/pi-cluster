import socketserver
import subprocess
import os
import logging
import requests
import subprocess
import json
import http.server
from http import HTTPStatus

SERVICE_PORT=9090

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()

fileHandler = logging.FileHandler("/etc/cruster/api.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# uncomment to output log to console
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# logger.addHandler(consoleHandler)

CRUSTER_DIR="/etc/cruster"

def read_status():
  status_fd = open("{}/status".format(CRUSTER_DIR), "r+")
  status = status_fd.read()
  status_fd.close()
  return status
def read_hostname():
  hostname_fd = open("/etc/hostname", "r+")
  hostname = hostname_fd.read()
  hostname_fd.close()
  return hostname
def read_clustername():
  clustername_fd = open("{}/clustername".format(CRUSTER_DIR), "r+")
  clustername = clustername_fd.read()
  clustername_fd.close()
  return clustername
def read_masterip():
  masterip_fd = open("{}/masterip".format(CRUSTER_DIR), "r+")
  masterip = masterip_fd.read()
  masterip_fd.close()
  return masterip
def read_gh_username():
  masterip_fd = open("{}/gh_username".format(CRUSTER_DIR), "r+")
  masterip = masterip_fd.read()
  masterip_fd.close()
  return masterip


def write_keys(keys):
  root_auth_keys_fd = open("/root/.ssh/authorized_keys", "w")
  root_auth_keys_fd.write(keys.decode('utf-8'))
  root_auth_keys_fd.close()
  pi_auth_keys_fd = open("/home/pi/.ssh/authorized_keys", "w")
  pi_auth_keys_fd.write(keys.decode('utf-8'))
  pi_auth_keys_fd.close()

# def write_hostname(new_hostname):
#   hostname_fd = open("/etc/hostname", "w+")
#   hostname_fd.write(new_hostname)
#   hostname_fd.close()

# def exec_write(self, cmd):
#   self.send_response(HTTPStatus.OK)
#   self.send_header("Access-Control-Allow-Origin", "*")
#   self.end_headers()
#   process = subprocess.Popen(cmd,
#                             stdout=subprocess.PIPE,
#                             stderr=subprocess.PIPE,
#                             universal_newlines=True)
#   while True:
#       output = process.stdout.readline()
#       err_output = process.stderr.readline()
#       if output != "":
#         self.wfile.write(output.encode('utf-8'))
#       if err_output != "":
#         self.wfile.write(("error: " + err_output).encode('utf-8'))
#       # Do something else
#       return_code = process.poll()
#       if return_code is not None:
#           self.wfile.write('RETURN CODE {}\r\n'.format(return_code).encode('utf-8'))
#           # Process has finished, read rest of the output
#           for output in process.stdout.readlines():
#               self.wfile.write(output.encode('utf-8'))
#           break



class Handler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    # if self.path == "/":
    #   print("got request for home")
    #   self.send_response(HTTPStatus.OK)
    #   self.end_headers()
    #   with open('/home/pi/stream/index.html', 'rb') as file:
    #     self.wfile.write(file.read())

    # elif self.path == "/join-command":
    #   stream = os.popen('kubeadm token create --print-join-command')
    #   output = stream.read()
    #   if output != "":
    #     self.send_response(HTTPStatus.OK)
    #     self.end_headers()
    #     self.wfile.write(output.encode('utf-8'))
    #   else:
    #     self.send_response(HTTPStatus.SERVICE_UNAVAILABLE)
    #     self.end_headers()
    #     self.wfile.write(b'Not yet ready')


    # elif self.path.startswith("/set-hostname"):
    #   new_hostname = self.path[14:]
    #   exec_write(self, ["hostname", new_hostname])
    #   write_hostname(new_hostname)
    #   self.wfile.write("Rebooting...\r\n".encode("utf-8"))
    #   exec_write(self, ["reboot"])

    # elif self.path == "/init-master":
    #   exec_write(self, ['bash', 'kubernetes-init-master.sh'])

    # elif self.path == "/reset":
    #   exec_write(self, ['kubeadm', 'reset', '-f'])

    # if self.path == "/node-info":
    if self.path == "/reset-github-keys":
      username = read_gh_username().strip().encode('utf-8')
      url = "https://github.com/{}.keys".format(username.decode('utf-8'))
      print(url)
      r = requests.get(url)
      if r.status_code < 400:
        write_keys(r.content)
        self.send_response(HTTPStatus.OK)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Success!")
      else:
        self.send_response(r.status_code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Couldn't get that github username....might not exist")

    if self.path == "/node-info":
      self.send_response(HTTPStatus.OK)
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      status = read_status()
      masterip = ""
      can_reset_keys = False
      try:
        masterip = read_masterip().strip()
      except:
        pass
      try:
        gh_username = read_gh_username()
        if gh_username != "":
          can_reset_keys = true
      except:
        pass
      self.wfile.write(json.dumps({
        'status': status.strip(),
        'hostname': read_hostname().strip(),
        'clustername': read_clustername().strip(),
        'masterip': masterip,
        'canresetkeys': can_reset_keys,
      }).encode('utf-8'))
  # def do_POST(self):
  #   content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
  #   post_data = self.rfile.read(content_length) # <--- Gets the data itself
  #   logger.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
  #       str(self.path), str(self.headers), post_data.decode('utf-8'))
  #   self.send_response(200)
  #   self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))



try:
  socketserver.TCPServer.allow_reuse_address = True
  httpd = socketserver.TCPServer(('', SERVICE_PORT), Handler)
  httpd.serve_forever()

except KeyboardInterrupt:
  print('^C received, shutting down the web server')
  httpd.server_close()