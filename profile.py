"""
A base profile for experimenting with NDN over simple wired connections.
"""

import geni.portal as portal
import geni.rspec.pg as rspec
#  import geni.rspec.emulab as elab


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


def create_nodes(count=4, cores=4, ram=8):
    """Allocates and runs an install script on a specified number of VM nodes"""

    nodes = []
    # index nodes by their proper number (not zero-indexed)
    nodes.append(None)

    # create each VM
    for i in range(1, count+1):
        nodes.append(mkVM('node' + str(i), GLOBALS.UBUNTU18_IMG, cores=cores, ram=ram))

    # run the install.sh script on each vm to install software
    for node in nodes:
        if node != None:
            node.addService(rspec.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
            node.addService(rspec.Execute(shell="sh", command="/local/repository/install.sh"))

    return nodes


def create_link(node1_num, node2_num):
    """Creates a link with conveniently-named ip addresses between the two specfied node numbers."""

    iface1 = nodes[node1_num].addInterface("if" + str(node1_num) + str (node2_num))
    iface1.component_id = "eth" + str(node2_num)
    iface1.addAddress(rspec.IPv4Address("10.10." + str(node1_num) + "." + str(node2_num), "255.255.255.0")) 

    iface2 = nodes[node2_num].addInterface("if" + str(node2_num) + str (node1_num))
    iface2.component_id = "eth" + str(node1_num)
    iface2.addAddress(rspec.IPv4Address("10.10." + str(node2_num) + "." + str(node1_num), "255.255.255.0")) 

    link = request.LAN("lan")
    link.addInterface(iface1)
    link.addInterface(iface2)


# create nodes
nodes = create_nodes()

# establish connectivity
create_link(1,2)
create_link(2,3)
create_link(3,4)
create_link(4,1)


#  if12 = nodes[0].addInterface("if12")
#  if12.component_id = "eth2"
#  if12.addAddress(rspec.IPv4Address("10.10.1.2", "255.255.255.0"))

#  if21 = nodes[1].addInterface("if21")
#  if21.component_id = "eth1"
#  if21.addAddress(rspec.IPv4Address("10.10.2.1", "255.255.255.0"))

#  link = request.LAN("lan")
#  link.addInterface(if12)
#  link.addInterface(if21)

#  if1 = nodes[1].addInterface("if1")
#  if1.component_id = "eth1"
#  if1.addAddress(rspec.IPv4Address("10.10.1.2", "255.255.255.0"))

#  if1 = nodes[1].addInterface("if1")
#  if1.component_id = "eth1"
#  if1.addAddress(rspec.IPv4Address("10.10.1.2", "255.255.255.0"))

<<<<<<< HEAD
#  link1 = request.Link(members=[nodes[1], nodes[2]])
#  link2 = request.Link(members=[nodes[2], nodes[3]])
#  link3 = request.Link(members=[nodes[3], nodes[4]])
#  link4 = request.Link(members=[nodes[4], nodes[1]])
=======
link1 = request.Link(members=[nodes[1], nodes[2]])
link2 = request.Link(members=[nodes[2], nodes[3]])
link3 = request.Link(members=[nodes[3], nodes[4]])
link4 = request.Link(members=[nodes[4], nodes[1]])
>>>>>>> parent of 50dea8b... fix list indexing


# output request
pc.printRequestRSpec(request)


#  old code here:

# configure VMs here:
#  node1 = mkVM('node1', GLOBALS.UBUNTU18_IMG, cores=4, ram=8)
#  node2 = mkVM('node2', GLOBALS.UBUNTU18_IMG, cores=4, ram=8)
#  node3 = mkVM('node3', GLOBALS.UBUNTU18_IMG, cores=4, ram=8)
#  node4 = mkVM('node4', GLOBALS.UBUNTU18_IMG, cores=4, ram=8)

# run the install.sh script on each vm to install software
#  node1.addService(rspec.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
#  node1.addService(rspec.Execute(shell="sh", command="/local/repository/install.sh"))

#  node2.addService(rspec.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
#  node2.addService(rspec.Execute(shell="sh", command="/local/repository/install.sh"))

#  node3.addService(rspec.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
#  node3.addService(rspec.Execute(shell="sh", command="/local/repository/install.sh"))

#  node4.addService(rspec.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
#  node4.addService(rspec.Execute(shell="sh", command="/local/repository/install.sh"))

# Add links between nodes (form a "circle" of connectivity)
#  link1 = request.Link(members=[node1, node2])
#  link2 = request.Link(members=[node2, node3])
#  link3 = request.Link(members=[node3, node4])
#  link4 = request.Link(members=[node4, node1])
