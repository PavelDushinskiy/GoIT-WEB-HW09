from typing import Any, List, Dict
from datetime import date
import re

NAME_REGEX = re.compile(r"[a-zA-Zа-яА-Я0-9,.'\w]{2,30}")


class NoteRecord:

    # def __init__(self, title: str, text: str, tags: List[str]) -> None:
    def __init__(self, title: str, text: str = None, created: date = date.today(), note_tags: Dict = None) -> None:
        self.name = title
        self.text = text
        self.created = created
        # TODO fixed created date
        self.note_tags = note_tags

    def __str__(self) -> str:
        return f'{self.name}\n{self.text}\n{", ".join([str(p) for p in self.note_tags.values()])}\n{self.created}'

    def change_title(self, new_title: str) -> None:
        """
        Changes the title of the note.

        :param new_title: a new title
        """

        self.name = new_title

    def change_tags(self, **kwargs: str) -> None:
        """
        Changes the tags of the note.

        :param kwargs: new tags
        """

        self.note_tags.clear()
        self.note_tags = kwargs

    def change_text(self, new_text: str) -> None:
        """
        Changes the text of the note.

        :param new_text: a new text
        """

        self.text = new_text


class Field:

    def __init__(self, value) -> None:
        self._value = None
        self.value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value


class Title(Field):

    @Field.value.setter
    def value(self, title: str):
        if not re.match(NAME_REGEX, title):
            raise ValueError("Title must be between 2 and 30 characters.")
        self._value = title

    def __hash__(self):
        return self.value.__hash__()

    def __eq__(self, obj):
        return self.value == obj

