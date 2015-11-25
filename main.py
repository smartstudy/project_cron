from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSVariableStatusItemLength, NSImage
from PyObjCTools import AppHelper


class App(NSApplication):
    def finishLaunching(self):
        # Make statusbar item
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.icon = NSImage.alloc().initByReferencingFile_('icon.png')
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((20, 20))
        self.statusitem.setImage_(self.icon)

        self.initialize_menu()

    def initialize_menu(self):
        self.menubarMenu = NSMenu.alloc().init()
        self.menubarMenu.addItem_(NSMenuItem.separatorItem())

        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menubarMenu.addItem_(self.quit)

        self.statusitem.setMenu_(self.menubarMenu)
        self.statusitem.setToolTip_('Project Cron')


if __name__ == "__main__":
    app = App.sharedApplication()
    AppHelper.runEventLoop()
