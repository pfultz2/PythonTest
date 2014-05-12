import http.client
import json

def send_request_data(method, url, obj):
    conn = http.client.HTTPConnection('localhost:8000')
    conn.request(method, url, json.dumps(obj), {'Content-Type': 'application/json'})

def send_request(method, url):
    conn = http.client.HTTPConnection('localhost:8000')
    conn.request(method, url)
    try:
        return json.loads(conn.getresponse().read().decode())
    except:
        return None


vpn_tom = {'name': 'tom', 'lat': 100.0, 'lon': 30.0 }
send_request_data('PUT', '/vpn', vpn_tom)

vpn_tim = {'name': 'tim', 'lat': 10000.0, 'lon': 500.0 }
send_request_data('PUT', '/vpn', vpn_tim)

vpn_bob = {'name': 'bob', 'lat': 1.0, 'lon': 3.0 }
send_request_data('PUT', '/vpn', vpn_bob)

result = send_request('GET', '/vpn?lat=1.0&lon=1.0')
print(result)
assert [x['name'] for x in result] == ['bob', 'tom', 'tim']

send_request('DELETE', '/vpn/bob')
send_request('DELETE', '/vpn/tom')
send_request('DELETE', '/vpn/tim')

empty_result = send_request('GET', '/vpn?lat=1.0&lon=1.0')
print(empty_result)
assert len(empty_result) == 0

