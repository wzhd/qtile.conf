import subprocess

from libqtile import hook

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(['fcitx-autostart'])
    subprocess.Popen(['redshift-gtk'])
