# Lab 4 — Three Router WAN Topology (R1, R2, R3)

## Topology Overview

```
 Network 1              Network 2              Network 3
 192.168.1.0/24         192.168.3.0/24        192.168.5.0/24
 
 PC1 (192.168.1.10)    PC2 (192.168.3.10)    PC3 (192.168.5.10)
   |                     |                      |
   | Fa0                 | Fa0                  | Fa0
   |                     |                      |
 Switch1              Switch2               Switch3
   |                     |                      |
   | Fa1/1               | Fa1/1                | Fa1/1
   |                     |                      |
 R1 Fa0/0             R2 Fa0/0              R3 Fa0/0
 192.168.1.1         192.168.3.1           192.168.5.1
   |                     |                      |
   | S0/0/0 (DCE)        | S0/0/0 (DTE)        | S0/0/1 (DTE)
   |                     |                      |
   +----192.168.2.0/24---+                     |
                        |                      |
                        | S0/0/1 (DCE)        |
                        +----192.168.4.0/24---+

WAN Links:
- R1 S0/0/0 (DCE, clock) ↔ R2 S0/0/0 (DTE)
- R2 S0/0/1 (DCE, clock) ↔ R3 S0/0/1 (DTE)
```

---

## Devices (8 total)

| Device | Type   | Model     | Notes |
|--------|--------|-----------|-------|
| **R1** | Router | Router-PT | |
| **R2** | Router | Router-PT | |
| **R3** | Router | Router-PT | |
| **Switch1** | Switch | Switch-PT | PC1 side |
| **Switch2** | Switch | Switch-PT | PC2 side |
| **Switch3** | Switch | Switch-PT | PC3 side |
| **PC1** | PC | PC-PT | |
| **PC2** | PC | PC-PT | |
| **PC3** | PC | PC-PT | |

---

## Addressing Table

| Device | Interface | IP Address   | Subnet Mask   | Default Gateway |
|--------|-----------|--------------|---------------|-----------------|
| R1 | Fa0/0 | 192.168.1.1 | 255.255.255.0 | N/A |
| R1 | S0/0/0 | 192.168.2.1 | 255.255.255.0 | N/A |
| R2 | S0/0/0 | 192.168.2.2 | 255.255.255.0 | N/A |
| R2 | Fa0/0 | 192.168.3.1 | 255.255.255.0 | N/A |
| R2 | S0/0/1 | 192.168.4.1 | 255.255.255.0 | N/A |
| R3 | S0/0/1 | 192.168.4.2 | 255.255.255.0 | N/A |
| R3 | Fa0/0 | 192.168.5.1 | 255.255.255.0 | N/A |
| PC1 | Fa0 | 192.168.1.10 | 255.255.255.0 | 192.168.1.1 |
| PC2 | Fa0 | 192.168.3.10 | 255.255.255.0 | 192.168.3.1 |
| PC3 | Fa0 | 192.168.5.10 | 255.255.255.0 | 192.168.5.1 |

---

## Cables

| # | Connection           | Cable Type           | Notes |
|---|----------------------|----------------------|-------|
| 1 | PC1 Fa0 ↔ Switch1 Fa0/1 | Copper Straight-Through | Different device types |
| 2 | Switch1 Fa1/1 ↔ R1 Fa0/0 | Copper Straight-Through | Different device types |
| 3 | PC2 Fa0 ↔ Switch2 Fa0/1 | Copper Straight-Through | Different device types |
| 4 | Switch2 Fa1/1 ↔ R2 Fa0/0 | Copper Straight-Through | Different device types |
| 5 | PC3 Fa0 ↔ Switch3 Fa0/1 | Copper Straight-Through | Different device types |
| 6 | Switch3 Fa1/1 ↔ R3 Fa0/0 | Copper Straight-Through | Different device types |
| 7 | R1 S0/0/0 ↔ R2 S0/0/0 | Serial DCE | R1 = DCE (clock), click R1 first |
| 8 | R2 S0/0/1 ↔ R3 S0/0/1 | Serial DCE | R2 = DCE (clock), click R2 first |

---

## Step 1: Build the Topology

### Add Devices

1. Add **Router-PT** → name **R1**
2. Add **Router-PT** → name **R2** (to the right of R1)
3. Add **Router-PT** → name **R3** (to the right of R2)
4. Add **Switch-PT** → name **Switch1** (to the left of R1)
5. Add **Switch-PT** → name **Switch2** (below R2)
6. Add **Switch-PT** → name **Switch3** (to the right of R3)
7. Add **PC-PT** → name **PC1** (to the left of Switch1)
8. Add **PC-PT** → name **PC2** (below Switch2)
9. Add **PC-PT** → name **PC3** (to the right of Switch3)

### Cable Connections

**Cable 1 — PC1 to Switch1 (Straight-Through)**
```
Select: Copper Straight-Through
PC1 Fa0 → Switch1 Fa0/1
```

