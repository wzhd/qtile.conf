from libqtile.config import Key
from libqtile.command import lazy

mod = "mod4"

keys_app = [
    Key([], "XF86AudioLowerVolume",         lazy.spawn("ponymix decrease 5")),
    Key([], "XF86AudioRaiseVolume",         lazy.spawn("ponymix increase 5 --max-volume 150")),
    Key([], "Print",             lazy.spawn("/home/wzhd/bin/maim-my")),
    Key(['shift'], "Print",      lazy.spawn('sh -c "maim /tmp/$(date +%F-%T).png"')),
    Key([mod], "w",              lazy.spawn("rofi -show window")),
    Key([mod], "c",              lazy.spawn("rofi -show ssh")),
    Key([mod], "r",              lazy.spawn("rofi -show drun")),
    Key([mod], "Return",         lazy.spawn("termite")),
    Key([mod], "w",              lazy.spawn("rofi -show window")),
]
