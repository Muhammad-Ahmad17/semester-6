# Complete Subnetting Calculations - DCCN Lab 7

## Network Topology Overview
This document contains complete subnet calculations for a three-router network topology with detailed rough work.

---

## Fundamental Concepts

### Subnet Mask Calculation Formula
```
Subnet Mask = 256 - Block Size (for the relevant octet)
Block Size = 2^(32 - CIDR) = 2^(Host Bits)
Usable Hosts = Block Size - 2 (subtract Network & Broadcast)
```

### Powers of 2 Reference Table
```
2^0 = 1      2^4 = 16     2^8 = 256
2^1 = 2      2^5 = 32     2^9 = 512
2^2 = 4      2^6 = 64     2^10 = 1024
2^3 = 8      2^7 = 128
```

### IPv4 Structure
```
Total bits in IPv4 address = 32 bits
Divided into 4 octets: XXX.XXX.XXX.XXX
Each octet = 8 bits
Range per octet = 0 to 255
```

---

# NETWORK 1: 172.16.1.16/28 (PC1 - R1 LAN)

## Step 1: Find Host Bits
```
Total bits in IPv4 = 32
Network bits (CIDR) = 28
Host bits = 32 - 28 = 4 bits
```

## Step 2: Calculate Block Size
```
Block Size = 2^(Host Bits)
Block Size = 2^4 = 16
```

## Step 3: Calculate Subnet Mask
```
/28 means 28 bits are ON (1s), remaining 4 bits are OFF (0s)

Binary breakdown:
  Octet 1    Octet 2    Octet 3    Octet 4
  8 bits     8 bits     8 bits     8 bits
  ────────   ────────   ────────   ────────
  11111111   11111111   11111111   11110000
     ↓          ↓          ↓          ↓
    255        255        255     256-16=240

Subnet Mask = 255.255.255.240
```

### Detailed 4th Octet Calculation:
```
11110000 in binary
= (1×128) + (1×64) + (1×32) + (1×16) + (0×8) + (0×4) + (0×2) + (0×1)
= 128 + 64 + 32 + 16
= 240

OR using formula: 256 - Block Size = 256 - 16 = 240
```

## Step 4: Calculate Usable Hosts
```
Usable Hosts = Block Size - 2
Usable Hosts = 16 - 2 = 14 hosts

Why -2?
  - 1 address reserved for Network Address
  - 1 address reserved for Broadcast Address
```

## Step 5: Find Network Address, Broadcast, Range
```
Given IP: 172.16.1.16
Block Size: 16

Method: Find nearest multiple of 16 ≤ given IP's last octet
  16 ÷ 16 = 1 (exactly divisible)
  Network Address = 172.16.1.16 ✓

Calculation for Network ranges (4th octet):
  0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240
  Our network starts at: 16

Broadcast Address = Network Address + Block Size - 1
Broadcast Address = 172.16.1.16 + 16 - 1
Broadcast Address = 172.16.1.31

Usable Range:
  First Usable IP = Network Address + 1 = 172.16.1.17
  Last Usable IP = Broadcast Address - 1 = 172.16.1.30
  Range = 172.16.1.17 to 172.16.1.30
```

## Step 6: Assign IPs
```
Default Gateway (Router Interface - R1 Fa0/0) = 172.16.1.17 (First usable)
PC1 NIC = 172.16.1.18 (Second usable)

Remaining available IPs: 172.16.1.19 to 172.16.1.30 (12 more hosts)
```

## Network 1 Summary Table

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| **Network Type** | LAN | Ethernet |
| **CIDR Notation** | Given | 172.16.1.16/28 |
| **Subnet Bits** | Given | /28 |
| **Host Bits** | 32 - 28 | 4 |
| **Block Size** | 2^4 | 16 |
| **Subnet Mask** | 255.255.255.(256-16) | 255.255.255.240 |
| **Subnet Mask (Binary)** | Last octet | 11110000 |
| **Network Address** | Multiple of 16 | 172.16.1.16 |
| **First Usable IP** | Network + 1 | 172.16.1.17 |
| **Last Usable IP** | Broadcast - 1 | 172.16.1.30 |
| **Broadcast Address** | Network + Block - 1 | 172.16.1.31 |
| **Total Addresses** | 2^4 | 16 |
| **Usable Hosts** | 16 - 2 | 14 |
| **Default Gateway** | First usable | 172.16.1.17 |
| **R1 Fa0/0** | First usable | 172.16.1.17 |
| **PC1 IP** | Second usable | 172.16.1.18 |
| **Available IPs** | For future use | 172.16.1.19 - 172.16.1.30 |

### Complete IP List for Network 1
```
172.16.1.16    → Network Address (Reserved)
172.16.1.17    → R1 Fa0/0 (Default Gateway)
172.16.1.18    → PC1
172.16.1.19    → Available
172.16.1.20    → Available
172.16.1.21    → Available
172.16.1.22    → Available
172.16.1.23    → Available
172.16.1.24    → Available
172.16.1.25    → Available
172.16.1.26    → Available
172.16.1.27    → Available
172.16.1.28    → Available
172.16.1.29    → Available
172.16.1.30    → Available
172.16.1.31    → Broadcast Address (Reserved)
```

