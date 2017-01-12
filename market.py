import os
import sys
import argparse

import run_tftp_server
from marketGUI.market_app import MarketApplication, MarketApplicationING, MarketApplicationRABO, MarketApplicationMONEYOU, \
    MarketApplicationBank, MarketApplicationABN
from scenarios.apps import MarketAppSceneBank, MarketAppSceneBankING, MarketAppSceneBankRABO, MarketAppSceneBankMONEYOU, \
    MarketAppSceneBorrower, MarketAppSceneInvestor

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--headless", help="Run the market in headless mode", action="store_true")
    parser.add_argument("--bank", help="Run the market as a bank.", type=str, choices=['abn', 'ing', 'rabo', 'moneyou'],)
    parser.add_argument("--scenario", help="Select a scenario to enable", type=str, choices=['bank', 'borrower', 'investor'],)

    args = parser.parse_args()
    start_tftp_server = True

    if not args.bank and not args.scenario:
        app = MarketApplication(sys.argv)
        start_tftp_server = False
    elif args.scenario == 'borrower':
        app = MarketAppSceneBorrower(sys.argv)
        start_tftp_server = False
    elif args.scenario == 'investor':
        app = MarketAppSceneInvestor(sys.argv)
        start_tftp_server = False
    elif args.bank == "abn":
        if args.scenario == "bank":
            app = MarketAppSceneBank(sys.argv)
        else:
            app = MarketApplicationABN(sys.argv)
    elif args.bank == "ing":
        if args.scenario == "bank":
            app = MarketAppSceneBankING(sys.argv)
        else:
            app = MarketApplicationING(sys.argv)
    elif args.bank == "rabo":
        if args.scenario == "bank":
            app = MarketAppSceneBankRABO(sys.argv)
        else:
            app = MarketApplicationRABO(sys.argv)
    elif args.bank == "moneyou":
        if args.scenario == "bank":
            app = MarketAppSceneBankMONEYOU(sys.argv)
        else:
            app = MarketApplicationMONEYOU(sys.argv)
    else:
        raise SystemExit("Unknown bank")

    if start_tftp_server:
        tftp_server = run_tftp_server.Server()
        tftp_server.set_logging(os.getcwd()+'/logging/', 'INFO')
        tftp_server.start()

    from twisted.application import reactors
    reactors.installReactor('qt5')

    from twisted.internet import reactor

    reactor.callWhenRunning(app.start_dispersy)
    app.initialize()
    reactor.runReturn()

    if not args.headless:
        from market.controllers.main_window_controller import MainWindowController

        form = MainWindowController(app=app)
        form.show()

    app.exec_()

