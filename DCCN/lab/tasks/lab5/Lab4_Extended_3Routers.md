# Extended Topology — Adding Router2 with Switch and PC2

## New Topology Overview

```
PC0 (192.168.1.10)
   |
   | Fa0 ──Straight── Fa0/1
   |
Switch0
   |
   | Fa1/1 ──Straight── Fa0/0
   |
Router0 (LAN: 192.168.1.1, WAN: 192.168.2.1)
   |
   | Se2/0 ════Serial DCE════ Se2/0
   |
Router1 (WAN: 192.168.2.2, LAN: 192.168.3.1, NEW WAN2: 192.168.4.1)
   |
   | Fa0/0 ──CrossOver── Fa0
   |
PC1 (192.168.3.10)
   |
   | Se3/0 ════Serial DCE════ Se3/0  [Router1 = DCE for this link]
   |
Router2 (WAN: 192.168.4.2, LAN: 192.168.5.1)
   |
   | Fa0/0 ──Straight── Fa0/1
   |
Switch2
   |
   | Fa1/1 ──Straight── Fa0
   |
PC2 (192.168.5.10)  [NEW]
```

---

## New Devices

| Device      | Type          | Model     |
|-------------|---------------|-----------|
| **Router2** | Router        | Router-PT |
| **Switch2** | Switch        | Switch-PT |
| **PC2**     | End Device    | PC-PT     |

---

## New Cables

| # | Connection                  | Cable Type          |
|---|-----------------------------|--------------------|
| 5 | Router1 `Se3/0` → Router2 `Se3/0` | **Serial DCE** (click Router1 first) |
| 6 | Router2 `Fa0/0` → Switch2 `Fa0/1` | **Straight-Through** |
| 7 | Switch2 `Fa1/1` → PC2 `Fa0` | **Straight-Through** |

---

## Updated IP Addressing

| Device      | Interface | IP Address   | Subnet Mask   |
|-------------|-----------|--------------|---------------|
| Router0     | Fa0/0     | 192.168.1.1  | 255.255.255.0 |
| Router0     | Se2/0     | 192.168.2.1  | 255.255.255.0 |
| Router1     | Se2/0     | 192.168.2.2  | 255.255.255.0 |
| Router1     | Fa0/0     | 192.168.3.1  | 255.255.255.0 |
| **Router1** | **Se3/0** | **192.168.4.1** | **255.255.255.0** |
| **Router2** | **Se3/0** | **192.168.4.2** | **255.255.255.0** |
| **Router2** | **Fa0/0** | **192.168.5.1** | **255.255.255.0** |
| PC0         | Fa0       | 192.168.1.10 | 255.255.255.0 |
| PC1         | Fa0       | 192.168.3.10 | 255.255.255.0 |
| **PC2**     | **Fa0**   | **192.168.5.10** | **255.255.255.0** |

---

## Step 1: Add New Devices

1. Add **Router-PT** → place right of Router1 → name it **Router2**
2. Add **Switch-PT** → place right of Router2 → name it **Switch2**
3. Add **PC-PT** → place far right → name it **PC2**

---

## Step 2: Cable the New Devices

### Cable 5 — Router1 Se3/0 to Router2 Se3/0 (Serial DCE)

1. Select **Serial DCE**
2. **Click Router1 FIRST** → select `Se3/0` (Router1 = DCE provides clock)
3. Click **Router2** → select `Se3/0`
4. Both sides red (normal until configured)

### Cable 6 — Router2 Fa0/0 to Switch2 Fa0/1 (Straight-Through)

1. Select **Copper Straight-Through**
2. Click **Router2** → select `Fa0/0`
3. Click **Switch2** → select `Fa0/1`

### Cable 7 — Switch2 Fa1/1 to PC2 Fa0 (Straight-Through)

1. Select **Copper Straight-Through**
2. Click **Switch2** → select `Fa1/1`
3. Click **PC2** → select `Fa0`

---

## Step 3: Update Router1 Configuration

**Add the new Se3/0 interface to Router1 CLI:**

```
Router1# configure terminal
Router1(config)# interface serial 3/0
Router1(config-if)# ip address 192.168.4.1 255.255.255.0
Router1(config-if)# clock rate 64000
Router1(config-if)# description WAN - Serial link to Router2 (DCE)
Router1(config-if)# no shutdown
Router1(config-if)# exit

! Add static route to Router2's LAN
Router1(config)# ip route 192.168.5.0 255.255.255.0 192.168.4.2

Router1(config)# exit
Router1# copy running-config startup-config
```

---

## Step 4: Configure Router2 Completely

