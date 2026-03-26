# Lab 7 - OSPF Routing Protocol Configuration
## Complete Solution with Step-by-Step Guide

---

## Lab Objectives

1. To construct a network for demonstration of the operation of OSPF routing protocol using Cisco Packet Tracer
2. To show the connectivity between nodes in a network using OSPF on all routers

---

## Network Topology

```
                          Network 2
                        10.10.10.0/24
                             |
                            PC2
                             |
                           Fa0/0
                             |
                   S0/0/0   R2   S0/0/1
                           /  \  DCE
             192.168.10.0/30  \  192.168.10.8/30
    Network 1    64 kbps        \    128 kbps     Network 3
  172.16.1.16/28   |             \      |      172.16.1.32/29
         |      S0/0/0            \   S0/0/1         |
        PC1       |                \    |          PC3
         |      DCE                  \ R3            |
       Fa0/0      |                   Fa0/0        Fa0/0
         |       R1                     |
         |    S0/0/1   256 kbps   S0/0/0
         |      DCE  \____________/
         |            192.168.10.4/30
```

---

## Part 1: Complete Addressing Table with Calculations

### Network Addressing Summary

| Network Name | Network Address | CIDR | Subnet Mask | Usable Range | Broadcast | Hosts |
|--------------|----------------|------|-------------|--------------|-----------|-------|
| Network 1 | 172.16.1.16 | /28 | 255.255.255.240 | .17 - .30 | 172.16.1.31 | 14 |
| Network 2 | 10.10.10.0 | /24 | 255.255.255.0 | .1 - .254 | 10.10.10.255 | 254 |
| Network 3 | 172.16.1.32 | /29 | 255.255.255.248 | .33 - .38 | 172.16.1.39 | 6 |
| WAN Link 1 (R1-R2) | 192.168.10.0 | /30 | 255.255.255.252 | .1 - .2 | 192.168.10.3 | 2 |
| WAN Link 2 (R1-R3) | 192.168.10.4 | /30 | 255.255.255.252 | .5 - .6 | 192.168.10.7 | 2 |
| WAN Link 3 (R2-R3) | 192.168.10.8 | /30 | 255.255.255.252 | .9 - .10 | 192.168.10.11 | 2 |

### Complete Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway |
|--------|-----------|------------|-------------|-----------------|
| **R1** | Fa0/0 | 172.16.1.17 | 255.255.255.240 | N/A |
| | S0/0/0 (DCE) | 192.168.10.1 | 255.255.255.252 | N/A |
| | S0/0/1 (DCE) | 192.168.10.5 | 255.255.255.252 | N/A |
| | Loopback 0 | 10.1.1.1 | 255.255.255.255 | N/A |
| **R2** | Fa0/0 | 10.10.10.1 | 255.255.255.0 | N/A |
| | S0/0/0 | 192.168.10.2 | 255.255.255.252 | N/A |
| | S0/0/1 (DCE) | 192.168.10.9 | 255.255.255.252 | N/A |
| | Loopback 0 | 10.2.2.2 | 255.255.255.255 | N/A |
| **R3** | Fa0/0 | 172.16.1.33 | 255.255.255.248 | N/A |
| | S0/0/0 | 192.168.10.6 | 255.255.255.252 | N/A |
| | S0/0/1 | 192.168.10.10 | 255.255.255.252 | N/A |
| | Loopback 0 | 10.3.3.3 | 255.255.255.255 | N/A |
| **PC1** | NIC | 172.16.1.18 | 255.255.255.240 | 172.16.1.17 |
| **PC2** | NIC | 10.10.10.2 | 255.255.255.0 | 10.10.10.1 |
| **PC3** | NIC | 172.16.1.34 | 255.255.255.248 | 172.16.1.33 |

---

## Part 2: OSPF Configuration Overview

### OSPF Basics

**OSPF (Open Shortest Path First)** is a link-state routing protocol that uses the Dijkstra algorithm to calculate the shortest path tree.

**Key Features:**
- Open standard protocol
- Supports VLSM/CIDR
- Fast convergence
- Scalable with areas
- Classless routing protocol
- Uses cost metric (10⁸/bandwidth)

**OSPF Terminology:**
- **Router ID**: Unique identifier for each OSPF router
- **Area**: Logical grouping of networks (Area 0 = backbone)
- **Cost**: Metric based on bandwidth (10⁸/bandwidth in bps)
- **Neighbor**: Adjacent OSPF router
- **DR/BDR**: Designated Router/Backup DR (on multi-access networks)
- **LSA**: Link State Advertisement
- **SPF**: Shortest Path First algorithm

---

## Part 3: Step-by-Step Configuration

### Task 1: Prepare the Network

**In Cisco Packet Tracer:**
1. Add devices: 3 Routers (2811 or similar), 3 PCs, 3 Switches
2. Connect as per topology diagram
3. Label all devices

---

### Task 2: Perform Basic Router Configurations

#### Router R1 - Basic Configuration

