import requests
from bs4 import BeautifulSoup
import os
from clint.textui import progress

a_arr = []
number_of_videos = 3
download_dir = "dnld/"
search_domain_name = "https://mixkit.co/"
asset_domain_name = "https://assets.mixkit.co/"

search_name = search_domain_name+"free-stock-video/"
preview_name = asset_domain_name+"videos/preview"
original_name = asset_domain_name+"videos/download"
page_part = "/?page="

large = "-large"
small = "-small"
extention = ".mp4"

def download_file(url,filepath):
	print(filepath)
	try:
		r = requests.get(url, stream=True)
		if os.path.isfile(filepath) == False:
			with open(filepath, 'wb') as f:
			    total_length = int(r.headers.get('content-length'))
			    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
			        if chunk:
			            f.write(chunk)
			            f.flush()
	except Exception as e:
		print("problem while downloading...",e)


def fetch_a_tags(page_no):
	if number_of_videos > len(a_arr):
		url = search_name+search_topic+page_part+str(page_no)
		print(url)
		x = requests.get(url)
		soup = BeautifulSoup(x.content, 'lxml')
		videos_a = soup.findAll('a', attrs = {'class':'item-grid-video-player__overlay-link'})
		a_arr.extend(videos_a)
		page_no = page_no+1
		fetch_a_tags(page_no)

print("***************************************")
while True:
	search_topic = input("Enter subject to search: ")
	if search_topic == "" or search_topic == " ":
		print("please enter search topic: ")
		continue
	else:
		break

print("***************************************")
while True:
	try:
		type_of_video = int(input("Enter type of videos (1:small 2:large 3:big 4:all) "))
		if type_of_video not in [1,2,3,4]:
			print("please enter type of videos between 1,2,3,4")
			continue
		else:
			break
	except:
		print("please enter type of videos between 1,2,3,4")
		continue

print("***************************************")
while True:
	try:
		number_of_videos = int(input("Enter number of videos: "))
		if number_of_videos == "" or number_of_videos == " ":
			print("please enter number of videos:")
			continue
		else:
			break
	except:
		print("please enter number of videos")
		continue

if not os.path.exists(download_dir):
	os.mkdir(download_dir)

fetch_a_tags(1)

counter = 1
for a in a_arr:
	print()
	part_link = a.get("href").replace("free-stock-video/","mixkit-").rstrip("/")
	temp_arr = part_link.split("-")
	video_number = temp_arr[len(temp_arr)-1]
	preview_link = preview_name+part_link
	preview_large_link = preview_link + large + extention
	preview_small_link = preview_link + small + extention
	original_link = original_name + part_link + extention
	
	dir_name = download_dir+video_number

	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
	else:
		print("folder already exists")

	if type_of_video in [1,4]:
		print("downloading small video...")
		print(preview_small_link)
		filepath = dir_name+"/"+video_number+small+extention
		download_file(preview_small_link,filepath)
	
	if type_of_video in [2,4]:
		print("downloading large video...")
		print(preview_large_link)
		filepath = dir_name+"/"+video_number+large+extention
		download_file(preview_large_link,filepath)

	if type_of_video in [3,4]:
		print("downloading original video...")
		print(original_link)
		filepath = dir_name+"/"+video_number+extention
		download_file(original_link,filepath)

	if counter >= number_of_videos:
		break

	counter = counter + 1



