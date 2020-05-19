#!/usr/bin/env python
import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN


tourDescription = """

# srsLTE Controlled RF

Use this profile to intantiate and end-to-end LTE network in a controlled RF
environment (SDRs with wired connections) using the lates srsLTE release.

The following nodes will be deployed:

* Intel NUC5300/B210 w/ srsLTE (`rue1`)
* Intel NUC5300/B210 w/ srsLTE (`enb1`)

"""

tourInstructions = """
"""


class GLOBALS(object):
    UBUNTU_1804_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
    SRSLTE_IMG = "urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE"
    NUC_HWTYPE = "nuc5300"


pc = portal.Context()
request = pc.makeRequestRSpec()

# Add a NUC eNB node
enb1 = request.RawPC("enb1")
enb1.hardware_type = GLOBALS.NUC_HWTYPE
enb1.disk_image = GLOBALS.SRSLTE_IMG
enb1.Desire("rf-controlled", 1)
enb1_rue1_rf = enb1.addInterface("rue1_rf")
enb1.addService(rspec.Execute(shell="bash", command="/local/repository/tune-cpu.sh"))

# Add a NUC UE node
rue1 = request.RawPC("rue1")
rue1.hardware_type = GLOBALS.NUC_HWTYPE
rue1.disk_image = GLOBALS.SRSLTE_IMG
rue1.Desire("rf-controlled", 1)
rue1_enb1_rf = rue1.addInterface("enb1_rf")
rue1.addService(rspec.Execute(shell="bash", command="/local/repository/tune-cpu.sh"))

# Create the RF link between the UE and eNodeB
rflink = request.RFLink("rflink")
rflink.addInterface(enb1_rue1_rf)
rflink.addInterface(rue1_enb1_rf)

link = request.Link("lan")
link.addNode(rue1)
link.addNode(enb1)
link.link_multiplexing = True
link.vlan_tagging = True
link.best_effort = True

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)

pc.printRequestRSpec(request)
