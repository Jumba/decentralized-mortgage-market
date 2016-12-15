import sys

from marketGUI.market_app import TestMarketApplication
from market.controllers.main_view_controller import MainWindowController


def main():
    app = TestMarketApplication(sys.argv)
    form = MainWindowController(app=app)
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
