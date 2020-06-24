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

    # run alternating install scripts on each vm to install software 
    odd_node = True
    for node in nodes:
        if node is not None:
            if odd_node:
                node.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install1.sh"))
                node.addService(pg.Execute(shell="sh", command="/local/repository/install1.sh"))
            else:
                node.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install2.sh"))
                node.addService(pg.Execute(shell="sh", command="/local/repository/install2.sh"))
            odd_node = not odd_node

    return nodes


# begin creating request
pc = portal.Context()
request = pc.makeRequestRSpec()

# declare dedicated VM host
pnode = request.RawPC('pnode')
pnode.hardware_type = GLOBALS.PNODE_D740

# create nodes on dedicated host
nodes = create_nodes(count=2, instantiateOn='pnode', cores=8, ram=32)

# establish connectivity between nodes
request.Link(members=[nodes[1], nodes[2]])

# output request
pc.printRequestRSpec(request)
