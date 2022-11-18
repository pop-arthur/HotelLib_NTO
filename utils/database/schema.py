from sqlalchemy import (
    Column, ForeignKey, Integer, MetaData, String, Table
)

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
    Column('full_name', String, nullable=False),
    Column('role', String, nullable=False),
    Column('phone', String, nullable=False),
    Column('email', String, nullable=False),
)
