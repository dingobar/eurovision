import requests
from requests.models import HTTPError
from datacleanupservice import DataCleanUpService


class CountryService:
    def __init__(self):
        self.baseurl = "https://restcountries.eu/rest/v2/"

    def get_country_info(self, code):
        return self.__get_country_information_by_name(code)

    def __get_country_information_by_name(self, names):
        names = DataCleanUpService.simplify_country_names(names)
        codes = []
        for name in names:
            r = requests.get(self.baseurl + "name/" + name)
            try:
                r.raise_for_status()
            except HTTPError as e:
                print(f"{repr(e)}: Country {name} was not found.")
            codes.append(r.json())
        return codes
