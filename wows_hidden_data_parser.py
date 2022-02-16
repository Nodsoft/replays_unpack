import json
import logging
import sys

from replay_parser import DefaultEncoder
from replay_unpack.clients import wows


class HiddenDataParser(object):
    def __init__(self, decompressed_hidden_data: bytes, game_version: str):
        self.decompressed_hidden_data = decompressed_hidden_data
        self.game_version = game_version

    def get_hidden_info(self):
        player = wows.ReplayPlayer(self.game_version.split('.'))
        player.play(self.decompressed_hidden_data)
        return player.get_info()

    def get_info(self):
        error = None
        try:
            hidden_data = self.get_hidden_info()
        except Exception as e:
            if isinstance(e, RuntimeError):
                error = str(e)
            else:
                error = 'Unknown error during parsing process'
            logging.exception(e)
            hidden_data = None

        return dict(hidden=hidden_data, error=error)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--game-version', '-gv', type=str, required=True)
    parser.add_argument(
        '--log_level',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
        required=False,
        default='ERROR'
    )

    argument_namespace = parser.parse_args()
    decompressed_replay_data = sys.stdin.buffer.read()
    logging.basicConfig(level=getattr(logging, argument_namespace.log_level))
    replay_info = HiddenDataParser(decompressed_replay_data, argument_namespace.game_version).get_info()

    print(json.dumps(replay_info, indent=1, cls=DefaultEncoder))
