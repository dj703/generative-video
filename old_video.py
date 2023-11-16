import ffmpeg

def create_clip(image, audio, filename):
    #  ffmpeg.input("image-output/" + image, format='mp3').output(
    #     filename + ".mp4", 
    #     vf='fps=25',
    #     acodec='aac',
    #     audio_bitrate='192k'
    # ).run(input="speech-output/" + audio, cmd='ffmpeg', overwrite_output=True, quiet=True)
    input_image = ffmpeg.input("image-output/" + image, loop=1) #ffmpeg.input('background.png', t=60, framerate=98, loop=1).output('output.mp4').run()
    input_audio = ffmpeg.input("speech-output/" + audio)

    (
        ffmpeg
        .concat(input_image, input_audio, v=1, a=1)
        .output("output.mp4")
        .run(overwrite_output=True)
    )


create_clip("20231115-110102-Harry_Potter-baby_boomer_1.png","20231115-110102-Harry_Potter-baby_boomer_1.mp3", "20231115-110102-Harry_Potter-baby_boomer_1")