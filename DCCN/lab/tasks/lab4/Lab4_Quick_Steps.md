# Lab 4 — Quick Steps to Replicate Topology

## Devices
- **PC0** (PC-PT)
- **Switch0** (Switch-PT)
- **Router0** (Router-PT)
- **Router1** (Router-PT)
- **PC1** (PC-PT)

---

## Connectivity Matrix

| Device 1 | Int 1   | ↔ Cable Type | ↔ | Int 2   | Device 2   |
|----------|---------|--------------|---|---------|------------|
| **PC0**  | Fa0     | Straight     | → | Fa0/1   | **Switch0** |
| **Switch0** | Fa1/1 | Straight     | → | Fa0/0   | **Router0** |
| **Router0** | Se2/0 | Serial DCE   | ⇄ | Se2/0   | **Router1** |
| **Router1** | Fa0/0 | Cross-Over   | → | Fa0     | **PC1**    |

---

## Network Diagram

```
PC0 (192.168.1.10)
   |
   | Fa0 ══Straight══ Fa0/1
   |
Switch0
   |
   | Fa1/1 ══Straight══ Fa0/0
   |
Router0 (LAN: 192.168.1.1, WAN: 192.168.2.1)
   |
   | Se2/0 ════Serial DCE════ Se2/0  [Router0 = DCE (clock provider)]
   |
Router1 (WAN: 192.168.2.2, LAN: 192.168.3.1)
   |
   | Fa0/0 ══Cross-Over══ Fa0
   |
PC1 (192.168.3.10)
```

---

## Cables
1. PC0 `Fa0` → Switch0 `Fa0/1` — **Straight-Through**
2. Switch0 `Fa1/1` → Router0 `Fa0/0` — **Straight-Through**
3. Router0 `Se2/0` → Router1 `Se2/0` — **Serial DCE** (click Router0 first)
4. Router1 `Fa0/0` → PC1 `Fa0` — **Cross-Over**

---

## Device & Interface Mapping

| Device      | Interface | IP Address    | Connected To          |
|-------------|-----------|---------------|-----------------------|
| **PC0**     | Fa0       | 192.168.1.10  | Switch0 Fa0/1         |
| **Switch0** | Fa0/1     | —             | PC0 Fa0               |
| **Switch0** | Fa1/1     | —             | Router0 Fa0/0         |
| **Router0** | Fa0/0     | 192.168.1.1   | Switch0 Fa1/1 (LAN)   |
| **Router0** | Se2/0     | 192.168.2.1   | Router1 Se2/0 (WAN/DCE) |
| **Router1** | Se2/0     | 192.168.2.2   | Router0 Se2/0 (WAN/DTE) |
| **Router1** | Fa0/0     | 192.168.3.1   | PC1 Fa0               |
| **PC1**     | Fa0       | 192.168.3.10  | Router1 Fa0/0         |

---

## Router0 Configuration

```
enable
configure terminal
hostname Router0
no ip domain-lookup
enable secret class
line console 0
password cisco
login  // Activates the password requirement. Without this, the password won't be enforced.
exit
line vty 0 4 // vty = virtual terminal , 0 4 = upto 0 to 4 reote user can connect
password cisco
login
exit
interface fastethernet 0/0
ip address 192.168.1.1 255.255.255.0
description LAN - Connected to Switch0
no shutdown
exit
interface serial 2/0
ip address 192.168.2.1 255.255.255.0
clock rate 64000
description WAN - Serial link to Router1 (DCE)
no shutdown
exit
ip route 192.168.3.0 255.255.255.0 192.168.2.2  // creating routing table to redirect 
exit
copy running-config startup-config
```

``` txt
PC0 (192.168.1.10) wants to reach PC1 (192.168.3.10)

Step 1: PC0 sends packet
        Destination: 192.168.3.10
        "I don't know this network!"
        → Sends to default gateway: 192.168.1.1 (Router0)

Step 2: Router0 receives it
        "Where is 192.168.3.10?"
        → Checks routing table
        → "I have route: 192.168.3.0/24 via 192.168.2.2"
        → Forwards to Router1 at 192.168.2.2

Step 3: Router1 receives it
        "Where is 192.168.3.10?"
        → "I have 192.168.3.0/24 directly on my Fa0/0!"
        → Forwards to PC1

Step 4: PC1 gets the packet ✓
```
---

## Router1 Configuration

```
enable
configure terminal
hostname Router1
no ip domain-lookup
enable secret class
line console 0
password cisco
login
exit
line vty 0 4
password cisco
login
exit
interface serial 2/0
ip address 192.168.2.2 255.255.255.0
description WAN - Serial link to Router0 (DTE)
no shutdown
exit
interface fastethernet 0/0
ip address 192.168.3.1 255.255.255.0
description LAN - Direct link to PC1
no shutdown
exit
ip route 192.168.1.0 255.255.255.0 192.168.2.1
exit
copy running-config startup-config
```

---

## PC0 Configuration
- IP: `192.168.1.10`
- Subnet: `255.255.255.0`
- Gateway: `192.168.1.1`

---

## PC1 Configuration
- IP: `192.168.3.10`
- Subnet: `255.255.255.0`
- Gateway: `192.168.3.1`

---

## Connectivity Paths

### PC0 → PC1 Path
```
PC0 (192.168.1.10)
  ↓ ping 192.168.3.10
Switch0 (forwards based on learned MAC)
  ↓
Router0 Fa0/0 (192.168.1.1) — LAN interface
Router0 Se2/0 (192.168.2.1) — WAN interface
  ↓ serial link (DCE provides clock)
Router1 Se2/0 (192.168.2.2) — WAN interface
Router1 Fa0/0 (192.168.3.1) — LAN interface
  ↓
PC1 (192.168.3.10)
  ✓ Reply sent back
```

### Data Path Summary
- **PC0 LAN:** 192.168.1.0/24 (via Switch0)
- **WAN Link:** 192.168.2.0/24 (serial, Router0=DCE)
- **PC1 LAN:** 192.168.3.0/24 (direct to Router1)

---

## Verification Commands

**Router0:**
```
show ip route
show ip interface brief
ping 192.168.2.2
```

**Router1:**
```
show ip route
show ip interface brief
ping 192.168.2.1
```

**PC0 → PC1:**
```
ping 192.168.3.10   ✓ Should work
```

---

**Done.**
