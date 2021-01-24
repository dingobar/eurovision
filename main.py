from musixmatch import Musixmatch
from dataservice import DataService
from countryservice import CountryService
from datacleanupservice import DataCleanUpService
from languagedetectionservice import LanguageDetectionService
from os import environ
import csv


def run():
    musixMatch = Musixmatch(environ["API_KEY"])
    dataService = DataService()
    countryService = CountryService()

    # LANGUAGE
    languagetable = LanguageDetectionService().get_language_table(
        dataService.all_lyrics
    )
    languagetable.name = "language"

    # MUSIXMATCH
    entries = dataService.all_entries
    track_info = musixMatch.label_entries(entries)
    tracktable = DataCleanUpService.make_track_information_table(track_info)

    # COUNTRY
    countries = dataService.all_countries
    country_info = countryService.get_country_info(countries)
    countrytable = DataCleanUpService.make_country_information_table(
        dataService.all_countries, country_info
    )

    # COMBINE
    df = (
        dataService.contestants.join(languagetable, how="left")
        .join(tracktable, how="left")
        .merge(countrytable, how="left", left_on="to_country", right_on="to_country")
    )

    # OUTPUT
    df.to_pickle("contestdata.pickle")
    df.to_feather("contestdata.arrow")
    df.to_csv("contestantdata.csv", quoting=csv.QUOTE_NONNUMERIC)


if __name__ == "__main__":
    run()
