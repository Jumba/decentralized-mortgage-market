import os
import sys

if __name__ == "__main__":

    from marketGUI.market_app import MarketApplication
    from marketGUI.market_window import MarketWindow

    app = MarketApplication(sys.argv)

    window = MarketWindow()
    sys.exit(app.exec_())