**Cable 2 — Switch1 to R1 (Straight-Through)**
```
Select: Copper Straight-Through
Switch1 Fa1/1 → R1 Fa0/0
```

**Cable 3 — PC2 to Switch2 (Straight-Through)**
```
Select: Copper Straight-Through
PC2 Fa0 → Switch2 Fa0/1
```

**Cable 4 — Switch2 to R2 (Straight-Through)**
```
Select: Copper Straight-Through
Switch2 Fa1/1 → R2 Fa0/0
```

**Cable 5 — PC3 to Switch3 (Straight-Through)**
```
Select: Copper Straight-Through
PC3 Fa0 → Switch3 Fa0/1
```

**Cable 6 — Switch3 to R3 (Straight-Through)**
```
Select: Copper Straight-Through
Switch3 Fa1/1 → R3 Fa0/0
```

**Cable 7 — R1 S0/0/0 to R2 S0/0/0 (Serial DCE)**
```
Select: Serial DCE
Click R1 FIRST → S0/0/0  (R1 = DCE)
Click R2 → S0/0/0
```

**Cable 8 — R2 S0/0/1 to R3 S0/0/1 (Serial DCE)**
```
Select: Serial DCE
Click R2 FIRST → S0/0/1  (R2 = DCE)
Click R3 → S0/0/1
```

---

## Step 2: Configure R1 (First Router)

Click **R1** → **CLI** tab:

```
Router> enable
Router# configure terminal

! Hostname
Router(config)# hostname R1

! Disable DNS lookup
R1(config)# no ip domain-lookup

! Enable secret
R1(config)# enable secret class

! Console password
R1(config)# line console 0
R1(config-line)# password cisco
R1(config-line)# login
R1(config-line)# exit

! VTY password
R1(config)# line vty 0 4
R1(config-line)# password cisco
R1(config-line)# login
R1(config-line)# exit

! Configure Fa0/0 — LAN side (PC1)
R1(config)# interface fastethernet 0/0
R1(config-if)# ip address 192.168.1.1 255.255.255.0
R1(config-if)# description LAN - Connected to PC1
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure S0/0/0 — WAN side to R2 (DCE)
R1(config)# interface serial 0/0/0
R1(config-if)# ip address 192.168.2.1 255.255.255.0
R1(config-if)# clock rate 64000
R1(config-if)# description WAN1 - Serial link to R2 (DCE)
R1(config-if)# no shutdown
R1(config-if)# exit

! Static routes
R1(config)# ip route 192.168.3.0 255.255.255.0 192.168.2.2
R1(config)# ip route 192.168.4.0 255.255.255.0 192.168.2.2
R1(config)# ip route 192.168.5.0 255.255.255.0 192.168.2.2

! Save
R1(config)# exit
R1# copy running-config startup-config
```

---

## Step 3: Configure R2 (Middle Router)

Click **R2** → **CLI** tab:

```
Router> enable
Router# configure terminal

! Hostname
Router(config)# hostname R2

! Disable DNS lookup
R2(config)# no ip domain-lookup

! Enable secret
R2(config)# enable secret class

! Console password
R2(config)# line console 0
R2(config-line)# password cisco
R2(config-line)# login
R2(config-line)# exit

! VTY password
R2(config)# line vty 0 4
R2(config-line)# password cisco
R2(config-line)# login
R2(config-line)# exit

! Configure S0/0/0 — WAN side to R1 (DTE)
R2(config)# interface serial 0/0/0
R2(config-if)# ip address 192.168.2.2 255.255.255.0
R2(config-if)# description WAN1 - Serial link to R1 (DTE)
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure Fa0/0 — LAN side (PC2)
R2(config)# interface fastethernet 0/0
R2(config-if)# ip address 192.168.3.1 255.255.255.0
R2(config-if)# description LAN - Connected to PC2
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure S0/0/1 — WAN side to R3 (DCE)
R2(config)# interface serial 0/0/1
R2(config-if)# ip address 192.168.4.1 255.255.255.0
R2(config-if)# clock rate 64000
R2(config-if)# description WAN2 - Serial link to R3 (DCE)
R2(config-if)# no shutdown
R2(config-if)# exit

! Static routes
R2(config)# ip route 192.168.1.0 255.255.255.0 192.168.2.1
R2(config)# ip route 192.168.5.0 255.255.255.0 192.168.4.2

! Save
R2(config)# exit
R2# copy running-config startup-config
```

---

## Step 4: Configure R3 (Last Router)

Click **R3** → **CLI** tab:

