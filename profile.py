# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

tourDescription = """
3 server nodes each running a different service connected to user nodes over vlan

"""

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Client image list
imageList = [
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD', 'UBUNTU 18.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//CENTOS8-64-STD', 'CENTOS 8'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//CENTOS7-64-STD', 'CENTOS 7'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//FBSD131-64-STD', 'FreeBSD 13.1'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//FBSD123-64-STD', 'FreeBSD 12.3'),
]

# Server image list, not tested with CentOS
imageList2 = [
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD', 'UBUNTU 18.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//FBSD131-64-STD', 'FreeBSD 13.1'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//FBSD123-64-STD', 'FreeBSD 12.3'),
]

# Do not change these unless you change the setup scripts too.
nfsServerName = "nfs"
nfsLanName    = "nfsLan"
nfsDirectory  = "/nfs"

# Number of NFS clients (there is always a server)
pc.defineParameter("usrCount", "Number of User nodes",
                   portal.ParameterType.INTEGER, 4)

pc.defineParameter("osImage", "Select OS image for clients",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList)

pc.defineParameter("osServerImage", "Select OS image for servers",
                   portal.ParameterType.IMAGE,
                   imageList2[0], imageList2)

pc.defineParameter("nfsSize", "Size of NFS Storage",
                   portal.ParameterType.STRING, "200GB",
                   longDescription="Size of disk partition to allocate on NFS server")

# Always need this when using parameters
params = pc.bindParameters()

# The NFS network. All these options are required.
nfsLan = request.LAN(nfsLanName)
nfsLan.best_effort       = True
nfsLan.vlan_tagging      = True
nfsLan.link_multiplexing = True

# The NFS server.
nfsServer = request.RawPC(nfsServerName)
nfsServer.disk_image = params.osServerImage
# Attach server to lan.
ifaceNFS=nfsServer.addInterface("ifNFS")
ifaceNFS.component_id = "ethNFS"
ifaceNFS.addAddress(pg.IPv4Address("192.168.1.25", "255.255.255.0"))
nfsLan.addInterface(ifaceNFS)
# Storage file system goes into a local (ephemeral) blockstore.
nfsBS = nfsServer.Blockstore("nfsBS", nfsDirectory)
nfsBS.size = params.nfsSize
# Initialization script for the server
nfsServer.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/nfs-server.sh"))

# The Email server.
emailServer = request.RawPC("emailServer")
emailServer.disk_image = params.osServerImage
ifaceEM=emailServer.addInterface("ifEM")
ifaceEM.component_id = "ethEM"
ifaceEM.addAddress(pg.IPv4Address("192.168.1.26", "255.255.255.0"))
nfsLan.addInterface(ifaceEM)
emailServer.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/email-server.sh"))

# The DNS server
dnsServer = request.RawPC("dnsServer")
dnsServer.disk_image = params.osServerImage
ifaceDNS=dnsServer.addInterface("ifDNS")
ifaceDNS.component_id = "ethDNS"
ifaceDNS.addAddress(pg.IPv4Address("192.168.1.27", "255.255.255.0"))
nfsLan.addInterface(ifaceDNS)
dnsServer.addService(pg.Execute(shell="sh", command="sudo bin/bash /local/repository/dns-server.sh"))

# The user nodes, also attached to the lan.
for i in range(1, params.usrCount+1):
    node = request.RawPC("node%d" % i)
    node.disk_image = params.osImage
    iface=node.addInterface("eth%d" % i)
    iface.addAddress(pg.IPv4Address("192.168.1.%d" % i, "255.255.255.0"))
    nfsLan.addInterface(iface)
    # Initialization script for the clients
    node.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/nfs-client.sh"))
    pass

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
