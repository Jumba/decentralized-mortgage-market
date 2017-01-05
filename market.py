import sys
from marketGUI.market_app import MarketApplication
from scenarios.apps import MarketAppSceneBank, MarketAppSceneBankING, MarketAppSceneBankRABO, MarketAppSceneBankMONEYOU, \
    MarketAppSceneBorrower, MarketAppSceneInvestor

if __name__ == "__main__":
    if len(sys.argv) == 1:
        app = MarketApplication(sys.argv)
    else:
        bank = sys.argv[1]
        if bank == "abn":
            app = MarketAppSceneBank(sys.argv)
        elif bank == "ing":
            app = MarketAppSceneBankING(sys.argv)
        elif bank == "rabo":
            app = MarketAppSceneBankRABO(sys.argv)
        elif bank == "moneyou":
            app = MarketAppSceneBankMONEYOU(sys.argv)
        elif bank == "borrower":
            app = MarketAppSceneBorrower(sys.argv)
        elif bank == "investor":
            app = MarketAppSceneInvestor(sys.argv)
        else:
            raise SystemExit("Unknown bank")

    headless = False
    if len(sys.argv) == 3:
        headless = sys.argv[2] == "headless"


    from twisted.application import reactors
    reactors.installReactor('qt5')

    from twisted.internet import reactor

    reactor.callWhenRunning(app.start_dispersy)
    app.initialize()
    reactor.runReturn()

    if not headless:
        from market.controllers.main_window_controller import MainWindowController

        form = MainWindowController(app=app)
        form.show()

    app.exec_()

