# Project Title: Benchmarking Network Services Using the POWDER Wireless Testbed 
**Author:** Dillon Horton dhorto23@students.kennesaw.edu

**Abstract:** 5G RAN slicing provides a way to split network infrastructure into self-contained slices which can have various virtual network functions (VNFs) mapped onto them. Much work has gone into creating robust mapping and resource allocation algorithms in order to efficiently embed VNFs onto the available nodes in a slice. However, in order to most efficiently embed these VNFs we need to understand the resource and bandwidth needs of the services we are trying to embed. This project seeks to provide an accurate assessment of the needs of three commonly used network services. We do this by testing each network service using real world physical machines on the POWDER network testbed. We collect bandwidth and CPU usage data from each test and use it to analyze the needs of the network service when being embedded onto physical nodes during network slicing.


## Note
Testing using this code requires creating an account on the POWDER wireless network testbed and creating a profile and experiment(see https://docs.powderwireless.net/ for more details). I have only tested functionality of the testing scenarios using Ubuntu on all the nodes. Running the testing bash files will require you to give them the host name of the server node you are using which will change between test runs based on which nodes POWDER provides for use. 
