import os
import json
from threading import Timer
from utils import logutil
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSVariableStatusItemLength, NSImage
from PyObjCTools import AppHelper
from models import Schedule
from time import sleep


class App(NSApplication):
    def finishLaunching(self):
        # Make statusbar item
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.icon = NSImage.alloc().initByReferencingFile_('icon.png')
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((20, 20))
        self.statusitem.setImage_(self.icon)
        self._schedules = []
        self._menu_items = []

        self._initialize_schedules()
        self._initialize_menu()

        self._timer = Timer(60, self.timer_callback)
        self._timer.start()

    def _initialize_schedules(self):
        USER_ROOT = os.path.expanduser('~')
        DOCUMENTS = os.path.join(USER_ROOT, 'Documents')
        SCHEDULES = os.path.join(DOCUMENTS, 'schedules.json')
        schedules = json.load(open(SCHEDULES, encoding='utf8'))
        for raw_info in schedules:
            self._schedules.append(Schedule(raw_info))

    def _initialize_menu(self):
        self.menubarMenu = NSMenu.alloc().init()
        for schedule in self._schedules:
            menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(schedule.name, 'execute:', '')
            self._menu_items.append(menu_item)
            self.menubarMenu.addItem_(menu_item)

        menu_item = NSMenuItem.separatorItem()
        self.menubarMenu.addItem_(menu_item)

        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menubarMenu.addItem_(self.quit)

        self.statusitem.setMenu_(self.menubarMenu)
        self.statusitem.setToolTip_('Crow')

    def timer_callback(self):
        self._timer = None
        for schedule in self._schedules:
            try:
                schedule.execute()
            except:
                import traceback
                logutil.error(schedule.name, traceback.format_exc())

        interval = 60
        self._timer = Timer(interval, self.timer_callback)
        self._timer.start()

    def execute_(self, notification):
        while self._timer is None:
            sleep(0.1)
        self._timer.cancel()
        self._timer = None

        for schedule in self._schedules:
            if schedule.name == notification.title():
                try:
                    schedule.execute_actions()
                except:
                    import traceback
                    logutil.error(schedule.name, traceback.format_exc())

        self.timer_callback()


if __name__ == "__main__":
    app = App.sharedApplication()
    AppHelper.runEventLoop()