---

# NETWORK 2: 10.10.10.0/24 (PC2 - R2 LAN)

## Step 1: Find Host Bits
```
Total bits in IPv4 = 32
Network bits (CIDR) = 24
Host bits = 32 - 24 = 8 bits
```

## Step 2: Calculate Block Size
```
Block Size = 2^(Host Bits)
Block Size = 2^8 = 256
```

## Step 3: Calculate Subnet Mask
```
/24 means 24 bits are ON (1s), remaining 8 bits are OFF (0s)

Binary breakdown:
  Octet 1    Octet 2    Octet 3    Octet 4
  8 bits     8 bits     8 bits     8 bits
  ────────   ────────   ────────   ────────
  11111111   11111111   11111111   00000000
     ↓          ↓          ↓          ↓
    255        255        255         0

Subnet Mask = 255.255.255.0

This is a Class C standard subnet (most common)
```

### Detailed 4th Octet Calculation:
```
00000000 in binary = 0 in decimal
All host bits available
```

## Step 4: Calculate Usable Hosts
```
Usable Hosts = Block Size - 2
Usable Hosts = 256 - 2 = 254 hosts

Large enough for most small to medium office networks
```

## Step 5: Find Network Address, Broadcast, Range
```
Given IP: 10.10.10.0
Block Size: 256 (entire 4th octet - full range 0-255)

Network Address = 10.10.10.0 (4th octet starts at 0)

Broadcast Address = Network Address + Block Size - 1
Broadcast Address = 10.10.10.0 + 256 - 1
Broadcast Address = 10.10.10.255

Usable Range:
  First Usable IP = Network Address + 1 = 10.10.10.1
  Last Usable IP = Broadcast Address - 1 = 10.10.10.254
  Range = 10.10.10.1 to 10.10.10.254
```

## Step 6: Assign IPs
```
Default Gateway (Router Interface - R2 Fa0/0) = 10.10.10.1 (First usable)
PC2 NIC = 10.10.10.2 (Second usable)

Remaining available IPs: 10.10.10.3 to 10.10.10.254 (252 more hosts)
```

## Network 2 Summary Table

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| **Network Type** | LAN | Ethernet |
| **CIDR Notation** | Given | 10.10.10.0/24 |
| **Subnet Bits** | Given | /24 |
| **Host Bits** | 32 - 24 | 8 |
| **Block Size** | 2^8 | 256 |
| **Subnet Mask** | Standard Class C | 255.255.255.0 |
| **Subnet Mask (Binary)** | Last octet | 00000000 |
| **Network Address** | Given | 10.10.10.0 |
| **First Usable IP** | Network + 1 | 10.10.10.1 |
| **Last Usable IP** | Broadcast - 1 | 10.10.10.254 |
| **Broadcast Address** | 0 + 256 - 1 | 10.10.10.255 |
| **Total Addresses** | 2^8 | 256 |
| **Usable Hosts** | 256 - 2 | 254 |
| **Default Gateway** | First usable | 10.10.10.1 |
| **R2 Fa0/0** | First usable | 10.10.10.1 |
| **PC2 IP** | Second usable | 10.10.10.2 |
| **Available IPs** | For future use | 10.10.10.3 - 10.10.10.254 |

### IP Range Overview for Network 2
```
10.10.10.0      → Network Address (Reserved)
10.10.10.1      → R2 Fa0/0 (Default Gateway)
10.10.10.2      → PC2
10.10.10.3      → Available
    ...
10.10.10.254    → Available (Last usable)
10.10.10.255    → Broadcast Address (Reserved)

Total: 254 usable addresses
```

---

# NETWORK 3: 172.16.1.32/29 (PC3 - R3 LAN)

## Step 1: Find Host Bits
```
Total bits in IPv4 = 32
Network bits (CIDR) = 29
Host bits = 32 - 29 = 3 bits
```

## Step 2: Calculate Block Size
```
Block Size = 2^(Host Bits)
Block Size = 2^3 = 8
```

## Step 3: Calculate Subnet Mask
```
/29 means 29 bits are ON (1s), remaining 3 bits are OFF (0s)

Binary breakdown:
  Octet 1    Octet 2    Octet 3    Octet 4
  8 bits     8 bits     8 bits     8 bits
  ────────   ────────   ────────   ────────
  11111111   11111111   11111111   11111000
     ↓          ↓          ↓          ↓
    255        255        255     256-8=248

Subnet Mask = 255.255.255.248
```

### Detailed 4th Octet Calculation:
```
11111000 in binary
= (1×128) + (1×64) + (1×32) + (1×16) + (1×8) + (0×4) + (0×2) + (0×1)
= 128 + 64 + 32 + 16 + 8
= 248

OR using formula: 256 - Block Size = 256 - 8 = 248
```

## Step 4: Calculate Usable Hosts
```
Usable Hosts = Block Size - 2
Usable Hosts = 8 - 2 = 6 hosts

Good for small networks (1 router + up to 5 devices)
```

