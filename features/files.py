from features.sorter import sort_folder
from features.bot_feature import BotFeature
import os.path


class Files(BotFeature):
    """
    A feature that allows a user to sort files in a given directory according to files extensions.
    """

    def __init__(self):
        super().__init__({
            "sort": self.sort
        })

    def name(self):
        return "files"

    @staticmethod
    def sort(*args: str) -> str:
        """
        Sorts the folder. Catches system errors when the operating system tries to reach the path.

        :param args:
        :return:
        """
        
        path = " ".join(args)
        if os.path.exists(path):
            sort_folder(path)
            return "Folder is sorted"
        else:
            return "Path does not exist. Try again."