from collections import UserDict
import re

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        
    def validate_phone(self):
        # Format phone number to delete all non-digit characters
        normalized_value = re.sub(r'\D', '', self.value)
        if re.fullmatch(r"\d{10}", normalized_value):
            self.value = normalized_value  # Update value with normalized phone number
            return True
        else:
            raise ValueError("Phone number must be exactly 10 digits")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones) if self.phones else "No phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"

    def add_phone(self, phone):
        phone_field = Phone(phone)
        try:
            phone_field.validate_phone()
            self.phones.append(phone_field)
        except ValueError as e:
            print(e)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                phone_field = Phone(new_phone)
                try:
                    phone_field.validate_phone()
                    self.phones[idx] = phone_field
                except ValueError as e:
                    print(e)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Value must be an instance of Record")
        self.data[record.name.value] = record
        
    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555") if john is not None else None
if found_phone:
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
