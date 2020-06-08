# Getting Started

**Instructions:**

Create a POWDER profile - the provided profile contained in profile.py provides a good starting point. Any number of nodes can be used, just be sure they are linked together in the geni-lab script. (note that only two can be linked per Link or Interface object)

Install NFD, NLSR, and NDNtools on nodes if neccessary (if the provided profile is used, the software will automatically be installed)
Detailed instructions can be found here: http://named-data.net/doc/NFD/current/INSTALL.html (note that installing from the PPA repository with apt-get is much simpler than building from source)

The NDN forwarding daemon should start automatically. This can be checked with `nfd-status`. To manually start and stop the forwarder, use `nfd-start` and `nfd-stop`.

Create routes between nodes with `nfdc route add`. For example, to create a udp tunnel that serves all names under /ndn/hello, use: `nfdc route add prefix /ndn/hello nexthop <face-uri | face-id>`
Faces (and their respective URIS or IDs) for creating routes can be found with `nfdc face list`.

Send test packets between nodes with `echo "Hello World" | ndnpoke /ndn/demo/hello` and `ndnpeek -p /ndn/demo/hello`.