```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R1
R1(config)# no ip domain-lookup
R1(config)# enable secret class
R1(config)# line console 0
R1(config-line)# password cisco
R1(config-line)# login
R1(config-line)# logging synchronous
R1(config-line)# exit
R1(config)# line vty 0 4
R1(config-line)# password cisco
R1(config-line)# login
R1(config-line)# exit
R1(config)# banner motd #Unauthorized Access Prohibited#

! Configure FastEthernet 0/0
R1(config)# interface FastEthernet0/0
R1(config-if)# ip address 172.16.1.17 255.255.255.240
R1(config-if)# description LAN Network 1
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure Serial 0/0/0 (DCE to R2)
R1(config)# interface Serial0/0/0
R1(config-if)# ip address 192.168.10.1 255.255.255.252
R1(config-if)# description Link to R2
R1(config-if)# clock rate 64000
R1(config-if)# bandwidth 64
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure Serial 0/0/1 (DCE to R3)
R1(config)# interface Serial0/0/1
R1(config-if)# ip address 192.168.10.5 255.255.255.252
R1(config-if)# description Link to R3
R1(config-if)# clock rate 256000
R1(config-if)# bandwidth 256
R1(config-if)# no shutdown
R1(config-if)# exit

R1(config)# end
R1# write memory
```

#### Router R2 - Basic Configuration

```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R2
R2(config)# no ip domain-lookup
R2(config)# enable secret class
R2(config)# line console 0
R2(config-line)# password cisco
R2(config-line)# login
R2(config-line)# logging synchronous
R2(config-line)# exit
R2(config)# line vty 0 4
R2(config-line)# password cisco
R2(config-line)# login
R2(config-line)# exit
R2(config)# banner motd #Unauthorized Access Prohibited#

! Configure FastEthernet 0/0
R2(config)# interface FastEthernet0/0
R2(config-if)# ip address 10.10.10.1 255.255.255.0
R2(config-if)# description LAN Network 2
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure Serial 0/0/0 (DTE to R1)
R2(config)# interface Serial0/0/0
R2(config-if)# ip address 192.168.10.2 255.255.255.252
R2(config-if)# description Link to R1
R2(config-if)# bandwidth 64
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure Serial 0/0/1 (DCE to R3)
R2(config)# interface Serial0/0/1
R2(config-if)# ip address 192.168.10.9 255.255.255.252
R2(config-if)# description Link to R3
R2(config-if)# clock rate 128000
R2(config-if)# bandwidth 128
R2(config-if)# no shutdown
R2(config-if)# exit

R2(config)# end
R2# write memory
```

#### Router R3 - Basic Configuration

```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R3
R3(config)# no ip domain-lookup
R3(config)# enable secret class
R3(config)# line console 0
R3(config-line)# password cisco
R3(config-line)# login
R3(config-line)# logging synchronous
R3(config-line)# exit
R3(config)# line vty 0 4
R3(config-line)# password cisco
R3(config-line)# login
R3(config-line)# exit
R3(config)# banner motd #Unauthorized Access Prohibited#

! Configure FastEthernet 0/0
R3(config)# interface FastEthernet0/0
R3(config-if)# ip address 172.16.1.33 255.255.255.248
R3(config-if)# description LAN Network 3
R3(config-if)# no shutdown
R3(config-if)# exit

! Configure Serial 0/0/0 (DTE to R1)
R3(config)# interface Serial0/0/0
R3(config-if)# ip address 192.168.10.6 255.255.255.252
R3(config-if)# description Link to R1
R3(config-if)# bandwidth 256
R3(config-if)# no shutdown
R3(config-if)# exit

! Configure Serial 0/0/1 (DTE to R2)
R3(config)# interface Serial0/0/1
R3(config-if)# ip address 192.168.10.10 255.255.255.252
R3(config-if)# description Link to R2
R3(config-if)# bandwidth 128
R3(config-if)# no shutdown
R3(config-if)# exit

R3(config)# end
R3# write memory
```

#### Verify Interface Configuration

```cisco
! On each router, verify interfaces
R1# show ip interface brief
```

**Expected Output:**
```
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        172.16.1.17     YES manual up                    up
Serial0/0/0            192.168.10.1    YES manual up                    up
Serial0/0/1            192.168.10.5    YES manual up                    up
```

---

### Task 3: Perform IP Configuration on Host PCs

#### PC1 Configuration
```
IP Address: 172.16.1.18
Subnet Mask: 255.255.255.240
Default Gateway: 172.16.1.17
```

#### PC2 Configuration
```
IP Address: 10.10.10.2
Subnet Mask: 255.255.255.0
Default Gateway: 10.10.10.1
```

#### PC3 Configuration
```
IP Address: 172.16.1.34
Subnet Mask: 255.255.255.248
Default Gateway: 172.16.1.33
```

**Test connectivity to default gateway from each PC:**
```
PC> ping 172.16.1.17    (from PC1)
PC> ping 10.10.10.1     (from PC2)
PC> ping 172.16.1.33    (from PC3)
```

---

### Task 4: Configure OSPF - Understanding the Basics

#### OSPF Configuration Syntax

```cisco
Router(config)# router ospf <process-id>
Router(config-router)# network <network-address> <wildcard-mask> area <area-id>
```

**Parameters Explained:**

