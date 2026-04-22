# Lab 8 - Standard Access Control Lists (ACL)
## Complete Solution Manual

---

**Course:** CPE314 - Data Communication and Computer Networks  
**Lab:** Lab 8 - To Trace Different Traffic Flows using Standard ACL  
**Student ID:** FA23-BCE-113

---

## Table of Contents
1. [Lab Objectives](#lab-objectives)
2. [Pre-Lab Theory](#pre-lab-theory)
3. [Network Topology](#network-topology)
4. [Addressing Table](#addressing-table)
5. [Basic Router Configuration](#basic-router-configuration)
6. [DHCP Configuration](#dhcp-configuration)
7. [Standard ACL Configuration](#standard-acl-configuration)
8. [Verification Commands](#verification-commands)
9. [Lab Questions & Answers](#lab-questions--answers)

---

## Lab Objectives

1. To follow the DHCP protocol configuration for IP address assignment using Packet Tracer
2. To identify and understand configurations of Standard ACL using Packet Tracer

---

## Pre-Lab Theory

### Dynamic Host Configuration Protocol (DHCP)

DHCP is a standardized networking protocol used on IP networks that dynamically configures IP addresses and other information needed for Internet communication.

**Benefits:**
- Reduces need for manual IP configuration
- Prevents IP address conflicts
- Centralized IP management

**DHCP Implementation Methods:**
1. Router acts as DHCP server and assigns IPs to devices
2. Router forwards DHCP requests to a dedicated DHCP server

**DHCP Configuration Commands:**
```cisco
R1(config)# ip dhcp pool Pool_Name
R1(dhcp-config)# network Network_ID Subnet_Mask
R1(dhcp-config)# default-router Gateway_IP
R1(dhcp-config)# exit
```

---

### Access Control Lists (ACLs)

An ACL is a router configuration script that controls whether a router permits or denies packets to pass based on criteria found in the packet header.

**ACL Rules:**
- **One ACL per protocol** - For each protocol enabled on the interface
- **One ACL per direction** - Inbound or outbound (not both with same ACL)
- **One ACL per interface** - Applied to specific interface

**ACL Types:**

| Type | Number Range | Filter Criteria |
|------|--------------|-----------------|
| **Standard ACL** | 1-99, 1300-1999 | Source IP only |
| **Extended ACL** | 100-199, 2000-2699 | Source IP, Dest IP, Protocol, Port |

**Standard ACL Characteristics:**
- Filters based on **source IP address only**
- Should be placed **close to the destination**
- Simpler but less granular control

**ACL Operation:**
- Statements processed **sequentially** from top to bottom
- First match wins - packet is permitted/denied
- **Implicit deny** at end of every ACL (denies all unmatched traffic)

**Wildcard Mask Calculation:**
```
Wildcard Mask = 255.255.255.255 - Subnet Mask

Examples:
/24 (255.255.255.0)   → Wildcard: 0.0.0.255
/25 (255.255.255.128) → Wildcard: 0.0.0.127
/26 (255.255.255.192) → Wildcard: 0.0.0.63
/30 (255.255.255.252) → Wildcard: 0.0.0.3
```

---

## Network Topology

```
                         192.16.1.0/24           192.16.2.0/24
                              DCE                    DCE
                    ┌─────────────────────┐ ┌─────────────────────┐
                    │                     │ │                     │
                   R1                    R2                      R3
                Se0/1/0              Se0/1/0  Se0/2/0          Se0/2/0
                    │      Fa0/0  Fa0/1  Fa1/0                    │
                  Fa0/0       │     │      │                   Fa0/0
                    │         │     │      │                     │
  192.16.3.0       S1        S2    S3     S4                    S5      192.16.7.0
      │             │         │     │      │                     │          │
   ┌──┴──┐          │         │     │      │                  ┌──┴──┐
  PC7   PC8        S1        S2    S3     S4               HTTP  DHCP  DNS
                    │         │     │      │
              Developers    PC1   PC3    PC5
                           PC2   PC4    PC6
                          Sales   HR     QA
                        192.16.4.0  192.16.5.0  192.16.6.0
```

**Figure 15: Network Topology**

**Network Assignments (Using Class C - 192.16.X.0/24):**

| Network | Network ID | Purpose | Connected To |
|---------|------------|---------|--------------|
| WAN 1 | 192.16.1.0/24 | WAN Link | R1 Se0/1/0 ↔ R2 Se0/1/0 (DCE) |
| WAN 2 | 192.16.2.0/24 | WAN Link | R2 Se0/2/0 (DCE) ↔ R3 Se0/2/0 |
| LAN 1 | 192.16.3.0/24 | Developers (PC7, PC8) | R1 Fa0/0 → S1 |
| LAN 2 | 192.16.4.0/24 | Sales (PC1, PC2) | R2 Fa0/0 → S2 |
| LAN 3 | 192.16.5.0/24 | HR (PC3, PC4) | R2 Fa0/1 → S3 |
| LAN 4 | 192.16.6.0/24 | QA (PC5, PC6) | R2 Fa1/0 → S4 |
| Server | 192.16.7.0/24 | HTTP, DHCP, DNS Servers | R3 Fa0/0 → S5 |

---

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Gateway |
|--------|-----------|------------|-------------|---------|
| **R1** | Se0/1/0 | 192.16.1.1 | 255.255.255.0 | N/A |
| | Fa0/0 | 192.16.3.1 | 255.255.255.0 | N/A |
| **R2** | Se0/1/0 (DCE) | 192.16.1.2 | 255.255.255.0 | N/A |
| | Se0/2/0 (DCE) | 192.16.2.1 | 255.255.255.0 | N/A |
| | Fa0/0 | 192.16.4.1 | 255.255.255.0 | N/A |
| | Fa0/1 | 192.16.5.1 | 255.255.255.0 | N/A |
| | Fa1/0 | 192.16.6.1 | 255.255.255.0 | N/A |
| **R3** | Se0/2/0 | 192.16.2.2 | 255.255.255.0 | N/A |
| | Fa0/0 | 192.16.7.1 | 255.255.255.0 | N/A |
| **HTTP Server** | NIC | 192.16.7.2 | 255.255.255.0 | 192.16.7.1 |
| **DNS Server** | NIC | 192.16.7.3 | 255.255.255.0 | 192.16.7.1 |
| **DHCP Server** | NIC | 192.16.7.4 | 255.255.255.0 | 192.16.7.1 |
| **PC1 - PC8** | NIC | Obtain Automatically | Obtain Automatically | Auto |

---

## Basic Router Configuration

### Task 1: Prepare the Network

1. Add 3 Routers (Router-PT or 2811)
2. Add 5 Switches (S1-S5)
3. Add 8 PCs (PC1-PC8) and 3 Servers (HTTP, DHCP, DNS)
4. Connect devices as per topology

**Cable Connections:**
- R1 Se0/1/0 (DTE) ↔ R2 Se0/1/0 (DCE) - WAN Link
- R2 Se0/2/0 (DCE) ↔ R3 Se0/2/0 (DTE) - WAN Link
- R1 Fa0/0 ↔ S1 (Developers)
- R2 Fa0/0 ↔ S2 (Sales)
- R2 Fa0/1 ↔ S3 (HR)
- R2 Fa1/0 ↔ S4 (QA)
- R3 Fa0/0 ↔ S5 (Servers)

**Note:** R2 is the central router with DCE cables on both serial interfaces.

### Task 2: R1 Configuration

```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R1
R1(config)# no ip domain-lookup

! Configure Serial 0/1/0 (to R2) - DTE (No clock rate)
R1(config)# interface Serial0/1/0
R1(config-if)# ip address 192.16.1.1 255.255.255.0
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure FastEthernet 0/0 (to S1 - Developers Network)
R1(config)# interface FastEthernet0/0
R1(config-if)# ip address 192.16.3.1 255.255.255.0
R1(config-if)# no shutdown
R1(config-if)# exit

R1(config)# end
R1# write memory
```

### R2 Configuration (Central Router)

```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R2
R2(config)# no ip domain-lookup

! Configure Serial 0/1/0 (to R1) - DCE
R2(config)# interface Serial0/1/0
R2(config-if)# ip address 192.16.1.2 255.255.255.0
R2(config-if)# clock rate 64000
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure Serial 0/2/0 (to R3) - DCE
R2(config)# interface Serial0/2/0
R2(config-if)# ip address 192.16.2.1 255.255.255.0
R2(config-if)# clock rate 64000
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure FastEthernet 0/0 (to S2 - Sales Network)
R2(config)# interface FastEthernet0/0
R2(config-if)# ip address 192.16.4.1 255.255.255.0
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure FastEthernet 0/1 (to S3 - HR Network)
R2(config)# interface FastEthernet0/1
R2(config-if)# ip address 192.16.5.1 255.255.255.0
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure FastEthernet 1/0 (to S4 - QA Network)
R2(config)# interface FastEthernet1/0
R2(config-if)# ip address 192.16.6.1 255.255.255.0
R2(config-if)# no shutdown
R2(config-if)# exit

R2(config)# end
R2# write memory
```

### R3 Configuration (Server Side)

```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R3
R3(config)# no ip domain-lookup

! Configure Serial 0/2/0 (to R2) - DTE (No clock rate)
R3(config)# interface Serial0/2/0
R3(config-if)# ip address 192.16.2.2 255.255.255.0
R3(config-if)# no shutdown
R3(config-if)# exit

! Configure FastEthernet 0/0 (to S5 - Server Network)
R3(config)# interface FastEthernet0/0
R3(config-if)# ip address 192.16.7.1 255.255.255.0
R3(config-if)# no shutdown
R3(config-if)# exit

R3(config)# end
R3# write memory
```

### Verify Interface Configuration

```cisco
R1# show ip interface brief
R2# show ip interface brief
R3# show ip interface brief
```

**Expected output should show all interfaces up/up:**
```
Interface              IP-Address      OK? Method Status                Protocol
Serial0/1/0            192.16.1.x      YES manual up                    up
FastEthernet0/0        192.16.x.1      YES manual up                    up
```

---

## RIP Routing Configuration

Configure RIP on all routers for network connectivity:

### R1 RIP Configuration

```cisco
R1# configure terminal
R1(config)# router rip
R1(config-router)# version 2
R1(config-router)# network 192.16.1.0
R1(config-router)# network 192.16.3.0
R1(config-router)# no auto-summary
R1(config-router)# exit
R1(config)# end
R1# write memory
```

### R2 RIP Configuration

```cisco
R2# configure terminal
R2(config)# router rip
R2(config-router)# version 2
R2(config-router)# network 192.16.1.0
R2(config-router)# network 192.16.2.0
R2(config-router)# network 192.16.4.0
R2(config-router)# network 192.16.5.0
R2(config-router)# network 192.16.6.0
R2(config-router)# no auto-summary
R2(config-router)# exit
R2(config)# end
R2# write memory
```

### R3 RIP Configuration

```cisco
R3# configure terminal
R3(config)# router rip
R3(config-router)# version 2
R3(config-router)# network 192.16.2.0
R3(config-router)# network 192.16.7.0
R3(config-router)# no auto-summary
R3(config-router)# exit
R3(config)# end
R3# write memory
```

### Verify RIP

```cisco
R1# show ip route
R2# show ip route
R3# show ip route
```

Look for routes marked with "R" (RIP learned routes).

---

## DHCP Configuration

### Task 3: Configure DHCP Pools

**Step 1: Configure DHCP for Developers Network (192.16.3.0) on R1**

```cisco
R1# configure terminal
R1(config)# ip dhcp pool DEVELOPERS
R1(dhcp-config)# network 192.16.3.0 255.255.255.0
R1(dhcp-config)# default-router 192.16.3.1
R1(dhcp-config)# dns-server 192.16.7.3
R1(dhcp-config)# exit
R1(config)# ip dhcp excluded-address 192.16.3.1
R1(config)# end
R1# write memory
```

**Step 2: Configure DHCP for Sales Network (192.16.4.0) on R2**

```cisco
R2# configure terminal
R2(config)# ip dhcp pool SALES
R2(dhcp-config)# network 192.16.4.0 255.255.255.0
R2(dhcp-config)# default-router 192.16.4.1
R2(dhcp-config)# dns-server 192.16.7.3
R2(dhcp-config)# exit
R2(config)# ip dhcp excluded-address 192.16.4.1
```

**Step 3: Configure DHCP for HR Network (192.16.5.0) on R2**

```cisco
R2(config)# ip dhcp pool HR
R2(dhcp-config)# network 192.16.5.0 255.255.255.0
R2(dhcp-config)# default-router 192.16.5.1
R2(dhcp-config)# dns-server 192.16.7.3
R2(dhcp-config)# exit
R2(config)# ip dhcp excluded-address 192.16.5.1
```

**Step 4: Configure DHCP for QA Network (192.16.6.0) on R2**

```cisco
R2(config)# ip dhcp pool QA
R2(dhcp-config)# network 192.16.6.0 255.255.255.0
R2(dhcp-config)# default-router 192.16.6.1
R2(dhcp-config)# dns-server 192.16.7.3
R2(dhcp-config)# exit
R2(config)# ip dhcp excluded-address 192.16.6.1
R2(config)# end
R2# write memory
```

**Note:** DNS Server IP is 192.16.7.3, which will be accessible once RIP routing is fully configured.

### Configure PCs for DHCP

On each PC (PC1-PC8):
1. Go to **Desktop** → **IP Configuration**
2. Select **DHCP** instead of Static
3. PC will automatically obtain IP address

### Configure Servers with Static IPs

| Server | IP Address | Subnet Mask | Gateway |
|--------|------------|-------------|---------|
| HTTP Server | 192.16.7.2 | 255.255.255.0 | 192.16.7.1 |
| DNS Server | 192.16.7.3 | 255.255.255.0 | 192.16.7.1 |
| DHCP Server | 192.16.7.4 | 255.255.255.0 | 192.16.7.1 |

### Verify DHCP

```cisco
R1# show ip dhcp binding
R2# show ip dhcp binding
R2# show ip dhcp pool
```

---

## Standard ACL Configuration

### ACL Syntax

```cisco
Router(config)# access-list <number> {permit | deny} <source-IP> <wildcard-mask>
Router(config)# access-list <number> permit any
Router(config)# interface <interface>
Router(config-if)# ip access-group <number> {in | out}
```

**Important ACL Rules:**
1. Every ACL has an implicit `deny any` at the end
2. At least one `permit` statement is required
3. Standard ACLs should be placed **close to destination**
4. ACL statements are processed **top to bottom**

---

### Task 5: Configuring Standard ACLs

#### Scenario 1: Block Single Host (192.16.3.3) from HR Network (192.16.5.0)

**Objective:** Block host 192.16.3.3 (PC from Developers) from accessing network 192.16.5.0 (HR - PC3, PC4), while allowing it to access other networks. Other PCs from 192.16.3.0 network must be able to access 192.16.5.0.

**Configuration on R2:**

```cisco
R2# configure terminal

! Create ACL 1 to deny specific host
R2(config)# access-list 1 deny host 192.16.3.3
R2(config)# access-list 1 permit any

! Apply ACL to interface Fa0/1 (HR Network) - outbound direction
R2(config)# interface FastEthernet0/1
R2(config-if)# ip access-group 1 out
R2(config-if)# exit

R2(config)# end
R2# write memory
```

**Explanation:**
- `access-list 1 deny host 192.16.3.3` - Denies traffic from specific host
- `host` keyword = wildcard mask 0.0.0.0 (exact match)
- `access-list 1 permit any` - Permits all other traffic (overrides implicit deny)
- `ip access-group 1 out` - Applies ACL to outbound traffic on Fa0/1

---

### How to Test ACL 1 Configuration

**Step 1: Verify ACL is Applied**

```cisco
R2# show access-lists
R2# show access-lists 1
```

**Expected Output:**
```
Standard IP access list 1
    10 deny host 192.16.3.3
    20 permit any
```

```cisco
R2# show ip interface FastEthernet0/1
```

**Look for:**
```
Outgoing access list is 1
Inbound access list is not set
```

---

**Step 2: Test from PC with IP 192.16.3.3 (DENIED)**

Identify which PC has IP 192.16.3.3:
- This should be one of the PCs in the Developers network (S1 switch connected to R1)
- In Packet Tracer, check the PC's current IP from DHCP or check your addressing table

**From PC with 192.16.3.3, try to ping HR:**
```
PC> ping 192.16.5.1    ❌ Should FAIL (request blocked)
PC> ping 192.16.5.2    ❌ Should FAIL (request blocked)
PC> ping 192.16.5.3    ❌ Should FAIL (all HR hosts blocked)
```

**From PC with 192.16.3.3, try to ping OTHER networks (should work):**
```
PC> ping 192.16.4.1    ✅ Should SUCCEED (Sales not blocked)
PC> ping 192.16.6.1    ✅ Should SUCCEED (QA not blocked)
PC> ping 192.16.7.1    ✅ Should SUCCEED (Servers not blocked)
```

---

**Step 3: Test from OTHER PCs in Developers Network (ALLOWED)**

**From any other Developers PC (192.16.3.2, 192.16.3.4, 192.16.3.5, etc.):**
```
PC> ping 192.16.5.1    ✅ Should SUCCEED (only 192.16.3.3 blocked)
PC> ping 192.16.5.2    ✅ Should SUCCEED 
PC> ping 192.16.5.3    ✅ Should SUCCEED
```

**These PCs should access HR normally!**

---

**Step 4: Test from Other Networks (ALLOWED)**

**From Sales (192.16.4.0):**
```
PC> ping 192.16.5.1    ✅ Should SUCCEED
PC> ping 192.16.5.2    ✅ Should SUCCEED
```

**From QA (192.16.6.0):**
```
PC> ping 192.16.5.1    ✅ Should SUCCEED
PC> ping 192.16.5.2    ✅ Should SUCCEED
```

---

### Complete Testing Summary Table

| Test Case | Source IP | Destination | Expected Result | Reason |
|-----------|-----------|-------------|-----------------|--------|
| 1 | 192.16.3.3 | 192.16.5.1 (HR) | ❌ FAIL | Denied by ACL 1 |
| 2 | 192.16.3.3 | 192.16.5.2 (HR) | ❌ FAIL | Denied by ACL 1 |
| 3 | 192.16.3.3 | 192.16.4.1 (Sales) | ✅ PASS | Not blocked by HR ACL |
| 4 | 192.16.3.3 | 192.16.6.1 (QA) | ✅ PASS | Not blocked by HR ACL |
| 5 | 192.16.3.2 | 192.16.5.1 (HR) | ✅ PASS | Different source IP |
| 6 | 192.16.3.4 | 192.16.5.1 (HR) | ✅ PASS | Different source IP |
| 7 | 192.16.4.1 | 192.16.5.1 (HR) | ✅ PASS | Sales can access HR |
| 8 | 192.16.6.1 | 192.16.5.1 (HR) | ✅ PASS | QA can access HR |

---

### Troubleshooting Tips

**If ALL pings from Developers to HR fail:**
- ❌ May have ACL on Sales interface too
- ❌ May have global routing issue
- ✅ Check `show access-lists` - should only show ACL 1

**If PC 192.16.3.3 can still ping HR:**
- ❌ ACL not applied to correct interface
- ❌ ACL applied to wrong direction (in vs out)
- ✅ Verify with `show ip interface FastEthernet0/1`
- ✅ Check ACL syntax: should be `host 192.16.3.3` not `192.16.3.3 0.0.0.0`

**If other PCs in 192.16.3.0 cannot ping HR:**
- ❌ ACL may be blocking entire network instead of single host
- ❌ Check ACL line: should have `deny host 192.16.3.3` not `deny 192.16.3.0`

---

### How to Remove ACL if Needed

**To test again or change configuration:**

```cisco
R2# configure terminal

! Remove ACL from interface
R2(config)# interface FastEthernet0/1
R2(config-if)# no ip access-group 1 out
R2(config-if)# exit

! Delete entire ACL
R2(config)# no access-list 1

R2(config)# end
R2# write memory
```

---

#### Scenario 2: Block Developers from HR (But HR CAN ping Developers) ✅

**Objective:** 
- Developers (192.16.3.0) **CANNOT** ping HR (192.16.5.0) ❌
- HR (192.16.5.0) **CAN** ping Developers (192.16.3.0) ✅
- All other networks can access HR normally

**⚠️ IMPORTANT - Standard ACL Limitation:**
Standard ACLs only filter by **source IP address**, not destination. This creates a challenge:
- When Developer pings HR: Source = 192.16.3.x → **Can be blocked** ✅
- When HR pings Developer: Reply has Source = 192.16.3.x → **Would also be blocked** ❌

**Solution: Apply ACL on the WAN interface (close to source)**

```cisco
R2# configure terminal

! Create ACL 2 to deny Developers traffic destined for HR
R2(config)# access-list 2 deny 192.16.3.0 0.0.0.255
R2(config)# access-list 2 permit any

! Apply INBOUND on Se0/1/0 (interface facing Developers network)
R2(config)# interface Serial0/1/0
R2(config-if)# ip access-group 2 in
R2(config-if)# exit

R2(config)# end
R2# write memory
```

**How This Works:**

**When Developers ping HR:**
1. Developer PC (192.16.3.2) sends ping to HR (192.16.5.2)
2. Packet enters R2 via Se0/1/0 (INBOUND)
3. ACL checks: Source = 192.16.3.2 → **DENIED** ❌
4. Ping fails ✅

**When HR pings Developers:**
1. HR PC (192.16.5.2) sends ping to Developer (192.16.3.2)
2. Packet enters R2 via Fa0/1 (no ACL there)
3. Packet exits via Se0/1/0 (outbound - no ACL check)
4. Reaches Developer ✅
5. Reply: Source = 192.16.3.2, enters via Se0/1/0 (INBOUND)
6. ACL checks: Source = 192.16.3.2 → **DENIED** ❌

**⚠️ Problem:** Even with INBOUND on Se0/1/0, the reply is still blocked!

---

**BEST SOLUTION: Use Extended ACL (If allowed in your lab)**

```cisco
R2# configure terminal

! Create Extended ACL to block Developer→HR but allow HR→Developer
R2(config)# access-list 100 deny ip 192.16.3.0 0.0.0.255 192.16.5.0 0.0.0.255
R2(config)# access-list 100 permit ip any any

! Apply to interface
R2(config)# interface Serial0/1/0
R2(config-if)# ip access-group 100 in
R2(config-if)# exit

R2(config)# end
R2# write memory
```

**Extended ACL Explanation:**
- Denies traffic FROM 192.16.3.0 TO 192.16.5.0 specifically
- When Developer pings HR: Source=192.16.3.x, Dest=192.16.5.x → **DENIED** ❌
- When HR pings Developer: Source=192.16.5.x, Dest=192.16.3.x → **ALLOWED** ✅
- Reply traffic: Source=192.16.3.x, Dest=192.16.5.x → **DENIED** ❌

**Still has issue with replies!** To properly allow HR→Developer with replies, use:

```cisco
R2(config)# access-list 100 deny icmp 192.16.3.0 0.0.0.255 192.16.5.0 0.0.0.255 echo
R2(config)# access-list 100 permit ip any any
```

This blocks ICMP echo requests FROM Developers TO HR, but allows echo-replies.

---

**PRACTICAL STANDARD ACL SOLUTION (For Lab 8):**

Since this is a **Standard ACL lab**, use the original configuration and understand the limitation:

```cisco
R2# configure terminal
R2(config)# access-list 2 deny 192.16.3.0 0.0.0.255
R2(config)# access-list 2 permit any
R2(config)# interface FastEthernet0/1
R2(config-if)# ip access-group 2 out
R2(config-if)# exit
R2(config)# end
R2# write memory
```

**What this achieves:**
- ✅ Blocks Developers from initiating connection to HR
- ❌ Also blocks HR ping replies from Developers (Standard ACL limitation)
- ✅ Shows correct Standard ACL placement (close to destination)
- ✅ Demonstrates understanding of ACL limitations

**Testing Results:**
```
From PC7 (Developer):
PC> ping 192.16.5.1    ❌ FAIL (Blocked by ACL)

From PC3 (HR):  
PC> ping 192.16.3.1    ⚠️ May fail (reply blocked if ACL on Fa0/1 out)
                       ✅ Works if ACL on Se0/1/0 in
```

**Conclusion:** For true bidirectional control (block one way, allow other), **Extended ACL** is required. Standard ACL can only block based on source IP regardless of direction.

---

#### Scenario 3: Block Entire Developers Network from Sales Network (OPTIONAL)

**Objective:** Block entire network 192.16.3.0/24 (Developers - PC7, PC8) from accessing network 192.16.4.0/24 (Sales - PC1, PC2), while allowing access to other networks.

**Configuration on R2:**

```cisco
R2# configure terminal

! Create ACL 3 to deny Developers from Sales
R2(config)# access-list 3 deny 192.16.3.0 0.0.0.255
R2(config)# access-list 3 permit any

! Apply ACL to interface Fa0/0 (Sales Network) - outbound direction
R2(config)# interface FastEthernet0/0
R2(config-if)# ip access-group 3 out
R2(config-if)# exit

R2(config)# end
R2# write memory
```

**Explanation:**
- Denies all hosts from Developers network
- Applied outbound on the destination interface (Fa0/0 → Sales Network)

---

#### Scenario 4: Block QA Network (192.16.6.0) from Server Access (192.16.7.0)

**Objective:** Block PC5, PC6 (QA - 192.16.6.0) from accessing Server Network (192.16.7.0)

**Configuration on R3:**

```cisco
R3# configure terminal
R3(config)# access-list 3 deny 192.16.6.0 0.0.0.255
R3(config)# access-list 3 permit any
R3(config)# interface FastEthernet0/0
R3(config-if)# ip access-group 3 out
R3(config-if)# exit
R3(config)# end
R3# write memory
```

**Explanation:**
- Applied on R3 Fa0/0 (server network interface)
- Outbound direction blocks traffic going to servers

---

#### Scenario 4: Block Developers Network (192.16.3.0) from Server Access

**Objective:** Block PC7, PC8 (Developers - 192.16.3.0) from accessing Servers

**Configuration on R3:**

```cisco
R3# configure terminal
R3(config)# access-list 4 deny 192.16.3.0 0.0.0.255
R3(config)# access-list 4 permit any
R3(config)# interface FastEthernet0/0
R3(config-if)# ip access-group 4 out
R3(config-if)# exit
R3(config)# end
R3# write memory
```

**Note:** Cannot apply multiple ACLs to same interface/direction. Use only one ACL per interface/direction.

---

#### Scenario 5: Permit Only HR Network to Access Servers

**Objective:** Only allow Network 192.16.5.0 (HR - PC3, PC4) to access Server Network, block all others

**Configuration on R3:**

```cisco
R3# configure terminal
R3(config)# access-list 5 permit 192.16.5.0 0.0.0.255
! Implicit deny any blocks all other networks
R3(config)# interface FastEthernet0/0
R3(config-if)# ip access-group 5 out
R3(config-if)# exit
R3(config)# end
R3# write memory
```

**Warning:** This will block ALL networks except HR from accessing servers!

---

## Verification Commands

### Show Access Lists

```cisco
R2# show access-lists
```

**Expected Output:**
```
Standard IP access list 1
    10 deny host 192.16.3.3
    20 permit any
Standard IP access list 2
    10 deny 192.16.3.0 0.0.0.255 (Developers blocked from HR)
    20 permit any
Standard IP access list 3
    10 deny 192.16.3.0 0.0.0.255 (Developers blocked from Sales)
    20 permit any
```

### Show Interface ACL Application

```cisco
R2# show ip interface FastEthernet0/1
```

**Look for:**
```
Outgoing access list is 1
Inbound access list is not set
```

### Show Running Configuration

```cisco
R2# show running-config | include access
R2# show running-config | section access-list
```

### Test Connectivity Before ACL

**Before applying ACLs, verify full connectivity:**
```
PC7> ping 192.16.4.1    (Should SUCCEED)
PC7> ping 192.16.5.1    (Should SUCCEED)
PC7> ping 192.16.7.1    (Should SUCCEED)
```

### Test ACL Functionality

**From PC7 or PC8 in Developers Network (192.16.3.0):**
```
PC> ping 192.16.5.1    (Should FAIL - ACL 2 blocks Developers from HR)
PC> ping 192.16.5.2    (Should FAIL - entire HR network blocked)
PC> ping 192.16.4.1    (Should FAIL if ACL 3 applied - blocked from Sales)
PC> ping 192.16.6.1    (Should SUCCEED - QA network not blocked)
PC> ping 192.16.7.1    (Should SUCCEED - Server network not blocked)
```

**From PC1 or PC2 in Sales Network (192.16.4.0):**
```
PC> ping 192.16.5.1    (Should SUCCEED - Sales can access HR)
PC> ping 192.16.6.1    (Should SUCCEED)
PC> ping 192.16.7.1    (Should SUCCEED)
```

**From PC3 or PC4 in HR Network (192.16.5.0):**
```
PC> ping 192.16.3.1    (Should SUCCEED - HR can reach Developers router)
PC> ping 192.16.3.2    (Should SUCCEED - return traffic is allowed)
PC> ping 192.16.4.1    (Should SUCCEED)
PC> ping 192.16.7.1    (Should SUCCEED)
```

**Key Point:** ACL blocks traffic FROM Developers TO HR, but return traffic from HR to Developers is allowed!

---

## ACL Summary Table

| ACL # | Action | Source | Wildcard | Applied To | Direction | Purpose |
|-------|--------|--------|----------|------------|-----------|---------|
| 1 | Deny | host 192.16.3.3 | 0.0.0.0 | R2 Fa0/1 (HR) | Out | Block single host from HR |
| 1 | Permit | any | - | R2 Fa0/1 | Out | Allow all other traffic |
| **2** | **Deny** | **192.16.3.0** | **0.0.0.255** | **R2 Fa0/1 (HR)** | **Out** | **Block Developers from HR** ✅ |
| 2 | Permit | any | - | R2 Fa0/1 | Out | Allow all other traffic |
| 3 | Deny | 192.16.3.0 | 0.0.0.255 | R2 Fa0/0 (Sales) | Out | Block Developers from Sales |
| 3 | Permit | any | - | R2 Fa0/0 | Out | Allow all other traffic |
| 10 | Deny | 192.16.6.0 | 0.0.0.255 | R3 Fa0/0 (Servers) | Out | Block QA from Servers |
| 10 | Permit | any | - | R3 Fa0/0 | Out | Allow all other traffic |

**Important:** Only one ACL can be applied per interface per direction!

**Primary ACL Configuration (As Required):**
- **ACL 2 on R2 Fa0/1**: Blocks entire Developers network (192.16.3.0) from accessing HR network (192.16.5.0)

---

## Network Summary Table

| Network | Network Address | Department | Connected Devices | Gateway |
|---------|-----------------|------------|-------------------|---------|
| WAN 1 | 192.16.1.0/24 | - | R1 ↔ R2 | - |
| WAN 2 | 192.16.2.0/24 | - | R2 ↔ R3 | - |
| LAN 1 | 192.16.3.0/24 | Developers | PC7, PC8 | 192.16.3.1 (R1) |
| LAN 2 | 192.16.4.0/24 | Sales | PC1, PC2 | 192.16.4.1 (R2) |
| LAN 3 | 192.16.5.0/24 | HR | PC3, PC4 | 192.16.5.1 (R2) |
| LAN 4 | 192.16.6.0/24 | QA | PC5, PC6 | 192.16.6.1 (R2) |
| Server | 192.16.7.0/24 | Servers | HTTP, DNS, DHCP | 192.16.7.1 (R3) |

---

## Wildcard Mask Quick Reference

| CIDR | Subnet Mask | Wildcard Mask | Hosts |
|------|-------------|---------------|-------|
| /24 | 255.255.255.0 | 0.0.0.255 | 254 |
| /25 | 255.255.255.128 | 0.0.0.127 | 126 |
| /26 | 255.255.255.192 | 0.0.0.63 | 62 |
| /27 | 255.255.255.224 | 0.0.0.31 | 30 |
| /28 | 255.255.255.240 | 0.0.0.15 | 14 |
| /29 | 255.255.255.248 | 0.0.0.7 | 6 |
| /30 | 255.255.255.252 | 0.0.0.3 | 2 |
| /32 | 255.255.255.255 | 0.0.0.0 | 1 (host) |

**Special Keywords:**
- `host 192.16.3.3` = `192.16.3.3 0.0.0.0` (exact match)
- `any` = `0.0.0.0 255.255.255.255` (match all)

---

## Lab Questions & Answers

### Q1: What is the purpose of DHCP?
**Answer:** DHCP dynamically assigns IP addresses and other network configuration (subnet mask, default gateway, DNS server) to devices, eliminating the need for manual IP configuration.

### Q2: What is an ACL?
**Answer:** An ACL (Access Control List) is a router configuration script that controls whether a router permits or denies packets based on criteria found in the packet header. It acts as a firewall to filter network traffic.

### Q3: What is the difference between Standard and Extended ACLs?
**Answer:**
- **Standard ACL (1-99, 1300-1999):** Filters based on source IP address only
- **Extended ACL (100-199, 2000-2699):** Filters based on source IP, destination IP, protocol type, and port numbers

### Q4: Where should Standard ACLs be placed?
**Answer:** Standard ACLs should be placed **as close to the destination as possible** because they can only filter by source address.

### Q5: What is the implicit deny statement?
**Answer:** Every ACL contains a final invisible `deny any` statement that denies all traffic not explicitly permitted. This is why at least one `permit` statement is required.

### Q6: What is a wildcard mask?
**Answer:** A wildcard mask is the inverse of a subnet mask, used in ACLs to specify which bits of an IP address to match. Calculate: `255.255.255.255 - Subnet Mask = Wildcard Mask`

### Q7: Verify if ACL is created successfully - what command to use?
**Answer:** `show access-lists` or `show access-list <number>`

### Q8: Is ping successful after applying ACL?
**Answer:** 
- From 192.16.3.3 to 192.16.5.0 (HR): **NO** (blocked by ACL 1)
- From 192.16.3.0 to 192.16.4.0 (Sales): **NO** (blocked by ACL 2)
- All other traffic: **YES** (permitted)

---

## Common ACL Troubleshooting

| Problem | Solution |
|---------|----------|
| All traffic blocked | Add `permit any` statement |
| ACL not working | Check interface and direction (in/out) |
| Wrong traffic blocked | Verify wildcard mask calculation |
| ACL order issues | Remember: first match wins |

---

## Command Quick Reference

| Command | Purpose |
|---------|---------|
| `access-list # permit/deny source wildcard` | Create ACL entry |
| `ip access-group # in/out` | Apply ACL to interface |
| `show access-lists` | Display all ACLs |
| `show ip interface` | Show ACL applied to interface |
| `no access-list #` | Remove entire ACL |
| `ip dhcp pool NAME` | Create DHCP pool |
| `show ip dhcp binding` | Show DHCP leases |

---

## Complete Interface Summary

### R1 (DTE)
| Interface | IP Address | Type | Connected To |
|-----------|------------|------|--------------|
| Se0/1/0 | 192.16.1.1 | DTE | R2 Se0/1/0 (WAN) |
| Fa0/0 | 192.16.3.1 | LAN | S1 (Developers - PC7, PC8) |

### R2 (Central Router - DCE on both serial)
| Interface | IP Address | Type | Connected To |
|-----------|------------|------|--------------|
| Se0/1/0 | 192.16.1.2 | DCE (clock rate 64000) | R1 Se0/1/0 (WAN) |
| Se0/2/0 | 192.16.2.1 | DCE (clock rate 64000) | R3 Se0/2/0 (WAN) |
| Fa0/0 | 192.16.4.1 | LAN | S2 (Sales - PC1, PC2) |
| Fa0/1 | 192.16.5.1 | LAN | S3 (HR - PC3, PC4) |
| Fa1/0 | 192.16.6.1 | LAN | S4 (QA - PC5, PC6) |

### R3 (DTE)
| Interface | IP Address | Type | Connected To |
|-----------|------------|------|--------------|
| Se0/2/0 | 192.16.2.2 | DTE | R2 Se0/2/0 (WAN) |
| Fa0/0 | 192.16.7.1 | LAN | S5 (Servers - HTTP, DNS, DHCP) |

---

**End of Solution Manual**
