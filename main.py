from pytube import YouTube as yt
from moviepy.editor import *
import os

def download(link):
    video = yt(link)
    video_stream = video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
    audio_stream = video.streams.filter(only_audio=True,file_extension="mp4").order_by('abr').desc().first()
    vid_size = video_stream.filesize / 1024 / 1024
    vid_size = str(int(vid_size)) 
    vid_name = video.title
    all_good = [False, False]
    try:
        print("Descargando video...")
        print("Tamaño: " + vid_size + " MB")
        video_stream.download(output_path="./media/", filename="video.mp4")
        all_good[0] = True
    except:
        print("Error al descargar el video")
    try:
        print("Descargando audio...")
        audio_stream.download(output_path="./media/", filename="audio.mp3")
        all_good[1] = True
    except:
        print("Error al descargar el audio")
    
    if all_good[0] and all_good[1]:
        vid_name = vid_name + ".mp4"
        vid_name = "./downloads/" + vid_name
        if os.path.isdir("./downloads") != True:
            os.mkdir("./downloads")
        combine("./media/video.mp4", "./media/audio.mp3", vid_name)
        
        
def combine(video,audio,output_name):
    video_clip = VideoFileClip(video)
    audio_clip = AudioFileClip(audio)
    new_audio_clip = CompositeAudioClip([audio_clip])
    video_clip.audio = new_audio_clip
    video_clip.write_videofile(output_name, codec="mpeg4")
    
def run():
    url = input("Pega el enlace al video: ")
    download(url)

if __name__ == "__main__":
    run()