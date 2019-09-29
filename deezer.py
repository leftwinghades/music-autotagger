import eyed3
import os
import requests

def get_album_id(artist, album):
    # print(artist)
    # print(album)
    search_params = artist.split() + album.split()
    url = SEARCH_URL + "+".join(search_params)
    # print(url)
    resp = requests.get(url)
    data = resp.json()
    results = data['results']
    for search_result in results:
        # print(search_result)
        if search_result["artistName"].lower() == artist.lower() and search_result["collectionName"].lower() == album.lower():
            # print("search result match")
            album_id = search_result["collectionId"]
            break
        else:
            album_id = "Could not find albumId"
    return album_id

def get_track_list(album_id):
    lookup_url = "http://itunes.apple.com/lookup?id={}&entity=song".format(album_id)
    # print(lookup_url)
    resp = requests.get(lookup_url)
    data = resp.json()
    results = data['results'][1:]
    return results

def main():
    albums_list = next(os.walk('.'))[1][1:] # [1:] to ignore .git folder
    for album in albums_list:
        print(album)
        artist_album = album.split(" - ")
        # print(artist_album)
        album_id = get_album_id(artist_album[0], artist_album[1])
        # album_id =  # hard code the albumId
        # print(album_id)
        track_list_json = get_track_list(album_id)
        album_path = "" + album # replace with path of root folder where the albums are
        for file in os.listdir(album_path): # optimise this later
            audiofile = eyed3.load(album_path + "\\" + file)
            for track in track_list_json:
                # print(track)
                if audiofile.tag.disc_num[0] == track["discNumber"] and audiofile.tag.track_num[0] == track["trackNumber"]:
                    # print("match")
                    audiofile.tag.title = track["trackName"]
                    audiofile.tag.artist = track["artistName"]
            audiofile.tag.save()
    print("Done")

SEARCH_URL = "https://itunes.apple.com/search?term="
main()