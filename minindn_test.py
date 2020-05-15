from mininet.log import setLogLevel, info

from minindn.minindn import Minindn
from minindn.util import MiniNDNCLI
from minindn.apps.app_manager import AppManager
from minindn.apps.nfd import Nfd
from minindn.apps.nlsr import Nlsr
# from minindn.helpers.routing_helper import IPRoutingHelper

if __name__ == '__main__':
    setLogLevel('info')

    Minindn.cleanUp()
    Minindn.verifyDependencies()

    # Can pass a custom parser, custom topology, or any Mininet params here
    ndn = Minindn()

    ndn.start()

    # IP reachability if needed
    # IPRoutingHelper.calcAllRoutes(ndn.net)
    # info("IP routes configured, start ping\n")
    # ndn.net.pingAll()

    # Start apps with AppManager which registers a clean up function with ndn
    info('Starting NFD on nodes\n')
    nfds = AppManager(ndn, ndn.net.hosts, Nfd)
    info('Starting NLSR on nodes\n')
    nlsrs = AppManager(ndn, ndn.net.hosts, Nlsr)

    # or can not start NLSRs with some delay in between:
    # nlsrs = AppManager(ndn, ndn.net.hosts, Nlsr)
    # for host in ndn.net.hosts:
    #     nlsrs.startOnNode(host)
    #     time.sleep(30)

    MiniNDNCLI(ndn.net)

    # Calls the clean up functions registered via AppManager
    ndn.stop()
