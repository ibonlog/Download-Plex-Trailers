import os
import sys
import yt_dlp
from googleapiclient.discovery import build
from dotenv import load_dotenv


"""
Downloads a video from the given URL and saves it to the specified target file path.

Args:
    url (str): The URL of the video to download.
    target_file (str): The file path to save the downloaded video.

Returns:
    None
"""
def download_video(url, target_file):
    with yt_dlp.YoutubeDL({'quiet': True, 'format': 'mp4/best','outtmpl': target_file}) as ydl:
        ydl.download(url)



"""
Searches for a video on youtube using the given query and returns the id of the first matching video. 
The function filters out results that contain certain words in either the channel title or video title.
Args:
    query (str): The search query to be used.
Returns:
    str: The id of the first matching video.
"""
def search_video(query):
    youtube = build('youtube','v3',developerKey = YOUTUBE_API_KEY)
    results = youtube.search().list(q = query, type ='video', part = "id, snippet", maxResults = 10, regionCode = "ES").execute().get("items", [])

    notin_channel_words = ["netflix", "spanish", "latino", "doblaje"]
    notin_title_words = ["latino","subtitulado","subtitulos","subtítulos", "resumen", "explica", "doblado"]
    first_result = ""
    for result in results:
        if first_result == "":
            first_result = result["id"]["videoId"]
        find_word = False
        for word in notin_channel_words:
            if word in result["snippet"]["channelTitle"].lower():
                find_word = True
                break
        
        if not find_word:
            for word in notin_title_words:
                if word in result["snippet"]["title"].lower():
                    find_word = True
                    break

        if not find_word:
            return result["id"]["videoId"]
        
    return first_result



"""
Get the left part of a string up to the last occurrence of a separator character.

Args:
    string (str): The input string.
    separator (str): The separator character.

Returns:
    str: The left part of the string up to the last occurrence of the separator character.
"""
def get_left_string(string, separator):
    return string[:string.rfind(separator)]



"""
Return the right part of a given string that occurs after the last occurrence of a separator.

Args:
    string (str): The input string.
    separator (str): The separator character.

Returns:
    str: the right part of the input string after the last occurrence of the given separator
"""
def get_right_string(string, separator):
    return string[string.rfind(separator)+1:]




"""
Takes in a path and returns a list of dictionaries containing information about 
specific files and directories. The information includes the type of media, the 
name of the media, the path of the media, and the path of a possible trailer for 
the media. If a file ends with ".mp4", ".mkv", or ".avi", the function assumes 
the file is a film and adds information about it to the list. If the word 
"season" or "temporada" is in the file name, the function assumes the file is a 
television show and adds information about it to the list. 

:param path: The path to search for files and directories.
:type path: str
:return: A list of dictionaries containing information about specific files and 
    directories.
:rtype: list(dict)
"""
def get_dir_and_files(path_search):
    dir_and_files = []
    paths = []
    video_extensions = ['.mp4', '.avi', '.mkv']

    for root, dirs, files in os.walk(path_search):
        
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()

            if "season" in root.lower() or "temporada" in root.lower() or "trailers" in root.lower():

                if file_extension in video_extensions and "trailers" not in root.lower():

                    path_filmorshow = get_left_string(root,os.sep)
                    
                    target_possible = os.path.join(get_left_string(root,os.sep), "Trailers/Trailer 1.mp4")
                    if not os.path.exists(target_possible) and path_filmorshow not in paths:
                        paths.append(path_filmorshow)
                        dir_and_files.append({"type": "show", "search": get_right_string(get_left_string(root,os.sep),os.sep), "path": path_filmorshow, "target": target_possible})

            elif file_extension in video_extensions and "trailer" not in file.lower():

                path_filmorshow = root

                target_possible = os.path.join(root, get_left_string(file, ".") + "-trailer.mp4")
                if not "trailer" in file.lower() and not os.path.exists(target_possible) and path_filmorshow not in paths:
                    paths.append(path_filmorshow)
                    dir_and_files.append({"type": "film", "search": get_right_string(root,os.sep), "path": path_filmorshow, "target": target_possible})
          
    return dir_and_files



load_dotenv()

if not len(sys.argv) == 3:
    print("Uso: python " + sys.argv[0] + " <search_path> <downloads_limit>")
    exit()

if not os.getenv('YOUTUBE_API_KEY') == None and not os.getenv('YOUTUBE_API_KEY') == "":
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
else:
    print("No se ha encontrado la variable de entorno YOUTUBE_API_KEY")
    exit()



# 0. obtener los parametros de entrada y leemos el fichero de variables de entorno
search_path = sys.argv[1]
downloads_limit = int(sys.argv[2])



# 1. obtener los nombres de las peliculas de los ficheros de las carpetas recursivamente
trailers_to_download = get_dir_and_files(search_path)

if not trailers_to_download:
    print("No se han encontrado peliculas o series para descargar los trailers")
    exit()
else:
    print("Se han encontrado " + str(len(trailers_to_download)) + " peliculas o series para descargar los trailers")


count_downloads = 0
# 2. buscar en youtube el trailer de cada pelicula y descargarlo
for trailer in trailers_to_download:

    if count_downloads < downloads_limit:
        if trailer["type"] == "show":
            search_string = trailer["search"] + " trailer serie en castellano"
        else:
            search_string = trailer["search"] + " trailer en castellano"

        video_id = search_video(search_string)
        if video_id:
            download_video('https://www.youtube.com/watch?v=' + video_id, trailer["target"])
            count_downloads += 1
            print("Trailer descargado para: " + trailer["search"])
        else:
            print("No se ha encontrado trailer para: " + trailer["search"])

