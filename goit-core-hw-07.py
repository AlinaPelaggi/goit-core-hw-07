#Модуль 7
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, value):
        self.birthday = Birthday(value)

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_record(self, record):
        self.contacts.append(record)

    def find(self, name):
        for contact in self.contacts:
            if contact.name.value.lower() == name.lower():
                return contact
        return None

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "The contact exists"
        except ValueError as e:
            return f"Error: {str(e)}"
        except IndexError:
            return "No such contacts"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError("Invalid number of arguments. Please provide the name and the phone number of the contact.")

    name, phone = args
    contact = book.find(name)
    if contact:
        contact.phones.append(Phone(phone))
        return "Contact updated successfully"
    else:
        new_contact = Record(name)
        new_contact.phones.append(Phone(phone))
        book.add_record(new_contact)
        return "Contact added successfully"

@input_error
def change_contact(args, book):
    if len(args) != 2:
        raise ValueError("Invalid number of arguments. Please provide the name and the phone number of the contact.")

    name, phone = args
    contact = book.find(name)
    if contact:
        contact.phones = [Phone(phone)]
        return "Contact updated successfully"
    else:
        return "Contact not found"

@input_error
def show_contact(args, book):
    if len(args) != 1:
        raise ValueError("Invalid number of arguments. Please provide the name of the contact.")

    name = args[0]
    contact = book.find(name)
    if contact:
        return ", ".join([phone.value for phone in contact.phones])
    else:
        return "Contact not found"

@input_error
def show_all(book):
    if not book.contacts:
        raise IndexError("No contacts found")
    return "\n".join([f"{contact.name.value}: {', '.join([phone.value for phone in contact.phones])}" for contact in book.contacts])

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Invalid number of arguments. Please provide the name of the contact and the date of birth in format DD.MM.YYYY")

    name, birthday = args
    contact = book.find(name)
    if contact:
        contact.add_birthday(birthday)
        return "Birthday added successfully"
    else:
        return "Contact not found"

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Invalid number of arguments. Please provide the name of the contact to show their birthday.")

    name = args[0]
    contact = book.find(name)
    if contact and contact.birthday:
        return contact.birthday.value.strftime('%d.%m.%Y')
    else:
        return "Birthday not found"

def get_upcoming_birthdays(book):
    upcoming_birthdays = []
    today = datetime.now()
    for contact in book.contacts:
        if contact.birthday:
            birthday = contact.birthday.value.replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            if birthday - today <= timedelta(days=7):
                upcoming_birthdays.append((contact.name.value, birthday))
    return upcoming_birthdays

@input_error
def birthdays(args, book):
    upcoming_birthdays = get_upcoming_birthdays(book)
    if upcoming_birthdays:
        return "\n".join([f"{name}: {birthday.strftime('%d.%m.%Y')}" for name, birthday in upcoming_birthdays])
    else:
        return "No upcoming birthdays"

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_contact(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()