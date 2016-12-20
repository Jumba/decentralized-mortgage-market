import os
import sys

import signal
from twisted.internet import reactor

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QApplication

from scenarios.apps import MarketAppSceneBorrower, MarketAppSceneBank, MarketAppSceneBankING, MarketAppSceneInvestor


def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    #if QMessageBox.question(None, '', "Are you sure you want to quit?",
    #                        QMessageBox.Yes | QMessageBox.No,
    #                        QMessageBox.No) == QMessageBox.Yes:
    reactor.stop()
    QApplication.quit()
    os._exit(0) # TODO: THIS SHOULD BE DONE PROPERLY

if __name__ == "__main__":

    from marketGUI.market_app import MarketApplication, MarketApplicationABN

    signal.signal(signal.SIGINT, sigint_handler)

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

    timer = QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    # Your code here.

    sys.exit(app.exec_())
