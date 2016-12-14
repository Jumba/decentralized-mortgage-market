import sys

from marketGUI.market_app import MarketApplication
from market.controllers.main_view_controller import MainWindowController


def main():
    app = MarketApplication(sys.argv)
    form = MainWindowController(app=app)
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
