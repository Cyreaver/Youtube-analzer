# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 13:22:54 2020
Youtube Transcript rip / analyse 
@author: Robbie C
"""

from youtube_transcript_api import YouTubeTranscriptApi
from re import search
import csv

#get the video id form userinput
video_url = input("Please enter the YouTube video URL:")

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
  #  print("Here is the full transcrip:{}".format(transcript_data))
    

#compare to transcrip to keywords/terms\
""" outdated function replaced with dismis2
s_term = "vaccine"

def dismis(term):
    for line in transcript_data:
        if search(term, line['text']):
            x_time = int(line['start'] - 3)
            print('Match found:\n{0}\nat time: {1}\nURL: https://www.youtube.com/watch?v={2}&feature=youtu.be&t={3}\n'.format(line['text'],line['start'],video_id,x_time))
"""

#open a csv containing all the search terms to check 
term_list = []

with open('term_list.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        term_list.append(row)

def dismis2(term):    
    with open('results.csv', 'w', newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(["Video searched: ",video_url])
        writer.writerow([])
        for line in transcript_data:
            for row in term:
                if search(str(row)[2:-2], line['text']):
                    x_time = int(line['start'] - 3)
                    URL = "https://www.youtube.com/watch?v=" +str(video_id) +"&feature=youtu.be&t=" + str(x_time)
                    writer.writerow(["Match found on search term:",str(row)[2:-2]])
                    writer.writerow(["Text",line['text']])
                    writer.writerow(["Timestamp",line['start']])
                    writer.writerow(["URL", URL])
                    writer.writerow([])
                    print('Match found on: {4}\n{0}\nat time: {1}\nURL: {3}\n'.format(line['text'],line['start'],video_id,URL, str(row)[2:-2]))

print("search terms: {}\n ".format(term_list))
dismis2(term_list)