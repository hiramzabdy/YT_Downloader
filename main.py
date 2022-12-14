from pytube import YouTube as yt
from pytube.cli import on_progress
from moviepy.editor import *
import os

def download(video, vid_index, waitlist_id=0):
    waitlist_id = str(waitlist_id)
    video_stream = video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()[vid_index]
    audio_stream = video.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by('abr').desc().first()
    vid_size = str(int((video_stream.filesize/1024/1024)))
    vid_name = video.title
    all_good = [False, False]
    os.system("clear")
    try:
        print("Descargando video... " + vid_name)
        print("Tamaño: " + vid_size + " MB\n")
        video_stream.download(output_path="./media/videos/", filename=waitlist_id + ".mp4")
        all_good[0] = True
    except:
        print("Error al descargar el video")
    try:
        print("Descargando audio...")
        audio_stream.download(output_path="./media/audios/", filename=waitlist_id + ".mp4")
        all_good[1] = True
    except:
        print("Error al descargar el audio")
    if all_good[0] and all_good[1]:
        #Se asegura de que el video termine en la carpeta downloads
        vid_name = vid_name + ".mp4"
        vid_name = "./downloads/" + vid_name
        #Se asegura de exista lel directorio de descarga
        if os.path.isdir("./downloads") != True:
            os.mkdir("./downloads")
        all_good = True
    else:
        print("Lo siento, hubo un error al obtener la información del video")
        all_good = False
    return all_good
    
def get_info(link):
    video = yt(link, on_progress_callback=on_progress)
    video_streams = video.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc()
    return video, video_streams

def decide_res(video, available_streams):
    os.system("clear")
    print(video.title)
    print("Resoluciones Disponibles: ")
    counter = 1
    for stream in available_streams:
        size = str(int((stream.filesize/1024/1024))) + " MB"
        print("#" + str(counter) + ". Res: " + stream.resolution + ", Tamaño: " + size)
        counter = counter + 1
    choice = 0
    
    while choice < 1 or choice >= counter:
        try:
            choice = int(input("¿Qué resolución? (Número de la lista): "))
        except:
            print("Sólo puedes ingresar números")
    choice = choice -1
    return choice

def filter_res():
    qualities = []
    itags = {}
    exists = False
    for stream in video_streams:
        for quality in qualities:
            if stream.resolution == quality:
                exists = True
        if exists == False:
            itags[stream.itag] = stream.resolution
            qualities.append(stream.resolution)
        else:
            exists = False
            
def combine(video,audio,output_name):
    os.system("clear")
    print("Espera un momento mientras convertimos tu video a la mejor calidad :)\n")
    video_clip = VideoFileClip(video)
    audio_clip = AudioFileClip(audio)
    new_audio_clip = CompositeAudioClip([audio_clip])
    video_clip.audio = new_audio_clip
    try:
        video_clip.write_videofile(output_name, codec="libx264")
        print("Video descargado y convertido exitosamente!")
    except:
        print("Hubo un error durante la conversión")
    os.system("rm -rf /media")

def run():
    url = input("Pega el enlace al video: ")
    video, video_streams = get_info(url)
    choice = decide_res(video, video_streams)
    all_good = download(video, choice)
    title = "/downloads/" + video.title + ".mp4"
    if all_good:
        ##Arreglar: No funciona para convertir videos con / en el título
        combine("./media/videos/0.mp4", "./media/audios/0.mp4", title)
    else:
        "Intenta de nuevo"
    

if __name__ == "__main__":
    run()