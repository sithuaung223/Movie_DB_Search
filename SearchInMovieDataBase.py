import http.client
import json
import time

# Variables
APIKEY     = "606aaffd7ca10f0b80804a1f0674e4e1"
START_DATE = "2017-12-01"
END_DATE   = "2017-12-31"

# Methods
def GetJsonDataWithUrl(url):
	payload = "{}"

	# Set Up Connection
	conn = http.client.HTTPSConnection("api.themoviedb.org")
	conn.request("GET", url, payload)
	response = conn.getresponse()

	# Move DB threw 429 response if requestes are over 40 within 10 seconds. Need to wait them until 10 seconds timer is out
	while (response.status == 429): 
		# Sleep 1 second
		print("sleep1")
		time.sleep(1)
		# Need to rest connection to avoid Sever keep-alive condition
		conn = http.client.HTTPSConnection("api.themoviedb.org")
		conn.request("GET", url, payload)
		response = conn.getresponse()

	# Parse Data into Json
	raw_data = response.read().decode("utf-8")
	json_data = json.loads(raw_data)

	return json_data


def GetListOfAllPagesWithURL(url, num_pages):
	data_pages_list = []

	# going through all pages
	for page_num in range(1, num_pages+1):
		url_page = "%s&page=%d" % (url, page_num)
		json_data = GetJsonDataWithUrl(url_page)
		data_pages_list.extend(json_data["results"]) # merge all the list from each page

	return data_pages_list


def ExtractGivenParameterList(infos_list, parameter):
	parameter_list = []

	# Merge All Lists only with specific key parameter
	for info in infos_list:
		parameter_list.append(info[parameter])

	return parameter_list


def SearchMovieIDWithStartDateAndEndDate(start_date, end_date):

	url_movie  = "/3/discover/movie?api_key=%s&primary_release_date.gte=%s&primary_release_date.lte=%s&sort_by=primary_release_date.asc" % (APIKEY, start_date, end_date)

	movie_data = GetJsonDataWithUrl(url_movie)
	print("STATUS: Get Movie Data!")

	movie_info_list = GetListOfAllPagesWithURL(url_movie, movie_data["total_pages"])
	print("STATUS: Get Movie Info Data List from All Pages!")

	movie_id_list = ExtractGivenParameterList(movie_info_list, "id")
	print("STATUs: Get Movie ID List!")

	return movie_id_list;


def SearchCastsWithIDLists(category, id_list):
	casts_set = set([]);

	# Go through all movies
	for id in id_list:
		url_credits  = "/3/%s/%d/credits?api_key=%s" % (category, id, APIKEY)
		credits_data = GetJsonDataWithUrl(url_credits)
		casts_info_list = ExtractGivenParameterList(credits_data["cast"], "id")
		casts_set.update(casts_info_list);
	print("STATUS: Get All CAST from %s" % category)

	print(len(casts_set))
	print(casts_set)
	return casts_set;

def SearchTvIDWithStartDateAndEndDate(start_date, end_date):

	url_tv  = "/3/discover/tv?api_key=%s&primary_release_date.gte=%s&primary_release_date.lte=%s&sort_by=primary_release_date.asc" % (APIKEY, start_date, end_date)

	tv_data = GetJsonDataWithUrl(url_tv)
	print("STATUS: Get TV Data!")

	tv_info_list = GetListOfAllPagesWithURL(url_tv, tv_data["total_pages"])
	print("STATUS: Get TV Info Data List from All Pages!")

	tv_id_list = ExtractGivenParameterList(tv_info_list, "id")
	print("STATUs: Get TV ID List!")

	return tv_id_list;

def main():
	movie_id_list = SearchMovieIDWithStartDateAndEndDate(START_DATE, END_DATE)
	movie_casts_set = SearchCastsWithIDLists("movie", movie_id_list)
	tv_id_list = SearchTvIDWithStartDateAndEndDate(START_DATE, END_DATE)
	tv_casts_set = SearchCastsWithIDLists("tv", tv_id_list)

	result_cast_list = movie_casts_set.intersection(tv_casts_set)
	print("Number of Actors and Actress who are in at least one movie and at least one tv episodes in December 2017 is %d" % len(result_cast_list))

if __name__=="__main__":
	main()


