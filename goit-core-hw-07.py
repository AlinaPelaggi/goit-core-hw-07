#Модуль 7
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)

# added class Birthday
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "The contact exists"
        except ValueError:
            return "Please enter the correct arguments"
        except IndexError:
            return "No such contacts"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone): #corrected
        if not isinstance(phone, Phone):
            raise ValueError("Invalid phone number format")
        self.phones.append(phone)

    def add_birthday(self, birthday): #added
        if not isinstance(birthday, Birthday):
            raise ValueError("Invalid birthday format")
        self.birthday = birthday

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone): #corrected from Modul6 error
        found = False
        if not new_phone.isdigit() or len(new_phone) != 10:
            raise ValueError("New phone number must be a 10-digit number")
        
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.value = new_phone
                found = True
                break
        if not found:
            raise ValueError("Phone number does not exist")

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        raise ValueError("Phone number does not exist")

    def __str__(self):  #CORRECTED
        phones = '; '.join(str(p) for p in self.phones)
        birthday = f', Birthday: {self.birthday.value.strftime("%d.%m.%Y")}' if self.birthday else ''
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"

class AddressBook(UserDict):
    @input_error
    def add_record(self, record):
        self.data[record.name.value] = record
    @input_error
    def find(self, name):
        return self.data.get(name)
    @input_error
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    @input_error
    def add_contact(self, args):
        name, phone, *_ = args
        message = "Contact updated."
        if name not in self.data:
            record = Record(name)
            if phone:
                record.add_phone(phone)
            self.add_record(record)
            message = "Contact added"
        else:
            message = "Contact already exists"
        return message
    @input_error
    def all_contact(self):
        lines = []
        for name, record in self.data.items():
            phones = '; '.join(str(phone) for phone in record.phones)
            if record.birthday:
                birthday = record.birthday.value
            else:
                birthday = ""
            lines.append(f"| {name:<20} | {phones:<20} | {birthday:<20} |")
        header = "| {:<20} | {:<20} | {:<20} |".format("Name", "Phones", "Birthday")
        separator = "-" * len(header)
        return "\n".join([separator, header, separator] + lines + [separator])
    def edit_phone(self, name, new_phone):
        record = book.find(name)
        if not record:
            raise ValueError("Contact not found")
        phone = record.phones
        Record.remove_phone(phone)
        record.add_phone(new_phone)
        return "Phone number updated."
    @input_error
    def add_birthday(self, args):
        name, birthday = args
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday added for {name}."
        else:
            return f"Contact '{name}' not found."
    @input_error
    def show_birthday(self, args):
        name, *_ = args
        record = book.find(name)
        if record:
            if record.birthday:
                return f"Birthday for {name}: {record.birthday.value}"
            else:
                return f"No birthday set for {name}."
        else:
            return f"Contact '{name}' not found."
#Get upcoming birthdays
    @input_error
    def birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []

        for name, record in self.data.items():
            if record.birthday:
                birthday = record.birthday.value
                birthday_date = datetime.strptime(birthday, '%d.%m.%Y').date()
                birthday_this_year = birthday_date.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= 7:
                    if birthday_this_year.weekday() >= 5:
                        delta = (7 - birthday_this_year.weekday())
                        birthday_this_year += timedelta(days=delta)

                    congratulation_date_str = birthday_this_year.strftime('%Y.%m.%d')
                    upcoming_birthdays.append({"name": name, "congratulation_date": congratulation_date_str})

        return upcoming_birthdays
    
if __name__ == "__main__":
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
        elif command == "add-contact":
            print(book.add_contact(args))
        elif command == "change":
            name, new_phone, *_ = args
            print(book.edit_phone(name, new_phone))
        elif command == "show-all":
            print(book.all_contact())
        elif command == "add-birthday":
            print(book.add_birthday(args))
        elif command == "show-birthday":
            print(book.show_birthday(args))
        elif command == "birthdays":
            print(book.birthdays())
        else:
            print("Invalid command.")
