from datetime import date, timedelta

from src.database.db import SessionLocal
from src.database.models import Contact

db = SessionLocal()

contacts_birthday = []

today = date.today()
next_7_days = [((today + timedelta(days=d)).month, (today + timedelta(days=d)).day) for d in range(1, 8)]
print(next_7_days)

m = list({(today + timedelta(days=d)).month for d in range(1, 8)})
d = [(today + timedelta(days=d)).day for d in range(1, 8)]
print(m)
print(d)

contacts = db.query(Contact).all()
for contact in contacts:
    day_birth = (contact.birthday.month, contact.birthday.day)
    if day_birth in next_7_days:
        contacts_birthday.append(contact)


