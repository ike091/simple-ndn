"""A base profile for experimenting with NDN over wired connections.

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
portal.context.defineParameter("physical", "Should the nodes be physical?", portal.ParameterType.BOOLEAN, False)

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

# allocate physical or virtual hosts
if params.physical:
    # request physical nodes
    node1 = request.RawPC('node1')
    node1.hardware_type = GLOBALS.PNODE_D740
    node1.disk_image = GLOBALS.UBUNTU18_IMG 
    node2 = request.RawPC('node2')
    node2.hardware_type = GLOBALS.PNODE_D740
    node2.disk_image = GLOBALS.UBUNTU18_IMG 

    # run install scripts
    node1.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
    node1.addService(pg.Execute(shell="sh", command="/local/repository/install.sh"))
    node2.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
    node2.addService(pg.Execute(shell="sh", command="/local/repository/install.sh"))

    # establish connectivity
    request.Link(members=[node1, node2])

else:
    # declare dedicated VM host
    pnode = request.RawPC('pnode')
    pnode.hardware_type = GLOBALS.PNODE_D740

    nodes = create_nodes(count=params.n, instantiateOn='pnode')

    # establish a "circle" of connectivity
    for i in range(1, params.n):
        request.Link(members=[nodes[i], nodes[i+1]])
    if params.n != 2:
        request.Link(members=[nodes[params.n], nodes[1]])


# output request
pc.printRequestRSpec(request)