Click **Router2** → **CLI** tab:

```
Router> enable
Router# configure terminal

! Hostname
Router(config)# hostname Router2

! Disable DNS lookup
Router2(config)# no ip domain-lookup

! Enable secret
Router2(config)# enable secret class

! Console password
Router2(config)# line console 0
Router2(config-line)# password cisco
Router2(config-line)# login
Router2(config-line)# exit

! VTY password
Router2(config)# line vty 0 4
Router2(config-line)# password cisco
Router2(config-line)# login
Router2(config-line)# exit

! Se3/0 — WAN side (DTE — receives clock from Router1)
Router2(config)# interface serial 3/0
Router2(config-if)# ip address 192.168.4.2 255.255.255.0
Router2(config-if)# description WAN - Serial link to Router1 (DTE)
Router2(config-if)# no shutdown
Router2(config-if)# exit

! Fa0/0 — LAN side (connects to Switch2)
Router2(config)# interface fastethernet 0/0
Router2(config-if)# ip address 192.168.5.1 255.255.255.0
Router2(config-if)# description LAN - Connected to Switch2
Router2(config-if)# no shutdown
Router2(config-if)# exit

! Static routes to reach other networks
Router2(config)# ip route 192.168.1.0 255.255.255.0 192.168.4.1
Router2(config)# ip route 192.168.2.0 255.255.255.0 192.168.4.1
Router2(config)# ip route 192.168.3.0 255.255.255.0 192.168.4.1

Router2(config)# exit
Router2# copy running-config startup-config
```

---

## Step 5: Update Router0 Configuration

**Add route to reach Router2's LAN (192.168.5.0):**

Click **Router0** → **CLI** tab:

```
Router0# configure terminal
Router0(config)# ip route 192.168.5.0 255.255.255.0 192.168.2.2
Router0(config)# exit
Router0# copy running-config startup-config
```

---

## Step 6: Configure PC2

Click **PC2** → **Desktop** → **IP Configuration**

Select **Static**:
- **IP Address:** `192.168.5.10`
- **Subnet Mask:** `255.255.255.0`
- **Default Gateway:** `192.168.5.1`

Close the window.

---

## Step 7: Verify All Routes

**Router0:**
```
Router0# show ip route
```
Should show:
```
C    192.168.1.0/24 is directly connected, FastEthernet0/0
C    192.168.2.0/24 is directly connected, Serial2/0
S    192.168.3.0/24 [1/0] via 192.168.2.2
S    192.168.5.0/24 [1/0] via 192.168.2.2
```

**Router1:**
```
Router1# show ip route
```
Should show:
```
C    192.168.2.0/24 is directly connected, Serial2/0
C    192.168.3.0/24 is directly connected, FastEthernet0/0
C    192.168.4.0/24 is directly connected, Serial3/0
S    192.168.1.0/24 [1/0] via 192.168.2.1
S    192.168.5.0/24 [1/0] via 192.168.4.2
```

**Router2:**
```
Router2# show ip route
```
Should show:
```
C    192.168.4.0/24 is directly connected, Serial3/0
C    192.168.5.0/24 is directly connected, FastEthernet0/0
S    192.168.1.0/24 [1/0] via 192.168.4.1
S    192.168.2.0/24 [1/0] via 192.168.4.1
S    192.168.3.0/24 [1/0] via 192.168.4.1
```

---

## Step 8: Test End-to-End Connectivity

**From PC0, ping all:**
```
ping 192.168.3.10  ✓ PC1
ping 192.168.5.10  ✓ PC2
```

**From PC1, ping:**
```
ping 192.168.1.10  ✓ PC0
ping 192.168.5.10  ✓ PC2
```

**From PC2, ping:**
```
ping 192.168.1.10  ✓ PC0
ping 192.168.3.10  ✓ PC1
```

All should work! ✓

---

## Updated Network Summary

| Network | Devices | Via |
|---------|---------|-----|
| **192.168.1.0/24** | PC0, Router0 Fa0/0 | Switch0 |
| **192.168.2.0/24** | Router0 Se2/0 ↔ Router1 Se2/0 | Serial DCE |
| **192.168.3.0/24** | PC1, Router1 Fa0/0 | Direct to Router1 |
| **192.168.4.0/24** | Router1 Se3/0 ↔ Router2 Se3/0 | Serial DCE |
| **192.168.5.0/24** | PC2, Router2 Fa0/0 | Switch2 |

---

## File Save!

```
File → Save as "Lab4_Extended_3Routers.pkt"
```

Then you have 3 PCs, 3 routers, 2 switches, all connected and routing! 🎉
