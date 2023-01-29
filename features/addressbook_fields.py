from re import match
import datetime
from typing import Match

DATE_FORMAT = "%d.%m.%Y"


class Field:
    """
    The base class for the fields of an addressbook.
    """

    def __init__(self, value):
        self._value = None
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __hash__(self) -> int:
        return self.value.__hash__()

    def __eq__(self, o: object) -> bool:
        return self.value == o

    def __contains__(self, needle):
        return True if needle in self.value else False

    @staticmethod
    def verify_value(value):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.verify_value(value)
        self._value = value


class Name(Field):
    """
    A name of a person in an addressbook.
    """

    def verify_value(self, value: str) -> None:
        """
        Verifies that name is not smaller than 2 characters long and not bigger than 30 characters. Raises exception if
        the name is too short or too long.

        :param value: a name to check
        """

        if len(value) < 2 or len(value) > 30:
            raise ValueError("Name must be between 2 and 30 characters.")


class Phone(Field):
    """
    A phone number of a person in an address book.
    """

    @classmethod
    def is_valid(cls, value: str) -> None | Match[str]:
        return match(r"(\+?\d{12}|\d{10})", value)

    def verify_value(self, value: str) -> None:
        """
        Checks if the phone is given in a valid format. Raises exception if the phone doesn't match one of the formats.

        :param value: phone number
        """

        if not Phone.is_valid(value):
            raise ValueError("Invalid phone format. Try +123456789012 or 1234567890.")


class Birthday(Field):
    """
    Person's birthday date.
    """

    def verify_value(self, value: datetime.date) -> None:
        """
        Checks if the birthdate is not in the future. Raises exception if the date is in the future.

        :param value: birthdate
        """

        if value > datetime.datetime.now().date():
            raise ValueError("Birthday can't be in future.")


class Email(Field):
    """
    Person's email.
    """

    @classmethod
    def is_valid(cls, value: str) -> None | Match[str]:
        """
        Checks if the email is valid.

        :param value: email to check
        """

        return match(r"[a-zA-Z][a-zA-Z_.0-9]+@[a-zA-Z_]+?\.[a-zA-Z]{2,}", value)


class Record:
    """
    A record about a person in an address book. Name field is compulsory, while other fields are optional and can
    be omitted.
    """

    def __init__(self, name: str):
        if not name:
            raise ValueError("The record must have a name.")
        self.name = name
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def add_phone(self, phone: str) -> None:
        """
        Adds a phone to the record. Raises exception if the phone is in a wrong format.

        :param phone: a phone number
        """

        if Phone.is_valid(phone):
            self.phones.append(phone)
        else:
            raise ValueError(f"Phone must be in format +380XXXXXXXXX/380XXXXXXXXX/0XXXXXXXXX")

    def count_days_to_birthday(self) -> str:
        """
        Counts the days left to the birthdate of the given person.

        :return: a number of days left
        """

        today = datetime.datetime.now().date()
        this_years_birthday = self.birthday.value.replace(year=today.year)

        if today < this_years_birthday:
            difference = this_years_birthday - today
            return difference.days
        if today == this_years_birthday:
            return "0"
        else:
            next_years_birthday = this_years_birthday.replace(year=this_years_birthday.year + 1)
            difference = next_years_birthday - today
            return difference.days

    def add_birthday(self, birthday: str) -> None:
        """
        Adds a birthdate to the record. Raises exception if birthdate is in a wrong format.

        :param birthday: datetime object
        """
        try:
            birthday_date = datetime.datetime.strptime(birthday, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(f"{birthday} does not march format '%d.%m.%Y'")

        self.birthday = birthday

    def add_email(self, email: str) -> None:
        """
        Adds email to the record. Raises exception if an email is in a wrong format.

        :param email: email to add
        """

        if Email.is_valid(email):
            self.email = email
        else:
            raise ValueError("Your email seems to be invalid.")

    def add_address(self, *args: str) -> None:
        """
        Adds address to the record.

        :param args: contact's address
        """

        self.address = " ".join(args)

    def __str__(self):
        phones = ", ".join(map(lambda phone: str(phone), self.phones)) if self.phones else "no saved phones"
        return f"Name: {self.name}, phones: {phones}, birthday: {self.birthday}, email: {self.email}, " \
               f"address: {self.address}"
