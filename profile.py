#!/usr/bin/env python
import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN
import geni.urn as URN


tourDescription = """

## srsLTE Controlled RF with shared vlan support (primarily for ORAN)

---

IMPORTANT: DO NOT start this expirment until you have first instantiated a
companion O-RAN experiment via the following profile:

  https://www.powderwireless.net/p/PowderProfiles/O-RAN

Furthermore, DO NOT start the srsLTE services in that experiment as
directed.  See the instructions in this profile for more information.

---

Use this profile to instantiate an end-to-end srsLTE network in a controlled RF
environment (wired connections between UE and eNB).

The following resources will be allocated:

  * Intel NUC5300/B210 w/ srsLTE UE(s) 
    * 1 or 2, depending on "Number of UEs" parameter: `rue1`, `rue2`
  * Intel NUC5300/B210 w/ srsLTE eNB/EPC (`enb1`)

"""

tourInstructions = """

### Prerequisites: ORAN Setup

You should have already started up an O-RAN experiment connected to
the same shared VLAN you specified during the "parameterize" step.
Make sure it is up and fully deployed first - see the instructions
included in that profile.  However, DO NOT start the srsLTE components
or `kpimon` xApp as directed in those instructions.

First, log in to `node-0` in your O-RAN experiment and edit
`/local/profile-public/scp-kpimon-config-file.json` to change the
eNodeB identifier.  Find the line that shows:

```
"ranList":"enB_macro_661_8112_0019b0"
```

And change it to:

```
"ranList":"enB_macro_14156_321_0019b0"
```

Don't forget to save the changes.

Next, make note of the `e2term-sctp` service's IP address in the ORAN
experiment.  To do that, open an SSH session to `node-0` in that
experiment and run:

```
# Extract `e2term-sctp` IP address
kubectl get svc -n ricplt --field-selector metadata.name=service-ricplt-e2term-sctp-alpha -o jsonpath='{.items[0].spec.clusterIP}'
```

You will need this address when starting the srsLTE eNodeB service.

### Start EPC and eNB

Login to `enb1` via `ssh` and start the srsLTE EPC services:

```
# start srsepc
sudo srsepc
```

Then in another SSH session on `enb1`, start the eNB service.
Substitute the IP address (or set it as an environment variable) in
this command for the one captured for the `e2term-sctp` ORAN service
in the previous step.

```
# start srsenb (with agent connectivity to ORAN RIC)
sudo srsenb --ric.agent.remote_ipv4_addr=${E2TERM_IP} --log.all_level=warn --ric.agent.log_level=debug --log.filename=stdout
```

There will be output in srsenb and the O-RAN e2term mgmt and other
service logs showing that the enb has connected to the O-RAN RIC.

### Start the `kpimon` xApp

Go back to the instructions in the O-RAN profile and follow the steps
for starting the `kpimon` xApp (start with step 3 under "Running the
O-RAN/srsLTE scp-kpimon demo").

You should start seeing `srsenb` send periodic reports once the
`kpimon` xApp starts.  These will appear in the `kpimon` xApp log
output as well in the srsenb output.

### Start the srsLTE UE

SSH to `rue1` and run:

```
sudo srsue
```

You should see changes in the `kpimon` output when `srsue` is
connected.  Try pinging `172.16.0.1` (the srs SPGW gateway address)
from the UE and watch the `kpimon` counters tick.

"""


class GLOBALS(object):
    NUC_HWTYPE = "nuc5300"
    UBUNTU_1804_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
    SRSLTE_IMG = "urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1"

pc = portal.Context()
pc.defineParameter("num_ues", "Number of NUC+B210 srsLTE UEs to allocate",
                   portal.ParameterType.INTEGER, 1, [1,2])
pc.defineParameter("enb_node", "eNodeB Node ID",
                   portal.ParameterType.STRING, "", advanced=True,
                   longDescription="Specific eNodeB node to bind to.")

