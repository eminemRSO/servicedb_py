from sqlalchemy.orm import Session
import models


def try_add_allowed_user(db: Session, user: str, service_id: int, owner: str):
    if get_service(db, owner, service_id):
        db_user = models.User(username=user, service_id=service_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return True
    return False


def add_allowed_user(db: Session, user: str, service_id: int):
    db_user = models.User(username=user, service_id=service_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_service(db: Session, user: str, file: bytes, service_name: str):
    db_service = models.Service(owner=user, service=file, service_name=service_name)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    add_allowed_user(db=db, user=db_service.owner, service_id=db_service.id)
    return db_service


def get_services(db: Session, user: str):
    return db.query(models.Service).filter(models.Service.owner == user).all()


def get_service(db: Session, user: str, service_id: int):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if service and user in [user.username for user in service.allowed]:
        return service
    return None


def delete_service(db: Session, owner: str, service_id: int):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if service and service.owner == owner:
        db.delete(service)
        db.commit()
        return service
    return None
