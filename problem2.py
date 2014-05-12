import http.server
import urllib.parse
import cgi
import sqlite3
import os.path
import json
import math

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SQLVPNConnection:
    def __init__(self, name):
        exists = os.path.isfile(name)
        self.conn = sqlite3.connect(name)
        if not exists: self.create()
        self.conn.row_factory = dict_factory

    def close(self):
        self.conn.close()

    def create(self):
        c = self.conn.cursor()
        c.execute('create table vpns (name text, lat real, lon real)')
        self.conn.commit()

    def put(self, data):
        c = self.conn.cursor()
        c.execute('insert into vpns values(?,?,?)', (data['name'], data['lat'], data['lon']))
        self.conn.commit()

    def delete(self, name):
        c = self.conn.cursor()
        c.execute('delete from vpns where name = ?', (name,))
        self.conn.commit()

    def get(self):
        c = self.conn.cursor()
        c.execute('select * from vpns')
        return c.fetchall()



# A Simple rest server
class RestServer(http.server.BaseHTTPRequestHandler):
    mime_type = ""
    mime_dict = {}
    params = {}
    resource = ""
    id = ""

    def rest_parse_mime(self):
        if self.headers['Content-Type'] == None: self.mime_type = 'text/plain'
        else: self.mime_type, self.mime_dict = cgi.parse_header(self.headers['Content-Type'])

    def rest_parse_content_params(self):
        if self.mime_type == 'multipart/form-data':
            self.params = cgi.parse_multipart(self.rfile, self.mime_dict)
        elif self.mime_type == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            self.params = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)


    def rest_parse_resource(self, path):
        parts = path[1:].split("/")
        if len(parts) > 0: self.resource = parts[0]
        if len(parts) > 1: self.id = parts[1]

    def rest_parse_request(self):
        self.rest_parse_mime()
        self.rest_parse_resource(self.path)
        self.rest_parse_content_params()

    def rest_parse_get_request(self):
        self.rest_parse_mime()
        x = urllib.parse.urlparse(self.path)
        self.params = urllib.parse.parse_qs(x.query)
        self.rest_parse_resource(x.path)

    def rest_dispatch(self):
        # try:
        result = getattr(self, self.command.lower() + "_" + self.resource)()
        self.send_response(200)
        self.end_headers()
        if result != None: self.wfile.write(bytes(result, 'UTF-8'))
        # except:
        #     self.send_error(404)

    def rest_json_content(self):
        encoding = self.headers.get_content_charset()
        if encoding == None: encoding = 'utf-8'
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode(encoding))
        return data
    

    def do_GET(self):
        self.rest_parse_get_request()
        self.rest_dispatch()

    def do_POST(self):
        self.rest_parse_request()
        self.rest_dispatch()

    def do_PUT(self):
        self.rest_parse_request()
        self.rest_dispatch()

    def do_DELETE(self):
        self.rest_parse_request()
        self.rest_dispatch()

def distance(x1, y1, x2, y2):
    return math.sqrt( (float(x2) - float(x1))**2 + (float(y2) - float(y1))**2 )

class VpnServer(RestServer):
    def get_vpn(self):
        lat = self.params['lat'][0]
        lon = self.params['lon'][0]
        vpns = self.vpn_db_connection().get()
        result = sorted(vpns, key=lambda elem:distance(lat, lon, elem['lat'], elem['lon']))
        self.vpn_db_connection().close()
        return json.dumps(result)

    def put_vpn(self):
        data = self.rest_json_content()
        self.vpn_db_connection().put(data)
        self.vpn_db_connection().close()

    def delete_vpn(self):
        self.vpn_db_connection().delete(self.id)
        self.vpn_db_connection().close()

    def vpn_db_connection(self):
        return SQLVPNConnection('vpn.db')


if __name__ == '__main__':
    server_address = ('localhost', 8000)
    httpd = http.server.HTTPServer(server_address, VpnServer)
    httpd.serve_forever()
