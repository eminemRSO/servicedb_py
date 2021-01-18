from sqlalchemy.orm import Session
import models
import data


def try_add_allowed_user(db: Session, user: str, service_id: int, owner: str):
    if get_service(db, owner, service_id):
        db_user = data.add_user(db, username=user, service_id=service_id)
        return db_user
    return None


def add_allowed_user(db: Session, user: str, service_id: int):
    db_user = data.add_user(db, username=user, service_id=service_id)
    return db_user


def create_service(db: Session, user: str, file: bytes, service_name: str):
    db_service = data.create_service(db, owner=user, service=file, service_name=service_name)
    return db_service


def get_services(db: Session, user: str):
    return data.search_all_allowed_services(db, user=user)


def get_service(db: Session, user: str, service_id: int):
    return data.get_service(db, user=user, id=service_id)


def delete_service(db: Session, owner: str, service_id: int):
    return data.delete_service(db, user=owner, id=service_id)
