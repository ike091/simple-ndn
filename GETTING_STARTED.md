# Getting Started

**POWDER Setup**

Create a POWDER profile - the provided profile contained in profile.py provides a good starting point. Any number of nodes can be used, just be sure they are connected somehow in the geni-lab script. 

**NFD (Named Data Networking Forwarding Daemon):**

Install NFD on nodes if necessary (if the provided profile is used, the software will automatically be installed). Detailed instructions can be found here: http://named-data.net/doc/NFD/current/INSTALL.html (note that installing from the PPA repository with apt-get is much simpler than building from source).

The NDN forwarding daemon should start automatically. This can be checked with `nfd-status`. To manually start and stop the forwarder, use `nfd-start` and `nfd-stop`.

Create routes between nodes with `nfdc route add`. For example, to create a UDP tunnel that serves all names under /ndn/hello, use: `nfdc route add prefix /ndn/hello nexthop <face-uri | face-id>`.
Faces (and their respective URIS or IDs) for creating routes can be found with `nfdc face list`.

**Testing**

Send test packets between nodes with `ndnpoke` and `ndnpeek`. If the PPA repository previously mentioned has been set up, these tools can easily be installed from it. If not, they can be built from source. For example, on the producer node, enter `echo "Hello World" | ndnpoke /ndn/demo/hello`. This will host one data packet containing the string "Hello World" located at `/ndn/demo/hello`. To request this data from another consumer node, use `ndnpeek -p /ndn/demo/hello`. 

**NLSR (Named-Data Link State Routing) Setup**

Install NLSR from the PPA repository or build from source. Modify the provided configuration file to appropriatly name routers and their neighbors.
