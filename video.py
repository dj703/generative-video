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
    path = "static/" + filename + ".mp4"
    command = [
        'ffmpeg',
        '-f', 'concat',   
        '-safe', '0',    
        '-i', "clip-output/" + filename + ".txt",      
        '-c', 'copy',     
        path
    ]
    subprocess.run(command)
    return path

# concat_clips("20231129-133649-Memes-baby_boomer")