pc.defineParameter(
    "multiplexLans", "Multiplex Networks",
    portal.ParameterType.BOOLEAN,True,
    longDescription="Multiplex any networks over physical interfaces using VLANs.  Some physical machines have only a single experiment network interface, so if you want multiple links/LANs, you have to enable multiplexing.  Currently, if you select this option.",
    advanced=True)
pc.defineParameter(
    "connectSharedVlan","Shared VLAN Name",
    portal.ParameterType.STRING,"",
    longDescription="Connect `enb1` to a shared VLAN.  This allows your srsLTE experiment to connect to another experiment (e.g., one running ORAN services). The shared VLAN must already exist.",
    advanced=True)
pc.defineParameter(
    "sharedVlanAddress","Shared VLAN IP Address",
    portal.ParameterType.STRING,"10.254.254.100/255.255.255.0",
    longDescription="Set the IP address and subnet mask for the shared VLAN interface.  Make sure you choose an unused address within the subnet of an existing shared vlan!  Also ensure that you specify the subnet mask as a dotted quad.",
    advanced=True)
pc.defineParameter(
    "oranAddress","ORAN Services Gateway Address",
    portal.ParameterType.STRING,"10.254.254.1",
    longDescription="The IP address of the ORAN services gateway running on an adjacent experiment connected to the same shared VLAN.",
    advanced=True)

params = pc.bindParameters()

# Handle shared vlan address param.
(sharedVlanAddress,sharedVlanNetmask) = (None,None)
if params.sharedVlanAddress:
    aa = params.sharedVlanAddress.split('/')
    if len(aa) != 2:
        perr = portal.ParameterError(
            "Invalid shared VLAN address!",
            ['sharedVlanAddress'])
        pc.reportError(perr)
    else:
        (sharedVlanAddress,sharedVlanNetmask) = (aa[0],aa[1])

pc.verifyParameters()
request = pc.makeRequestRSpec()

# Add a NUC eNB node
enb1 = request.RawPC("enb1")
enb1.component_id = params.enb_node
enb1.hardware_type = GLOBALS.NUC_HWTYPE
enb1.disk_image = GLOBALS.SRSLTE_IMG
enb1.Desire("rf-controlled", 1)
enb1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/tune-cpu.sh"))
enb1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/setup-ip-config.sh %s" % params.oranAddress))
enb1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/update-config-files.sh"))
enb1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/setup-srslte.sh"))

# Connect enb1 to shared vlan, if requested.
if params.connectSharedVlan:
    shiface = enb1.addInterface("ifSharedVlan")
    if sharedVlanAddress:
        shiface.addAddress(
            rspec.IPv4Address(sharedVlanAddress,sharedVlanNetmask))
    sharedvlan = request.Link('shared-vlan')
    sharedvlan.addInterface(shiface)
    sharedvlan.connectSharedVlan(params.connectSharedVlan)
    if params.multiplexLans:
        sharedvlan.link_multiplexing = True
        sharedvlan.best_effort = True

# Add a srsLTE SDR-based UE nodes
for i in range(1,params.num_ues+1):
    ue = request.RawPC("rue%d" % i)
    ue.hardware_type = GLOBALS.NUC_HWTYPE
    ue.disk_image = GLOBALS.SRSLTE_IMG
    ue.addService(rspec.Execute(shell="bash", command="/local/repository/bin/update-config-files.sh"))
    ue.addService(rspec.Execute(shell="bash", command="/local/repository/tune-cpu.sh"))
    ue.Desire("rf-controlled", 1)
    # Create the RF link between the UE and eNodeB
    rflink = request.RFLink("rflink%d" % i)
    ue_enb1_rf = ue.addInterface("enb1_rf")
    enb1_ue_rf = enb1.addInterface("rue%d_rf" % i)
    rflink.addInterface(enb1_ue_rf)
    rflink.addInterface(ue_enb1_rf)

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)

pc.printRequestRSpec(request)
