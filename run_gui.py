import sys

from marketGUI.market_app import TestMarketApplication
from market.controllers.main_window_controller import MainWindowController


def main():
    app = TestMarketApplication(sys.argv)
    form = MainWindowController(app=app)
    form.show()
    app.run()


if __name__ == '__main__':
    main()
