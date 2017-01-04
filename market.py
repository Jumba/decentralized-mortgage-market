import sys
from marketGUI.market_app import MarketApplication

from PyQt5.QtWidgets import QApplication
#from PyQt5.QtCore import QTimer


app = MarketApplication(sys.argv)
from twisted.application import reactors
reactors.installReactor('qt5')

from twisted.internet import reactor
print reactor

#reactor.callWhenRunning(app.start_dispersy)
reactor.runReturn()

from market.controllers.main_window_controller import MainWindowController

#form = MainWindowController(app=app)
#form.show()


if __name__ == "__main__":
    pass

    import qt5reactor
    #qt5reactor.install()





    # timer = QTimer()
    # timer.start(500)  # You may change this if you wish.
    # timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    # # Your code here.


    #app.run()

    #sys.exit(app.exec_())
