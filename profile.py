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

Use this profile to intantiate an end-to-end LTE network in a controlled RF
environment (wired connections between UE and eNB). The UE can be srsLTE-based
or a Nexus 5.

If you elect to use a Nexus 5, these nodes will be deployed:

* Nexus 5 (`rue1`)
* Generic Compute Node w/ ADB image (`adbnode`)
* Intel NUC5300/B210 w/ srsLTE eNB/EPC (`enb1`)

If instead you choose to use an srsLTE UE, these will be deployed:

* Intel NUC5300/B210 w/ srsLTE (`rue1`) or
* Intel NUC5300/B210 w/ srsLTE eNB/EPC (`enb1`)

"""

tourInstructions = """

### Prerequisites: ORAN Setup

You should have already started up an O-RAN experiment connected to the
same shared VLAN you specified during the "parameterize" step.  Make
sure it is up and fully deployed first - see the instructions included
in that profile.  However, DO NOT start the srsLTE components as
directed in those instructions.  DO start the `kpimon` and `nexran`
xApps as instructed, but first you must make a small change to the
`kpimon` configuration file.

Edit `/local/profile-public/scp-kpimon-config-file.json` to change the
eNodeB identifier.  Find the line that shows:

```
ranList=enB_macro_661_8112_0019b0
```

And change it to:

```
ranList=enB_macro_XXX_YYYY_0019b0
```

Save the changes.

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

You should see `srsenb` send periodic `kpimon` reports.  These will
appear in the `kpimon` xApp log output as well in your ORAN experiment.

### Nexus 5

If you've deployed a Nexus 5, you should see it sync with the eNB eventually and
obtain an IP address. Login to `adbnode` in order to access `rue1` via `adb`:

```
# on `adbnode`
pnadb -a
adb shell
```

Once you have an `adb` shell to `rue1`, you can use `ping` to test the
connection, e.g.,

```
# in adb shell connected to rue1
# ping SGi IP
ping 172.16.0.1
```

If the Nexus 5 fails to sync with the eNB, try rebooting it via the `adb` shell.
After reboot, you'll have to repeat the `pnadb -a` and `adb shell` commands on
`adbnode` to reestablish a connection to the Nexus 5.

### srsLTE UE

If you've deployed an srsLTE UE, login to `rue1` and do:

```
/local/repository/bin/start.sh
```

This will start a `tmux` session with two panes: one running srsue and the other
holding a spare terminal for running tests with `ping` and `iperf`. Again, if
you'd like to run `srsue` manually, do:

```
sudo srsue /etc/srslte/ue.conf
```

"""


class GLOBALS(object):
    NUC_HWTYPE = "nuc5300"
    COTS_UE_HWTYPE = "nexus5"
    UBUNTU_1804_IMG = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
    SRSLTE_IMG = "urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1"
    COTS_UE_IMG = URN.Image(PN.PNDEFS.PNET_AM, "PhantomNet:ANDROID444-STD")
    ADB_IMG = URN.Image(PN.PNDEFS.PNET_AM, "PhantomNet:UBUNTU14-64-PNTOOLS")


pc = portal.Context()
pc.defineParameter("ue_type", "UE Type", portal.ParameterType.STRING, "srsue",
                   [("srsue", "srsLTE UE (B210)"), ("nexus5", "COTS UE (Nexus 5)")],
                   longDescription="Type of UE to deploy.")

pc.defineParameter("enb_node", "eNodeB Node ID",
                   portal.ParameterType.STRING, "", advanced=True,
                   longDescription="Specific eNodeB node to bind to.")

pc.defineParameter("ue_node", "UE Node ID",
                   portal.ParameterType.STRING, "", advanced=True,
                   longDescription="Specific UE node to bind to.")
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
enb1_rue1_rf = enb1.addInterface("rue1_rf")
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

# Add a UE node
if params.ue_type == "nexus5":
    adbnode = request.RawPC("adbnode")
    adbnode.disk_image = GLOBALS.ADB_IMG
    rue1 = request.UE("rue1")
    rue1.hardware_type = GLOBALS.COTS_UE_HWTYPE
    rue1.disk_image = GLOBALS.COTS_UE_IMG
    rue1.adb_target = "adbnode"
elif params.ue_type == "srsue":
    rue1 = request.RawPC("rue1")
    rue1.hardware_type = GLOBALS.NUC_HWTYPE
    rue1.disk_image = GLOBALS.SRSLTE_IMG
    rue1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/update-config-files.sh"))
    rue1.addService(rspec.Execute(shell="bash", command="/local/repository/tune-cpu.sh"))

rue1.component_id = params.ue_node
rue1.Desire("rf-controlled", 1)
rue1_enb1_rf = rue1.addInterface("enb1_rf")

# Create the RF link between the UE and eNodeB
rflink = request.RFLink("rflink")
rflink.addInterface(enb1_rue1_rf)
rflink.addInterface(rue1_enb1_rf)

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)

pc.printRequestRSpec(request)
