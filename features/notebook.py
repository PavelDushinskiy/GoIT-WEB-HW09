import datetime

from features.bot_feature import BotFeature
from features.records_container import RecordsContainer
from features.notebook_fields import NoteRecord
from database.db import session
from database.models import Tag
from datetime import date


class Notebook(BotFeature):
    """
    An app feature that helps users to manage their notes.
    """

    def __init__(self, save_file: str):
        self.save_file = save_file
        self.data = RecordsContainer(save_file)

        super().__init__({
            "make": self.make_note,
            "change": self.change_note,
            "remove": self.data.remove_record,
            "show": self.data.show_all,
            "search": self.data.search_record
        })

    @staticmethod
    def name():
        return "notes"

    def make_note(self) -> str:
        """
        Creates a new note. Raises exception if note with a given title already exists.

        :return: success message
        """

        title = input('Enter the title: ').strip()

        if self.data.record_exists(title):
            raise f"Note {title} already exists! Try another name."

        text = input('Enter the text: ')
        list_note_tags = input('Enter the tags: ').strip().split()
        next_key = session.query(Tag).count() + 1
        new_note_tags = {x + next_key: y for x, y in zip(range(len(list_note_tags)), list_note_tags)}
        # TODO example change list to dict
        note = NoteRecord(title, text, date.today(), new_note_tags)
        self.data.add_record(note)
        return f"Note {title} was created successfully!"

    def change_note(self, *args: str) -> str:
        """
        Changes existing notes. Raises exception if a note that the user wants to change does not exist.

        :param args: note title
        :return: success message
        """

        title = " ".join(args)
        if self.data.record_exists(title):
            note_to_change = self.data[title]
            while True:
                to_change = input("What do you want to change? Type title, tags or text: ")
                if to_change.lower() not in ["title", "tags", "text"]:
                    print("Unknown command")
                    continue
                elif to_change.lower() == "title":
                    new_title = input("Enter a new title: ")
                    note_to_change.change_title(new_title)
                    self.data.add_record(note_to_change)
                    self.data.remove_record(title)
                elif to_change.lower() == "tags":
                    new_tags = input("Enter new tags: ")
                    note_to_change.change_tags(new_tags)
                    # TODO change in dict
                elif to_change.lower() == "text":
                    new_text = input("Enter new text here: ")
                    note_to_change.change_text(new_text)

                to_continue = input("Do you want to change something else in this note? Enter y or n: ")
                if to_continue.lower() not in ["y", "n"]:
                    print("Enter y or n.")
                    continue
                elif to_continue.lower() == "y":
                    continue
                else:
                    return "The note was changed successfully!"
        else:
            raise KeyError("Note with this title doesn't exist.")