## Step 5: Find Network Address, Broadcast, Range
```
Given IP: 172.16.1.32
Block Size: 8

Method: Find nearest multiple of 8 ≤ given IP's last octet
  32 ÷ 8 = 4 (exactly divisible)
  Network Address = 172.16.1.32 ✓

Calculation for Network ranges (4th octet):
  0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96...
  Our network starts at: 32

Broadcast Address = Network Address + Block Size - 1
Broadcast Address = 172.16.1.32 + 8 - 1
Broadcast Address = 172.16.1.39

Usable Range:
  First Usable IP = Network Address + 1 = 172.16.1.33
  Last Usable IP = Broadcast Address - 1 = 172.16.1.38
  Range = 172.16.1.33 to 172.16.1.38
```

## Step 6: Assign IPs
```
Default Gateway (Router Interface - R3 Fa0/0) = 172.16.1.33 (First usable)
PC3 NIC = 172.16.1.34 (Second usable)

Remaining available IPs: 172.16.1.35 to 172.16.1.38 (4 more hosts)
```

## Network 3 Summary Table

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| **Network Type** | LAN | Ethernet |
| **CIDR Notation** | Given | 172.16.1.32/29 |
| **Subnet Bits** | Given | /29 |
| **Host Bits** | 32 - 29 | 3 |
| **Block Size** | 2^3 | 8 |
| **Subnet Mask** | 255.255.255.(256-8) | 255.255.255.248 |
| **Subnet Mask (Binary)** | Last octet | 11111000 |
| **Network Address** | Multiple of 8 | 172.16.1.32 |
| **First Usable IP** | Network + 1 | 172.16.1.33 |
| **Last Usable IP** | Broadcast - 1 | 172.16.1.38 |
| **Broadcast Address** | 32 + 8 - 1 | 172.16.1.39 |
| **Total Addresses** | 2^3 | 8 |
| **Usable Hosts** | 8 - 2 | 6 |
| **Default Gateway** | First usable | 172.16.1.33 |
| **R3 Fa0/0** | First usable | 172.16.1.33 |
| **PC3 IP** | Second usable | 172.16.1.34 |
| **Available IPs** | For future use | 172.16.1.35 - 172.16.1.38 |

### Complete IP List for Network 3
```
172.16.1.32    → Network Address (Reserved)
172.16.1.33    → R3 Fa0/0 (Default Gateway)
172.16.1.34    → PC3
172.16.1.35    → Available
172.16.1.36    → Available
172.16.1.37    → Available
172.16.1.38    → Available
172.16.1.39    → Broadcast Address (Reserved)
```

---

# WAN LINK 1: R1 ↔ R2 (192.168.10.0/30)

## Link Information
- **Connection**: R1 S0/0/0 ↔ R2 S0/0/0
- **Speed**: 64 kbps
- **DCE Side**: R1 (provides clock signal)
- **Link Type**: Point-to-Point Serial

## Step 1: Find Host Bits
```
Total bits in IPv4 = 32
Network bits (CIDR) = 30
Host bits = 32 - 30 = 2 bits
```

## Step 2: Calculate Block Size
```
Block Size = 2^(Host Bits)
Block Size = 2^2 = 4
```

## Step 3: Calculate Subnet Mask
```
/30 means 30 bits are ON (1s), remaining 2 bits are OFF (0s)

Binary breakdown:
  Octet 1    Octet 2    Octet 3    Octet 4
  8 bits     8 bits     8 bits     8 bits
  ────────   ────────   ────────   ────────
  11111111   11111111   11111111   11111100
     ↓          ↓          ↓          ↓
    255        255        255     256-4=252

Subnet Mask = 255.255.255.252
```

### Detailed 4th Octet Calculation:
```
11111100 in binary
= (1×128) + (1×64) + (1×32) + (1×16) + (1×8) + (1×4) + (0×2) + (0×1)
= 128 + 64 + 32 + 16 + 8 + 4
= 252

OR using formula: 256 - Block Size = 256 - 4 = 252
```

## Step 4: Calculate Usable Hosts
```
Usable Hosts = Block Size - 2
Usable Hosts = 4 - 2 = 2 hosts

Perfect for point-to-point WAN links!
Only 2 usable IPs needed (one for each router end)
```

## Step 5: Find Network Address, Broadcast, Range
```
Given IP: 192.168.10.0
Block Size: 4

Network Address = 192.168.10.0 (starts at 0)

Calculation for Network ranges (4th octet):
  0, 4, 8, 12, 16, 20, 24, 28...
  Our network starts at: 0

Broadcast Address = Network Address + Block Size - 1
Broadcast Address = 192.168.10.0 + 4 - 1
Broadcast Address = 192.168.10.3

Usable Range:
  First Usable IP = Network Address + 1 = 192.168.10.1
  Last Usable IP = Broadcast Address - 1 = 192.168.10.2
  Range = 192.168.10.1 to 192.168.10.2
```

## Step 6: Assign IPs and Configure DCE
```
R1 S0/0/0 (DCE) = 192.168.10.1 (First usable)
R2 S0/0/0 (DTE) = 192.168.10.2 (Second usable)

Clock Rate Configuration (on DCE side - R1):
  Command: clock rate 64000
  Speed: 64 kbps = 64000 bps
```

