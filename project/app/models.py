from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String)
    service = Column(LargeBinary)
    service_name = Column(String)

    allowed = relationship("Users", back_populates="service")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    service_id = Column(Integer, ForeignKey("service.id"))

    service = relationship("Service", back_populates="allowed")
