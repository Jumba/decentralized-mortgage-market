import logging
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from market.api.api import MarketAPI
from market.community.community import MortgageMarketCommunity
from market.database.backends import PersistentBackend
from market.database.database import MockDatabase
from market.dispersy.dispersy import Dispersy
from market.dispersy.endpoint import StandaloneEndpoint
from market.models.house import House

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
import time

def start_dispersy():
    master_key = "3081a7301006072a8648ce3d020106052b8104002703819200040578e79f08d3270c5af04ace5b572ecf46eef54502c1" \
                 "4f3dc86f4cd29e86f05dad976b08da07b8d97d73fc8243459e09b6b208a2c8cbf6fdc7b78ae2668606388f39ef0fa715cf2" \
                 "104ad21f1846dd8f93bb25f2ce785cced2c9231466a302e5f9e0e70f72a3a912f2dae7a9a38a5e7d00eb7aef23eb42398c38" \
                 "59ffadb28ca28a1522addcaa9be4eec13095f48f7cf35".decode("HEX")
    dispersy = Dispersy(StandaloneEndpoint(1236, '0.0.0.0'), unicode('.'), u'dispersy3.db')
    dispersy.statistics.enable_debug_statistics(True)
    dispersy.start(autoload_discovery=True)

    my_member = dispersy.get_new_member()
    master_member = dispersy.get_member(public_key=master_key)

    api = MarketAPI(MockDatabase(PersistentBackend('.')))

    community = MortgageMarketCommunity.init_community(dispersy, master_member, my_member)
    community.api = api

    house = House('2617Hm', '340', 9003)

    LoopingCall(lambda:community.send_model_request([('users', '3081a7301006072a8648ce3d020106052b810400270381920004008b7da3e9cf183cd8a709179fcf915b223c338fdb6a87245d25585af47b64164efeb531685423afeea580563f95fabf0a2e10f90afd4ee5f79adc6a46f5d6f1e6b2d4174d6329ac004b3e974e237c1c9a28025f3f10d2dd9802d2ef5f61d742ac80ece2a742b45cb201ae10003991ed54606e123ccc8c1939a02a786a6e381ff5e5f1264c9727074b42d3e1d9a67e76'), ('house', '12321')])).start(1.0)


def main():
    reactor.callWhenRunning(start_dispersy)
    reactor.run()

if __name__ == "__main__":
    main()
