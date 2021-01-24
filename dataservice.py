import pandas as pd
from pathlib import Path


class DataService:
    def __init__(self, limit=0):
        self.datapath = Path("data")
        self.contestants = self.___read_contestants()
        self.votes = self.___read_votes()

        if limit:
            self.contestants = self.contestants.head(limit)
            self.votes = self.votes.head(limit)

    def ___read_contestants(self):
        return pd.read_csv(self.datapath / "contestants.csv")

    def ___read_votes(self):
        return pd.read_csv(self.datapath / "votes.csv")

    @property
    def all_entries(self):
        return list(self.contestants[["performer", "song"]].values)

    @property
    def all_countries(self):
        return list(self.contestants["to_country"].unique())

    @property
    def all_lyrics(self):
        return [l.replace(r"\n", " ") for l in list(self.contestants["lyrics"])]
