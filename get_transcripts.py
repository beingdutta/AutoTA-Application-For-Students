import pandas as pd 
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract

ids = ['oZgbwa8lvDE', 'VRcixOuG-TU']  # Example video IDs
count = 0
for i in range(len(ids)):
    #url = df['video_url'][0]
    try:
        id = ids[i]

        transcript = YouTubeTranscriptApi.get_transcript(id)
        #print(transcript[0])
        file_df = pd.DataFrame()
        for j in range(len(transcript)):
            file_df = file_df._append([dict(transcript[j])])
        file_df.reset_index()
        transcript_filename = str(id)+".csv"
        file_path = "/Users/sourjyadip/Desktop/autota/transcripts/" + transcript_filename
        file_df.to_csv(file_path)
        print(i, " done")
    except:
        count += 1

print("number of skipped videos: ", count)