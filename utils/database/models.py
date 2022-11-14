from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, ForeignKey, Integer, MetaData, String, Table
)

Base = declarative_base()


class HotelModel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    place_id = Column(Integer, ForeignKey('regions.id', ondelete='SET NULL'), nullable=True)
    phone = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey('admins.id', ondelete='SET NULL'), nullable=True)
    description = Column(String(500), nullable=False)

    def __repr__(self):
        return f"Hotel(id={self.id!r}, name={self.name!r})"


class RegionModel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, nullable=False)
    region_name = Column(String(200), nullable=False)

    def __repr__(self):
        return f"Hotel(id={self.id!r}, region={self.region_name!r})"


class AdminModel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __repr__(self):
        return f"Hotel(id={self.id!r}, name={self.name!r})"
