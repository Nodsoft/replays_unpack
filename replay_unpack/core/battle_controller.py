# coding=utf-8
import copy
from abc import ABCMeta, abstractmethod
from typing import Dict

from replay_unpack.core.entity import Entity


def cleanup_vehicle_properties(raw_properties: dict[str, dict]) -> dict[str, dict]:
    refined_properties = dict()
    for main_key, main_val in raw_properties.items():
        refined_child_properties = dict()
        for key, val in copy.deepcopy(main_val).items():
            if isinstance(val, bytes):
                val = val.decode("latin-1")
            refined_child_properties[key] = val

        refined_properties[main_key] = refined_child_properties

    return refined_properties


def extract_and_refine_vehicle_properties(entities: dict[int, Entity]) -> dict[int, dict[str, dict]]:
    vehicles = dict()
    for entity in entities.values():
        if entity.get_name() == "Vehicle":
            properties = copy.deepcopy(entity.properties)
            vehicles[entity.id] = cleanup_vehicle_properties(properties)

    return vehicles


class IBattleController(metaclass=ABCMeta):
    """
    Proxy to real battle controller of given version
    """

    @property
    @abstractmethod
    def entities(self) -> Dict[int, Entity]:
        pass

    @abstractmethod
    def create_entity(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def destroy_entity(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def on_player_enter_world(self, entity_id: int):
        pass

    @property
    @abstractmethod
    def map(self) -> str:
        pass

    @map.setter
    def map(self, value: str):
        pass

    def get_info(self) -> Dict:
        pass
