#!/usr/bin/env python
import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN
import geni.urn as URN


tourDescription = """

# srsLTE Controlled RF

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

### Start EPC and eNB

After your experiment becomes ready, login to `enb1` via `ssh` and do:

```
/local/repository/bin/start.sh
```

This will start a `tmux` session with three panes, running `srsepc` and
`srsenb`, and then leaving your cursor in the last pane. After you've associated
a UE with this eNB, you can use the third pane to run tests with `ping` or
`iperf`. If you are not familiar with `tmux`, it's a terminal multiplexer that
has some similarities to screen. Here's a [tmux cheat
sheet](https://tmuxcheatsheet.com), but `ctrl-b o` (move to other pane) and
`ctrl-b x` (kill pane), should get you pretty far. `ctrl-b d` will detach you
from the `tmux` session and leave it running in the background. You can reattach
with `tmux attach`.

If you'd like to start `srsepc` and `srsenb` manually, here are the commands:

```
# start srsepc
sudo srsepc /etc/srslte/epc.conf

# start srsenb
sudo srsenb /etc/srslte/enb.conf
```

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
pc.defineParameter("ue_type", "UE Type", portal.ParameterType.STRING, "nexus5",
                   [("srsue", "srsLTE UE (B210)"), ("nexus5", "COTS UE (Nexus 5)")],
                   longDescription="Type of UE to deploy.")

params = pc.bindParameters()
pc.verifyParameters()
request = pc.makeRequestRSpec()

# Add a NUC eNB node
enb1 = request.RawPC("enb1")
enb1.hardware_type = GLOBALS.NUC_HWTYPE
enb1.disk_image = GLOBALS.SRSLTE_IMG
enb1.Desire("rf-controlled", 1)
enb1_rue1_rf = enb1.addInterface("rue1_rf")
enb1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/update-config-files.sh"))
enb1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/tune-cpu.sh"))
enb1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/add-nat-and-ip-forwarding.sh"))

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