## WAN Link 1 Summary Table

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| **Link Type** | WAN | Serial Point-to-Point |
| **CIDR Notation** | Given | 192.168.10.0/30 |
| **Subnet Bits** | Given | /30 |
| **Host Bits** | 32 - 30 | 2 |
| **Block Size** | 2^2 | 4 |
| **Subnet Mask** | 255.255.255.(256-4) | 255.255.255.252 |
| **Subnet Mask (Binary)** | Last octet | 11111100 |
| **Network Address** | Given | 192.168.10.0 |
| **First Usable IP** | Network + 1 | 192.168.10.1 |
| **Last Usable IP** | Broadcast - 1 | 192.168.10.2 |
| **Broadcast Address** | 0 + 4 - 1 | 192.168.10.3 |
| **Total Addresses** | 2^2 | 4 |
| **Usable Hosts** | 4 - 2 | 2 |
| **R1 S0/0/0 (DCE)** | First usable | 192.168.10.1 |
| **R2 S0/0/0 (DTE)** | Second usable | 192.168.10.2 |
| **Clock Rate** | 64 kbps | 64000 |
| **Bandwidth** | 64 kilobits/sec | 64 kbps |

### Complete IP List for WAN Link 1
```
192.168.10.0    → Network Address (Reserved)
192.168.10.1    → R1 S0/0/0 (DCE side)
192.168.10.2    → R2 S0/0/0 (DTE side)
192.168.10.3    → Broadcast Address (Reserved)
```

### Router Configuration Commands
```
R1:
interface Serial0/0/0
 ip address 192.168.10.1 255.255.255.252
 clock rate 64000
 no shutdown

R2:
interface Serial0/0/0
 ip address 192.168.10.2 255.255.255.252
 no shutdown
```

---

# WAN LINK 2: R1 ↔ R3 (192.168.10.4/30)

## Link Information
- **Connection**: R1 S0/0/1 ↔ R3 S0/0/0
- **Speed**: 256 kbps
- **DCE Side**: R1 (provides clock signal)
- **Link Type**: Point-to-Point Serial

## Step 1: Find Host Bits
```
Total bits in IPv4 = 32
Network bits (CIDR) = 30
Host bits = 32 - 30 = 2 bits
```

## Step 2: Calculate Block Size
```
Block Size = 2^(Host Bits)
Block Size = 2^2 = 4
```

## Step 3: Calculate Subnet Mask
```
/30 → Subnet Mask = 255.255.255.252
(Same calculation as WAN Link 1)
```

## Step 4: Calculate Usable Hosts
```
Usable Hosts = 4 - 2 = 2 hosts
```

## Step 5: Find Network Address, Broadcast, Range
```
Given IP: 192.168.10.4
Block Size: 4

Method: Find nearest multiple of 4 ≤ given IP's last octet
  4 ÷ 4 = 1 (exactly divisible)
  Network Address = 192.168.10.4 ✓

Calculation for Network ranges (4th octet):
  0, 4, 8, 12, 16, 20, 24, 28...
  Our network starts at: 4

Broadcast Address = Network Address + Block Size - 1
Broadcast Address = 192.168.10.4 + 4 - 1
Broadcast Address = 192.168.10.7

Usable Range:
  First Usable IP = Network Address + 1 = 192.168.10.5
  Last Usable IP = Broadcast Address - 1 = 192.168.10.6
  Range = 192.168.10.5 to 192.168.10.6
```

## Step 6: Assign IPs and Configure DCE
```
R1 S0/0/1 (DCE) = 192.168.10.5 (First usable)
R3 S0/0/0 (DTE) = 192.168.10.6 (Second usable)

Clock Rate Configuration (on DCE side - R1):
  Command: clock rate 256000
  Speed: 256 kbps = 256000 bps
```

## WAN Link 2 Summary Table

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| **Link Type** | WAN | Serial Point-to-Point |
| **CIDR Notation** | Given | 192.168.10.4/30 |
| **Subnet Bits** | Given | /30 |
| **Host Bits** | 32 - 30 | 2 |
| **Block Size** | 2^2 | 4 |
| **Subnet Mask** | 255.255.255.252 | 255.255.255.252 |
| **Subnet Mask (Binary)** | Last octet | 11111100 |
| **Network Address** | Multiple of 4 | 192.168.10.4 |
| **First Usable IP** | Network + 1 | 192.168.10.5 |
| **Last Usable IP** | Broadcast - 1 | 192.168.10.6 |
| **Broadcast Address** | 4 + 4 - 1 | 192.168.10.7 |
| **Total Addresses** | 2^2 | 4 |
| **Usable Hosts** | 4 - 2 | 2 |
| **R1 S0/0/1 (DCE)** | First usable | 192.168.10.5 |
| **R3 S0/0/0 (DTE)** | Second usable | 192.168.10.6 |
| **Clock Rate** | 256 kbps | 256000 |
| **Bandwidth** | 256 kilobits/sec | 256 kbps |

### Complete IP List for WAN Link 2
```
192.168.10.4    → Network Address (Reserved)
192.168.10.5    → R1 S0/0/1 (DCE side)
192.168.10.6    → R3 S0/0/0 (DTE side)
192.168.10.7    → Broadcast Address (Reserved)
```

