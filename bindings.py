from libqtile.config import Key
from libqtile.command import lazy

mod = "mod4"

keys_app = [
    Key([mod], "Return",         lazy.spawn("termite")),
]
