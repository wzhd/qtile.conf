from collections import namedtuple

import xcffib
import xcffib.xproto

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.config import Match
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile import hook

from bindings import keys_app
import autostart
from widgets.backlight import Backlight

_screen = xcffib.connect().get_setup().roots[0]
scaling = _screen.width_in_pixels / _screen.width_in_millimeters / 4

def scale(size):
    return int(size*scaling)

mod = "mod4"

keys = [
    *keys_app,
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.up(),
    ),
    Key(
        [mod], "j",
        lazy.layout.down(),
    ),

    Key(
        [mod], "h",
        lazy.layout.left()
    ),
    Key(
        [mod], "l",
        lazy.layout.right()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_up()
    ),

    Key([mod],          "comma",    lazy.layout.grow()),
    Key([mod],          "period",   lazy.layout.shrink()),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),
    Key([mod, 'shift'], "space", lazy.prev_layout()),
    Key([mod, 'shift'], "c", lazy.window.kill()),
    Key([mod],          "m", lazy.window.toggle_fullscreen()),
    Key([mod],          "8",    lazy.window.down_opacity()),
    Key([mod],          "9",   lazy.window.up_opacity()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
]

MyGroup = namedtuple('MyGroup', ['name', 'key', 'layout', 'matches'])
mygroups = [
    MyGroup('🇦', 'a', 'floating', [Match(wm_class=['KeePass2', 'main.py', 'clientui.py', 'Thunar'])]),
    MyGroup('🇧', 's', 'max', [Match(wm_class=['Zathura', 'Qemu-system-x86_64', 'GoldenDict'])]),
    MyGroup('🌐', 'd', 'max', [Match(wm_class=['Firefox', 'qutebrowser', 'Google-chrome', 'chromium'])]),
    MyGroup('⏎', 'f', None, [Match(wm_class=['Emacs', 'Atom'])]),
    MyGroup('⚒', 'u', None, [Match(wm_class=['Termite'])]),
    MyGroup('📓', 'i', None, [Match(wm_class=['Zim', 'mpv'])]),
    MyGroup('🇴', 'o', None, None),
    MyGroup('🇵', 'p', None, None),
]

groups = []

for i in mygroups:
    groups.append(Group(i.name, layout=i.layout, matches=i.matches))

    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.key, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.key, lazy.window.togroup(i.name))
    )


layouts = [
    layout.Max(),
    layout.columns.Columns(fair=True, border_focus='#881111', border_normal='#220000', border_width=4),
    layout.verticaltile.VerticalTile(border_width=4),
    layout.Floating(),
]

widget_defaults = dict(
    font='Noto Serif',
    fontsize=scale(16),
    padding=scale(1.5),
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(margin_x=1, margin_y=0, fontsize=scale(12), disable_drag=True, inactive='909090', font='DejaVu Sans'),
                widget.Prompt(),
                widget.TaskList(highlight_method='block', max_title_width=scale(200)),
                widget.Notify(),
                widget.Systray(icon_size=scale(22)),
                Backlight(),
                widget.Volume(foreground = "70ff70"),
                widget.MemoryGraph(foreground='908'),
                widget.SwapGraph(foreground='C02020'),
                widget.Sep(),
                widget.NetGraph(interface='wlp1s0'),
                widget.Battery(
                    energy_now_file='charge_now',
                    energy_full_file='charge_full',
                    power_now_file='current_now',
                    update_delay = 5,
                    foreground = "7070ff",
                ),
                widget.BatteryIcon(),
                widget.TextBox("my config", name="default"),
                widget.ThermalSensor(tag_sensor='Physical id 0'),
                widget.Clock(format='%b-%d %a %H:%M'),
                widget.CurrentLayout(),
            ],
            scale(22),
        ),
    ),
]

@hook.subscribe.client_managed
def show_window(window):
    window.group.cmd_toscreen()

@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

floating_names = ('Search Dialog', 'Module' , 'Goto' , 'IDLE Preferences')
@hook.subscribe.client_new
def idle_dialogues(window):
    if window.window.get_name() in floating_names:
        window.floating = True

floating_wmclasses = (
    'libreoffice-calc',
    'LibreOffice 3.4',
    'Onboard',
    'Thunar',
)
@hook.subscribe.client_new
def libreoffice_dialogues(window):
    if window.window.get_wm_class()[1] in floating_wmclasses:
        window.floating = True

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