### Router Configuration Commands
```
R1:
interface Serial0/0/1
 ip address 192.168.10.5 255.255.255.252
 clock rate 256000
 no shutdown

R3:
interface Serial0/0/0
 ip address 192.168.10.6 255.255.255.252
 no shutdown
```

---

# WAN LINK 3: R2 ↔ R3 (192.168.10.8/30)

## Link Information
- **Connection**: R2 S0/0/1 ↔ R3 S0/0/1
- **Speed**: 128 kbps
- **DCE Side**: R2 (provides clock signal)
- **Link Type**: Point-to-Point Serial

## Step 1: Find Host Bits
```
Total bits in IPv4 = 32
Network bits (CIDR) = 30
Host bits = 32 - 30 = 2 bits
```

## Step 2: Calculate Block Size
```
Block Size = 2^(Host Bits)
Block Size = 2^2 = 4
```

## Step 3: Calculate Subnet Mask
```
/30 → Subnet Mask = 255.255.255.252
(Same calculation as previous WAN links)
```

## Step 4: Calculate Usable Hosts
```
Usable Hosts = 4 - 2 = 2 hosts
```

## Step 5: Find Network Address, Broadcast, Range
```
Given IP: 192.168.10.8
Block Size: 4

Method: Find nearest multiple of 4 ≤ given IP's last octet
  8 ÷ 4 = 2 (exactly divisible)
  Network Address = 192.168.10.8 ✓

Calculation for Network ranges (4th octet):
  0, 4, 8, 12, 16, 20, 24, 28...
  Our network starts at: 8

Broadcast Address = Network Address + Block Size - 1
Broadcast Address = 192.168.10.8 + 4 - 1
Broadcast Address = 192.168.10.11

Usable Range:
  First Usable IP = Network Address + 1 = 192.168.10.9
  Last Usable IP = Broadcast Address - 1 = 192.168.10.10
  Range = 192.168.10.9 to 192.168.10.10
```

## Step 6: Assign IPs and Configure DCE
```
R2 S0/0/1 (DCE) = 192.168.10.9 (First usable)
R3 S0/0/1 (DTE) = 192.168.10.10 (Second usable)

Clock Rate Configuration (on DCE side - R2):
  Command: clock rate 128000
  Speed: 128 kbps = 128000 bps
```

## WAN Link 3 Summary Table

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| **Link Type** | WAN | Serial Point-to-Point |
| **CIDR Notation** | Given | 192.168.10.8/30 |
| **Subnet Bits** | Given | /30 |
| **Host Bits** | 32 - 30 | 2 |
| **Block Size** | 2^2 | 4 |
| **Subnet Mask** | 255.255.255.252 | 255.255.255.252 |
| **Subnet Mask (Binary)** | Last octet | 11111100 |
| **Network Address** | Multiple of 4 | 192.168.10.8 |
| **First Usable IP** | Network + 1 | 192.168.10.9 |
| **Last Usable IP** | Broadcast - 1 | 192.168.10.10 |
| **Broadcast Address** | 8 + 4 - 1 | 192.168.10.11 |
| **Total Addresses** | 2^2 | 4 |
| **Usable Hosts** | 4 - 2 | 2 |
| **R2 S0/0/1 (DCE)** | First usable | 192.168.10.9 |
| **R3 S0/0/1 (DTE)** | Second usable | 192.168.10.10 |
| **Clock Rate** | 128 kbps | 128000 |
| **Bandwidth** | 128 kilobits/sec | 128 kbps |

### Complete IP List for WAN Link 3
```
192.168.10.8    → Network Address (Reserved)
192.168.10.9    → R2 S0/0/1 (DCE side)
192.168.10.10   → R3 S0/0/1 (DTE side)
192.168.10.11   → Broadcast Address (Reserved)
```

### Router Configuration Commands
```
R2:
interface Serial0/0/1
 ip address 192.168.10.9 255.255.255.252
 clock rate 128000
 no shutdown

R3:
interface Serial0/0/1
 ip address 192.168.10.10 255.255.255.252
 no shutdown
```

---

# FINAL COMPLETE ADDRESSING TABLE

## Router Interfaces Configuration

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Network | Interface Type |
|--------|-----------|------------|-------------|-----------------|---------|----------------|
| **R1** | Fa0/0 | 172.16.1.17 | 255.255.255.240 | N/A | 172.16.1.16/28 | LAN |
| **R1** | S0/0/0 (DCE) | 192.168.10.1 | 255.255.255.252 | N/A | 192.168.10.0/30 | WAN |
| **R1** | S0/0/1 (DCE) | 192.168.10.5 | 255.255.255.252 | N/A | 192.168.10.4/30 | WAN |
| **R2** | Fa0/0 | 10.10.10.1 | 255.255.255.0 | N/A | 10.10.10.0/24 | LAN |
| **R2** | S0/0/0 | 192.168.10.2 | 255.255.255.252 | N/A | 192.168.10.0/30 | WAN |
| **R2** | S0/0/1 (DCE) | 192.168.10.9 | 255.255.255.252 | N/A | 192.168.10.8/30 | WAN |
| **R3** | Fa0/0 | 172.16.1.33 | 255.255.255.248 | N/A | 172.16.1.32/29 | LAN |
| **R3** | S0/0/0 | 192.168.10.6 | 255.255.255.252 | N/A | 192.168.10.4/30 | WAN |
| **R3** | S0/0/1 | 192.168.10.10 | 255.255.255.252 | N/A | 192.168.10.8/30 | WAN |

