# Getting Started

**POWDER Setup**

Create a POWDER profile - the provided profiles contained in profile.py or simple_profile.py provide good starting points. Any number of nodes can be used in the profile.

**NFD (Named Data Networking Forwarding Daemon):**

Install NFD on nodes if necessary (if one of the provided profiles is used, the software will automatically be installed). If not, detailed instructions can be found here: http://named-data.net/doc/NFD/current/INSTALL.html (note that installing from the PPA repository with apt-get is much simpler than building from source).

The NDN forwarding daemon should start automatically. This can be verified with `nfd-status`, which will output some useful NFD information. To manually start and stop the forwarder, use `nfd-start` and `nfd-stop`.

To send data between NDN nodes, some setup is necessary. To forward data, NFD relies on "faces", its own abstraction of interface. These faces can be TCP or UDP tunnels, Ethernet connections, local Unix sockets, etc. These faces are manipulated with the `nfdc face` command. For example, to see a list of existing faces, use `nfdc face list`.

NFD also requires that routes be created, so data can be forwarded to its correct location. Routes can be manipulated with the `nfdc route` command.

For example, to connect two NDN nodes over a UDP tunnel, first add a UDP face to each node. On the first node, run `nfdc face create udp4://<NODE_2_IPv4_ADDRESS_HERE>`. On the second node, run `nfdc face create udp4://<NODE_1_IPv4_ADDRESS_HERE>`. Note that IP addesses and other useful network information can be found with the `ifconfig` command.
Next, create a route to tell the first node where to find data named under the prefix "/ndn/node2". Run the command `nfdc route add prefix /ndn/node2 nexthop udp4://<NODE_2_IPv4_ADDRESS_HERE>`. Now, any interest packets that reach the first node that have the prefix "/ndn/node2" will be forwarded to the second node.


**Testing**

Send test packets between nodes with `ndnpoke` and `ndnpeek`. If the PPA repository previously mentioned has been set up, these tools can easily be installed with `apt-get`. If not, they can be built from source. 

To test our previous example, enter `echo "Hello World!" | ndnpoke /ndn/node2/hello` on the second node. This will host one data packet on the second node containing the string "Hello World!" with the name "/ndn/node2/hello". To request this data from the first node, enter `ndnpeek -p /ndn/node2/hello`. If everything has been set up correctly, the first node will print "Hello World!" to stdout, indicating success!

**NLSR (Named-Data Link State Routing) Setup**

Install NLSR from the PPA repository or build from source. Modify the provided configuration file to appropriatly name routers and their neighbors (if a two-node network was used, the network should be automatically configured properly). The advertising section of the configuration files can also be modified to tell the network what data is available where.
