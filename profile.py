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
portal.context.defineParameter("bandwidth", "Bandwidth of link (Kbps)", portal.ParameterType.BANDWIDTH, 110000)
portal.context.defineParameter("latency", "Latency of link (milliseconds)", portal.ParameterType.LATENCY, 1)

# retrieve the values the user specifies during instantiation
params = portal.context.bindParameters()

#  check parameter validity
if params.n < 2 or params.n > 10:
    portal.context.reportError(portal.ParameterError("You must choose at least 2 and no more than 10 nodes."))


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


def create_nodes(count=2, instantiateOn='pnode', cores=4, ram=8):
    """Allocates and runs an install script on a specified number of VM nodes

    Returns a list of nodes.
    """

    nodes = []
    # index nodes by their proper number (not zero-indexed)
    nodes.append(None)

    # create each VM
    for i in range(1, count + 1):
        nodes.append(mkVM('node' + str(i), GLOBALS.UBUNTU18_IMG, instantiateOn=instantiateOn, cores=cores, ram=ram))

    # run the install.sh script on each vm to install software
    for node in nodes:
        if node is not None:
            node.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
            node.addService(pg.Execute(shell="sh", command="/local/repository/install.sh"))

    return nodes


# begin creating request
pc = portal.Context()
request = pc.makeRequestRSpec()

# declare dedicated VM host
pnode = request.RawPC('pnode')
pnode.hardware_type = GLOBALS.PNODE_D740

# create nodes on dedicated host
if params.n == 2:
    nodes = create_nodes(count=params.n, instantiateOn='pnode', cores=8, ram=32)
else:
    nodes = create_nodes(count=params.n, instantiateOn='pnode')

# establish a "circle" of connectivity
links = []
for i in range(1, params.n):
    links.append(request.Link(members=[nodes[i], nodes[i+1]]))
# complete the circle
if params.n != 2:
    links.append(request.Link(members=[nodes[params.n], nodes[1]]))

# set link performance
for link in links:
    # Kbps
    link.bandwidth = params.bandwidth
    # milliseconds
    link.latency = params.latency
    # Packet loss is a number 0.0 <= loss <= 1.0
    link.plr = 0.0 


# output request
pc.printRequestRSpec(request)

