import subprocess

def create_clip(filename):
    command = [
        'ffmpeg',
        # '-loop', '1',           # Loop the image
        '-i', "image-output/" + filename + ".png",       # Input image file
        '-i', "speech-output/" + filename + ".mp3",       # Input audio file
        # '-c:v', 'libx264',      # Video codec
        # '-c:a', 'aac',          # Audio codec
        # '-strict', 'experimental',
        # '-b:a', '192k',          # Audio bitrate
        # '-t', str(duration),    # Duration of the output video
        # '-shortest',            # Finish encoding when the shortest input stream ends
        "clip-output/" + filename + ".mp4"
    ]
    subprocess.run(command)

def concat_clips(filename): #filename is a text file containing the names of all the clips
    command = [
        'ffmpeg',
        '-f', 'concat',       
        '-i', "clip-output/" + filename + ".txt",      
        '-c', 'copy',     
        "video-output/" + filename + ".mp4"
    ]
    subprocess.run(command)




# create_clip("20231115-110102-Harry_Potter-baby_boomer_2.png","20231115-110102-Harry_Potter-baby_boomer_2.mp3", "20231115-110102-Harry_Potter-baby_boomer_2")
# concat_clips("20231115-141346-MIT_Media_Lab-a_fifth_grader")
