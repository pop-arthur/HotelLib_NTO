from sqlalchemy import (
    Column, Date, ForeignKey, Integer,
    MetaData, String, Table, Enum as sqlEnum,
    Float
)

from enum import Enum, unique

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


@unique
class TypeOfFood(Enum):
    without = 'без питания'
    three_times = '3-х разовое'
    with_breakfast = 'С завтраком'


@unique
class TypeOfClient(Enum):
    legal = 'юридическое  лицо'
    individual = 'физическое лицо'


hotels = Table(
    'hotels',
    metadata,

    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(200), nullable=False),
    Column('place_id', Integer, ForeignKey('regions.id', ondelete='SET NULL'), nullable=True),
    Column('phone', String, nullable=False),
    Column('admin_id', Integer, ForeignKey('admins.id', ondelete='SET NULL'), nullable=True),
    Column('description', String(500), nullable=False),
)

regions = Table(
    'regions',
    metadata,

    Column('id', Integer, primary_key=True, nullable=False),
    Column('region_name', String, nullable=False)
)

admins = Table(
    'admins',
    metadata,

    Column('id', Integer, primary_key=True, nullable=False),
    Column('role', String, nullable=False),
    Column('entity_id', Integer, ForeignKey('entities.id', ondelete='SET NULL'), nullable=True),

)

tours = Table(
    'tours',
    metadata,

    Column('id', Integer, primary_key=True, nullable=False),
    Column('hotel_id', Integer, ForeignKey('hotels.id', ondelete='SET NULL'), nullable=True),
    Column('date_start', Date, nullable=False),
    Column('date_end', Date, nullable=False),
    Column('days', String(), nullable=False),
    Column('type', sqlEnum(TypeOfFood, name='type_of_food'), nullable=False),
    Column('tour_cost', Float(precision=2), nullable=False),
    Column('description', String(500), nullable=False),
)

entities = Table(
    'entities',
    metadata,

    Column('id', Integer, primary_key=True, nullable=False),
    Column('phone', String, nullable=False),
    Column('email', String, nullable=False),
    Column('full_name', String, nullable=False),

)

clients = Table(
    'clients',
    metadata,

    Column('id', Integer, primary_key=True, nullable=False),
    Column('entity_id', Integer, ForeignKey('entities.id', ondelete='SET NULL'), nullable=True),
    Column('type', sqlEnum(TypeOfClient, name='type_of_client'), nullable=False),
)
