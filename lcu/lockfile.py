import base64

lockfile = open(r'C:\Riot Games\League of Legends\lockfile', 'r')
string = lockfile.read()

data = string.split(':')

process = data[0]
password = data[1]
port = data[2]
auth_base = "riot:" + data[3]
auth_bytes = auth_base.encode()
auth_byte64 = base64.b64encode(auth_bytes)
auth = auth_byte64.decode('ascii')
protocol = data[4]