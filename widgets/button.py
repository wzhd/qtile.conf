import subprocess

from libqtile.log_utils import logger
from libqtile.widget import base


class ButtonWidget(base.InLoopPollText):

    defaults = [
        ('launch', None, 'Command to run'),
    ]

    def __init__(self, **config):
        print(config)
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(ButtonWidget.defaults)

    def button_press(self, x, y, button):
        if button == 1:  # down
            if self.launch:
                logger.info("launching %s" % self.launch)
                subprocess.Popen(self.launch)

    def poll(self):
        return 'Run'
