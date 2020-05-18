"""
A base profile for experimenting with NDN over simple wired connections.
"""

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.emulab as elab


class GLOBALS(object):
    SITE_URN = "urn:publicid:IDN+emulab.net+authority+cm"
    UBUNTU18_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
    PNODE_TYPE = "d840"


def mkVM(name, image, cores=4, ram=4096):
    """Creates a VM with the specified parameters"""
    node = request.XenVM(name)
    node.disk_image = image
    node.cores = cores
    node.ram = ram
    node.exclusive = True
    node.routable_control_ip = True
    node.InstantiateOn('pnode')
    return node


pc = portal.Context()

request = pc.makeRequestRSpec()


# Declare dedicated VM host
pnode = request.RawPC('pnode')
pnode.hardware_type = GLOBALS.PNODE_TYPE


# configure VMs and links here:
node1 = mkVM('node1', GLOBALS.UBUNTU18_IMG, cores=2, ram=2048)
node2 = mkVM('node2', GLOBALS.UBUNTU18_IMG, cores=2, ram=2048)
node3 = mkVM('node3', GLOBALS.UBUNTU18_IMG, cores=2, ram=2048)
node4 = mkVM('node4', GLOBALS.UBUNTU18_IMG, cores=2, ram=2048)

# Add links between all four nodes
link1 = request.Link(members=[node1, node2])
link2 = request.Link(members=[node2, node3])
link3 = request.Link(members=[node3, node4])
link4 = request.Link(members=[node4, node1])


# link = request.Link("link")
# link.trivial_ok = True
# link.addNode(node1)
# link.addNode(node2)
# link.addNode(node3)
# link.addNode(node4)

# link1 = request.Link(members=[node1, node2, node3, node4])

# print request
pc.printRequestRSpec(request)