## PC/End Device Configuration

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Connected Network |
|--------|-----------|------------|-------------|-----------------|-------------------|
| **PC1** | NIC | 172.16.1.18 | 255.255.255.240 | 172.16.1.17 | 172.16.1.16/28 |
| **PC2** | NIC | 10.10.10.2 | 255.255.255.0 | 10.10.10.1 | 10.10.10.0/24 |
| **PC3** | NIC | 172.16.1.34 | 255.255.255.248 | 172.16.1.33 | 172.16.1.32/29 |

## Serial Link Speeds (DCE Interfaces Only)

| Router | Interface | Role | Clock Rate (bps) | Speed | Connected To |
|--------|-----------|------|------------------|-------|--------------|
| **R1** | S0/0/0 | DCE | 64000 | 64 kbps | R2 S0/0/0 |
| **R1** | S0/0/1 | DCE | 256000 | 256 kbps | R3 S0/0/0 |
| **R2** | S0/0/1 | DCE | 128000 | 128 kbps | R3 S0/0/1 |

---

# COMPLETE NETWORK SUMMARY

## All Networks at a Glance

| Network Name | Network Address | CIDR | Subnet Mask | Block Size | Usable Hosts | Usable Range | Broadcast | Type |
|--------------|----------------|------|-------------|------------|--------------|--------------|-----------|------|
| **LAN 1 (R1)** | 172.16.1.16 | /28 | 255.255.255.240 | 16 | 14 | .17 - .30 | 172.16.1.31 | Ethernet |
| **LAN 2 (R2)** | 10.10.10.0 | /24 | 255.255.255.0 | 256 | 254 | .1 - .254 | 10.10.10.255 | Ethernet |
| **LAN 3 (R3)** | 172.16.1.32 | /29 | 255.255.255.248 | 8 | 6 | .33 - .38 | 172.16.1.39 | Ethernet |
| **WAN 1 (R1-R2)** | 192.168.10.0 | /30 | 255.255.255.252 | 4 | 2 | .1 - .2 | 192.168.10.3 | Serial |
| **WAN 2 (R1-R3)** | 192.168.10.4 | /30 | 255.255.255.252 | 4 | 2 | .5 - .6 | 192.168.10.7 | Serial |
| **WAN 3 (R2-R3)** | 192.168.10.8 | /30 | 255.255.255.252 | 4 | 2 | .9 - .10 | 192.168.10.11 | Serial |

---

# QUICK REFERENCE GUIDES

## CIDR to Subnet Mask Conversion Table

| CIDR | Subnet Mask | Binary (Last Octet) | Block Size | Usable Hosts | Common Use |
|------|-------------|---------------------|------------|--------------|------------|
| /24 | 255.255.255.0 | 00000000 | 256 | 254 | Standard Class C |
| /25 | 255.255.255.128 | 10000000 | 128 | 126 | Medium subnets |
| /26 | 255.255.255.192 | 11000000 | 64 | 62 | Small office |
| /27 | 255.255.255.224 | 11100000 | 32 | 30 | Small networks |
| /28 | 255.255.255.240 | 11110000 | 16 | 14 | Very small LANs |
| /29 | 255.255.255.248 | 11111000 | 8 | 6 | Tiny LANs |
| /30 | 255.255.255.252 | 11111100 | 4 | 2 | Point-to-Point |
| /31 | 255.255.255.254 | 11111110 | 2 | 2* | P2P (RFC 3021) |
| /32 | 255.255.255.255 | 11111111 | 1 | 0 | Host route |

*Note: /31 is special for point-to-point links (no network/broadcast addresses)

## /30 Networks Pattern (Point-to-Point WAN Links)

```
Block Size = 4
Networks increment by 4

Network .0   → Usable: .1, .2   → Broadcast: .3
Network .4   → Usable: .5, .6   → Broadcast: .7
Network .8   → Usable: .9, .10  → Broadcast: .11
Network .12  → Usable: .13, .14 → Broadcast: .15
Network .16  → Usable: .17, .18 → Broadcast: .19
Network .20  → Usable: .21, .22 → Broadcast: .23
Network .24  → Usable: .25, .26 → Broadcast: .27
Network .28  → Usable: .29, .30 → Broadcast: .31
```

## Subnetting Quick Formulas

```
1. Host Bits = 32 - CIDR
   Example: /28 → 32 - 28 = 4 host bits

2. Block Size = 2^(Host Bits)
   Example: 4 host bits → 2^4 = 16

3. Subnet Mask (last octet) = 256 - Block Size
   Example: 256 - 16 = 240

4. Usable Hosts = Block Size - 2
   Example: 16 - 2 = 14 hosts

5. Network Address = Nearest multiple of Block Size ≤ IP
   Example: IP .17, Block 16 → Network .16

6. Broadcast = Network + Block Size - 1
   Example: .16 + 16 - 1 = .31

7. First Usable = Network + 1
   Example: .16 + 1 = .17

8. Last Usable = Broadcast - 1
   Example: .31 - 1 = .30
```