**Process ID**:
- Value from 1 to 65535
- Locally significant (can be different on each router)
- Groups OSPF configuration commands
- Recommended: Use same process ID for consistency (we'll use 1)

**Network Address**:
- Directly connected network to advertise in OSPF
- Must match the network address (not an interface IP)

**Wildcard Mask**:
- Inverse of subnet mask
- Calculation: 255.255.255.255 - Subnet Mask
- Example: For 255.255.255.0 → Wildcard = 0.0.0.255
- Example: For 255.255.255.252 → Wildcard = 0.0.0.3

**Area**:
- Logical grouping of networks
- Area 0 = Backbone (we'll use this for all networks)
- Must be same for routers to form adjacencies

#### Wildcard Mask Calculation Examples

**Example 1: /24 Network**
```
Subnet Mask:  255.255.255.0
              255.255.255.255
           -  255.255.255.0
           ─────────────────
Wildcard:     0  .0  .0  .255
```

**Example 2: /30 Network**
```
Subnet Mask:  255.255.255.252
              255.255.255.255
           -  255.255.255.252
           ─────────────────
Wildcard:     0  .0  .0  .3
```

**Example 3: /28 Network**
```
Subnet Mask:  255.255.255.240
              255.255.255.255
           -  255.255.255.240
           ─────────────────
Wildcard:     0  .0  .0  .15
```

**Example 4: /29 Network**
```
Subnet Mask:  255.255.255.248
              255.255.255.255
           -  255.255.255.248
           ─────────────────
Wildcard:     0  .0  .0  .7
```

---

### Task 5: Configure OSPF on R1 Router

#### R1 Networks to Advertise:
1. Network 1 (LAN): 172.16.1.16/28
2. WAN Link to R2: 192.168.10.0/30
3. WAN Link to R3: 192.168.10.4/30

#### Calculate Wildcard Masks for R1:

```
Network 1: 172.16.1.16/28
  Subnet Mask: 255.255.255.240
  Wildcard:    0.0.0.15

WAN to R2: 192.168.10.0/30
  Subnet Mask: 255.255.255.252
  Wildcard:    0.0.0.3

WAN to R3: 192.168.10.4/30
  Subnet Mask: 255.255.255.252
  Wildcard:    0.0.0.3
```

#### R1 OSPF Configuration:

```cisco
R1# configure terminal
R1(config)# router ospf 1
R1(config-router)# network 172.16.1.16 0.0.0.15 area 0
R1(config-router)# network 192.168.10.0 0.0.0.3 area 0
R1(config-router)# network 192.168.10.4 0.0.0.3 area 0
R1(config-router)# end
R1# write memory
```

**What happens:**
- OSPF process 1 is started on R1
- All three directly connected networks are advertised
- R1 will send OSPF Hello packets on all interfaces
- Area 0 is the backbone area

---

### Task 6: Configure OSPF on R2 and R3 Routers

#### Router R2 Configuration

**R2 Networks to Advertise:**
1. Network 2 (LAN): 10.10.10.0/24
2. WAN Link to R1: 192.168.10.0/30
3. WAN Link to R3: 192.168.10.8/30

**Calculate Wildcard Masks for R2:**
```
Network 2: 10.10.10.0/24
  Subnet Mask: 255.255.255.0
  Wildcard:    0.0.0.255

WAN to R1: 192.168.10.0/30
  Subnet Mask: 255.255.255.252
  Wildcard:    0.0.0.3

WAN to R3: 192.168.10.8/30
  Subnet Mask: 255.255.255.252
  Wildcard:    0.0.0.3
```

**R2 OSPF Configuration:**
```cisco
R2# configure terminal
R2(config)# router ospf 1
R2(config-router)# network 10.10.10.0 0.0.0.255 area 0
R2(config-router)# network 192.168.10.0 0.0.0.3 area 0
R2(config-router)# network 192.168.10.8 0.0.0.3 area 0
R2(config-router)# end
R2# write memory
```

**Expected Console Message:**
```
%OSPF-5-ADJCHG: Process 1, Nbr 192.168.10.1 on Serial0/0/0 from LOADING to FULL, Loading Done
```
This message indicates OSPF neighbor relationship with R1 has been established.

**Answer to Lab Question:**
- **What is the IP address of the OSPF neighbor router?** 192.168.10.1 (R1's Serial0/0/0)
- **What interface on R2 is the neighbor adjacent to?** Serial0/0/0

#### Router R3 Configuration

**R3 Networks to Advertise:**
1. Network 3 (LAN): 172.16.1.32/29
2. WAN Link to R1: 192.168.10.4/30
3. WAN Link to R2: 192.168.10.8/30

**Calculate Wildcard Masks for R3:**
```
Network 3: 172.16.1.32/29
  Subnet Mask: 255.255.255.248
  Wildcard:    0.0.0.7

WAN to R1: 192.168.10.4/30
  Subnet Mask: 255.255.255.252
  Wildcard:    0.0.0.3

WAN to R2: 192.168.10.8/30
  Subnet Mask: 255.255.255.252
  Wildcard:    0.0.0.3
```

**R3 OSPF Configuration:**
```cisco
R3# configure terminal
R3(config)# router ospf 1
R3(config-router)# network 172.16.1.32 0.0.0.7 area 0
R3(config-router)# network 192.168.10.4 0.0.0.3 area 0
R3(config-router)# network 192.168.10.8 0.0.0.3 area 0
R3(config-router)# end
R3# write memory
```

**Expected Console Messages:**
```
%OSPF-5-ADJCHG: Process 1, Nbr 192.168.10.5 on Serial0/0/0 from LOADING to FULL, Loading Done
%OSPF-5-ADJCHG: Process 1, Nbr 192.168.10.9 on Serial0/0/1 from LOADING to FULL, Loading Done
```

---

### Task 7: Configure OSPF Router IDs

#### Understanding Router IDs

**Router ID Selection (Priority Order):**
1. Manually configured using `router-id` command (highest priority)
2. Highest IP address of any loopback interface
3. Highest IP address of any active physical interface (lowest priority)

**Why Use Loopback Interfaces?**
- Always up (never goes down)
- Provides stable Router ID
- Best practice for OSPF

#### Check Current Router IDs

Before configuring loopback interfaces, check current Router IDs:

```cisco
R1# show ip protocols
```

**Expected Output (R1):**
```
Routing Protocol is "ospf 1"
  Router ID 192.168.10.5
  ...
```

**Answer to Lab Questions:**
- **What is the router ID for R1?** 192.168.10.5 (highest IP on active interfaces)
- **What is the router ID for R2?** 192.168.10.9
- **What is the router ID for R3?** 192.168.10.10

#### Configure Loopback Interfaces

**Router R1:**
```cisco
R1# configure terminal
R1(config)# interface loopback 0
R1(config-if)# ip address 10.1.1.1 255.255.255.255
R1(config-if)# description Router ID for OSPF
R1(config-if)# exit
R1(config)# end
R1# write memory
```

**Router R2:**
```cisco
R2# configure terminal
R2(config)# interface loopback 0
R2(config-if)# ip address 10.2.2.2 255.255.255.255
R2(config-if)# description Router ID for OSPF
R2(config-if)# exit
R2(config)# end
R2# write memory
```

**Router R3:**
```cisco
R3# configure terminal
R3(config)# interface loopback 0
R3(config-if)# ip address 10.3.3.3 255.255.255.255
R3(config-if)# description Router ID for OSPF
R3(config-if)# exit
R3(config)# end
R3# write memory
```

#### Reload Routers to Apply New Router IDs

**Important:** The new Router ID won't take effect until OSPF process is restarted.

```cisco
R1# write memory
R1# reload
Proceed with reload? [confirm]

! Wait for router to reboot, then repeat for R2 and R3
R2# write memory
R2# reload

R3# write memory
R3# reload
```

#### Verify New Router IDs

After reloading all routers:

```cisco
R1# show ip protocols
```

**Expected Output:**
```
Routing Protocol is "ospf 1"
  Router ID 10.1.1.1
  ...
```

**Answers to Lab Questions:**
- **When the router is reloaded, what is the router ID for R1?** 10.1.1.1
- **When the router is reloaded, what is the router ID for R2?** 10.2.2.2
- **When the router is reloaded, what is the router ID for R3?** 10.3.3.3

#### Verify Router IDs Changed

```cisco
R1# show ip ospf neighbor
```

**Expected Output:**
```
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.2.2.2         0    FULL/  -        00:00:35    192.168.10.2    Serial0/0/0
10.3.3.3         0    FULL/  -        00:00:31    192.168.10.6    Serial0/0/1
```

---

### Task 8: Verify OSPF Operation

#### Step 1: Show OSPF Neighbors (on R1)

```cisco
R1# show ip ospf neighbor
```

**Expected Output:**
```
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.2.2.2         0    FULL/  -        00:00:38    192.168.10.2    Serial0/0/0
10.3.3.3         0    FULL/  -        00:00:34    192.168.10.6    Serial0/0/1
```

**Explanation:**
- **Neighbor ID**: Router ID of neighbor (10.2.2.2 = R2, 10.3.3.3 = R3)
- **Pri**: Priority (0 for point-to-point links)
- **State**: FULL = full adjacency established
- **Dead Time**: Time until neighbor is declared dead (resets with Hello packets)
- **Address**: IP address of neighbor interface
- **Interface**: Local interface connecting to neighbor

#### Step 2: Show IP Protocols (on R1)

```cisco
R1# show ip protocols
```

**Expected Output:**
```
Routing Protocol is "ospf 1"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Router ID 10.1.1.1
  Number of areas in this router is 1. 1 normal 0 stub 0 nssa
  Maximum path: 4
  Routing for Networks:
    172.16.1.16 0.0.0.15 area 0
    192.168.10.0 0.0.0.3 area 0
    192.168.10.4 0.0.0.3 area 0
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.2.2.2        110          00:05:23
    10.3.3.3        110          00:04:18
  Distance: (default is 110)
```

**Key Information:**
- **Router ID**: 10.1.1.1
- **Networks advertised**: Shows all networks configured under OSPF
- **Routing Information Sources**: OSPF neighbors (R2 and R3)
- **Administrative Distance**: 110 (default for OSPF)

#### Step 3: Examine OSPF Routes in Routing Table

```cisco
R1# show ip route
```

**Expected Output:**
```
Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

     10.0.0.0/32 is subnetted, 3 subnets
O       10.2.2.2 [110/65] via 192.168.10.2, 00:06:12, Serial0/0/0
C       10.1.1.1 is directly connected, Loopback0
O       10.3.3.3 [110/65] via 192.168.10.6, 00:05:07, Serial0/0/1
     172.16.0.0/16 is variably subnetted, 2 subnets, 2 masks
C       172.16.1.16/28 is directly connected, FastEthernet0/0
O       172.16.1.32/29 [110/65] via 192.168.10.6, 00:05:07, Serial0/0/1
O    10.10.10.0/24 [110/65] via 192.168.10.2, 00:06:12, Serial0/0/0
     192.168.10.0/30 is subnetted, 3 subnets
C       192.168.10.0 is directly connected, Serial0/0/0
C       192.168.10.4 is directly connected, Serial0/0/1
O       192.168.10.8 [110/128] via 192.168.10.6, 00:05:07, Serial0/0/1
                     [110/128] via 192.168.10.2, 00:06:12, Serial0/0/0
```

**Route Code Explanation:**
- **C**: Directly connected network
- **O**: OSPF learned route
- **[110/65]**: [Administrative Distance / Metric (Cost)]
- **via 192.168.10.2**: Next hop IP address
- **Serial0/0/0**: Exit interface

**OSPF Routes on R1:**
- `O 10.2.2.2` - R2's loopback (learned via OSPF)
- `O 10.3.3.3` - R3's loopback (learned via OSPF)
- `O 172.16.1.32/29` - Network 3 (learned from R3)
- `O 10.10.10.0/24` - Network 2 (learned from R2)
- `O 192.168.10.8` - R2-R3 link (learned via both R2 and R3 - load balanced)

#### Step 4: Repeat for R2 and R3

**On R2:**
```cisco
R2# show ip ospf neighbor
R2# show ip protocols
R2# show ip route
```

**On R3:**
```cisco
R3# show ip ospf neighbor
R3# show ip protocols
R3# show ip route
```

#### Step 5: Test Connectivity with Ping

**From PC1 to PC2:**
```
PC1> ping 10.10.10.2
```

**Expected Result:** Success! (Reply from 10.10.10.2)

**From PC1 to PC3:**
```
PC1> ping 172.16.1.34
```

**Expected Result:** Success!

**Explanation:**
- OSPF has propagated all network information
- Each router knows how to reach all networks
- PCs can communicate across different networks

#### Step 6: Check Serial Interface Bandwidth

```cisco
R1# show interfaces serial0/0/0
```

**Look for this line in output:**
```
BW 1544 Kbit, DLY 20000 usec,
```

**Answer to Lab Question:**
- **What is the default bandwidth of the Serial 0/0/0 interface?** 1544 Kbps (T1 speed)

#### Step 7: Calculate OSPF Cost

**OSPF Cost Formula:**
```
Cost = 10⁸ / Bandwidth (in bps)
Cost = 100,000,000 / Bandwidth
```

**For Serial 0/0/0 (default 1544 kbps):**
```
Cost = 100,000,000 / 1,544,000
Cost = 64.766... ≈ 64 (Cisco rounds down)
```

**Answer to Lab Question:**
- **Calculate the cost of link using formula 10⁸/bandwidth. Is calculated and router measured value same?**
  - Calculated: 100,000,000 / 1,544,000 = 64.77
  - Router shows: 64
  - Yes, they match (router rounds down)

---

### Task 9: Configure Additional OSPF Features

#### Step 1: Change Bandwidth to Match Actual Link Speed

The actual link speed between R1-R2 is 64 kbps (not the default 1544 kbps).

**On R1:**
```cisco
R1# configure terminal
R1(config)# interface serial0/0/0
R1(config-if)# bandwidth 64
R1(config-if)# exit
R1(config)# end
R1# write memory
```

**On R2:**
```cisco
R2# configure terminal
R2(config)# interface serial0/0/0
R2(config-if)# bandwidth 64
R2(config-if)# exit
R2(config)# end
R2# write memory
```

#### Step 2: Verify New OSPF Cost

```cisco
R1# show ip ospf interface serial0/0/0
```

**Look for:**
```
Cost: 1562
```

**Calculation:**
```
Cost = 100,000,000 / 64,000 = 1562.5 ≈ 1562
```

**Answer to Lab Question:**
- **What is new cost of serial0/0/0 link?** 1562

#### Step 3: View Default Hello and Dead Intervals

```cisco
R1# show ip ospf interface serial0/0/0
```

**Look for:**
```
Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
```

**Default Values for Point-to-Point Links:**
- **Hello Interval**: 10 seconds (how often Hello packets sent)
- **Dead Interval**: 40 seconds (time before neighbor declared dead)
- **Wait**: 40 seconds
- **Retransmit**: 5 seconds

**Answer to Lab Question:**
- **What is default dead interval?** 40 seconds
- **What do you observe?**
  - Hello interval = 10 seconds
  - Dead interval = 40 seconds (4 × Hello interval)
  - This is default for point-to-point and broadcast networks

#### Step 4: Configure OSPF Hello and Dead Intervals

**Important:** Hello and Dead intervals MUST match on both ends of the link for OSPF adjacency to form.

**On R1 Serial 0/0/0:**
```cisco
R1# configure terminal
R1(config)# interface serial0/0/0
R1(config-if)# ip ospf hello-interval 5
R1(config-if)# ip ospf dead-interval 20
R1(config-if)# exit
R1(config)# end
R1# write memory
```

**On R2 Serial 0/0/0:**
```cisco
R2# configure terminal
R2(config)# interface serial0/0/0
R2(config-if)# ip ospf hello-interval 5
R2(config-if)# ip ospf dead-interval 20
R2(config-if)# exit
R2(config)# end
R2# write memory
```

#### Step 5: Verify New Timers

```cisco
R1# show ip ospf interface serial0/0/0
```

**Look for:**
```
Timer intervals configured, Hello 5, Dead 20, Wait 20, Retransmit 5
```

**Verify neighbor adjacency is still up:**
```cisco
R1# show ip ospf neighbor
```

**Expected Output:**
```
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.2.2.2         0    FULL/  -        00:00:19    192.168.10.2    Serial0/0/0
10.3.3.3         0    FULL/  -        00:00:36    192.168.10.6    Serial0/0/1
```

**Note:** Dead Time for R2 neighbor should now count down from 20 instead of 40.

---

## Part 4: Complete OSPF Command Reference

### Basic OSPF Configuration Commands

```cisco
! Enable OSPF routing
router ospf <process-id>

! Advertise networks
network <network-address> <wildcard-mask> area <area-id>

! Set Router ID (optional but recommended)
router-id <ip-address>

! Configure loopback interface
interface loopback <number>
ip address <ip-address> <subnet-mask>
```

### OSPF Interface Commands

```cisco
! Set interface bandwidth (affects cost calculation)
interface <interface-type> <interface-number>
bandwidth <kbps>

! Manually set OSPF cost
ip ospf cost <cost-value>

! Configure Hello interval
ip ospf hello-interval <seconds>

! Configure Dead interval
ip ospf dead-interval <seconds>

! Set OSPF priority (for DR/BDR election)
ip ospf priority <0-255>

! Configure OSPF network type
ip ospf network <point-to-point|broadcast|non-broadcast|point-to-multipoint>
```

### OSPF Verification Commands

```cisco
! Show OSPF neighbors
show ip ospf neighbor

! Show OSPF neighbor details
show ip ospf neighbor detail

! Show OSPF routing protocol info
show ip protocols

! Show routing table
show ip route
show ip route ospf

! Show OSPF interface information
show ip ospf interface
show ip ospf interface brief
show ip ospf interface <interface-name>

! Show OSPF database
show ip ospf database

! Show OSPF process information
show ip ospf

! Show interface details
show interfaces <interface-name>

! Show running configuration
show running-config
show running-config | section ospf
```

### OSPF Troubleshooting Commands

```cisco
! Debug OSPF adjacency formation
debug ip ospf adj

! Debug OSPF events
debug ip ospf events

! Debug OSPF Hello packets
debug ip ospf hello

! Debug OSPF packet details
debug ip ospf packet

! Clear OSPF process (resets adjacencies)
clear ip ospf process

! Turn off debugging
no debug all
undebug all
```

---

## Part 5: OSPF Cost Calculation Reference

### Cost Calculation Formula

```
OSPF Cost = Reference Bandwidth / Interface Bandwidth
Default Reference Bandwidth = 100 Mbps = 100,000,000 bps
Cost = 10⁸ / Bandwidth (bps)
```

### Common Interface Costs (Default Reference Bandwidth)

| Interface Type | Bandwidth | Cost Calculation | OSPF Cost |
|----------------|-----------|------------------|-----------|
| Serial (default) | 1544 kbps (T1) | 100,000,000 / 1,544,000 | 64 |
| Serial (64 kbps) | 64 kbps | 100,000,000 / 64,000 | 1562 |
| Serial (128 kbps) | 128 kbps | 100,000,000 / 128,000 | 781 |
| Serial (256 kbps) | 256 kbps | 100,000,000 / 256,000 | 390 |
| Ethernet | 10 Mbps | 100,000,000 / 10,000,000 | 10 |
| Fast Ethernet | 100 Mbps | 100,000,000 / 100,000,000 | 1 |
| Gigabit Ethernet | 1000 Mbps | 100,000,000 / 1,000,000,000 | 1* |

*Note: For Gigabit and faster interfaces, cost = 1 with default reference bandwidth

### Changing Reference Bandwidth (Optional)

To accommodate higher-speed interfaces:

```cisco
router ospf 1
 auto-cost reference-bandwidth <mbps>
```

Example for 10 Gbps networks:
```cisco
router ospf 1
 auto-cost reference-bandwidth 10000
```

This changes reference bandwidth to 10 Gbps:
- Fast Ethernet cost becomes: 10,000,000,000 / 100,000,000 = 100
- Gigabit cost becomes: 10,000,000,000 / 1,000,000,000 = 10
- 10 Gigabit cost becomes: 10,000,000,000 / 10,000,000,000 = 1

---

## Part 6: OSPF Metric Calculation Examples

### Example 1: Cost from R1 to Network 2 (10.10.10.0/24)

**Path: R1 → S0/0/0 → R2 → Fa0/0**

```
R1 Serial0/0/0 (64 kbps configured):
  Cost = 100,000,000 / 64,000 = 1562

R2 FastEthernet0/0 (100 Mbps):
  Cost = 100,000,000 / 100,000,000 = 1

Total Cost = 1562 + 1 = 1563
```

However, in OSPF, the exit interface cost is counted, so:
- Cost from R1 to R2 = 1562 (R1's S0/0/0 cost)
- R2 local network has cost 0 (directly connected)
- Total OSPF metric = 1562

### Example 2: Cost from R1 to Network 3 (172.16.1.32/29)

**Path: R1 → S0/0/1 → R3 → Fa0/0**

```
R1 Serial0/0/1 (256 kbps configured):
  Cost = 100,000,000 / 256,000 = 390

Total OSPF metric = 390
```

### Example 3: Cost from R2 to Network 3

**Two possible paths:**

**Path 1: R2 → S0/0/0 → R1 → S0/0/1 → R3**
```
R2 S0/0/0 cost + R1 S0/0/1 cost = 1562 + 390 = 1952
```

**Path 2: R2 → S0/0/1 → R3**
```
R2 S0/0/1 (128 kbps):
  Cost = 100,000,000 / 128,000 = 781
```

**OSPF will choose Path 2** (cost 781 < 1952)

---

## Part 7: Expected Routing Tables After Full Configuration

### R1 Routing Table

```cisco
R1# show ip route ospf
```

```
     10.0.0.0/32 is subnetted, 3 subnets
O       10.2.2.2 [110/1563] via 192.168.10.2, Serial0/0/0
O       10.3.3.3 [110/391] via 192.168.10.6, Serial0/0/1
O    10.10.10.0/24 [110/1563] via 192.168.10.2, Serial0/0/0
     172.16.0.0/16 is variably subnetted, 2 subnets, 2 masks
O       172.16.1.32/29 [110/391] via 192.168.10.6, Serial0/0/1
     192.168.10.0/30 is subnetted, 3 subnets
O       192.168.10.8 [110/1172] via 192.168.10.2, Serial0/0/0
                     [110/1172] via 192.168.10.6, Serial0/0/1
```

### R2 Routing Table

```cisco
R2# show ip route ospf
```

```
     10.0.0.0/32 is subnetted, 3 subnets
O       10.1.1.1 [110/1563] via 192.168.10.1, Serial0/0/0
O       10.3.3.3 [110/782] via 192.168.10.10, Serial0/0/1
     172.16.0.0/16 is variably subnetted, 2 subnets, 2 masks
O       172.16.1.16/28 [110/1563] via 192.168.10.1, Serial0/0/0
O       172.16.1.32/29 [110/782] via 192.168.10.10, Serial0/0/1
     192.168.10.0/30 is subnetted, 3 subnets
O       192.168.10.4 [110/1953] via 192.168.10.1, Serial0/0/0
                     [110/1172] via 192.168.10.10, Serial0/0/1
```

### R3 Routing Table

```cisco
R3# show ip route ospf
```

```
     10.0.0.0/32 is subnetted, 3 subnets
O       10.1.1.1 [110/391] via 192.168.10.5, Serial0/0/0
O       10.2.2.2 [110/782] via 192.168.10.9, Serial0/0/1
O    10.10.10.0/24 [110/782] via 192.168.10.9, Serial0/0/1
     172.16.0.0/16 is variably subnetted, 2 subnets, 2 masks
O       172.16.1.16/28 [110/391] via 192.168.10.5, Serial0/0/0
     192.168.10.0/30 is subnetted, 3 subnets
O       192.168.10.0 [110/1953] via 192.168.10.5, Serial0/0/0
                     [110/1172] via 192.168.10.9, Serial0/0/1
```

---

## Part 8: Troubleshooting Common OSPF Issues

### Issue 1: OSPF Neighbors Not Forming

**Symptoms:**
- `show ip ospf neighbor` shows no neighbors
- Routing table missing OSPF routes

**Possible Causes and Solutions:**

1. **Interface down**
   ```cisco
   show ip interface brief
   ! If down, check:
   interface <name>
   no shutdown
   ```

2. **Area mismatch**
   ```cisco
   show ip ospf interface
   ! Both routers must have same area
   network x.x.x.x y.y.y.y area 0
   ```

3. **Hello/Dead interval mismatch**
   ```cisco
   show ip ospf interface serial0/0/0
   ! Must match on both sides
   ip ospf hello-interval 10
   ip ospf dead-interval 40
   ```

4. **Authentication mismatch**
   ```cisco
   show ip ospf interface
   ! Check if authentication enabled
   ```

5. **Subnet mask mismatch**
   ```cisco
   show ip interface brief
   ! Verify both ends have correct mask
   ```

### Issue 2: OSPF Running but Routes Not Installing

**Possible Causes:**

1. **Network not advertised**
   ```cisco
   show ip protocols
   ! Check "Routing for Networks" section
   router ospf 1
   network x.x.x.x y.y.y.y area 0
   ```

2. **Better route exists**
   ```cisco
   show ip route
   ! Check if static or other protocol has better AD
   ```

3. **ACL blocking OSPF**
   ```cisco
   show access-lists
   ! Check for ACLs on interfaces
   ```

### Issue 3: Incorrect OSPF Cost

**Check and Fix:**

```cisco
! View current cost
show ip ospf interface brief

! Fix bandwidth
interface serial0/0/0
bandwidth 64

! Or set cost manually
ip ospf cost 1562
```

### Issue 4: Router ID Conflict

**Symptoms:**
- Adjacencies flapping
- Duplicate Router IDs

**Solution:**
```cisco
! Configure unique loopback
interface loopback 0
ip address 10.X.X.X 255.255.255.255

! Restart OSPF
clear ip ospf process
```

---

## Part 9: Lab Verification Checklist

### Pre-Configuration Checks
- [ ] All devices powered on and accessible
- [ ] Cables properly connected as per topology
- [ ] All interfaces administratively up (no shutdown)
- [ ] IP addresses correctly assigned
- [ ] Clock rates set on DCE interfaces
- [ ] PCs can ping their default gateways

### OSPF Configuration Checks
- [ ] OSPF process enabled on all routers
- [ ] All networks properly advertised with correct wildcard masks
- [ ] All routers in Area 0
- [ ] Loopback interfaces configured for Router IDs
- [ ] Routers reloaded after loopback configuration

### Verification Checks
- [ ] `show ip ospf neighbor` shows all expected neighbors in FULL state
- [ ] `show ip protocols` displays correct OSPF configuration
- [ ] `show ip route` shows OSPF routes (marked with 'O')
- [ ] All remote networks reachable
- [ ] PCs can ping each other across networks
- [ ] OSPF costs calculated correctly
- [ ] Bandwidth configured correctly on serial links

### Advanced Configuration Checks
- [ ] Bandwidth set to match actual link speeds
- [ ] OSPF costs verified with show commands
- [ ] Hello and Dead intervals configured (if required)
- [ ] Timers match on both ends of each link

### Final Connectivity Tests
- [ ] PC1 can ping PC2 (10.10.10.2)
- [ ] PC1 can ping PC3 (172.16.1.34)
- [ ] PC2 can ping PC3
- [ ] All OSPF routes stable (no flapping)
- [ ] Configuration saved on all routers

---

## Part 10: Quick Configuration Summary

### Router R1 - Complete Configuration

```cisco
enable
configure terminal
hostname R1
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
line vty 0 4
 password cisco
 login
banner motd #Unauthorized Access#

interface Loopback0
 ip address 10.1.1.1 255.255.255.255

interface FastEthernet0/0
 ip address 172.16.1.17 255.255.255.240
 no shutdown

interface Serial0/0/0
 ip address 192.168.10.1 255.255.255.252
 clock rate 64000
 bandwidth 64
 ip ospf hello-interval 5
 ip ospf dead-interval 20
 no shutdown

interface Serial0/0/1
 ip address 192.168.10.5 255.255.255.252
 clock rate 256000
 bandwidth 256
 no shutdown

router ospf 1
 network 172.16.1.16 0.0.0.15 area 0
 network 192.168.10.0 0.0.0.3 area 0
 network 192.168.10.4 0.0.0.3 area 0

end
write memory
```

### Router R2 - Complete Configuration

```cisco
enable
configure terminal
hostname R2
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
line vty 0 4
 password cisco
 login
banner motd #Unauthorized Access#

interface Loopback0
 ip address 10.2.2.2 255.255.255.255

interface FastEthernet0/0
 ip address 10.10.10.1 255.255.255.0
 no shutdown

interface Serial0/0/0
 ip address 192.168.10.2 255.255.255.252
 bandwidth 64
 ip ospf hello-interval 5
 ip ospf dead-interval 20
 no shutdown

interface Serial0/0/1
 ip address 192.168.10.9 255.255.255.252
 clock rate 128000
 bandwidth 128
 no shutdown

router ospf 1
 network 10.10.10.0 0.0.0.255 area 0
 network 192.168.10.0 0.0.0.3 area 0
 network 192.168.10.8 0.0.0.3 area 0

end
write memory
```

### Router R3 - Complete Configuration

```cisco
enable
configure terminal
hostname R3
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
line vty 0 4
 password cisco
 login
banner motd #Unauthorized Access#

interface Loopback0
 ip address 10.3.3.3 255.255.255.255

interface FastEthernet0/0
 ip address 172.16.1.33 255.255.255.248
 no shutdown

interface Serial0/0/0
 ip address 192.168.10.6 255.255.255.252
 bandwidth 256
 no shutdown

interface Serial0/0/1
 ip address 192.168.10.10 255.255.255.252
 bandwidth 128
 no shutdown

router ospf 1
 network 172.16.1.32 0.0.0.7 area 0
 network 192.168.10.4 0.0.0.3 area 0
 network 192.168.10.8 0.0.0.3 area 0

end
write memory
```

---

## Conclusion

This lab successfully demonstrates:

1. ✅ **OSPF Configuration** - All routers properly configured with OSPF
2. ✅ **Neighbor Adjacencies** - All OSPF neighbors in FULL state
3. ✅ **Route Propagation** - All networks learned via OSPF
4. ✅ **End-to-End Connectivity** - PCs can communicate across networks
5. ✅ **Router IDs** - Configured using loopback interfaces
6. ✅ **Cost Calculation** - Properly configured bandwidth affects path selection
7. ✅ **OSPF Timers** - Hello and Dead intervals customized

**Key Takeaways:**
- OSPF is a sophisticated link-state routing protocol
- Proper planning of Router IDs improves network stability
- Bandwidth configuration affects cost and path selection
- All OSPF parameters must match for adjacencies to form
- OSPF provides fast convergence and scales well

---

**Lab Completed Successfully!**

**Document Created:** 2026-03-25
**Course:** CPE314 - Data Communication and Computer Networks
**Lab Number:** 7
**Topic:** OSPF Routing Protocol Configuration

---

**End of Document**
