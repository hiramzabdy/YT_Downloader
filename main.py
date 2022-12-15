from pytube import YouTube as yt
from pytube.cli import on_progress
from moviepy.editor import *
import os
import shutil

def download_non_progressive(chosen_stream,video,waitlist_id=0):
    waitlist_id = str(waitlist_id)
    audio_stream = video.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by('abr').desc().first()
    
    vid_size = str(int((chosen_stream.filesize/1024/1024)))
    vid_name = chosen_stream.title
    all_good = [False, False]
    os.system("clear")
    try:
        print("Descargando video... " + vid_name)
        print("Tamaño: " + vid_size + " MB\n")
        chosen_stream.download(output_path="./media/videos/", filename=waitlist_id + ".mp4")
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
    
def download_progressive(chosen_stream):
    vid_size = str(int((chosen_stream.filesize/1024/1024)))
    vid_name = chosen_stream.title
    try: 
        os.system("clear")
        print("Descargando video... " + vid_name)
        print("Tamaño: " + vid_size + " MB\n")
        chosen_stream.download(output_path="./downloads")
        print("Video descargado exitosamente!")
    except:
        print("Ocurrió un error durante la descarga")

def download_audio(chosen_stream):
    aud_size = str(int((chosen_stream.filesize/1024/1024)))
    aud_name = chosen_stream.title
    try: 
        os.system("clear")
        print("Descargando audio... " + aud_name)
        print("Tamaño: " + aud_size + " MB\n")
        chosen_stream.download(output_path="./downloads/audios", filename = aud_name + ".m4a")
        print("Audio descargado exitosamente!")
    except:
        print("Ocurrió un error durante la descarga")

def get_info(link):
    video = yt(link, on_progress_callback=on_progress)
    return video

def decide_res(video, qualities, itags):
    os.system("clear")
    downloadable_streams = []
    
    for quality in qualities:
        tag = itags[quality]
        stream = video.streams.get_by_itag(tag)
        downloadable_streams.append(stream)
        
    def print_res(downloadable_streams):
        i = 1
        for stream in downloadable_streams:
            size = str(int((stream.filesize/1024/1024))) + " MB"
            if stream.is_progressive:
                print("#" + str(i) + ". Res: " + stream.resolution + ", Tamaño: " + size + " (No requiere conversión)")
            elif stream.type != "audio":
                print("#" + str(i) + ". Res: " + stream.resolution + ", Tamaño: " + size)
            elif stream.type == "audio":
                print("#" + str(i) + ". Res: Audio" + ", Tamaño: " + size + " (Descarga sólo el audio)")
            i = i +1
    
    choice = 0
    
    while choice < 1 or choice > len(downloadable_streams):
        try:
            os.system("clear")
            print(video.title)
            print("\nResoluciones Disponibles:\n")
            print_res(downloadable_streams)
            choice = int(input("\n¿Qué resolución? (Número de la lista): "))
        except:
            print("Sólo puedes ingresar números")
    choice = choice -1
    chosen_stream = downloadable_streams[choice]
    return chosen_stream

def filter_res(video):
    video_streams_av01 = video.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc()
    qualities = []
    itags = {}
    exists = False
    for stream in video_streams_av01:
        resolution = stream.resolution.replace("p","")
        resolution = int(resolution)
        if resolution >= 1080:
            for quality in qualities:
                if stream.resolution == quality:
                    exists = True
            if exists == False:
                itags[stream.resolution] = stream.itag
                qualities.append(stream.resolution)
            else:
                exists = False
    video_streams_progressive = video.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
    for stream in video_streams_progressive:
        resolution = stream.resolution.replace("p","")
        resolution = int(resolution)
        itags[stream.resolution] = stream.itag
        qualities.append(stream.resolution)
    audio_stream = video.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()
    itags["Audio"] = audio_stream.itag
    qualities.append("Audio")
    
    return qualities, itags
            
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
    #Esta parte remueve el directorio de trabajo, lo cual no afecta su funcionamiento ahora, pero lo hará cuando agrege la función de descargar varios videos en una ejecución
    shutil.rmtree("./media/", ignore_errors=False, onerror=None)

def normalize(title):
    new_title = ""
    for letter in title:
        if letter != "/":
            new_title = new_title + letter
        else:
            new_title = new_title + "-"
    return new_title

def run():
    os.system("clear")
    url = input("Pega el enlace al video: ")
    video = get_info(url)
    qualities, itags = filter_res(video)
    chosen_stream = decide_res(video, qualities, itags)
    all_good = False
    if chosen_stream.is_progressive:
        download_progressive(chosen_stream)
    elif chosen_stream.type == "audio":    
        download_audio(chosen_stream)
    else:
        all_good = download_non_progressive(chosen_stream, video)
        title = normalize(video.title)
        title = "./downloads/" + title + ".mp4"
        if all_good:
            combine("./media/videos/0.mp4", "./media/audios/0.mp4", title)
        else:
            "\nIntenta de nuevo"
    

if __name__ == "__main__":
    run()