## Binary to Decimal Quick Reference

```
Bit Position:  128  64  32  16   8   4   2   1
Bit Value:      1   1   1   1   1   1   1   1  = 255

Common Subnet Mask Values:
11111111 = 255
11111110 = 254
11111100 = 252
11111000 = 248
11110000 = 240
11100000 = 224
11000000 = 192
10000000 = 128
00000000 = 0
```

## Network Class Identification

| Class | First Octet Range | Default Mask | Private Ranges | Purpose |
|-------|------------------|--------------|----------------|---------|
| **A** | 1-126 | 255.0.0.0 (/8) | 10.0.0.0/8 | Large networks |
| **B** | 128-191 | 255.255.0.0 (/16) | 172.16.0.0/12 | Medium networks |
| **C** | 192-223 | 255.255.255.0 (/24) | 192.168.0.0/16 | Small networks |
| **D** | 224-239 | N/A | N/A | Multicast |
| **E** | 240-255 | N/A | N/A | Experimental |

*Note: 127.x.x.x is reserved for loopback*

---

# CISCO ROUTER CONFIGURATION COMMANDS

## Complete Router Configurations

### Router R1 Configuration
```
Router> enable
Router# configure terminal
Router(config)# hostname R1

! Configure FastEthernet 0/0 (LAN)
R1(config)# interface FastEthernet0/0
R1(config-if)# ip address 172.16.1.17 255.255.255.240
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure Serial 0/0/0 (DCE to R2)
R1(config)# interface Serial0/0/0
R1(config-if)# ip address 192.168.10.1 255.255.255.252
R1(config-if)# clock rate 64000
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure Serial 0/0/1 (DCE to R3)
R1(config)# interface Serial0/0/1
R1(config-if)# ip address 192.168.10.5 255.255.255.252
R1(config-if)# clock rate 256000
R1(config-if)# no shutdown
R1(config-if)# exit

R1(config)# end
R1# write memory
```

### Router R2 Configuration
```
Router> enable
Router# configure terminal
Router(config)# hostname R2

! Configure FastEthernet 0/0 (LAN)
R2(config)# interface FastEthernet0/0
R2(config-if)# ip address 10.10.10.1 255.255.255.0
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure Serial 0/0/0 (DTE to R1)
R2(config)# interface Serial0/0/0
R2(config-if)# ip address 192.168.10.2 255.255.255.252
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure Serial 0/0/1 (DCE to R3)
R2(config)# interface Serial0/0/1
R2(config-if)# ip address 192.168.10.9 255.255.255.252
R2(config-if)# clock rate 128000
R2(config-if)# no shutdown
R2(config-if)# exit

R2(config)# end
R2# write memory
```

### Router R3 Configuration
```
Router> enable
Router# configure terminal
Router(config)# hostname R3

! Configure FastEthernet 0/0 (LAN)
R3(config)# interface FastEthernet0/0
R3(config-if)# ip address 172.16.1.33 255.255.255.248
R3(config-if)# no shutdown
R3(config-if)# exit

! Configure Serial 0/0/0 (DTE to R1)
R3(config)# interface Serial0/0/0
R3(config-if)# ip address 192.168.10.6 255.255.255.252
R3(config-if)# no shutdown
R3(config-if)# exit

! Configure Serial 0/0/1 (DTE to R2)
R3(config)# interface Serial0/0/1
R3(config-if)# ip address 192.168.10.10 255.255.255.252
R3(config-if)# no shutdown
R3(config-if)# exit

R3(config)# end
R3# write memory
```

## PC Configuration

### PC1 Configuration
```
IP Address: 172.16.1.18
Subnet Mask: 255.255.255.240
Default Gateway: 172.16.1.17
```

### PC2 Configuration
```
IP Address: 10.10.10.2
Subnet Mask: 255.255.255.0
Default Gateway: 10.10.10.1
```

### PC3 Configuration
```
IP Address: 172.16.1.34
Subnet Mask: 255.255.255.248
Default Gateway: 172.16.1.33
```

## Verification Commands

```
! Show IP configuration
Router# show ip interface brief

! Show detailed interface info
Router# show interfaces

! Show running configuration
Router# show running-config

! Show IP routing table
Router# show ip route

! Test connectivity
Router# ping <IP-address>

! Show interface status
Router# show ip interface <interface-name>

! Show clock rate (on DCE interfaces)
Router# show controllers Serial0/0/0
```

---

# TROUBLESHOOTING GUIDE

## Common Issues and Solutions

### 1. Serial Link Down
```
Problem: Serial interface shows "down/down"

Checks:
- Verify clock rate configured on DCE side
- Check cable connections
- Verify both ends have "no shutdown"
- Confirm IP addresses are in same subnet

Commands:
show ip interface brief
show controllers serial0/0/0
```

