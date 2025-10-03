import re

def validation_str(string: str) -> tuple[str, bool]:
    pattern = r"^[a-zа-я]{1,20}$"
    if re.fullmatch(pattern, string):
        return string
    return False

def validation_phone(phone: str) -> tuple[str, bool]:
    pattern = r"^8[0-9]{10}$"
    if re.fullmatch(pattern, phone):
        return phone
    return False
def validation_email(email: str) -> tuple[str, bool]:
    pattern = r"^[a-z0-9.]{5,100}@[a-z]{3,10}.[a-z]{2,5}$"
    if re.fullmatch(pattern, email):
        return email
    return False