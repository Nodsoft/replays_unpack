# coding=utf-8
import sys
import json
import logging
import os
import time
import typing
from json import JSONEncoder

from replay_unpack.clients import wows
from replay_unpack.replay_reader import ReplayReader, ReplayInfo


class DefaultEncoder(JSONEncoder):
    def default(self, o):
        try:
            return o.__dict__
        except AttributeError:
            return str(o)


class ReplayParser(object):
    BASE_PATH = os.path.dirname(__file__)

    def __init__(self, binary_replay_data: typing.IO, strict: bool = False, raw_data_output=None):
        self._binary_replay_data = binary_replay_data
        self._is_strict_mode = strict
        self._reader = ReplayReader(binary_replay_data)
        self._raw_data_output = raw_data_output

    def get_info(self):
        replay = self._reader.get_replay_data()

        error = None
        try:
            hidden_data = self._get_hidden_data(replay)
        except Exception as e:
            if isinstance(e, RuntimeError):
                error = str(e)
            logging.exception(e)
            hidden_data = None

            # raise error in strict mode
            if self._is_strict_mode:
                raise

        return dict(
            open=replay.engine_data,
            extra_data=replay.extra_data,
            hidden=hidden_data,
            error=error
        )

    def _get_hidden_data(self, replay: ReplayInfo):
        player = wows.ReplayPlayer(replay.engine_data
                                   .get('clientVersionFromXml')
                                   .replace(' ', '')
                                   .split(','))

        if self._raw_data_output:
            with open(self._raw_data_output, 'wb') as f:
                f.write(replay.decrypted_data)

        player.play(replay.decrypted_data, self._is_strict_mode)
        return player.get_info()


if __name__ == '__main__':
    start = time.time()
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', type=str, required=False)
    parser.add_argument(
        '--log_level',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
        required=False,
        default='ERROR'
    )
    parser.add_argument(
        '--strict_mode',
        action='store_true',
        required=False
    )
    parser.add_argument(
        '--raw_data_output',
        help='File where raw replay content (decoded and decompressed) will be written',
        required=False,
        default=None
    )

    namespace = parser.parse_args()
    if namespace.replay is None:
        replay_data = sys.stdin.buffer
    else:
        replay_data = open(namespace.replay, 'rb')
    logging.basicConfig(
        level=getattr(logging, namespace.log_level))
    replay_info = ReplayParser(
        replay_data, strict=namespace.strict_mode,
        raw_data_output=namespace.raw_data_output).get_info()
    print(json.dumps(replay_info, indent=1, cls=DefaultEncoder))
    end = time.time()
    print("Total duration: " + str(end - start))
