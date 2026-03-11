# Lab 5 Solution (Pages 54-58)

## Task 3: Test and Verify Configurations

### Step 1: LAN Connectivity
- From PC1, ping default gateway possible? **Yes** (`192.168.1.1`)
- From PC2, ping default gateway possible? **Yes** (`192.168.3.1`)
- From PC3, ping default gateway possible? **Yes** (`192.168.5.1`)

### Step 2: WAN Connectivity
- `show ip interface brief`: all relevant interfaces up? **Yes**, after `no shutdown`.
- From R2, ping R1 possible? **Yes** (`ping 192.168.2.1`)
- From R2, ping R3 possible? **Yes** (`ping 192.168.4.2`)

### Step 3: Routing Table (Before Static Routes)
- Networks missing in R1 table: `192.168.3.0/24`, `192.168.4.0/24`, `192.168.5.0/24`
- Networks missing in R2 table: `192.168.1.0/24`, `192.168.5.0/24`
- Networks missing in R3 table: `192.168.1.0/24`, `192.168.2.0/24`, `192.168.3.0/24`
- Why all networks are not present? Routers initially know only directly connected networks.
- What can be added so non-directly connected networks can ping each other? Add routing (static/default/dynamic).

---

## Task 4: Configure Static Route Using Next-Hop Address

### Step 1 (R3 to Network 2)
```bash
R3(config)# ip route 192.168.3.0 255.255.255.0 192.168.4.1
```

### Step 2 (R2 to Network 3)
```bash
R2(config)# ip route 192.168.5.0 255.255.255.0 192.168.4.2
```

### Step 3 (R2 to Network 1)
```bash
R2(config)# ip route 192.168.1.0 255.255.255.0 192.168.2.1
```

### Step 4 (R1 to Network 2)
```bash
R1(config)# ip route 192.168.3.0 255.255.255.0 192.168.2.2
```

---

## Task 5: Test and Verify Static Routes

### Step 1: Routing Table Observation
- New entries appear with `S` code in `show ip route`.

### Step 2: Ping Results
- PC2 to PC1 ping successful? **Yes**. R2 has route to `192.168.1.0/24`, R1 has route to `192.168.3.0/24`.
- PC3 to PC2 ping successful? **Yes**. R3 has route to `192.168.3.0/24`, R2 has route to `192.168.5.0/24`.
- PC1 to PC3 ping successful? **No** (at this stage), because full end-to-end routes are not complete yet.

---

## Task 6: Configure Default Static Route

### Step 1: Default Route on R1
```bash
R1(config)# ip route 0.0.0.0 0.0.0.0 s0/0/0
```
(Alternative: `R1(config)# ip route 0.0.0.0 0.0.0.0 192.168.2.2`)

Observation: `S* 0.0.0.0/0` appears in routing table.

### Step 2: Remove old static route from R1
```bash
R1(config)# no ip route 192.168.3.0 255.255.255.0 192.168.2.2
```
Note: Manual line showing `R3(config)# ...` is a typo; removal should be done on R1.

Ping PC2 to PC1 successful after this? **Yes**, because R1 forwards unknown destinations to R2 via default route.

### Step 3: Default Route on R3
```bash
R3(config)# ip route 0.0.0.0 0.0.0.0 s0/0/1
```
(Alternative: `R3(config)# ip route 0.0.0.0 0.0.0.0 192.168.4.1`)

Observation: `S* 0.0.0.0/0` appears in R3 routing table.

### Step 4: Final Ping Verification
- PC2 to PC1: **Successful**
- PC3 to PC2: **Successful**
- PC1 to PC3: **Successful**

Reason: R1 and R3 use default routes toward R2, and R2 has specific routes for edge LANs.

---

## Quick Command Summary

```bash
! R1
ip route 192.168.3.0 255.255.255.0 192.168.2.2
ip route 0.0.0.0 0.0.0.0 s0/0/0
no ip route 192.168.3.0 255.255.255.0 192.168.2.2

! R2
ip route 192.168.1.0 255.255.255.0 192.168.2.1
ip route 192.168.5.0 255.255.255.0 192.168.4.2

! R3
ip route 192.168.3.0 255.255.255.0 192.168.4.1
ip route 0.0.0.0 0.0.0.0 s0/0/1
```
