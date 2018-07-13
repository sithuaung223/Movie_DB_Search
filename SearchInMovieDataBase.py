import http.client
import json
import time


def GetMovieListFromJsonData(json_data):
	movie_list = []
	movie_list.append();


def GetJsonDataWithUrl(url):
	payload = "{}"

	time.sleep(0.25)
	CONN.request("GET", url, payload)
	response = CONN.getresponse()
	raw_data = response.read().decode("utf-8")
	json_data = json.loads(raw_data)

	return json_data


def GetListOfAllPagesWithURL(url, num_pages):
	data_pages_list = []

	# going through all pages
	print(num_pages)
	for page_num in range(1, num_pages+1):
		url_page = "%s&page=%d" % (url, page_num)
		json_data = GetJsonDataWithUrl(url_page)
		data_pages_list.extend(json_data["results"]) # merge all the list from each page

	return data_pages_list

def ExtractGivenParameterList(infos_list, parameter):
	parameter_list = []

	for info in infos_list:
		parameter_list.append(info[parameter])

	return parameter_list


def SearchMovieIDWithStartDateAndEndDate(start_date, end_date):

	# get num pages
	url_movie  = "/3/discover/movie?api_key=%s&primary_release_date.gte=%s&primary_release_date.lte=%s&sort_by=primary_release_date.asc" % (APIKEY, start_date, end_date)
	movie_data = GetJsonDataWithUrl(url_movie)
	movie_info_list = GetListOfAllPagesWithURL(url_movie, movie_data["total_pages"])
	print(len(movie_info_list))
	movie_id_list = ExtractGivenParameterList(movie_info_list, "id")

	return movie_id_list;

# Variables
APIKEY     = "606aaffd7ca10f0b80804a1f0674e4e1"
CONN       = http.client.HTTPSConnection("api.themoviedb.org")
START_DATE = "2017-12-01"
END_DATE   = "2017-12-31"

movie_id_list = SearchMovieIDWithStartDateAndEndDate(START_DATE, END_DATE)
print(movie_id_list)



