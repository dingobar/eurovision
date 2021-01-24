import requests


class Musixmatch:
    def __init__(self, apikey):
        self.baseurl = r"https://api.musixmatch.com/ws/1.1/"
        self.apikey = apikey

    def label_entries(self, entries):
        return [self.label_entry(e) for e in entries]

    def label_entry(self, entry):
        return self.__call_musixmatch_api(entry)

    def __call_musixmatch_api(self, entry):
        params = {
            "apikey": self.apikey,
            "q_artist": entry[0],
            "q_track": entry[1],
        }
        r = requests.get(self.baseurl + "matcher.track.get", params)
        r.raise_for_status()
        result = r.json()["message"]

        if result.get("header", {})["status_code"] != 200:
            print(f"Song {params['q_artist']} . {params['q_track']}  not found!!!")
        return r.json()
