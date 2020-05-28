"""A base profile for experimenting with NDN over wired connections."""

import geni.portal as portal 
import geni.rspec.pg as pg 
import geni.rspec.emulab as elab


class GLOBALS(object):
    """useful constant values for setting up a powder experiment""" 
    SITE_URN = "urn:publicid:IDN+emulab.net+authority+cm"
    # standard Ubuntu release
    UBUNTU18_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
    PNODE_D740 = "d740"  # 24 cores, 192 GB RAM PNODE_D840 = "d840"  # 64 cores, 768 GB RAM


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
pc = portal.Context() request = pc.makeRequestRSpec()

# Declare dedicated VM host
pnode = request.RawPC('pnode') pnode.hardware_type = GLOBALS.PNODE_D740


def create_nodes(count=4, cores=4, ram=8):
    """Allocates and runs an install script on a specified number of VM nodes"""

    nodes = []
    # index nodes by their proper number (not zero-indexed)
    nodes.append(None)

    # create each VM
    for i in range(1, count+1): nodes.append(mkVM('node' + str(i),
        GLOBALS.UBUNTU18_IMG, cores=cores, ram=ram))

    # run the install.sh script on each vm to install software
    for node in nodes: 
        if node != None:
            node.addService(pg.Execute(shell="sh", command="chmod +x /local/repository/install.sh"))
            node.addService(pg.Execute(shell="sh", command="/local/repository/install.sh"))

    return nodes


def create_link(node1_num, node2_num):
    """Creates a link with conveniently-named ip addresses between the two specfied node numbers.""" 

    iface1 = nodes[node1_num].addInterface("if" + str(node1_num) + str (node2_num))
    iface1.component_id = "eth" + str(node2_num)
    iface1.addAddress(pg.IPv4Address("10.10." + str(node1_num) + "." + str(node2_num), "255.255.255.0")) 

    iface2 = nodes[node2_num].addInterface("if" + str(node2_num) + str (node1_num))
    iface2.component_id = "eth" + str(node1_num)
    iface2.addAddress(pg.IPv4Address("10.10." + str(node2_num) + "." + str(node1_num), "255.255.255.0")) 

    link = request.LAN("lan" + str(node1_num) + str(node2_num))
    link.addInterface(iface1) link.addInterface(iface2)


# create nodes
nodes = create_nodes()

# establish connectivity
create_link(1,2)
create_link(2,3)
create_link(3,4)
create_link(4,1)

# output request
pc.printRequestRSpec(request)
