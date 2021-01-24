from os import stat
import pandas as pd


class DataCleanUpService:
    @staticmethod
    def simplify_country_names(countries):
        mappings = {
            "Yugoslavia": "Serbia",
            "Bosnia & Herzegovina": "Bosnia",
            "North Macedonia": "Macedonia",
            "Serbia & Montenegro": "Serbia",
        }
        s = pd.Series(countries)
        s = s.map(mappings).fillna(s)
        return s.to_list()

    @staticmethod
    def make_country_information_table(countries, countryinfo):
        zipped = zip(countries, countryinfo)
        flatlists = []
        for c, ci in zipped:
            ci = ci[0]
            selected = {
                "to_country": c,
                "callingCode": ci.get("callingCodes", [])[0],
                "region": ci.get("region"),
                "subregion": ci.get("subregion"),
                "population": ci.get("population"),
                "latitude": ci.get("latlng")[0],
                "lognitude": ci.get("latlng")[1],
                "area": ci.get("area"),
                "gini": ci.get("gini"),
                "timezones": ci.get("timezones")[0],
                "boarders": ci.get("borders"),
                "alliances": [a.get("name") for a in ci.get("regionalBlocs", [])],
            }
            flatlists.append(selected)
        return pd.DataFrame(flatlists)

    @staticmethod
    def make_track_information_table(trackinfo):
        flatlists = []
        for ti in trackinfo:
            ti = ti.get("message", {}).get("body", {})
            if not ti:
                flatlists.append({
                    "albumName": None,
                    "trackName": None,
                    "trackRatingMusixmatch": None,
                    "instrumental": None,
                    "explicit": None,
                    "genres": []
                })
                continue
            ti = ti.get("track")
            selected = {
                "albumName": ti.get("album_name"),
                "trackName": ti.get("track_name"),
                "trackRatingMusixmatch": ti.get("track_rating"),
                "instrumental": bool(ti.get("instrumental", 0)),
                "explicit": bool(ti.get("explicit")),
                "genres": [
                    a.get("music_genre", {}).get("music_genre_name")
                    for a in ti.get("primary_genres", {}).get("music_genre_list", [])
                ],
            }
            flatlists.append(selected)
        return pd.DataFrame(flatlists)
