import http.client
import json

def SearchMovieWithStartDateAndEndDate(start_date,end_date):
	payload = "{}"

	url = "/3/discover/movie?api_key=%s&primary_release_date.gte=%s&primary_release_date.lte=%s" % (APIKEY, start_date, end_date)
	conn.request("GET", url, payload)

	res = conn.getresponse()
	data = res.read().decode("utf-8")
	json_obj = json.loads(data)

	print(data)

APIKEY     = "606aaffd7ca10f0b80804a1f0674e4e1"
conn       = http.client.HTTPSConnection("api.themoviedb.org")
start_date = "2017-12-01"
end_date   = "2017-12-31"
SearchMovieWithStartDateAndEndDate(start_date, end_date)


