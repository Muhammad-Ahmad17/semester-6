# Lab 6 Solution (Pages 60-64)

## Task 3: Test and Verify Configurations (Before Routing)

### Step 1: LAN Connectivity
- From PC1, ping default gateway possible? **Yes** (`10.0.0.1`)
- From PC2, ping default gateway possible? **Yes** (`12.0.0.1`)
- From PC3, ping default gateway possible? **Yes** (`14.0.0.1`)

### Step 2: WAN Connectivity
- `show ip interface brief`: all relevant interfaces up? **Yes**, after `no shutdown` and setting clock rates (if required on DCE ends).
- From R2, ping R1 possible? **Yes** (`ping 11.0.0.1`)
- From R2, ping R3 possible? **Yes** (`ping 13.0.0.2`)

### Step 3: Routing Table Observation
- Routers initially know only their directly connected networks.
- Why all networks are not present? Because dynamic or static routing has not been configured yet.
- Can PC1 ping PC3? **No**, because the routers do not have routes to non-directly connected networks.

---

## Task 4: Configure RIP v1

To configure RIP, use the `router rip` command followed by the `network` command for each directly connected Class A network.

---

## Task 5: Enable RIPv1 on Router 1

### Step 1 & 2: Run Commands
```bash
R1(config)# router rip
R1(config-router)# network 10.0.0.0
R1(config-router)# network 11.0.0.0
```

---

## Task 6: Enable RIPv1 on Router 3

### Step 1 & 2: Run Commands
```bash
R3(config)# router rip
R3(config-router)# network 13.0.0.0
R3(config-router)# network 14.0.0.0
```

### Step 3: Use ping to check connectivity
- Ping to check connectivity between the host PC2 and PC1, is ping successful and why?
  **No**. We have not configured RIP on R2 yet, so R2 does not advertise or forward routes between R1 and R3.
- Ping to check connectivity between the host PC3 and PC2, is ping successful and why?
  **No**. Same reason; R2 is not participating in RIP yet to route between PC2's network and PC3's network.
- Ping to check connectivity between the host PC1 and PC3, is ping successful and why?
  **No**. R2 is the middle router and it is not running RIP, so the end-to-end path is incomplete.

---

## Task 7: Enable RIPv1 on Router 2

### Step 1 & 2: Run Commands
```bash
R2(config)# router rip
R2(config-router)# network 11.0.0.0
R2(config-router)# network 12.0.0.0
R2(config-router)# network 13.0.0.0
```

---

## Task 8: Test and Verify the Routes

### Step 1: View the routing table
- Run `show ip route` command on each router. 
- **Observations:** New entries appear marked with an `R`, which stands for RIP. R1 now knows about 12.0.0.0, 13.0.0.0, and 14.0.0.0. R2 knows about 10.0.0.0 and 14.0.0.0. R3 knows about 10.0.0.0, 11.0.0.0, and 12.0.0.0.

### Step 2: Administrative Distance
- What is the value of Administrative Distance for RIP networks? **120**

### Step 3: Metrics value
- What is the metrics value against each network in R1 routing table? Explain it.
  **[120/1]** or **[120/2]**. The metric for RIP is hop count. A metric of `1` means the destination network is 1 router hop away. A metric of `2` means it is 2 hops away.

### Step 4: Use ping to check connectivity
- Ping to check connectivity between the host PC2 and PC1, is ping successful? **Yes**
- Ping to check connectivity between the host PC3 and PC2, is ping successful? **Yes**
- Ping to check connectivity between the host PC1 and PC3, is ping successful? **Yes**

---

## Task 9: Summary, Reflection, and Documentation

Save the outputs of:
- `show running-config`
- `show ip route`
- `show ip interface brief`

## Quick Command Summary

```bash
! R1
router rip
network 10.0.0.0
network 11.0.0.0

! R2
router rip
network 11.0.0.0
network 12.0.0.0
network 13.0.0.0

! R3
router rip
network 13.0.0.0
network 14.0.0.0
```
