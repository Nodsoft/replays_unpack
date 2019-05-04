#!/usr/bin/python
# coding=utf-8
from build.entities import Avatar

__author__ = "Aleksandr Shyshatsky"


class Avatar(Avatar):
    def __init__(self):
        self.methodsMap = {
            9: 'onVisibilityChanged',
            53: 'receiveVehicleDeath',
            67: 'onConnected',
            68: 'receiveShellInfo',
            90: 'onGameRoomStateChanged',
            69: 'onNewPlayerSpawnedInBattle',
            13: 'onBattleEnd',
            0: 'onBattleInterrupted',
            91: 'receiveShotPack',
            70: 'receiveProjectileTrace',
            92: 'receiveDamageReport',
            22: 'targetLoss',
            64: 'receive_addSquadron',
            61: 'receive_addMinimapSquadron',
            40: 'receive_removeMinimapSquadron',
            58: 'receive_updateMinimapSquadronPosition',
            63: 'receive_setSquadronActive',
            41: 'receive_removeSquadron',
            71: 'receive_updateSquadron',
            42: 'receive_bombDropped',
            55: 'receive_planeDeath',
            43: 'receive_squadrounOutOfFuel',
            14: 'receive_squadronNotify',
            62: 'receive_squadronDropBombs',
            23: 'receive_assignOrderStatus',
            15: 'receive_squadronChangeState',
            16: 'receive_squadronPopOrder',
            17: 'receive_lastOrdersCanceled',
            18: 'receive_cancelOrder',
            72: 'receive_squadronAddOrders',
            73: 'receive_squadronChangeOrderGoal',
            19: 'receive_squadronClearOrders',
            48: 'receive_squadronAttackPlaneState',
            49: 'receive_squadronUpdatePassiveAura',
            74: 'receive_refresh',
            54: 'receive_squadronFormation',
            44: 'receive_landSquadron',
            56: 'receive_targetID',
            75: 'receive_prepareBombing',
            59: 'receive_startBombing',
            76: 'receive_startTorpedo',
            32: 'receive_inDefenceChanged',
            93: 'battleLogicAction',
            57: 'receive_CommonCMD',
            77: 'onChatMessage',
            51: 'notifyStartAttackPlane',
            52: 'notifyStopAttackPlane',
            60: 'onShipCollision',
            24: 'onEndShipCollision',
            33: 'onDisconnectedFromServer',
            94: 'onArenaStateReceived',
            78: 'receiveChatHistory',
            45: 'onCheckGamePing',
            46: 'onCheckCellPing',
            79: 'updateMinimapVisionInfo',
            10: 'onRibbon',
            1: 'onWorldStateReceived',
            47: 'onAchievementEarned',
            80: 'onBattleAchievementsRestored',
            81: 'receiveAvatarInfo',
            20: 'onEvaluationAccepted',
            25: 'artilleryAlert',
            11: 'capturedAsAGoal',
            95: 'onEnterPreBattle',
            21: 'onLeavePreBattle',
            2: 'createPreBattle',
            3: 'leavePreBattle',
            34: 'onOwnerChanged',
            96: 'receivePlayerData',
            82: 'updatePreBattlesInfo',
            4: 'preBattleJoined',
            26: 'changePreBattleGrants',
            27: 'onActionFailed',
            50: 'onShutdownTime',
            83: 'onBuildingsDataChanged',
            84: 'receiveDamageStat',
            85: 'inviteToPreBattle',
            86: 'onInviteSent',
            35: 'onInviteRevoked',
            36: 'onInviteRejected',
            37: 'onInviteAccepted',
            87: 'rejectInvite',
            88: 'updateCoolDown',
            38: 'revokeInvite',
            28: 'startAppearing',
            29: 'startDissapearing',
            12: 'setIntuitionAngle',
            5: 'hideIntuitionIndicator',
            30: 'ownSmokeCreated',
            31: 'clientInsideSmoke',
            6: 'vehicleLeaveSmoke',
            7: 'notifyAboutSmokePenalty',
            8: 'ownSmokeStartsFade',
            39: 'ownSmokeTimeLifeChanges',
        }

        self.attributesMap = {
            6: 'ownShipId',
            0: 'useATBAandAirDefense',
            9: 'vehiclePosition',
            1: 'teamId',
            2: 'isBattleStopped',
            7: 'selectedWeapon',
            3: 'isFlyMode',
            4: 'intuitionActive',
            8: 'attrs',
            5: 'isInOfflineMode',
            10: 'minefields'
        }

        super(Avatar, self).__init__()

