"""
A base profile for experimenting with NDN over simple wired connections.
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


def mkVM(name, image, cores=4, ram=4):
    """Creates a VM with the specified parameters"""
    node = request.XenVM(name)
    node.disk_image = image
    node.cores = cores
    node.ram = ram * 1024
    node.exclusive = True
    node.routable_control_ip = True
    node.InstantiateOn('pnode')
    return node


# begin creating request
pc = portal.Context()

request = pc.makeRequestRSpec()


# Declare dedicated VM host
pnode = request.RawPC('pnode')
pnode.hardware_type = GLOBALS.PNODE_D740

# configure VMs and links here:
node1 = mkVM('node1', GLOBALS.UBUNTU18_IMG, cores=4, ram=8)
node2 = mkVM('node2', GLOBALS.UBUNTU18_IMG, cores=4, ram=8)
node3 = mkVM('node3', GLOBALS.UBUNTU18_IMG, cores=4, ram=8)
node4 = mkVM('node4', GLOBALS.UBUNTU18_IMG, cores=4, ram=8)

# Add links between nodes (form a "circle" of connectivity)
link1 = request.Link(members=[node1, node2])
link2 = request.Link(members=[node2, node3])
link3 = request.Link(members=[node3, node4])
link4 = request.Link(members=[node4, node1])

# run the install.sh script on each vm to install software
node1.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
node1.addService(pg.Execute(shell="sh", command="/local/repository/install.sh"))

node2.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
node2.addService(pg.Execute(shell="sh", command="/local/repository/install.sh"))

node3.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
node3.addService(pg.Execute(shell="sh", command="/local/repository/install.sh"))

node4.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
node4.addService(pg.Execute(shell="sh", command="/local/repository/install.sh"))

# output request
pc.printRequestRSpec(request)
