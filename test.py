import http.client
import time

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

for i in range(50):

	conn.request("GET", "/3/configuration?api_key=606aaffd7ca10f0b80804a1f0674e4e1", payload)
	res = conn.getresponse()
	print (res.status)
	print (res.read())
	while(res.status == 429):
		print("sleep 0.05")
		time.sleep(0.05)
		conn = http.client.HTTPSConnection("api.themoviedb.org")
		conn.request("GET", "/3/configuration?api_key=606aaffd7ca10f0b80804a1f0674e4e1", payload)
		res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))