# Experimental Notes

**Things we've learned:**
* Use `ndnpeek` and `ndnpoke` to transmit request and data packets
	*  `ndnpoke` transmits a single data packet; however, multiple requests for that data can be satisfied if the data is cached in the Content Store.
* Routes are one-way, and they must exist in the RIB before interests can be satisfied
* `nfd-status` prints lots of useful information



**Questions to ask:**
* What are the channels found with the `nfdc channel list` command? How are they different from the faces found with `nfdc face list`
* Figure out how to add ethernet faces - we're stuck here


**Helpful hints:**
* Use `ifconfig` or `ip link` to find MAC addresses of the various VMs.
* NFD configuration file is located at /etc/ndn/nfd.conf
* See FAQ for setting up ethernet faces
* Use `nfdc` to view all subcommands
* Use the `nfdc cs` commands to manipulate the content store
* ndn-traffic-generator (`ndn-traffic-server` and `ndn-traffic-client`) may need to be run from a bash shell, not the defualt c shell

