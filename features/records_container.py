from collections import UserDict

import psycopg2

from database.db import session
from database.models import Person, Phone, Note, Tag, Notes2Tags
from features.addressbook_fields import Record
from features.notebook_fields import NoteRecord


DATE_FORMAT = "%d.%m.%Y"


class RecordsContainer(UserDict):
    """
    A class that holds records.
    """

    def __init__(self, save_file):
        super().__init__()
        self.data = RecordsContainer.load_data(save_file) or {}

    @classmethod
    def load_data(cls, filepath: str) -> None | dict:
        """
        Loads records from a database.

        """
        loaded_data = {}
        match filepath:
            case 'address_book.bin':
                try:
                    for person_ in session.query(Person).all():
                        record = Record(person_.name)
                        record.name = person_.name
                        record.birthday = person_.birthday
                        record.address = person_.address
                        record.email = person_.email
                        for phone_ in session.query(Phone).filter(Phone.person_id == person_.id):
                            record.phones.append(phone_.phone)
                        loaded_data[person_.name] = record
                    return loaded_data
                except psycopg2.OperationalError as e:
                    print(f'Unfortunately, {e}')
            case 'notebook.bin':
                try:
                    for note_ in session.query(Note).all():
                        note_record = NoteRecord(note_.title)
                        note_record.name = note_.title
                        note_record.text = note_.text
                        note_record.created = note_.created.date()
                        note_record.note_tags = {}
                        for tag_ in session.query(Tag) \
                            .join(Notes2Tags, Tag.id == Notes2Tags.tag_id) \
                                .filter(Notes2Tags.note_id == note_.id):
                            note_record.note_tags[str(tag_.id)] = tag_.tag
                        # TODO change to dict
                        loaded_data[note_.title] = note_record
                    return loaded_data
                except psycopg2.OperationalError as e:
                    print(f'Unfortunately, {e}')

    @staticmethod
    def backup_data(handler) -> None:
        """
        Saves records to a database.

        :param handler: whose data to save
        """
        match handler.name():
            case 'contacts':
                session.query(Person).delete()
                session.query(Phone).delete()
                session.execute("ALTER SEQUENCE persons_id_seq RESTART WITH 1")
                session.execute("ALTER SEQUENCE phones_id_seq RESTART WITH 1")
                session.commit()

                for rec_id, record in enumerate(handler.data.values(), start=1):
                    db_person = Person(
                        name=record.name,
                        birthday=record.birthday,
                        email=record.email,
                        address=record.address)
                    for rec in record.phones:
                        db_phone = Phone(
                            phone=rec,
                            person_id=rec_id
                        )
                        session.add(db_phone)
                    session.add(db_person)
                session.commit()
            case 'notes':
                session.query(Note).delete()
                session.query(Tag).delete()
                session.query(Notes2Tags).delete()
                session.execute("ALTER SEQUENCE notes_id_seq RESTART WITH 1")
                session.execute("ALTER SEQUENCE tags_id_seq RESTART WITH 1")
                session.execute("ALTER SEQUENCE notes_to_tags_id_seq RESTART WITH 1")
                session.commit()
                for rec_id, note_record in enumerate(handler.data.values(), start=1):
                    db_note = Note(
                        title=note_record.name,
                        text=note_record.text,
                        created=note_record.created)
                    session.add(db_note)
                    session.commit()
                    for key, tag_ in note_record.note_tags.items():
                        db_tag = Tag(tag=tag_)
                        session.add(db_tag)
                        session.commit()
                        # TODO change to dict
                        db_note_to_tag = Notes2Tags(
                            note_id=rec_id,
                            tag_id=key)
                        session.add(db_note_to_tag)
                session.commit()

    def add_record(self, record) -> None:
        """
        Adds a new record.

        :param record:
        :return:
        """
        self.data[record.name] = record

    def remove_record(self, *args: str) -> str:
        """
        Removes a given record. Throws exception if the record does not exist.

        :return: success message
        """

        record_name = " ".join(args)
        if self.record_exists(record_name):
            del self.data[record_name]
            return f"{record_name} was deleted successfully!"
        else:
            raise KeyError(f"{record_name} was not found!")

    def record_exists(self, record_name: str) -> bool:
        """
        Checks if record exists.

        :param record_name: a name of a record
        :return: True is exists False otherwise
        """

        return record_name in self.data

    def show_all(self) -> str:
        """
        Shows all existing records.

        :return: all records as a string
        """

        if self.data:
            result = ""
            for record in self.data.values():
                result += "\n" + str(record) + "\n"
            return result
        else:
            return "You don't have any data yet."

    def search_record(self, needle: str) -> str:
        """
        Searches and returns a record that contains a needle.

        :param needle: what to search
        :return: a result string
        """
        result = list(filter(lambda record: needle in str(record).lower(), self.data.values()))
        if result:
            return "\n".join(["\n" + str(r) for r in result])
        else:
            return "Sorry, couldn't find any records that match the query."
