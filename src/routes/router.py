from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.db import get_db
from src.auths.auth import get_current_user
from src.repository.repository import (
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_contacts_birthday_soon
)
from src.schemas import ContactCreate, ContactUpdate, ContactResponse

router = APIRouter()



@router.post("/contacts/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    try:
        db_contact = create_contact(contact, db)
        return db_contact
    except HTTPException as e:
        print(f"Error in create_new_contact: {e.detail}")
        raise
    except Exception as e:
        print(f"Error in create_new_contact: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/contacts/", response_model=List[ContactResponse])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    contacts = get_contacts(db, current_user, skip=skip, limit=limit)
    return contacts


@router.get("/contacts/search/", response_model=list[ContactResponse])
def search_contacts_route(name: Optional[str] = None, email: Optional[str] = None, db: Session = Depends(get_db)):
    contacts = search_contacts(db, name, email)
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found")
    return contacts


@router.get("/contacts/birthday/", response_model=List[ContactResponse])
def contacts_birthday_soon(days: int = 7, db: Session = Depends(get_db)):
    return get_contacts_birthday_soon(db, days)


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_contact = get_contact(db, contact_id, current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_contact = update_contact(db, contact_id, contact.dict(), current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact_route(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_contact(db, contact_id, current_user)
