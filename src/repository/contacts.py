from typing import List
from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(**body.dict())
    contact.user_id = user.id
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.notes = body.notes
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts_by_name(name: str, skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.name.icontains(name)).offset(skip).limit(limit).all()


async def search_contacts_by_surname(surname: str, skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.surname.icontains(surname)).offset(skip).limit(limit).all()


async def search_contacts_by_email(email: str, skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.email.icontains(email)).offset(skip).limit(limit).all()


async def search_contacts_by_birthday(user: User, db: Session) -> List[Contact]:
    contacts_birthday = []

    today = date.today()
    next_7_days = [
        ((today + timedelta(days=d)).month,(today + timedelta(days=d)).day) 
        for d in range(1, 8)
        ]
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in contacts:
        day_birth = (contact.birthday.month, contact.birthday.day)
        if day_birth in next_7_days:
            contacts_birthday.append(contact)
            
    return contacts_birthday
