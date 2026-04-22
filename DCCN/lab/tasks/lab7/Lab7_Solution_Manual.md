# Lab 7 - OSPF Routing Protocol
## Complete Solution Manual

---

**Course:** CPE314 - Data Communication and Computer Networks  
**Lab:** Lab 7 - OSPF Routing Protocol  
**Student ID:** FA23-BCE-113

---

## Table of Contents
1. [Lab Objectives](#lab-objectives)
2. [Network Topology](#network-topology)
3. [Subnetting Calculations](#subnetting-calculations)
4. [Complete Addressing Table](#complete-addressing-table)
5. [Router Configurations](#router-configurations)
6. [OSPF Configuration](#ospf-configuration)
7. [Verification Commands](#verification-commands)
8. [Lab Questions & Answers](#lab-questions--answers)

---

## Lab Objectives

1. Construct a network demonstrating OSPF routing protocol operation using Cisco Packet Tracer
2. Show connectivity between nodes using OSPF on all routers

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

## Subnetting Calculations

### Network 1: 172.16.1.16/28 (R1 LAN)

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| Host Bits | 32 - 28 | 4 bits |
| Block Size | 2^4 | 16 |
| Subnet Mask | 255.255.255.(256-16) | 255.255.255.240 |
| Network Address | - | 172.16.1.16 |
| First Usable IP | Network + 1 | 172.16.1.17 |
| Last Usable IP | Broadcast - 1 | 172.16.1.30 |
| Broadcast Address | Network + 16 - 1 | 172.16.1.31 |
| Usable Hosts | 16 - 2 | 14 |
| **Wildcard Mask** | 255.255.255.255 - 255.255.255.240 | **0.0.0.15** |

### Network 2: 10.10.10.0/24 (R2 LAN)

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| Host Bits | 32 - 24 | 8 bits |
| Block Size | 2^8 | 256 |
| Subnet Mask | - | 255.255.255.0 |
| Network Address | - | 10.10.10.0 |
| First Usable IP | Network + 1 | 10.10.10.1 |
| Last Usable IP | Broadcast - 1 | 10.10.10.254 |
| Broadcast Address | 10.10.10.0 + 256 - 1 | 10.10.10.255 |
| Usable Hosts | 256 - 2 | 254 |
| **Wildcard Mask** | 255.255.255.255 - 255.255.255.0 | **0.0.0.255** |

### Network 3: 172.16.1.32/29 (R3 LAN)

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| Host Bits | 32 - 29 | 3 bits |
| Block Size | 2^3 | 8 |
| Subnet Mask | 255.255.255.(256-8) | 255.255.255.248 |
| Network Address | - | 172.16.1.32 |
| First Usable IP | Network + 1 | 172.16.1.33 |
| Last Usable IP | Broadcast - 1 | 172.16.1.38 |
| Broadcast Address | 172.16.1.32 + 8 - 1 | 172.16.1.39 |
| Usable Hosts | 8 - 2 | 6 |
| **Wildcard Mask** | 255.255.255.255 - 255.255.255.248 | **0.0.0.7** |

### WAN Links: /30 Networks (Point-to-Point)

| WAN Link | Network | Subnet Mask | Usable IPs | Wildcard |
|----------|---------|-------------|------------|----------|
| R1 ↔ R2 | 192.168.10.0/30 | 255.255.255.252 | .1 - .2 | 0.0.0.3 |
| R1 ↔ R3 | 192.168.10.4/30 | 255.255.255.252 | .5 - .6 | 0.0.0.3 |
| R2 ↔ R3 | 192.168.10.8/30 | 255.255.255.252 | .9 - .10 | 0.0.0.3 |

---

## Complete Addressing Table

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

## Router Configurations

### Router R1 - Complete Configuration

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

! Configure Loopback 0
R1(config)# interface loopback 0
R1(config-if)# ip address 10.1.1.1 255.255.255.255
R1(config-if)# exit

R1(config)# end
R1# write memory
```

### Router R2 - Complete Configuration

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

! Configure Loopback 0
R2(config)# interface loopback 0
R2(config-if)# ip address 10.2.2.2 255.255.255.255
R2(config-if)# exit

R2(config)# end
R2# write memory
```

### Router R3 - Complete Configuration

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

! Configure Loopback 0
R3(config)# interface loopback 0
R3(config-if)# ip address 10.3.3.3 255.255.255.255
R3(config-if)# exit

R3(config)# end
R3# write memory
```

### PC Configurations

| PC | IP Address | Subnet Mask | Default Gateway |
|----|------------|-------------|-----------------|
| PC1 | 172.16.1.18 | 255.255.255.240 | 172.16.1.17 |
| PC2 | 10.10.10.2 | 255.255.255.0 | 10.10.10.1 |
| PC3 | 172.16.1.34 | 255.255.255.248 | 172.16.1.33 |

---

## OSPF Configuration

### OSPF Basics

**OSPF (Open Shortest Path First)** is a link-state routing protocol that:
- Uses Dijkstra's SPF algorithm
- Supports VLSM/CIDR
- Uses cost metric: **Cost = 10⁸ / Bandwidth**
- Administrative Distance: 110

### Wildcard Mask Summary

| Network | Subnet Mask | Wildcard Mask |
|---------|-------------|---------------|
| 172.16.1.16/28 | 255.255.255.240 | 0.0.0.15 |
| 10.10.10.0/24 | 255.255.255.0 | 0.0.0.255 |
| 172.16.1.32/29 | 255.255.255.248 | 0.0.0.7 |
| 192.168.10.x/30 | 255.255.255.252 | 0.0.0.3 |

### R1 OSPF Configuration

```cisco
R1# configure terminal
R1(config)# router ospf 1
R1(config-router)# network 172.16.1.16 0.0.0.15 area 0
R1(config-router)# network 192.168.10.0 0.0.0.3 area 0
R1(config-router)# network 192.168.10.4 0.0.0.3 area 0
R1(config-router)# end
R1# write memory
```

### R2 OSPF Configuration

```cisco
R2# configure terminal
R2(config)# router ospf 1
R2(config-router)# network 10.10.10.0 0.0.0.255 area 0
R2(config-router)# network 192.168.10.0 0.0.0.3 area 0
R2(config-router)# network 192.168.10.8 0.0.0.3 area 0
R2(config-router)# end
R2# write memory
```

### R3 OSPF Configuration

```cisco
R3# configure terminal
R3(config)# router ospf 1
R3(config-router)# network 172.16.1.32 0.0.0.7 area 0
R3(config-router)# network 192.168.10.4 0.0.0.3 area 0
R3(config-router)# network 192.168.10.8 0.0.0.3 area 0
R3(config-router)# end
R3# write memory
```

### Configure OSPF Timers (Optional)

```cisco
! On R1 Serial 0/0/0
R1(config)# interface serial0/0/0
R1(config-if)# ip ospf hello-interval 5
R1(config-if)# ip ospf dead-interval 20
R1(config-if)# exit

! On R2 Serial 0/0/0 (must match)
R2(config)# interface serial0/0/0
R2(config-if)# ip ospf hello-interval 5
R2(config-if)# ip ospf dead-interval 20
R2(config-if)# exit
```

---

## Verification Commands

### Show OSPF Neighbors

```cisco
R1# show ip ospf neighbor
```

**Expected Output:**
```
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.2.2.2         0    FULL/  -        00:00:38    192.168.10.2    Serial0/0/0
10.3.3.3         0    FULL/  -        00:00:34    192.168.10.6    Serial0/0/1
```

### Show IP Protocols

```cisco
R1# show ip protocols
```

### Show Routing Table

```cisco
R1# show ip route
```

**OSPF routes are marked with 'O'**

### Show OSPF Interface Details

```cisco
R1# show ip ospf interface serial0/0/0
```

### Test Connectivity

```
PC1> ping 10.10.10.2     (PC1 to PC2)
PC1> ping 172.16.1.34    (PC1 to PC3)
PC2> ping 172.16.1.18    (PC2 to PC1)
PC2> ping 172.16.1.34    (PC2 to PC3)
PC3> ping 172.16.1.18    (PC3 to PC1)
PC3> ping 10.10.10.2     (PC3 to PC2)
```

---

## Lab Questions & Answers

### Q1: What is the IP address of the OSPF neighbor router on R2?
**Answer:** 192.168.10.1 (R1's Serial0/0/0)

### Q2: What interface on R2 is the neighbor adjacent to?
**Answer:** Serial0/0/0

### Q3: What is the router ID for each router (before loopback)?
**Answer:**
- R1: 192.168.10.5 (highest IP on active interfaces)
- R2: 192.168.10.9
- R3: 192.168.10.10

### Q4: What is the router ID after configuring loopback and reloading?
**Answer:**
- R1: 10.1.1.1
- R2: 10.2.2.2
- R3: 10.3.3.3

### Q5: What is the default bandwidth of Serial 0/0/0?
**Answer:** 1544 Kbps (T1 speed)

### Q6: Calculate OSPF cost using formula 10⁸/bandwidth
**Answer:**
- Default (1544 kbps): Cost = 100,000,000 / 1,544,000 = **64**
- 64 kbps link: Cost = 100,000,000 / 64,000 = **1562**
- 128 kbps link: Cost = 100,000,000 / 128,000 = **781**
- 256 kbps link: Cost = 100,000,000 / 256,000 = **390**

### Q7: What is the default dead interval?
**Answer:** 40 seconds (4 × Hello interval of 10 seconds)

### Q8: Why use loopback interfaces for Router ID?
**Answer:**
- Always UP (never goes down physically)
- Provides stable Router ID
- Best practice for OSPF stability

---

## OSPF Cost Calculation Summary

| Link | Bandwidth | Cost Formula | Cost Value |
|------|-----------|--------------|------------|
| FastEthernet | 100 Mbps | 10⁸/100,000,000 | 1 |
| T1 (default) | 1.544 Mbps | 10⁸/1,544,000 | 64 |
| R1-R3 | 256 Kbps | 10⁸/256,000 | 390 |
| R2-R3 | 128 Kbps | 10⁸/128,000 | 781 |
| R1-R2 | 64 Kbps | 10⁸/64,000 | 1562 |

---

## Quick Reference Commands

| Purpose | Command |
|---------|---------|
| Show OSPF neighbors | `show ip ospf neighbor` |
| Show routing table | `show ip route` |
| Show OSPF routes only | `show ip route ospf` |
| Show OSPF configuration | `show running-config \| section ospf` |
| Show interface OSPF info | `show ip ospf interface` |
| Show OSPF database | `show ip ospf database` |
| Debug OSPF | `debug ip ospf events` |

---

**End of Solution Manual**
