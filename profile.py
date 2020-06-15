"""A base profile for experimenting with NDN.

Instructions:
Wait for the profile instance to start, and then log into either VM via the ssh ports specified below.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as elab


class GLOBALS(object):
    """useful constant values for setting up a powder experiment"""
    SITE_URN = "urn:publicid:IDN+emulab.net+authority+cm"
    # standard Ubuntu release
    UBUNTU18_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
    PNODE_D740 = "d740"  # 24 cores, 192 GB RAM
    PNODE_D840 = "d840"  # 64 cores, 768 GB RAM


# define network parameters
portal.context.defineParameter("n", "Number of network nodes", portal.ParameterType.INTEGER, 2)

# retrieve the values the user specifies during instantiation
params = portal.context.bindParameters()

#  check parameter validity
if params.n < 1 or params.n > 4:
    portal.context.reportError(portal.ParameterError("You must choose at least 2 and no more than 4 nodes."))


def mkVM(name, image, instantiateOn, cores, ram):
    """Creates a VM with the specified parameters

    Returns that VM
    """
    node = request.XenVM(name)
    node.disk_image = image
    node.cores = cores
    node.ram = ram * 1024
    node.exclusive = True
    node.routable_control_ip = True
    node.InstantiateOn(instantiateOn)
    return node


def create_nodes(count=2, prefix=1, instantiateOn='pnode', cores=2, ram=4):
    """Allocates and runs an install script on a specified number of VM nodes

    Returns a list of nodes.
    """

    nodes = []
    # index nodes by their proper number (not zero-indexed)
    nodes.append(None)

    # create each VM
    for i in range(1, count + 1):
        nodes.append(mkVM('node' + str(prefix) + '.' + str(i), GLOBALS.UBUNTU18_IMG, instantiateOn=instantiateOn, cores=cores, ram=ram))

    # run install scripts on each vm to install software
    for node in nodes:
        if node is not None:
            node.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install1.sh"))
            node.addService(pg.Execute(shell="sh", command="/local/repository/install1.sh"))

    return nodes


def create_routers(instantiateOn='pnode', cores=4, ram=8):
    """Allocates and runs an install script on two virtualized routers

    Returns a list of routers.
    """

    routers = []
    # index routers by their proper number (not zero-indexed)
    routers.append(None)

    # create each VM
    for i in range(1, 3):
        routers.append(mkVM('router' + str(i), GLOBALS.UBUNTU18_IMG, instantiateOn=instantiateOn, cores=cores, ram=ram))

    # run alternating install scripts on each vm to install software
    odd_router = True
    for router in routers:
        if router is not None:
            if odd_router:
                router.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install1.sh"))
                router.addService(pg.Execute(shell="sh", command="/local/repository/install1.sh"))
            else:
                router.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install2.sh"))
                router.addService(pg.Execute(shell="sh", command="/local/repository/install2.sh"))
            odd_router = not odd_router

    return routers


# begin creating request
pc = portal.Context()
request = pc.makeRequestRSpec()

# declare a dedicated VM host
pnode = request.RawPC('pnode')
pnode.hardware_type = GLOBALS.PNODE_D740

# create nodes on dedicated host
routers = create_routers()
nodes1 = create_nodes(count=params.n, prefix=1)
nodes2 = create_nodes(count=params.n, prefix=2)

# setup the first LAN
for node in nodes1:
    if node is not None:
        request.Link(members=[routers[1], node])

# setup the second LAN
for node in nodes2:
    if node is not None:
        request.Link(members=[routers[2], node])

# setup a link between routerss
request.Link(members=[routers[1], routers[2]])

# output request
pc.printRequestRSpec(request)
