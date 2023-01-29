from features.addressbook_fields import Record
from features.bot_feature import BotFeature
from features.records_container import RecordsContainer


class AddressBook(BotFeature):
    """
    A feature that allows users to manage their contacts.
    """

    def __init__(self, save_file: str):
        self.save_file = save_file
        self.data = RecordsContainer(save_file)

        super().__init__({
            "add": self.add_contact,
            "change": self.change_contact,
            "remove": self.data.remove_record,
            "show": self.data.show_all,
            "birthdays": self.check_birthdays,
            "search": self.data.search_record
        })

    def name(self):
        return "contacts"

    def add_contact(self):
        name = input("Enter the name: ").strip()
        if self.data.record_exists(name):
            raise ValueError("This name is already in your phonebook. If you want to change something type 'change'.")

        record = Record(name)
        self.data.add_record(record)

        phones = input("Enter the phone or phones: ").strip().split()
        if phones:
            for phone in phones:
                record.add_phone(phone)

        birthday = input("Enter the birthdate: ").strip()
        if birthday:
            record.add_birthday(birthday)

        email = input("Enter the email: ").strip()
        if email:
            record.add_email(email)

        address = input("Enter the address: ").strip()
        if address:
            record.add_address(address)

        return f"Contact {name} was created successfully!"

    def change_contact(self, *args: str) -> str:
        """
        Changes the contact data. Throws exception if the contact with the given name doesn't exist.

        :param args: name of a contact to change
        :return: success message or KeyError
        """

        name = " ".join(args)
        if self.data.record_exists(name):
            contact_to_change = self.data[name]
            while True:
                to_change = input("What do you want to change? Type phone, email, birthday or address: ")
                if to_change.lower() not in ["phone", "email", "address", "birthday"]:
                    print("Unknown command")
                    continue
                elif to_change.lower() == "phone":
                    new_phones = input("Enter a new phone or phones separated by spaces: ").strip()
                    contact_to_change.phones.clear()
                    for new_phone in new_phones.split():
                        contact_to_change.add_phone(new_phone)
                elif to_change.lower() == "email":
                    new_email = input("Enter a new email: ")
                    contact_to_change.add_email(new_email)
                elif to_change.lower() == "address":
                    new_address = input("Enter new address here: ")
                    contact_to_change.add_address(new_address)
                elif to_change.lower() == "birthday":
                    new_birthday = input("Enter a birthdate in format '%d.%m.%Y': ")
                    contact_to_change.add_birthday(new_birthday)

                to_continue = input("Do you want to change something else in this contact? Enter y or n: ")
                if to_continue.lower() not in ["y", "n"]:
                    print("Enter y or n.")
                    continue
                elif to_continue.lower() == "y":
                    continue
                else:
                    return "The contact was changed successfully!"
        else:
            raise KeyError("Contact with this name doesn't exist.")

    def check_birthdays(self, period: str) -> str:
        """
        Creates and returns a list of people who have birthdays in a given period.

        :param period: number of days starting from today
        :return: a list of contacts as a string
        """
        if not period.isdigit():
            raise ValueError("Enter a number of days.")

        result = ""
        for contact in self.data.values():
            if contact.birthday is None:
                continue
            else:
                days_to_contacts_bd = contact.count_days_to_birthday()
                if int(days_to_contacts_bd) <= int(period):
                    result += str(contact) + "\n"
        if result:
            return result
        else:
            return "No one has birthday in this period."
