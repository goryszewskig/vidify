"""
This init module lists the available players for the app and how to initialize
them.
"""

import importlib
from enum import Enum

from spotivids.config import Config
from spotivids.player.generic import PlayerBase


class PlayerData(Enum):
    """
    The available players enumeration. It contains information about how to
    initialize them: the module, the class name and the possible parameters
    needed (flags from the config).

    Note: all player entries must have their name in uppercase.
    """

    def __new__(cls, module: str, class_name: str, config_flags_name: str
                ) -> object:
        obj = object.__new__(cls)
        # The module location to import (for dependency injection).
        obj.module = module
        # The player's class name inside its module.
        obj.class_name = class_name
        # The name of the player's option in the Config module used to provide
        # flags or additional information. The flags argument is always
        # optional.
        obj.config_flags_name = config_flags_name
        return obj

    VLC = ('spotivids.player.vlc', 'VLCPlayer', 'vlc_args')
    MPV = ('spotivids.player.mpv', 'MpvPlayer', 'mpv_flags')


class PlayerNotFoundError(AttributeError):
    """
    Exception raised when the player wasn't found.
    """

    def __init__(self, msg: str = "The selected player isn't available."
                                  " Please check your config or specify one by"
                                  " using a valid `--player` argument."):
        super().__init__(msg)


def initialize_player(key: str, config: Config) -> PlayerBase:
    """
    Choosing a player from the list and initializing an abstract player
    instance with the information inside the `player` enumeration object.
    """

    # Finding the config player and initializing it.
    try:
        player = PlayerData[key.upper()]
    except KeyError:
        raise PlayerNotFoundError

    # Importing the module first
    mod = importlib.import_module(player.module)
    # Then obtaining the player class
    cls = getattr(mod, player.class_name)
    # No other arguments are needed for now, so all this does is initialize
    # the player with the config flags (if present).
    try:
        flags = getattr(config, player.flags_name)
    except AttributeError:
        obj = cls()
    else:
        obj = cls(flags)
    return obj