```
Router> enable
Router# configure terminal

! Hostname
Router(config)# hostname R3

! Disable DNS lookup
R3(config)# no ip domain-lookup

! Enable secret
R3(config)# enable secret class

! Console password
R3(config)# line console 0
R3(config-line)# password cisco
R3(config-line)# login
R3(config-line)# exit

! VTY password
R3(config)# line vty 0 4
R3(config-line)# password cisco
R3(config-line)# login
R3(config-line)# exit

! Configure S0/0/1 — WAN side to R2 (DTE)
R3(config)# interface serial 0/0/1
R3(config-if)# ip address 192.168.4.2 255.255.255.0
R3(config-if)# description WAN2 - Serial link to R2 (DTE)
R3(config-if)# no shutdown
R3(config-if)# exit

! Configure Fa0/0 — LAN side (PC3)
R3(config)# interface fastethernet 0/0
R3(config-if)# ip address 192.168.5.1 255.255.255.0
R3(config-if)# description LAN - Connected to PC3
R3(config-if)# no shutdown
R3(config-if)# exit

! Static routes
R3(config)# ip route 192.168.1.0 255.255.255.0 192.168.4.1
R3(config)# ip route 192.168.2.0 255.255.255.0 192.168.4.1
R3(config)# ip route 192.168.3.0 255.255.255.0 192.168.4.1

! Save
R3(config)# exit
R3# copy running-config startup-config
```

---

## Step 5: Configure PCs

### PC1 Configuration

Click **PC1** → **Desktop** → **IP Configuration** → **Static**

```
IP Address: 192.168.1.10
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.1.1
```

### PC2 Configuration

Click **PC2** → **Desktop** → **IP Configuration** → **Static**

```
IP Address: 192.168.3.10
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.3.1
```

### PC3 Configuration

Click **PC3** → **Desktop** → **IP Configuration** → **Static**

```
IP Address: 192.168.5.10
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.5.1
```

---

## Step 6: Verify Configuration

### Check Routing Tables

**R1:**
```
R1# show ip route
```
Should show:
```
C    192.168.1.0/24 is directly connected, FastEthernet0/0
C    192.168.2.0/24 is directly connected, Serial0/0/0
S    192.168.3.0/24 [1/0] via 192.168.2.2
S    192.168.4.0/24 [1/0] via 192.168.2.2
S    192.168.5.0/24 [1/0] via 192.168.2.2
```

**R2:**
```
R2# show ip route
```
Should show:
```
S    192.168.1.0/24 [1/0] via 192.168.2.1
C    192.168.2.0/24 is directly connected, Serial0/0/0
C    192.168.3.0/24 is directly connected, FastEthernet0/0
C    192.168.4.0/24 is directly connected, Serial0/0/1
S    192.168.5.0/24 [1/0] via 192.168.4.2
```

**R3:**
```
R3# show ip route
```
Should show:
```
S    192.168.1.0/24 [1/0] via 192.168.4.1
S    192.168.2.0/24 [1/0] via 192.168.4.1
S    192.168.3.0/24 [1/0] via 192.168.4.1
C    192.168.4.0/24 is directly connected, Serial0/0/1
C    192.168.5.0/24 is directly connected, FastEthernet0/0
```

### Check Interface Status

**R1:**
```
R1# show ip interface brief
```
All interfaces should be `up/up`

**R2:**
```
R2# show ip interface brief
```
All interfaces should be `up/up`

**R3:**
```
R3# show ip interface brief
```
All interfaces should be `up/up`

---

## Step 7: Test Connectivity

### Test from PC1

```
C:\> ping 192.168.3.10  ✓ PC2
C:\> ping 192.168.5.10  ✓ PC3
```

### Test from PC2

```
C:\> ping 192.168.1.10  ✓ PC1
C:\> ping 192.168.5.10  ✓ PC3
```

### Test from PC3

```
C:\> ping 192.168.1.10  ✓ PC1
C:\> ping 192.168.3.10  ✓ PC2
```

All pings should succeed! ✓

---

## Step 8: Test Router-to-Router

**From R1:**
```
R1# ping 192.168.4.2    ✓ R3 WAN interface
```

**From R2:**
```
R2# ping 192.168.1.1    ✓ R1 LAN
R2# ping 192.168.5.1    ✓ R3 LAN
```

**From R3:**
```
R3# ping 192.168.1.1    ✓ R1 WAN
```

---

## Summary

| Link | Type | Router1 Interface | Router2 Interface | Clock Rate | who is DCE |
|------|------|-------------------|-------------------|------------|-----------|
| WAN1 | Serial | R1 S0/0/0 | R2 S0/0/0 | 64000 | **R1** |
| WAN2 | Serial | R2 S0/0/1 | R3 S0/0/1 | 64000 | **R2** |

**Key Points:**
- R1 S0/0/0 is **DCE** → has `clock rate 64000`
- R2 S0/0/0 is **DTE** → NO clock rate
- R2 S0/0/1 is **DCE** → has `clock rate 64000`
- R3 S0/0/1 is **DTE** → NO clock rate

---

## Save Your Work!

```
File → Save as "Lab4_3Router_Topology.pkt"
```

**Done! You now have 3 routers, 3 PCs, all interconnected!** 🎉
