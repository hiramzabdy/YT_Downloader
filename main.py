from pytube import YouTube as yt
from pytube.cli import on_progress
from moviepy.editor import *
import os
import shutil

def download_non_progressive(chosen_stream,video,waitlist_id=0):
    #Waitlist has no uses for now. It will when enabling simoultaneous downloads feature.
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
    #Downloads progressive stream. Max res 720p. No convertion.
    vid_size = str(int((chosen_stream.filesize/1024/1024)))
    vid_name = chosen_stream.title
    try: 
        os.system("clear")
        print("Descargando video... " + vid_name)
        print("Tamaño: " + vid_size + " MB\n")
        chosen_stream.download(output_path="./downloads")
        print("Video descargado exitosamente!\n")
        
    except:
        print("Ocurrió un error durante la descarga")

def download_audio(chosen_stream):
    #Downloads audio stream
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
    #Returns the vid as an object and adds a progress bar to it.
    try:
        video = yt(link, on_progress_callback=on_progress)
        return video
    except Exception as e:
        print("No sé pudo obtener información del link")
        return False

def decide_res(video, downloadable_streams):
    #Asks the user for resolution to download.
    os.system("clear")
    
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
    #Gets the video resolution and chooses the best quality (codecs) for each resolution, returns no duplicates.
    video_streams_adaptive = video.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc()
    video_streams_progressive = video.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
    qualities = []
    itags = {}
    exists = False
    
    for stream in video_streams_adaptive: #Returns the best adative stream for each quality and its itag.
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

    for stream in video_streams_progressive: #As there are only two progressive streams (720p and 360p) or less, there are no duplicates.
        resolution = stream.resolution.replace("p","")
        resolution = int(resolution)
        itags[stream.resolution] = stream.itag
        qualities.append(stream.resolution)
    audio_stream = video.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by('abr').desc().first()
    itags["Audio"] = audio_stream.itag
    qualities.append("Audio")

    #Selects streams and appends them to list
    downloadable_streams = []
    for quality in qualities:
        stream = video.streams.get_by_itag(itags[quality])
        downloadable_streams.append(stream)
    return downloadable_streams
            
def combine(video,audio,output_name):
    #Merges audio and video. Deletes working directory when finished.
    os.system("clear")
    video_clip = VideoFileClip(video)
    audio_clip = AudioFileClip(audio)
    new_audio_clip = CompositeAudioClip([audio_clip])
    video_clip.audio = new_audio_clip
    try:
        print("Convirtiendo audio y video... en progreso...\n")
        video_clip.write_videofile(output_name, codec="libx264")
        os.system("clear")
        print("Video descargado y convertido exitosamente!")
    except:
        print("Hubo un error durante la conversión")

def normalize(title):
    #Gets rid of the slash (/) signs that might cause errors in the program.
    new_title = ""
    for letter in title:
        if letter == "/":
            new_title = new_title + "-"
        else:
            new_title = new_title + letter
    return new_title

def get_urls_from_file(filename="links.txt"):
    #Gets each line as a link.
    try:
        links = []
        with open(filename) as file:
            links = file.readlines()
        return links
    except Exception as ex:
        print("Hubo un problema al extraer los links del archivo <links.txtx>")
        print(ex)

def decide_mode():
    #Decides which mode the program should work on. Can add as many modes as needed.
    mode = 0
    while mode < 1 or mode > 3:
        try:
            os.system("clear")
            mode = int(input("¿Qué modo de descarga?\n\n#1: Normal (Pegas el enlace al video y seleccionas la calidad)\n#2: Links (Toma los enlaces del archivo <links.txt>)\n#3: Links audio (Toma los enlaces del archivo <links.txt>) \n\n Respuesta: "))
        except:
            print("Retrying")
    return mode

def run_one_link():
    os.system("clear")
    url = input("Pega el enlace al video: ")
    video = get_info(url)
    if video != False:
        streams = filter_res(video)
        chosen_stream = decide_res(video, streams)
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
                print("\nImposible convertir. No se descargó el audio o el video correctamente")

def run_on_links():
    #Gets the links from the links file. Downloads each in the best quality available. If res > 720p, conversion is needed to merge audio and video.
    links = get_urls_from_file()
    for link in links:
        os.system("clear")
        video = get_info(link)
        if video != False:
            streams = filter_res(video)
            chosen_stream = streams[0] #Gets the first stream, which has the largest res and highest quality.
            all_good = False
            if chosen_stream.is_progressive: #Max 720p res video. No conversion needed.
                download_progressive(chosen_stream)
            else: #Downloads audio and video and merges them.
                all_good = download_non_progressive(chosen_stream, video)
                title = normalize(video.title) #Replaces / for -, so next steps run properly.
                title = "./downloads/" + title + ".mp4"
                if all_good:
                    combine("./media/videos/0.mp4", "./media/audios/0.mp4", title)
                else:
                    print("\nError al descargar audio o video")
        else:
            print("No se pudo obtener información del link proporcionado")

def run_on_links_audio():
    #Gets the links from the links file. Downloads each as an audio in the best quality available.
    links = get_urls_from_file()
    for link in links:
        os.system("clear")
        video = get_info(link)
        if video != False:
            chosen_stream = video.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by('abr').desc().first()
            download_audio(chosen_stream)
        else:
            print("No se pudo obtener información del link proporcionado")
    os.system("clear")
    print("Proceso finalizado!")

def run():
    mode = decide_mode()
    if mode == 1:
        run_one_link()
    elif mode == 2:
        run_on_links()
    elif mode == 3:
        run_on_links_audio()
    shutil.rmtree("./media/", ignore_errors=False, onerror=None)

if __name__ == "__main__":
    run()