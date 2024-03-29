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
hardware      = "d710"

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
nfsServer.hardware_type = hardware
nfsServer.disk_image = params.osServerImage
# Attach server to lan.
nfsLan.addInterface(nfsServer.addInterface())
# Storage file system goes into a local (ephemeral) blockstore.
nfsBS = nfsServer.Blockstore("nfsBS", nfsDirectory)
nfsBS.size = params.nfsSize
# Initialization script for the server
nfsServer.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/nfs-server.sh"))
nfsServer.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/mongo-setup.sh"))
# The Email server.
emailServer = request.RawPC("emailServer")
emailServer.hardware_type = hardware
emailServer.disk_image = params.osServerImage
nfsLan.addInterface(emailServer.addInterface())
emailServer.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/email-server.sh"))
emailServer.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/mongo-setup.sh"))

# The DNS server
dnsServer = request.RawPC("dnsServer")
dnsServer.hardware_type = hardware
dnsServer.disk_image = params.osServerImage
nfsLan.addInterface(dnsServer.addInterface())
dnsServer.addService(pg.Execute(shell="sh", command="sudo bin/bash /local/repository/dns-server.sh"))
dnsServer.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/mongo-setup.sh"))

""" Potential setup for MongoDB server 
dbServer = request.RawPC("dbServer")
dbServer.hardware_type = hardware
dbServer.disk_image = params.osServerImage
nfsLan.addInterface(dbServer.addInterface())
dbServer.addService(pg.Execute(shell="sh", command="sudo bin/bash /local/repository/mongodb.sh")
"""

# The user nodes, also attached to the lan.
for i in range(1, params.usrCount+1):
    node = request.RawPC("node%d" % i)
    node.hardware_type = hardware
    node.disk_image = params.osImage
    nfsLan.addInterface(node.addInterface())
    # Initialization script for the clients
    node.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/nfs-client.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /bin/bash /local/repository/mongo-setup.sh"))
    pass

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
