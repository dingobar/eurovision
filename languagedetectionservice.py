import pandas as pd
from google.cloud import translate_v2 as translate
from itertools import zip_longest

translate_client = translate.Client()


class LanguageDetectionService:
    def __detect_language(self, texts):
        """Detects the text's language."""

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        results = []
        for text in texts:
            text = text[0 : min(len(text), 1000)]
            results.append(translate_client.detect_language(text).get("language"))

        return results

    def get_language_table(self, texts):
        return pd.Series(self.__detect_language(texts)).to_frame()
