# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 17:22:54 2020
Youtube Transcript rip / analyse 
@author: Robbie C
"""
import urllib.request
import json
import urllib
from youtube_transcript_api import YouTubeTranscriptApi
from re import search
import csv
    
#open a csv containing all the search terms toz check 
term_list = []

with open('term_list.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        term_list.append(row)

#open a csv containing all the search terms toz check 
video_list = []

with open('videos.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        video_list.append(row)
        
def dismis_multi(term):    
  for video in video_list:    
    try:
      video_url = str(video)[2:-2]

      #set the Video id (/watch?v= ID)
      video_id = video_url[32:]

      # retrieve the available transcripts
      transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

      #return data based on transcripts
      for transcript in transcript_list:

          # the Transcript object provides metadata properties
          print("The video id is:{}\n".format(transcript.video_id))

          # fetch the actual transcript data
          transcript_data = transcript.fetch() 

      vid_title, author_name = get_title(video_id)
      
      with open("videos/" + vid_title + '.csv', 'w', newline='') as file: 
          writer = csv.writer(file)
          writer.writerow(["Title: ",vid_title])
          writer.writerow(["Author: ",author_name])
          writer.writerow(["Video URL: ",video_url])
          writer.writerow([])
          x = 0
          for line in transcript_data:
              for row in term:
                  if search(str(row)[2:-2], line['text']):
                      x_time = int(line['start'] - 3)
                      URL = "https://www.youtube.com/watch?v=" +str(video_id) +"&feature=youtu.be&t=" + str(x_time)
                      writer.writerow(["Match found on search term:",str(row)[2:-2]])
                      try:
                        writer.writerow(['Text',transcript_data[x-1]['text'] + " " + transcript_data[x]['text']+ " " + transcript_data[x+1]['text']])       
                      except:
                        writer.writerow(['Longer text',transcript_data[x-1]['text']]) 
                      writer.writerow(["Timestamp",line['start']])
                      writer.writerow(["URL", URL])
                      writer.writerow([])
                      try:
                        print('Match found on: {0}\n{1} {2} {3}\nat time: {4}\nURL: {5}\n'.format(str(row)[2:-2],transcript_data[x-1]['text'],transcript_data[x]['text'],transcript_data[x+1]['text'],line['start'],video_id,URL))
                      except:
                        print('Match found on: {0}\n{1} {2}\nat time: {4}\nURL: {5}\n'.format(str(row)[2:-2],transcript_data[x-1]['text'],transcript_data[x]['text'],['text'],line['start'],video_id,URL))
              x+=1   
                       
      print("Your results have been saved in the following file: {}.csv\n".format(vid_title))
    except:
      print("Error, transcript likely unavilable. Please check the URL")
      with open("videos/failed_videos.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title: ",vid_title])
        writer.writerow(["Author: ",author_name])
        writer.writerow(["Video URL: ",video_url])
        writer.writerow([])

def dismis_single(term):    
    #get the video id form userinput
    video_url = input("Please enter the YouTube video URL: ")

    #set the Video id (/watch?v= ID)
    video_id = video_url[32:]

    # retrieve the available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    #return data based on transcripts
    for transcript in transcript_list:

        # the Transcript object provides metadata properties
        print("The video id is:{}\n".format(transcript.video_id))

        # fetch the actual transcript data
        transcript_data = transcript.fetch() 

    vid_title, author_name = get_title(video_id)
    
    with open("videos/" + vid_title + '.csv', 'w', newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(["Title: ",vid_title])
        writer.writerow(["Author: ",author_name])
        writer.writerow(["Video URL: ",video_url])
        writer.writerow([])
        x = 0
        for line in transcript_data:
          for row in term:
              if search(str(row)[2:-2], line['text']):
                  x_time = int(line['start'] - 3)
                  URL = "https://www.youtube.com/watch?v=" +str(video_id) +"&feature=youtu.be&t=" + str(x_time)
                  writer.writerow(["Match found on search term:",str(row)[2:-2]])
                  try:
                    writer.writerow(['Text',transcript_data[x-1]['text'] + " " + transcript_data[x]['text']+ " " + transcript_data[x+1]['text']])              
                  except:
                    writer.writerow(['Longer text',transcript_data[x-1]['text']]) 
                  writer.writerow(["Timestamp",line['start']])
                  writer.writerow(["URL", URL])
                  writer.writerow([])
                  try:
                    print('Match found on: {0}\n{1} {2} {3}\nat time: {4}\nURL: {5}\n'.format(str(row)[2:-2],transcript_data[x-1]['text'],transcript_data[x]['text'],transcript_data[x+1]['text'],line['start'],video_id,URL))
                  except:
                     print('Match found on: {0}\n{1} {2}\nat time: {4}\nURL: {5}\n'.format(str(row)[2:-2],transcript_data[x-1]['text'],transcript_data[x]['text'],['text'],line['start'],video_id,URL))
          x+=1
                    
        print("Your results have been saved in the following file: {}.csv\n".format(vid_title))
    

def get_title(vid_id):    
  #code to retreive video title    
  params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % vid_id}
  url = "https://www.youtube.com/oembed"
  query_string = urllib.parse.urlencode(params)
  url = url + "?" + query_string

  with urllib.request.urlopen(url) as response:
      response_text = response.read()
      data = json.loads(response_text.decode())
      
      vid_title = data['title']
      author_name = data['author_name']
      print("video title: " + vid_title + "\n")
      return vid_title, author_name

#running the prog. Print the search terms 
print("search terms: {}\n ".format(term_list))
i = 0
#Check if the user wants single entry input or multiple 
while i <  1: 
  choice = str(input("Would you like to check a single video or multiple? "))

  if choice == "single": 
    try:
      dismis_single(term_list)
      i=1
      exit
    except:
        print("Error, transcript likely unavilable. Please check the URL")

  if choice == "multiple":
    dismis_multi(term_list)
    i=1
    exit
  
  else: 
    print("please use either 'single' or 'multiple' as your response")
