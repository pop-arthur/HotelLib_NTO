from typing import Tuple

from sqlalchemy import Table

from utils.database.schema import admins, hotels, regions


class Unit:
    """
    Class for processing actions with unit table
    """

    table: Table

    def add_unit(self, vals: Tuple) -> Tuple:
        """
        :param vals: unit's values
        :return: added unit
        """

        pass

    def get_unit_by_id(self, unit_id: int) -> Tuple:
        """
        :param unit_id: ID of the unit
        :return: unit
        """

        pass

    def get_unit_by_args(self, vals: Tuple) -> Tuple:
        """
        :param vals: unit's values
        :return: unit
        """

        pass

    def delete_unit(self, unit_id: int) -> int:
        """
        :param unit_id: ID of the unit to be deleted
        :return: status of delete:
        0 -> Not found unit with this ID
        1 -> Successful deleted
        """

        pass

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
