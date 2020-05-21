# Getting Started

**To-do:**
* Install and experiment with ndn-tools
* Understand testbed interfaces
* Experiment with nlsr software, and potentially add it to the auto-download script
  * configuration files?
* Experiment with ndn client-side libraries
* Better understand the routing software
  * configuration files?
  * autogenerate routes to producers
  * avoid manual setup of routes
* Experiment with ndn traffic generators

**Instructions:**

Create a POWDER profile - the provided profile contained in powder_test.py provides a good starting point. Any number of nodes can be used, just be sure they are linked together in the geni-lab script. (note that only two can be linked per Link or Interface object)

Install NFD software on nodes if neccessary (if the provided profile is used, the software will automatically be installed)
Detailed instructions can be found here: http://named-data.net/doc/NFD/current/INSTALL.html (note that installing from the PPA repository with apt-get is much simpler than building from source)

Start the NDN forwarding daemon on each node with `nfd-start`.

Create routes between nodes with `nfdc route add`.
Faces for creating routes can be found with `nfdc face list`.

Send test packets between nodes with `echo "Hello World" | ndnpoke /ndn/demo/hello` and `ndnpeek -p /ndn/demo/hello`.

**Notes:**

Use `ifconfig` or `ip link` to find MAC addresses of the various VMs.


