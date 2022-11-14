from typing import List, Tuple

from sqlalchemy import delete, select, Table
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from __config__ import PROJECT_SOURCE_PATH_DB
from utils.database.schema import admins, hotels, regions


class Unit:
    """
    Class for processing actions with unit table
    """

    table: Table
    database_path: str = f"{PROJECT_SOURCE_PATH_DB}/database.db"

    @staticmethod
    def get_session() -> Session:
        return Session()

    def add_unit(self, vals: Tuple) -> Tuple:
        """
        :param vals: unit's values
        :return: added unit
        """

        pass

    def get_unit_by_id(self, unit_id: int) -> Row:
        """
        :param unit_id: ID of the unit
        :return: unit
        """
        return self.get_session().execute(
            select(self.table).where(self.table.c.id == unit_id)
        ).one()

    def get_unit_by_args(self, vals: Tuple) -> Tuple:
        """
        :param vals: unit's values
        :return: unit
        """

        pass

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


class Admins(Unit):
    table = admins


class Regions(Unit):
    table = regions
