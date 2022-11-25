from typing import Any, List, Tuple, Dict

from sqlalchemy import create_engine, delete, insert, Table, select, update
from sqlalchemy.engine import Connection, Row

from __config__ import PROJECT_SOURCE_PATH_DB
from utils.database.schema import admins, clients, entities, hotels, regions, tours, TypeOfClient, TypeOfFood

database_path: str = f"sqlite:///{PROJECT_SOURCE_PATH_DB}/database.db"
engine = create_engine(database_path)


class Unit:
    """
    Class for processing actions with unit table
    """

    table: Table
    database_path: str = f"{PROJECT_SOURCE_PATH_DB}/database.db"

    @staticmethod
    def get_session() -> Connection:
        return engine.connect()

    def add_unit(self, vals: Dict) -> Row:
        """
        :param vals: unit's values
        :return: added unit
        """
        session = self.get_session()
        user = session.execute(insert(self.table).values(**vals))
        # session.commit()

        # return self.get_unit_by_id(user.inserted_primary_key)

    def update_unit_by_id(self, unit_id: int, vals: Dict) -> None:
        """
        :param unit_id: ID of the unit
        :param vals: Dict with data to update unit
        :return: unit
        """

        self.get_session().execute(
            update(self.table).where(self.table.c.id == unit_id).values(**vals)
        )

    def delete_unit_by_id(self, unit_id: int):
        try:
            session = self.get_session()
            session.execute(delete(self.table).where(self.table.c.id == unit_id))
            # session.commit()

            return 1
        except Exception:
            return 0

    def get_unit_by_args(self, vals: Dict) -> Row:
        """
        :param vals: unit's values
        :return: unit
        """

        return self.get_session().execute(
            select(self.table).where(**vals)
        ).one()

    def get_unit_by_id(self, unit_id: int) -> Row:
        """
        :param unit_id: ID of the unit
        :return: unit
        """
        return self.get_session().execute(
            select(self.table).where(self.table.c.id == unit_id)
        ).one()

    def update_unit_by_id(self, unit_id: int, vals: Dict) -> None:
        """
        :param unit_id: ID of the unit
        :param vals: Dict with data to update unit
        :return: unit
        """

        self.get_session().execute(
            update(self.table).where(self.table.c.id == unit_id).values(**vals)
        )

    def get_units(self) -> List[Row]:
        return self.get_session().execute(select(self.table)).all()

    def delete_unit(self, unit_id: int) -> int:
        """
        :param unit_id: ID of the unit to be deleted
        :return: status of delete:
        0 -> Not found unit with this ID
        1 -> Successful deleted
        """

        try:
            self.get_session().execute(delete(self.table).where(self.table.c.id == unit_id))
            return 1
        except BaseException as err:
            print(err)
        return 0

    def get_or_create_unit(self, vals: Tuple):
        """
        :param vals: unit's values
        :return: created unit (or this unit from database) and status
        0 -> unit already exists
        1 -> unit is created
        """

        unit = self.get_unit_by_args(vals)
        if unit:
            return unit, 0
        unit = self.add_unit(vals)

        return unit, 1


class Hotel(Unit):
    table = hotels
    hotel_indexes = [0, 1, 3, 5]
    admin_indexes = [7, 8, 9, 10]
    region_indexes = [12]

    def get_units(self):
        join_rows = self.get_session().execute(
            self.join_all_connected_tables(select(
                self.table, Admins.table, Regions.table, Entities.table
            ))
        ).all()
        return list(map(lambda x: [x[0], x[1], x[10], x[3], x[14], x[5]], join_rows))

    def get_pretty_units(self) -> List[List[Any]]:
        join_rows = self.get_session().execute(
            self.join_all_connected_tables(select(
                self.table, Admins.table, Regions.table, Entities.table
            ))
        ).all()

        hotels_info, admins_info, regions_info = [], [], []

        for row in join_rows:
            hotel_info, admin_info, region_info = row[:6], row[6:11], row[11:]
            hotel_info = list(hotel_info)
            admin_info = list(admin_info)
            region_info = list(region_info)
            hotel_info[2], hotel_info[4] = region_info[1], admin_info[1]

            hotels_info.append(hotel_info)
            admins_info.append(admin_info)
            regions_info.append(region_info)

        return hotels_info

    def join_regions(self, sql_request):
        return sql_request.join(Regions.table, self.table.c.place_id == Regions.table.c.id)

    def join_all_connected_tables(self, sql_request):
        return self.join_admins(self.join_regions(sql_request))

    def join_admins(self, sql_request):
        """
        :param sql_request:
        :return:
        """

        return sql_request.join(Admins.table, self.table.c.admin_id == Admins.table.c.id).join(
            Entities.table, Admins.table.c.entity_id == Entities.table.c.id
        )


class Admins(Unit):
    table = admins

    def join_entities(self, sql_request):
        return sql_request.join(Entities.table, self.table.c.entity_id == Entities.table.c.id)

    def get_units(self):
        return list(map(
            lambda x: [x[0], x[1]] + list(x[4:]),
            self.get_session().execute(self.join_entities(select(self.table, Entities.table))).all())
        )


class Regions(Unit):
    table = regions


class Tours(Unit):
    table = tours
    convert_types: dict = {e.name: e.value for e in TypeOfClient}

    def join_hotels(self, sql_request):
        return sql_request.join(Hotel.table, self.table.c.hotel_id == Hotel.table.c.id)

    def get_units(self) -> List[List[Any]]:
        return list(map(
            lambda x: [x[0], x[9]] + list(x[2:5]) + [x[5].value] + list(x[6:8]),
            self.get_session().execute(self.join_hotels(select(self.table, Hotel.table))).all())
        )


class Entities(Unit):
    table = entities


class Clients(Unit):
    table = clients
    convert_types: dict = {e.name: e.value for e in TypeOfFood}

    def join_entities(self, sql_request):
        return sql_request.join(Entities.table, self.table.c.entity_id == Entities.table.c.id)

    def get_units(self):
        return list(map(
            lambda x: list(x[0:2]) + [x[2].value] + list(x[4:]),
            self.get_session().execute(self.join_entities(select(self.table, Entities.table))).all())
        )