### 2. Cannot Ping Across Network
```
Problem: PC cannot reach gateway or other networks

Checks:
- Verify Default Gateway is correct
- Check subnet mask matches
- Ensure router interface is up
- Verify routing (default or dynamic)

Commands:
show ip route
ping <gateway-ip>
traceroute <destination-ip>
```

### 3. Wrong Subnet Calculation
```
Problem: Devices not communicating

Checks:
- Recalculate network address
- Verify block size matches CIDR
- Check all IPs in usable range
- Confirm subnet mask matches CIDR

Formula Check:
Network Address % Block Size = 0
```

### 4. DCE/DTE Confusion
```
Problem: Serial link won't come up

Remember:
- DCE side MUST have clock rate
- DTE side should NOT have clock rate
- Check cable type (DCE has clock symbol)
- Clock rate in bps (64 kbps = 64000)
```

---

# PRACTICE SUBNETTING PROBLEMS

## Problem 1: Find the Network
```
Given: IP 192.168.15.75/27

Step 1: Host bits = 32 - 27 = 5 bits
Step 2: Block size = 2^5 = 32
Step 3: Subnet mask = 256 - 32 = 224 → 255.255.255.224
Step 4: Network ranges: 0, 32, 64, 96, 128...
Step 5: 75 falls between 64 and 96
        Network Address = 192.168.15.64

Answer:
Network: 192.168.15.64/27
Broadcast: 192.168.15.95
Usable: 192.168.15.65 - 192.168.15.94
Hosts: 30
```

## Problem 2: How Many Subnets?
```
Given: Network 10.0.0.0/8 needs to be subnetted with /24

Step 1: Original network bits = 8
Step 2: New subnet bits = 24
Step 3: Subnet bits borrowed = 24 - 8 = 16 bits
Step 4: Number of subnets = 2^16 = 65,536 subnets

Each subnet has:
- Block size = 2^8 = 256 addresses
- Usable hosts = 254
```

## Problem 3: Design a Network
```
Requirement: Need 5 point-to-point WAN links

Solution: Use /30 subnets (2 usable IPs each)
Starting from 192.168.100.0:

Link 1: 192.168.100.0/30  (.1 - .2)
Link 2: 192.168.100.4/30  (.5 - .6)
Link 3: 192.168.100.8/30  (.9 - .10)
Link 4: 192.168.100.12/30 (.13 - .14)
Link 5: 192.168.100.16/30 (.17 - .18)
```

---

# APPENDIX: BINARY CONVERSION

## Decimal to Binary Conversion
```
Example: Convert 192 to binary

Step 1: Find largest power of 2 ≤ 192
        128 fits, remainder: 192 - 128 = 64
Step 2: Find next power ≤ 64
        64 fits, remainder: 64 - 64 = 0
Step 3: Fill remaining positions with 0

Position: 128  64  32  16   8   4   2   1
Value:     1   1   0   0   0   0   0   0
Result: 11000000 = 192
```

## Binary to Decimal Conversion
```
Example: Convert 11111000 to decimal

Position: 128  64  32  16   8   4   2   1
Binary:    1   1   1   1   1   0   0   0
Multiply:  128  64  32  16   8   0   0   0

Sum: 128 + 64 + 32 + 16 + 8 = 248
```

## Subnet Mask Binary Patterns
```
/24: 11111111.11111111.11111111.00000000
/25: 11111111.11111111.11111111.10000000
/26: 11111111.11111111.11111111.11000000
/27: 11111111.11111111.11111111.11100000
/28: 11111111.11111111.11111111.11110000
/29: 11111111.11111111.11111111.11111000
/30: 11111111.11111111.11111111.11111100

Pattern: All 1s (network bits) on left, all 0s (host bits) on right
```

---

# SUMMARY CHECKLIST

## Before Configuring Network:

- [ ] Calculate all subnet masks correctly
- [ ] Verify block sizes match CIDR notation
- [ ] Confirm network addresses are valid
- [ ] Check usable IP ranges don't overlap
- [ ] Identify DCE interfaces for clock rates
- [ ] Document all IP assignments
- [ ] Verify default gateways are router IPs
- [ ] Ensure broadcast addresses calculated correctly

## During Configuration:

- [ ] Apply IP addresses to correct interfaces
- [ ] Set clock rates on DCE interfaces only
- [ ] Use correct subnet masks
- [ ] Issue "no shutdown" on all interfaces
- [ ] Save configuration with "write memory"
- [ ] Verify interface status with "show ip int brief"

## After Configuration:

- [ ] Test connectivity with ping
- [ ] Verify routing table with "show ip route"
- [ ] Check interface stats with "show interfaces"
- [ ] Test end-to-end connectivity (PC to PC)
- [ ] Document any changes or issues

---

# CONCLUSION

This document provides complete subnetting calculations with detailed rough work for:
- 3 LAN networks (/28, /24, /29)
- 3 WAN serial links (/30)
- Complete addressing scheme
- Router configurations
- Verification commands
- Troubleshooting guide

**Created for**: DCCN Lab 7
**Date**: 2026-03-25
**Network Type**: Multi-router topology with serial WAN links

---

**End of Document**
