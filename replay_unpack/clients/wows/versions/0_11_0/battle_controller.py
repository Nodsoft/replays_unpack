# coding=utf-8
import logging
import pickle

from replay_unpack.core import IBattleController
from replay_unpack.core.entity import Entity
from .constants import DamageStatsType, Category, TaskType, Status
from replay_unpack.core.battle_controller import extract_and_refine_vehicle_properties

try:
    from .constants import DEATH_TYPES
except ImportError:
    DEATH_TYPES = {}
from .players_info import PlayersInfo


class BattleController(IBattleController):

    def __init__(self):
        self._entities = {}
        self._achievements = {}
        self._ribbons = {}
        self._players = PlayersInfo()
        self._battle_result = None
        self._damage_map = {}
        self._shots_damage_map = {}
        self._death_map = []
        self._map = {}
        self._player_id = None
        self._arena_id = None

        self._dead_planes = {}

        Entity.subscribe_method_call('Avatar', 'onBattleEnd', self.onBattleEnd)
        Entity.subscribe_method_call('Avatar', 'onArenaStateReceived', self.onArenaStateReceived)
        Entity.subscribe_method_call('Avatar', 'onGameRoomStateChanged', self.onPlayerInfoUpdate)
        Entity.subscribe_method_call('Avatar', 'receiveVehicleDeath', self.receiveVehicleDeath)
        # Entity.subscribe_method_call('Vehicle', 'setConsumables', self.onSetConsumable)
        Entity.subscribe_method_call('Avatar', 'onRibbon', self.onRibbon)
        Entity.subscribe_method_call('Avatar', 'onAchievementEarned', self.onAchievementEarned)
        Entity.subscribe_method_call('Avatar', 'receiveDamageStat', self.receiveDamageStat)
        Entity.subscribe_method_call('Avatar', 'receive_planeDeath', self.receive_planeDeath)
        Entity.subscribe_method_call('Avatar', 'onNewPlayerSpawnedInBattle', self.onNewPlayerSpawnedInBattle)

        Entity.subscribe_method_call('Vehicle', 'receiveDamagesOnShip', self.g_receiveDamagesOnShip)

    def onSetConsumable(self, vehicle, blob):
        print(pickle.loads(blob))

    @property
    def entities(self):
        return self._entities

    @property
    def battle_logic(self):
        return next(e for e in self._entities.values() if e.get_name() == 'BattleLogic')

    def create_entity(self, entity: Entity):
        self._entities[entity.id] = entity

    def destroy_entity(self, entity: Entity):
        self._entities.pop(entity.id)

    def on_player_enter_world(self, entity_id: int):
        self._player_id = entity_id

    def get_info(self):
        return dict(
            achievements=self._achievements,
            ribbons=self._ribbons,
            players=self._players.get_info(),
            battle_result=self._battle_result,
            damage_map=self._damage_map,
            shots_damage_map=self._shots_damage_map,
            death_map=self._death_map,
            death_info=self._getDeathsInfo(),
            map=self._map,
            player_id=self._player_id,
            control_points=self._getCapturePointsInfo(),
            tasks=list(self._getTasksInfo()),
            skills=dict(),
            # planes are only updated in AOI
            # so information is not right
            # planes=self._dead_planes,
            arena_id=self._arena_id,
            vehicles=extract_and_refine_vehicle_properties(self.entities)
        )

    def _getDeathsInfo(self):
        deaths = {}
        for killedVehicleId, fraggerVehicleId, typeDeath in self._death_map:
            death_type = DEATH_TYPES.get(typeDeath)
            if death_type is None:
                logging.warning('Unknown death type %s', typeDeath)
                continue

            deaths[killedVehicleId] = {
                'killer_id': fraggerVehicleId,
                'icon': death_type['icon'],
                'name': death_type['name'],
            }
        return deaths

    def _getCapturePointsInfo(self):
        return self.battle_logic.properties['client']['state'].get('controlPoints', [])

    def _getTasksInfo(self):
        tasks = self.battle_logic.properties['client']['state'].get('tasks', [])
        for task in tasks:
            yield {
                "category": Category.names[task['category']],
                "status": Status.names[task['status']],
                "name": task['name'],
                "type": TaskType.names[task['type']]
            }

    def onBattleEnd(self, avatar, teamId, state):
        self._battle_result = dict(
            winner_team_id=teamId,
            victory_type=state
        )

    def onNewPlayerSpawnedInBattle(self, avatar, pickle_data):
        self._players.create_or_update_players(
            pickle.loads(pickle_data))

    def onArenaStateReceived(self, avatar, arenaUniqueId, teamBuildTypeId, preBattlesInfo, playersStates,
                             observersState, buildingsInfo):
        self._arena_id = arenaUniqueId
        self._players.create_or_update_players(
            pickle.loads(playersStates, encoding='latin1'))

    def onPlayerInfoUpdate(self, avatar, playersData, observersData):
        self._players.create_or_update_players(
            pickle.loads(playersData))

    def receiveDamageStat(self, avatar, blob):
        normalized = {}
        for (type_, bool_), value in pickle.loads(blob).items():
            # TODO: improve damage_map and list other damage types too
            if bool_ != DamageStatsType.DAMAGE_STATS_ENEMY:
                continue
            normalized.setdefault(type_, {}).setdefault(bool_, 0)
            normalized[type_][bool_] = value
        self._damage_map.update(normalized)

    def onRibbon(self, avatar, ribbon_id):
        self._ribbons.setdefault(avatar.id, {}).setdefault(ribbon_id, 0)
        self._ribbons[avatar.id][ribbon_id] += 1

    def onAchievementEarned(self, avatar, avatar_id, achievement_id):
        self._achievements.setdefault(avatar_id, {}).setdefault(achievement_id, 0)
        self._achievements[avatar_id][achievement_id] += 1

    def receiveVehicleDeath(self, avatar, killedVehicleId, fraggerVehicleId, typeDeath):
        self._death_map.append((killedVehicleId, fraggerVehicleId, typeDeath))

    def g_receiveDamagesOnShip(self, vehicle, damages):
        for damage_info in damages:
            self._shots_damage_map.setdefault(vehicle.id, {}).setdefault(damage_info['vehicleID'], 0)
            self._shots_damage_map[vehicle.id][damage_info['vehicleID']] += damage_info['damage']

    def receive_planeDeath(self, avatar, squadronID, planeIDs, reason, attackerId):
        self._dead_planes.setdefault(attackerId, 0)
        self._dead_planes[attackerId] += len(planeIDs)

    @property
    def map(self):
        raise NotImplemented()

    @map.setter
    def map(self, value):
        self._map = value.lstrip('spaces/')
