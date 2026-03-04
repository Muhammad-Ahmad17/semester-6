# Chapter 3: Transport Layer — Complete Beginner-Friendly Guide

### *Based on Kurose & Ross — Computer Networking: A Top-Down Approach*

---

## Table of Contents

1. [Introduction & Transport-Layer Services](#1-introduction--transport-layer-services)
2. [Multiplexing and Demultiplexing](#2-multiplexing-and-demultiplexing)
3. [Connectionless Transport: UDP](#3-connectionless-transport-udp)
4. [Principles of Reliable Data Transfer](#4-principles-of-reliable-data-transfer)
5. [Connection-Oriented Transport: TCP](#5-connection-oriented-transport-tcp)
6. [Principles of Congestion Control](#6-principles-of-congestion-control)
7. [TCP Congestion Control](#7-tcp-congestion-control)
8. [Evolution of Transport-Layer Functionality](#8-evolution-of-transport-layer-functionality)
9. [Summary & Key Takeaways](#9-summary--key-takeaways)
10. [Complete Glossary](#10-complete-glossary)
11. [Self-Test Questions & Answers](#11-self-test-questions--answers)

---

---

# 1. Introduction & Transport-Layer Services

## 1.1 What Is the Transport Layer?

The transport layer sits between the **application layer** (your apps) and the **network layer** (IP routing). Its job is to provide **logical communication between application processes** running on different hosts.

```
Host A                                    Host B
┌──────────────┐                    ┌──────────────┐
│ Application  │  ←── logical ──→  │ Application  │
│   Process    │    communication   │   Process    │
├──────────────┤                    ├──────────────┤
│  Transport   │                    │  Transport   │
├──────────────┤                    ├──────────────┤
│   Network    │───Router───Router──│   Network    │
├──────────────┤                    ├──────────────┤
│  Data Link   │                    │  Data Link   │
├──────────────┤                    ├──────────────┤
│  Physical    │                    │  Physical    │
└──────────────┘                    └──────────────┘
```

**Key insight:** The transport layer runs ONLY on end hosts (your computer, the server). Routers in between only look at network-layer (IP) headers — they don't inspect TCP/UDP headers.

## 1.2 Transport vs Network Layer — The Household Analogy

Kurose & Ross use a beautiful analogy:

> Imagine two households on opposite sides of the country. Each household has 12 kids. The kids in one house write letters to kids in the other house. In each household, one kid (say Ann and Bill) is responsible for collecting letters from siblings, putting them in the mailbox, and distributing received letters to the correct sibling.

| Real World              | Network Equivalent                    |
| ----------------------- | ------------------------------------- |
| Houses                  | Hosts (computers)                     |
| Kids                    | Application processes                 |
| Letters                 | Application messages                  |
| Ann & Bill (collectors) | Transport-layer protocol (TCP/UDP)    |
| Postal service          | Network-layer protocol (IP)           |
| Postal mail carriers    | Routers                               |

**What Ann & Bill do = what the transport layer does:**
- Collect letters from siblings (multiplexing)
- Deliver received letters to the right sibling (demultiplexing)
- The postal service (IP) simply moves mail between houses — it doesn't care which kid the letter is for

**What Ann & Bill CANNOT do:**
- They can't control postal delays (network congestion)
- They can't change the postal routes (routing)
- They can't magically make the postal service faster

This shows that the transport layer is **constrained by** what the network layer offers.

## 1.3 What Services Does the Transport Layer Provide?

The transport layer extends the network layer's **host-to-host** delivery into **process-to-process** delivery. Here's what the two Internet transport protocols offer:

| Service                      | TCP | UDP |
| ---------------------------- | --- | --- |
| Process-to-process delivery  | ✅  | ✅  |
| Multiplexing/Demultiplexing  | ✅  | ✅  |
| Integrity checking (checksum)| ✅  | ✅  |
| Reliable data transfer       | ✅  | ❌  |
| In-order delivery            | ✅  | ❌  |
| Flow control                 | ✅  | ❌  |
| Congestion control           | ✅  | ❌  |
| Connection setup             | ✅  | ❌  |
| Timing/bandwidth guarantees  | ❌  | ❌  |

> **Important:** Neither TCP nor UDP provides timing guarantees, bandwidth guarantees, or security (natively). For security, we layer **TLS** on top of TCP.

## 1.4 The Internet's Network Layer: IP

Before going further, understand what IP provides:

- **Best-effort delivery:** IP tries to deliver packets but makes NO guarantees.
- Packets may be **lost**, **duplicated**, **reordered**, or **corrupted**.
- IP is an **unreliable service**.

This means TCP must build reliability ON TOP of an unreliable network layer — which is like building a guaranteed delivery service using carrier pigeons that sometimes get lost!

---

---

# 2. Multiplexing and Demultiplexing

## 2.1 The Core Concept

When your computer is running 10 apps simultaneously (browser, email, game, Spotify, etc.), all of their data flows through the **same network interface**. The transport layer must:

- **Multiplexing (at sender):** Gather data from ALL application sockets, add transport headers with port numbers, and pass segments down to the network layer.
- **Demultiplexing (at receiver):** Examine port numbers in incoming segments and deliver each segment's data to the correct application socket.

```
           Sending Host                              Receiving Host
  ┌───────────────────────┐                  ┌───────────────────────┐
  │ App1   App2   App3    │                  │ App1   App2   App3    │
  │ :80    :443   :53     │                  │ :80    :443   :53     │
  │   \     |     /       │                  │   /     |     \       │
  │    \    |    /        │                  │  /      |      \      │
  │  ┌──────────────┐    │                  │  ┌──────────────┐     │
  │  │  Transport   │    │                  │  │  Transport   │     │
  │  │  (mux)       │    │                  │  │  (demux)     │     │
  │  └──────┬───────┘    │                  │  └──────┬───────┘     │
  │         │             │                  │         │             │
  │  ┌──────┴───────┐    │                  │  ┌──────┴───────┐     │
  │  │   Network    │    │    Internet      │  │   Network    │     │
  │  │   (IP)       │────│────────────────── │  │   (IP)       │     │
  │  └──────────────┘    │                  │  └──────────────┘     │
  └───────────────────────┘                  └───────────────────────┘
```

## 2.2 How Demultiplexing Works

Every transport-layer segment has a **source port** and **destination port** field in its header. The receiver uses these to route the segment to the correct socket.

### Sockets — The Interface

A **socket** is the "door" between the application process and the transport layer. Each socket has a unique identifier.

- **UDP socket:** Identified by a **2-tuple**: `(destination IP, destination port)`
- **TCP socket:** Identified by a **4-tuple**: `(source IP, source port, destination IP, destination port)`

This difference is HUGE and frequently tested. Let's understand why.

## 2.3 Connectionless (UDP) Demultiplexing

UDP uses only the **destination IP and destination port** to decide where to deliver.

**Consequence:** If two different clients send UDP packets to the same server port, both segments go to the **same socket**.

```
Client A (IP: 1.1.1.1, port 9157) ──→ Server (port 6428) ──→ Same socket!
Client B (IP: 2.2.2.2, port 5775) ──→ Server (port 6428) ──→ Same socket!
```

The server application must use the source IP/port in the received segment to know who sent what and where to send responses.

## 2.4 Connection-Oriented (TCP) Demultiplexing

TCP uses the **full 4-tuple** to identify a socket:
`(source IP, source port, destination IP, destination port)`

**Consequence:** If two different clients connect to the same server port, the server creates a **separate socket for each connection**.

```
Client A (IP: 1.1.1.1, port 9157) ──→ Server (port 80) ──→ Socket #1
Client B (IP: 2.2.2.2, port 5775) ──→ Server (port 80) ──→ Socket #2
Client A (IP: 1.1.1.1, port 9158) ──→ Server (port 80) ──→ Socket #3 (different!)
```

This is why a web server can handle thousands of clients on port 80 — each connection gets its OWN socket identified by the unique 4-tuple.

### The Welcoming Socket

A TCP server has a special **welcoming socket** that listens for new connection requests on a well-known port (e.g., 80). When a new client connects:

1. Client sends SYN to the welcoming socket (port 80)
2. Server accepts the connection → creates a **new socket** for this specific client
3. All further communication with this client uses the new socket
4. The welcoming socket continues listening for more clients

```
Server Welcoming Socket (port 80)
     │
     ├───→ New socket for Client A (1.1.1.1:9157 ↔ Server:80)
     ├───→ New socket for Client B (2.2.2.2:5775 ↔ Server:80)
     └───→ New socket for Client C (3.3.3.3:4821 ↔ Server:80)
```

## 2.5 Port Numbers in Detail

Port numbers are **16-bit unsigned integers** (range: 0 to 65535).

| Range         | Name              | Who Assigns?                     | Examples                                    |
| ------------- | ----------------- | -------------------------------- | ------------------------------------------- |
| 0 – 1023      | Well-Known        | IANA (Internet Assigned Numbers) | HTTP=80, HTTPS=443, DNS=53, SMTP=25, SSH=22|
| 1024 – 49151  | Registered        | IANA (looser rules)              | MySQL=3306, RDP=3389, Minecraft=25565       |
| 49152 – 65535 | Dynamic/Ephemeral | OS assigns automatically         | Your browser's source port                  |

**Fun fact:** When you open multiple tabs in your browser, each tab might get a different ephemeral source port (e.g., 49201, 49202, 49203...).

---

---

# 3. Connectionless Transport: UDP

## 3.1 Overview — UDP Does Almost Nothing (And That's the Point)

UDP takes the application's message, slaps on a source port, destination port, length, and checksum header, and hands it to IP. That's it.

**What UDP adds beyond raw IP:**
1. Port numbers (for multiplexing/demultiplexing)
2. A checksum (for error detection)

**What UDP does NOT add:**
- ❌ Connection setup/teardown
- ❌ Reliable delivery
- ❌ In-order delivery
- ❌ Flow control
- ❌ Congestion control
- ❌ Retransmission of lost packets

## 3.2 Why Would Anyone Choose UDP Over TCP?

| Reason                        | Explanation                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------ |
| **No connection setup delay** | TCP requires a 3-way handshake before sending data. UDP sends immediately.     |
| **No connection state**       | Servers don't need to track connections — can support more simultaneous clients.|
| **Small header overhead**     | UDP header = 8 bytes. TCP header = 20+ bytes. Less overhead per packet.        |
| **No congestion control**     | App can send as fast as it wants. TCP slows down when network is congested.    |
| **Fine-grained app control**  | App decides exactly when and what to send. TCP buffers and segments data.      |

### Applications That Use UDP

| Application             | Why UDP?                                          | App-Layer Protocol |
| ----------------------- | ------------------------------------------------- | ------------------ |
| DNS                     | Short request-response; setup overhead wasteful   | DNS                |
| SNMP (network mgmt)    | Must work even when network is stressed           | SNMP               |
| Streaming media         | Tolerates loss; time-sensitive                    | RTP over UDP       |
| Internet telephony/VoIP | Real-time; retransmission too slow                | SIP, RTP           |
| Online gaming           | Speed > perfect delivery; old data is useless     | Custom protocols   |
| IoT/Sensor networks     | Lightweight devices; minimal protocol overhead    | CoAP               |
| DHCP                    | Need to get an IP address (can't do TCP without one!) | DHCP            |

**Important note:** Some apps build their OWN reliability on top of UDP when they need it. For example, DNS uses UDP but will retry if no response comes back. Some video apps use UDP with forward error correction (FEC). Google's QUIC protocol builds reliability over UDP to avoid TCP's head-of-line blocking.

## 3.3 UDP Segment Structure

The UDP header is beautifully simple — only **8 bytes** (4 fields × 2 bytes each):

```
 0               8               16              24             31
 ┌───────────────┬───────────────┐
 │  Source Port   │  Dest Port    │    ← 4 bytes (ports)
 ├───────────────┼───────────────┤
 │    Length      │   Checksum    │    ← 4 bytes (metadata)
 ├───────────────┴───────────────┤
 │                               │
 │     Application Data          │    ← variable length
 │        (payload)              │
 │                               │
 └───────────────────────────────┘
```

| Field           | Size     | Description                                                          |
| --------------- | -------- | -------------------------------------------------------------------- |
| **Source Port**  | 16 bits  | Port of sending process (used for replies; can be 0 if no reply expected) |
| **Dest Port**   | 16 bits  | Port of receiving process                                            |
| **Length**       | 16 bits  | Total length of UDP segment (header + data) in bytes. Minimum = 8.   |
| **Checksum**    | 16 bits  | Error-detection code. Optional in IPv4, mandatory in IPv6.           |

**Maximum UDP payload size:**
- Theoretical max: 65535 − 8 (UDP header) − 20 (IP header) = **65507 bytes**
- Practical max: Usually limited by MTU (~1472 bytes to avoid IP fragmentation)

## 3.4 UDP Checksum — Complete Walkthrough

The checksum provides a basic error-detection mechanism. Let's walk through it step by step.

### Why a Checksum at All?

Even though data link layers (like Ethernet) have their own error checking (CRC), errors can still be introduced:
- Inside routers (memory corruption)
- During transfer between layers
- The link-layer check might not protect the entire path

So UDP provides an **end-to-end** check as a safety net.

### The Pseudo-Header

Before computing the checksum, UDP prepends a **pseudo-header** (not actually transmitted!) containing:

```
┌──────────────────────────────────────┐
│       Source IP Address (32 bits)     │
├──────────────────────────────────────┤
│    Destination IP Address (32 bits)   │
├────────┬─────────┬───────────────────┤
│ Zeros  │Protocol │  UDP Length        │
│ (8)    │  (8)    │   (16 bits)       │
└────────┴─────────┴───────────────────┘
```

The pseudo-header ensures the segment reaches the correct host — if a packet is misdelivered to the wrong IP, the checksum will fail.

### Step-by-Step Checksum Calculation

**Setting up:**
1. Lay out the pseudo-header + UDP header (with checksum field set to 0) + data
2. If the total number of bytes is odd, pad with a zero byte at the end
3. Treat everything as a sequence of **16-bit words**

**Computing:**
4. **Add** all 16-bit words using **one's complement addition**
   - Regular binary addition, BUT if there's a carry out of bit 15 (overflow), **wrap it around** and add 1 to the result

5. Take the **one's complement** of the final sum (flip all bits: 0→1, 1→0)
6. This is the **checksum** → place it in the checksum field

**Verifying (at receiver):**
7. Add all 16-bit words of the received segment (including the checksum field)
8. If the result is `1111 1111 1111 1111` (all 1s) → **no error detected**
9. If any bit is 0 → **error detected** → discard the segment

### Detailed Example

Suppose we have three 16-bit words to checksum:

```
Word 1:   0110 0110 0110 0000
Word 2:   0101 0101 0101 0101
Word 3:   1000 1111 0000 1100
```

**Step 1: Add Word 1 + Word 2:**
```
  0110 0110 0110 0000
+ 0101 0101 0101 0101
─────────────────────
  1011 1011 1011 0101
```

**Step 2: Add result + Word 3:**
```
  1011 1011 1011 0101
+ 1000 1111 0000 1100
─────────────────────
1 0100 1010 1100 0001   ← 17 bits! There's a carry (the leading 1)
```

**Step 3: Wraparound — add the carry back:**
```
  0100 1010 1100 0001
+                   1
─────────────────────
  0100 1010 1100 0010
```

**Step 4: One's complement (flip all bits):**
```
  0100 1010 1100 0010  → sum
  1011 0101 0011 1101  → checksum ✓
```

**Verification at receiver:**
```
  0110 0110 0110 0000   (Word 1)
+ 0101 0101 0101 0101   (Word 2)
+ 1000 1111 0000 1100   (Word 3)
+ 1011 0101 0011 1101   (Checksum)
─────────────────────
  1111 1111 1111 1111   → All 1s = NO ERROR ✓
```

### Limitations of the Checksum

- It can **detect** many errors but **cannot correct** them
- Some errors can cancel out (e.g., if one bit flips from 0→1 and another from 1→0 in the same position of different words) — this is rare but possible
- It's much weaker than CRC used at the data link layer
- Still valuable as an end-to-end sanity check

---

---

# 4. Principles of Reliable Data Transfer

## 4.1 Why This Section Matters

This is arguably the **most important section** in Chapter 3. Before diving into TCP's specific implementation, Kurose & Ross teach you the **general principles** of building reliability over an unreliable channel.

The idea: Build a protocol step by step, starting simple, and adding complexity as we discover problems. Each version handles a new type of channel imperfection.

## 4.2 The Framework

```
┌─────────┐    reliable channel    ┌─────────┐
│ Sending  │ ════════════════════> │Receiving │    ← What the APPLICATION sees
│   App    │                       │   App    │
└────┬─────┘                       └────┬─────┘
     │                                  │
┌────┴─────┐                       ┌────┴─────┐
│  rdt     │   unreliable channel  │  rdt     │    ← What we're BUILDING
│ (sender) │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─> │(receiver)│
└────┬─────┘                       └────┬─────┘
     │                                  │
┌────┴─────┐                       ┌────┴─────┐
│Unreliable│                       │Unreliable│    ← What we're stuck with (IP)
│ Channel  │ ───────────────────── │ Channel  │
└──────────┘                       └──────────┘
```

- **rdt** = reliable data transfer protocol (what we're designing)
- **udt** = unreliable data transfer (what the channel provides)

We use **Finite State Machines (FSMs)** to describe each protocol version.

## 4.3 rdt 1.0 — Reliable Transfer Over a Perfectly Reliable Channel

**Channel assumption:** The channel is PERFECT — no bit errors, no packet loss.

**Protocol:** Dead simple.
- Sender: Take data from app → make packet → send it
- Receiver: Receive packet → extract data → deliver to app

```
Sender FSM:                     Receiver FSM:

Wait for        rdt_send(data)   Wait for       rdt_rcv(packet)
call from  ───────────────────>  call from  ──────────────────>
above       make_pkt(data)       below       extract(packet, data)
            udt_send(packet)                 deliver_data(data)
      ↺ (stay in same state)           ↺ (stay in same state)
```

**This is trivial.** No error handling needed. Real life is never this easy.

## 4.4 rdt 2.0 — Channel With Bit Errors (Stop-and-Wait with ACK/NAK)

**Channel assumption:** Bits can be **flipped** during transmission, but no packets are lost.

**New problem:** The receiver might get corrupted data. How does the sender know?

**Solution — ARQ (Automatic Repeat reQuest):**
1. **Error detection:** Add a checksum
2. **Receiver feedback:** Send ACK (positive acknowledgment) or NAK (negative acknowledgment)
3. **Retransmission:** Sender re-sends if it gets a NAK

```
Sender:
┌─────────────┐  rdt_send(data)    ┌──────────────────┐
│ Wait for    │───────────────────→│ Wait for ACK     │
│ call from   │  make_pkt(data,   │ or NAK           │
│ above       │  checksum)         │                  │
└─────────────┘  udt_send(pkt)    └────────┬─────────┘
      ↑                                    │
      │  ACK received                      │ NAK received
      │  (data was OK)                     │ (data was bad)
      └────────────────────────────────────│
                                           │ udt_send(pkt)
                                           │ [resend same packet]
                                           ↺
```

**How it works in practice:**
```
Sender → "Hello" with checksum → Receiver
                                  Receiver checks: ✓ OK → sends ACK
Sender gets ACK → moves to next message

Sender → "World" with checksum → Receiver  
                                  Receiver checks: ✗ corrupted! → sends NAK
Sender gets NAK → resends "World"
```

### Fatal Flaw of rdt 2.0

**What if the ACK or NAK itself is corrupted?!**

```
Sender → "Hello" → Receiver
                    Receiver: OK → sends ACK
Sender receives: garbled mess... is it ACK or NAK?
  - If sender assumes NAK → retransmits "Hello" → receiver gets duplicate!
  - If sender assumes ACK → moves on → possibly lost data!
```

rdt 2.0 doesn't handle this. We need rdt 2.1.

## 4.5 rdt 2.1 — Handling Corrupted ACKs/NAKs (Sequence Numbers)

**Solution:** Add a **sequence number** to each packet. Since this is stop-and-wait (one packet at a time), we only need 1 bit: **0 or 1**.

**How it works:**
- Sender alternates between sending packet #0 and packet #1
- If the sender gets a garbled ACK/NAK → it **resends** the current packet
- Receiver checks the sequence number:
  - If it's a **new** packet (sequence number changed) → accept it
  - If it's a **duplicate** (same sequence number as last) → discard it, re-send ACK

```
Normal operation:
Sender: Send pkt 0 → Receiver: got pkt 0, send ACK
Sender: Send pkt 1 → Receiver: got pkt 1, send ACK
Sender: Send pkt 0 → Receiver: got pkt 0, send ACK
... (alternating 0, 1, 0, 1, ...)

Corrupted ACK scenario:
Sender: Send pkt 0        → Receiver: got pkt 0, send ACK
Sender: ACK is corrupted! → Resend pkt 0
                           → Receiver: got pkt 0 again (duplicate!)
                              Checks seq # → it's 0, I already have 0
                              → Discard duplicate, re-send ACK
Sender: Gets ACK → now send pkt 1
```

## 4.6 rdt 2.2 — NAK-Free Protocol

**Insight:** We don't actually need NAKs. Instead of sending a NAK, the receiver can send an **ACK for the last correctly received packet**.

If the sender receives an ACK for the previous packet (instead of the current one), it knows the current packet wasn't received correctly → retransmit.

```
Instead of:  NAK for packet 1
Use:         ACK for packet 0 (= "I'm still waiting for packet 1")

This is a "duplicate ACK" — the sender gets ACK 0 twice, meaning packet 1 was not received.
```

**Why bother?** This simplification leads directly to TCP's approach (TCP uses only ACKs, never NAKs).

## 4.7 rdt 3.0 — Channel With Bit Errors AND Packet Loss

**Channel assumption:** Bits can be flipped **AND** entire packets can be lost (both data and ACKs).

**New problem:** If a packet or its ACK is lost, the sender waits forever for an ACK that will never come.

**Solution: Countdown Timer**

The sender starts a timer after sending each packet:
- If ACK arrives before timeout → great, move on
- If timeout expires → assume loss → retransmit

```
Timeline scenarios for rdt 3.0:

Scenario A: No loss (normal)
  Sender          Receiver
  pkt 0 ──────→  receives pkt 0
               ←────── ACK 0
  pkt 1 ──────→  receives pkt 1
               ←────── ACK 1

Scenario B: Packet lost
  Sender          Receiver
  pkt 0 ──X       (lost in network)
  ... timer expires ...
  pkt 0 ──────→  receives pkt 0
               ←────── ACK 0

Scenario C: ACK lost
  Sender          Receiver
  pkt 0 ──────→  receives pkt 0
               X────── ACK 0 (lost)
  ... timer expires ...
  pkt 0 ──────→  receives pkt 0 (duplicate! seq# = 0 again)
                 → Discard, re-send ACK 0
               ←────── ACK 0

Scenario D: Premature timeout (ACK delayed, not lost)
  Sender          Receiver
  pkt 0 ──────→  receives pkt 0
  ... timer expires (ACK is slow) ...
  pkt 0 ──────→  receives pkt 0 (duplicate!)
               ←────── ACK 0 (delayed original)
                 → Discard duplicate, re-send ACK 0
               ←────── ACK 0 (for retransmission)
  Sender gets ACK 0 → moves to pkt 1
  (ignores the extra ACK 0)
```

### rdt 3.0 Works! But It's Slow...

rdt 3.0 is also called **alternating-bit protocol** (sequence numbers alternate 0, 1, 0, 1).

**The problem:** It's a **stop-and-wait** protocol. The sender sends ONE packet, then waits for an ACK before sending the next one. Most of the time, the sender is just sitting idle.

**Example of the waste:**

```
Link: 1 Gbps, RTT: 30 ms, Packet size: 1000 bytes

Time to transmit 1 packet: L/R = 8000 bits / 10⁹ bps = 8 μs

Utilization = L/R ÷ (RTT + L/R) = 8 μs / 30.008 ms = 0.00027 = 0.027%

The sender is busy only 0.027% of the time! 99.97% idle!
```

This is terrible. We need **pipelining**.

## 4.8 Pipelined Reliable Data Transfer

**Solution:** Don't wait! Send **multiple packets** before receiving ACKs.

```
Stop-and-Wait:                    Pipelining:
  ┌─────┐                         ┌─────┐
  │pkt 0│→ wait... ACK... next    │pkt 0│→
  └─────┘                         │pkt 1│→
                                  │pkt 2│→
  Sender mostly idle              │pkt 3│→  ← ACK 0 arrives
                                  │pkt 4│→  ← ACK 1 arrives
                                  └─────┘
                                  Sender stays busy!
```

**Pipelining requires:**
1. **Larger range of sequence numbers** (not just 0 and 1)
2. **Buffering** at sender and/or receiver (to handle out-of-order packets)
3. A strategy for handling loss — two main approaches:
   - **Go-Back-N (GBN)**
   - **Selective Repeat (SR)**

## 4.9 Go-Back-N (GBN)

### Core Idea

The sender can have up to **N** unacknowledged packets in the pipeline (N = window size). If a packet is lost, the sender **goes back** and retransmits that packet AND all subsequent packets.

### The Sender's Window

```
       Already      Sent, not yet    Usable, not    Not usable
       ACKed        ACKed            yet sent        (beyond window)
  ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
  0   1   2   3   4   5   6   7   8   9  10  11  12  13
              ↑               ↑           ↑
            base         nextseqnum     base+N
         (oldest                     (window limit)
         unACKed pkt)

  Window size N = 7 in this example
  [base ... base+N-1] = the "window"
```

### GBN Rules

**Sender:**
- Maintains a window of size N
- Uses **cumulative ACKs**: ACK(n) means "I've received everything up to and including n"
- Has a **single timer** for the oldest unACKed packet
- On timeout: retransmit ALL packets in the window (from base to nextseqnum-1)

**Receiver:**
- Always sends ACK for the **last in-order** packet received
- **Discards** any out-of-order packets (does NOT buffer them)
- Simple: only needs to remember the expected sequence number

### GBN Example — Packet Loss

```
Window size N = 4

Sender sends:  pkt0   pkt1   pkt2   pkt3
                 ↓      ↓      ✗      ↓       pkt2 is LOST
Receiver:      gets 0  gets 1  ---   gets 3
               ACK 0   ACK 1        ACK 1    ← pkt3 is out-of-order!
                                              Receiver discards pkt3
                                              Re-sends ACK 1 (last in-order)

Sender gets ACK 0, ACK 1... timeout for pkt2!
Sender retransmits: pkt2, pkt3, pkt4, pkt5    ← Goes back to pkt2 and resends ALL

This is wasteful! pkt3 was received fine but is retransmitted anyway.
```

### GBN Sequence Number Space

With **k bits** for sequence numbers: possible values = 0 to 2^k − 1

**Window size constraint:** N ≤ 2^k − 1

Why? If N = 2^k, the receiver can't distinguish between a new packet and a retransmission of an old one (sequence numbers wrap around).

## 4.10 Selective Repeat (SR)

### Core Idea

Like GBN, the sender can have up to N unacknowledged packets. But when a packet is lost, **only that specific packet** is retransmitted — NOT the ones after it.

### Key Difference from GBN

| Aspect               | Go-Back-N                         | Selective Repeat                  |
| --------------------- | --------------------------------- | --------------------------------- |
| **Receiver buffers?** | No — discards out-of-order        | Yes — buffers out-of-order        |
| **ACK type**          | Cumulative ("got everything ≤ n") | Individual ("got packet n")       |
| **Retransmit**        | All from lost packet onward       | Only the lost packet              |
| **Sender timer**      | Single timer for base             | Individual timer per packet       |
| **Receiver complexity**| Very simple                      | More complex (needs buffer)       |
| **Efficiency**        | Wastes bandwidth retransmitting   | More efficient (less wasted data) |

### SR Sender & Receiver Windows

```
Sender window:
  ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
  │✓ │✓ │  │✓ │  │  │  │  │  │  │  │
  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
  0   1   2   3   4   5   6   7   8
          ↑                   ↑
        base              base+N
  ✓ = ACKed,  blank = sent not ACKed or not yet sent

Receiver window:
  ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
  │  │  │  │✓ │  │  │  │  │  │  │  │
  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
  2   3   4   5   6   7   8   9  10
  ↑                           ↑
 rcv_base                   rcv_base+N
  ✓ = buffered out-of-order packet
```

### SR Example — Packet Loss

```
Window size N = 4

Sender sends:  pkt0   pkt1   pkt2   pkt3
                 ↓      ↓      ✗      ↓       pkt2 is LOST
Receiver:      gets 0  gets 1  ---   gets 3
               ACK 0   ACK 1        ACK 3    ← Receiver buffers pkt3!
                                              Sends individual ACK for pkt3

Sender gets ACK 0, ACK 1, ACK 3
         → knows pkt2 is missing
         → timeout for pkt2
         → retransmits ONLY pkt2

Receiver gets pkt2 → now has 0,1,2,3 → delivers all to app
```

### SR Sequence Number Constraint

**Window size:** N ≤ 2^(k-1) = 2^k / 2

This is MORE restrictive than GBN. Why? Because the receiver buffers out-of-order packets, there's a bigger risk of confusing new packets with old retransmissions when sequence numbers wrap around.

**Example of the problem with N = 4, k = 2 (seq #s: 0,1,2,3):**

```
Scenario 1: All ACKs received
  Sender sends 0,1,2 → gets ACK 0,1,2 → window moves → sends 3,0,1
  Receiver expects 3,0,1 (new packets)

Scenario 2: All ACKs lost
  Sender sends 0,1,2 → timeout → retransmits 0,1,2
  Receiver already delivered 0,1,2 → sees "0" again → thinks it's NEW packet 0!
  
  Receiver can't tell if "packet 0" is a retransmission or a new packet!
```

With N ≤ 2^(k-1) = 2, this ambiguity is avoided because the windows never overlap in sequence number space.

## 4.11 Summary — Building Blocks of Reliability

The mechanisms we've built up:

| Mechanism              | Purpose                        | First Appeared In |
| ---------------------- | ------------------------------ | ----------------- |
| Checksum               | Detect bit errors              | rdt 2.0           |
| ACK                    | Confirm correct receipt        | rdt 2.0           |
| NAK                    | Report corruption              | rdt 2.0           |
| Sequence numbers       | Detect duplicates              | rdt 2.1           |
| Timer                  | Detect loss                    | rdt 3.0           |
| Pipelining             | Improve performance            | GBN / SR          |
| Cumulative ACK         | Acknowledge multiple packets   | GBN               |
| Selective ACK          | ACK individual packets         | SR                |
| Receiver buffering     | Accept out-of-order packets    | SR                |

TCP uses a **combination** of these — it's closest to Selective Repeat but uses cumulative ACKs (a hybrid approach).

---

---

# 5. Connection-Oriented Transport: TCP

## 5.1 TCP Overview

TCP is the Internet's reliable transport protocol. It uses many of the mechanisms from Section 4 but with additional sophistication.

### TCP's Defining Characteristics

- **Connection-oriented:** Must perform a 3-way handshake before data transfer
- **Full-duplex:** Data flows in BOTH directions simultaneously
- **Point-to-point:** One sender, one receiver (no broadcast/multicast)
- **Byte-stream oriented:** TCP sees data as a stream of bytes, not separate messages
- **Reliable:** Every byte is delivered, in order, exactly once
- **Pipelined:** Multiple segments can be in flight (window-based)

### TCP Connection Components

When a TCP connection is established, both sides allocate:

- **Send buffer:** Holds data waiting to be sent
- **Receive buffer:** Holds incoming data waiting to be read by the app
- **State variables:** Sequence numbers, window sizes, timers

```
Application writes → Send Buffer → TCP segments → Network
Network → TCP segments → Receive Buffer → Application reads
```

### Maximum Segment Size (MSS)

TCP doesn't send the entire buffer at once. It breaks data into chunks called **segments**, each carrying at most **MSS** bytes of application data.

- **MSS** is the maximum amount of **application-layer data** in a segment
- Typically **1460 bytes** (to fit in a 1500-byte Ethernet frame: 1500 − 20 IP hdr − 20 TCP hdr = 1460)
- MSS does NOT include the TCP header — it's only the data portion

```
Ethernet Frame (1500 bytes MTU):
┌──────────────┬──────────────┬─────────────────────┐
│  IP Header   │  TCP Header  │  Application Data   │
│  (20 bytes)  │  (20 bytes)  │  (≤ 1460 bytes)    │
└──────────────┴──────────────┴─────────────────────┘
                               ← This is MSS →
```

## 5.2 TCP Segment Structure

The TCP header is **20 bytes minimum** (up to 60 bytes with options).

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
┌───────────────────────┬───────────────────────┐
│     Source Port (16)   │  Destination Port (16) │
├────────────────────────────────────────────────┤
│              Sequence Number (32)               │
├────────────────────────────────────────────────┤
│          Acknowledgment Number (32)             │
├──────┬──────┬──────────┬───────────────────────┤
│Header│Unused│  Flags   │    Receive Window      │
│Length│ (4)  │  (6)     │       (16)             │
│ (4)  │      │          │                        │
├───────────────────────┬───────────────────────┤
│   Checksum (16)       │  Urgent Pointer (16)   │
├───────────────────────┴───────────────────────┤
│            Options (variable, 0-40 bytes)      │
├────────────────────────────────────────────────┤
│                                                │
│              Application Data                  │
│                                                │
└────────────────────────────────────────────────┘
```

### Field-by-Field Explanation

| Field                   | Size     | What It Does                                                                         |
| ----------------------- | -------- | ------------------------------------------------------------------------------------ |
| **Source Port**          | 16 bits  | Identifies the sending application                                                   |
| **Destination Port**    | 16 bits  | Identifies the receiving application                                                 |
| **Sequence Number**     | 32 bits  | Byte number of the FIRST data byte in this segment                                   |
| **ACK Number**          | 32 bits  | The NEXT byte the receiver expects (cumulative acknowledgment)                       |
| **Header Length**       | 4 bits   | Length of TCP header in 32-bit words (min=5 → 20 bytes, max=15 → 60 bytes)          |
| **Unused/Reserved**     | 4 bits   | Reserved for future use, set to 0                                                    |
| **Flags**               | 6 bits   | Control bits: URG, ACK, PSH, RST, SYN, FIN                                          |
| **Receive Window**      | 16 bits  | Number of bytes the receiver is willing to accept (flow control)                     |
| **Checksum**            | 16 bits  | Error detection (mandatory, includes pseudo-header like UDP)                         |
| **Urgent Pointer**      | 16 bits  | Points to the end of urgent data (only valid if URG flag is set)                     |
| **Options**             | 0-40 B   | Optional extensions: MSS, window scaling, SACK, timestamps                           |

### The 6 TCP Flags (Control Bits)

| Flag | Full Name       | Purpose                                                             |
| ---- | --------------- | ------------------------------------------------------------------- |
| URG  | Urgent          | Urgent data present; check Urgent Pointer. Rarely used today.       |
| ACK  | Acknowledgment  | ACK Number field is valid. Set in virtually all segments after SYN.  |
| PSH  | Push            | Receiver should deliver data to app immediately (don't buffer).     |
| RST  | Reset           | Abort the connection immediately. Something is seriously wrong.     |
| SYN  | Synchronize     | Initiates a connection. Used in the first two handshake packets.    |
| FIN  | Finish          | Sender is done sending. Initiates connection teardown.              |

### Important TCP Options

| Option              | Size    | Purpose                                                        |
| ------------------- | ------- | -------------------------------------------------------------- |
| **MSS**             | 4 bytes | Declares max segment size (negotiated during handshake)        |
| **Window Scale**    | 3 bytes | Multiplies window size field by 2^n (allows windows > 64 KB)  |
| **SACK Permitted**  | 2 bytes | Says "I support Selective Acknowledgments"                     |
| **SACK**            | Var.    | Lists byte ranges received out-of-order (helps sender retransmit) |
| **Timestamps**      | 10 bytes| Helps measure RTT accurately and detect wrapped sequence numbers |

## 5.3 Sequence Numbers and ACK Numbers — Deep Dive

This is the trickiest part of TCP for beginners. Let's go very slow.

### Sequence Numbers Count BYTES, Not Packets

TCP treats data as a **byte stream**. Each byte has a number. The sequence number in a segment's header = the byte number of the **first** byte in that segment's data.

**Example:** Suppose:
- Initial Sequence Number (ISN) = 0
- MSS = 5 bytes (unrealistically small, for illustration)
- You want to send "HelloWorld!" (11 bytes)

```
Segment 1: seq=0,  data = "Hello"  (bytes 0-4)
Segment 2: seq=5,  data = "World"  (bytes 5-9)
Segment 3: seq=10, data = "!"      (byte 10)
```

The sequence number jumps by the number of data bytes in each segment.

### ACK Numbers: "Send Me Byte # Next"

The ACK number tells the sender: "I've received all bytes up to (but not including) this number. Send me this byte next."

```
After receiving Segment 1 (bytes 0-4):
  Receiver sends: ACK = 5  ("I have 0-4, give me byte 5")

After receiving Segment 2 (bytes 5-9):
  Receiver sends: ACK = 10 ("I have 0-9, give me byte 10")

After receiving Segment 3 (byte 10):
  Receiver sends: ACK = 11 ("I have 0-10, give me byte 11")
```

### Cumulative ACK

TCP uses **cumulative acknowledgments**: ACK = N means "I have all bytes with numbers **less than** N."

**If packets arrive out of order:**
```
Received: Segment 1 (bytes 0-4)  → ACK = 5
Received: Segment 3 (byte 10)   → ACK = 5 (still! Can't ACK 10 because byte 5-9 is missing)
Received: Segment 2 (bytes 5-9) → ACK = 11 (now has everything 0-10!)
```

### What Does the Receiver Do with Out-of-Order Segments?

The RFC doesn't specify this strictly. In practice, TCP implementations **buffer** out-of-order segments (like Selective Repeat) rather than discarding them (like Go-Back-N). This is much more efficient.

### Initial Sequence Number (ISN)

When a connection starts, each side picks a **random** initial sequence number (not 0!).

**Why random?**
- **Security:** Prevents attackers from guessing sequence numbers and injecting fake packets
- **Avoid confusion:** Old packets from a previous connection between the same ports won't be misinterpreted as part of the new connection

### Piggybacking

In a full-duplex connection, data flows both ways. TCP **piggybacks** ACKs onto data segments going in the opposite direction:

```
Host A → Host B: data (seq=42), ACK=79     ← ACK for B's data piggybacked on A's data
Host B → Host A: data (seq=79), ACK=50     ← ACK for A's data piggybacked on B's data
```

This saves bandwidth — no need for separate ACK-only packets (though they can be sent if there's no data to piggyback).

## 5.4 TCP Connection Management

### 5.4.1 The 3-Way Handshake (Connection Establishment)

```
    Client                              Server
      │                                   │
      │ ① SYN                             │
      │──────────────────────────────────→│
      │   SYN=1, seq=client_isn           │  Client: "I want to connect"
      │                                   │  Picks random seq # (client_isn)
      │                                   │
      │ ② SYN-ACK                         │
      │←──────────────────────────────────│
      │   SYN=1, ACK=1                    │  Server: "OK, I want to connect too"
      │   seq=server_isn                  │  Picks random seq # (server_isn)
      │   ack=client_isn+1                │  Acknowledges client's SYN
      │                                   │
      │ ③ ACK (can carry data!)           │
      │──────────────────────────────────→│
      │   SYN=0, ACK=1                    │  Client: "Great, let's go!"
      │   seq=client_isn+1                │  Connection is ESTABLISHED
      │   ack=server_isn+1                │
      │                                   │
```

**Step details:**

| Step | Sender → Receiver | SYN | ACK | Seq #           | Ack #            | Can carry data? |
| ---- | ------------------ | --- | --- | --------------- | ---------------- | --------------- |
| 1    | Client → Server    | 1   | 0   | client_isn      | —                | No              |
| 2    | Server → Client    | 1   | 1   | server_isn      | client_isn + 1   | No              |
| 3    | Client → Server    | 0   | 1   | client_isn + 1  | server_isn + 1   | Yes!            |

**Why 3 steps (not 2)?**
- If only 2 steps: old duplicate SYN packets could cause the server to open fake connections
- Step 3 confirms the client is actually there and received the server's response
- Recall: this is the same reason rdt protocols need sequence numbers — to avoid confusion

**Real-world analogy — Phone call:**
- You: "Hello, can you hear me?" (SYN)
- Friend: "Yes I can, can you hear me?" (SYN-ACK)
- You: "Yes!" (ACK)
- Both confirmed → start the conversation

### 5.4.2 Connection Teardown (4-Way Handshake)

Either side can initiate closing. TCP uses a graceful close with FIN flags:

```
    Client                              Server
      │                                   │
      │ ① FIN                             │
      │──────────────────────────────────→│  Client: "I'm done sending data"
      │   FIN=1, seq=u                    │
      │                                   │
      │ ② ACK                             │
      │←──────────────────────────────────│  Server: "OK, noted"
      │   ACK=1, ack=u+1                 │  (Server CAN still send data!)
      │                                   │  ← Half-close state
      │                                   │
      │  ... Server finishes sending ...  │
      │                                   │
      │ ③ FIN                             │
      │←──────────────────────────────────│  Server: "I'm done too"
      │   FIN=1, seq=w                    │
      │                                   │
      │ ④ ACK                             │
      │──────────────────────────────────→│  Client: "OK, goodbye"
      │   ACK=1, ack=w+1                 │
      │                                   │
      │   ╔══════════════════╗            │
      │   ║  TIME_WAIT       ║            │  Client waits 2 × MSL
      │   ║  (30s - 4 min)   ║            │  before fully closing
      │   ╚══════════════════╝            │
```

**Why 4 steps (not 2 or 3)?**
- TCP is full-duplex — each direction must be closed independently
- After step 1-2: Client can't send, but Server CAN still send → **half-close**
- After step 3-4: Both directions closed → connection fully terminated

**Why TIME_WAIT?**
1. If the final ACK (step 4) is lost, the server re-sends its FIN. The client needs to be alive to re-send the ACK.
2. Ensures old delayed segments expire before the same port pair is reused for a new connection.

**MSL (Maximum Segment Lifetime):** The longest time a segment can exist in the network. Typically 30 seconds to 2 minutes. TIME_WAIT lasts **2 × MSL**.

### 5.4.3 TCP Connection States

TCP goes through defined states. The most important ones:

**Client states during connection:**
```
CLOSED → SYN_SENT → ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED
```

**Server states during connection:**
```
CLOSED → LISTEN → SYN_RCVD → ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED
```

**Full state diagram (simplified):**
```
              Client                              Server
              ──────                              ──────
             CLOSED                              CLOSED
               │                                    │
         send SYN                              app: listen
               │                                    │
            SYN_SENT ──── rcv SYN+ACK ────→    LISTEN
               │          send ACK              SYN_RCVD
               │                                    │
          ESTABLISHED ◄──── rcv ACK ──────── ESTABLISHED
               │                                    │
          (data transfer in both directions)         │
               │                                    │
         send FIN                              rcv FIN
               │                               send ACK
          FIN_WAIT_1                           CLOSE_WAIT
               │                                    │
          rcv ACK                              send FIN
               │                                    │
          FIN_WAIT_2                            LAST_ACK
               │                                    │
          rcv FIN                              rcv ACK
          send ACK                                  │
               │                               CLOSED
          TIME_WAIT
               │
          (2 × MSL timeout)
               │
             CLOSED
```

### 5.4.4 What Happens When a Segment Arrives for a Non-Existent Port?

- **TCP:** Host sends back a segment with the **RST** flag set. This immediately tells the sender "nobody's listening here!"
- **UDP:** Host sends back an **ICMP Port Unreachable** message (Type 3, Code 3). The UDP protocol itself is silent.

### 5.4.5 SYN Flood Attack

An attacker sends thousands of SYN packets (step 1) from fake IP addresses. The server allocates resources for each half-open connection (SYN_RCVD state) and waits for ACKs that never come. Eventually, the server runs out of memory.

**Defense: SYN Cookies**
- Server does NOT allocate resources on receiving a SYN
- Instead, the server encodes connection info into the sequence number (SYN cookie) of the SYN-ACK
- Only when the client responds with a valid ACK (proving it's real) does the server allocate resources
- If the client is fake, no resources were wasted

## 5.5 Round-Trip Time (RTT) Estimation and Timeout

### Why Does TCP Need to Estimate RTT?

TCP needs to set its **retransmission timeout (RTO)** wisely:
- Too short → unnecessary retransmissions (thinking packets are lost when they're just slow)
- Too long → slow recovery from actual losses (sitting idle waiting)

The timeout should be slightly larger than the current RTT. But RTT varies!

### Measuring RTT

**SampleRTT:** The time between sending a segment and receiving its ACK. Measured for one segment at a time (not for retransmitted segments — to avoid ambiguity).

**Problem:** SampleRTT fluctuates wildly due to network congestion, different routes, etc.

### Smoothing — Exponential Weighted Moving Average (EWMA)

TCP smooths out the measurements:

$$\text{EstimatedRTT} = (1 - \alpha) \cdot \text{EstimatedRTT} + \alpha \cdot \text{SampleRTT}$$

Where $\alpha = 0.125$ (recommended by RFC 6298).

**In plain English:** The new estimate is 87.5% of the old estimate + 12.5% of the latest measurement. This gives more weight to historical values, smoothing out spikes.

**Example:**
```
Old EstimatedRTT = 100 ms
New SampleRTT = 150 ms (a spike!)

New EstimatedRTT = 0.875 × 100 + 0.125 × 150 = 87.5 + 18.75 = 106.25 ms
```

The spike of 150 ms only moved the estimate from 100 to 106.25 — smoothed!

### Measuring Variability — DevRTT

We also track how much the RTT varies:

$$\text{DevRTT} = (1 - \beta) \cdot \text{DevRTT} + \beta \cdot |\text{SampleRTT} - \text{EstimatedRTT}|$$

Where $\beta = 0.25$.

DevRTT captures the **deviation** — if RTT is stable, DevRTT is small; if volatile, DevRTT is large.

### Computing the Timeout Interval

$$\text{TimeoutInterval} = \text{EstimatedRTT} + 4 \cdot \text{DevRTT}$$

The safety margin ($4 \times \text{DevRTT}$) ensures we don't have premature timeouts. When the network is stable (low DevRTT), timeout is tight. When variable, timeout is generous.

### Timeout Doubling (Exponential Backoff)

When a timeout actually fires (packet is retransmitted):
- TCP **doubles** the timeout value for the next retransmission
- This avoids flooding a congested network with retransmissions
- The timeout resets to the computed value when a new ACK arrives

```
1st timeout: RTO = 1 second → retransmit
2nd timeout: RTO = 2 seconds → retransmit
3rd timeout: RTO = 4 seconds → retransmit
... and so on (exponential backoff)
``

ACK received → RTO resets to EstimatedRTT + 4×DevRTT
```

## 5.6 TCP Reliable Data Transfer

TCP builds reliability using the mechanisms from Section 4, adapted for the byte-stream nature of TCP.

### Simplified TCP Sender Behavior

The TCP sender responds to three events:

**Event 1: Data received from application**
1. Create segment with sequence number = `NextSeqNum`
2. Start timer if not already running (timer is for the oldest unACKed segment)
3. Send the segment
4. `NextSeqNum = NextSeqNum + length(data)`

**Event 2: Timer timeout**
1. Retransmit the segment that caused the timeout (the oldest unACKed segment)
2. Restart the timer

**Event 3: ACK received**
1. If ACK acknowledges previously unACKed segments:
   - Update `SendBase` (move the window forward)
   - If there are still unACKed segments, restart timer
   - If all segments are ACKed, stop timer

### TCP Retransmission Scenarios

Let's walk through the key scenarios:

**Scenario 1: Lost ACK**
```
Host A                              Host B
  │                                   │
  │──── seq=92, 8 bytes data ────────→│
  │                                   │── ACK=100
  │         (ACK is LOST!)       X ←──│
  │                                   │
  │   ... timeout ...                 │
  │                                   │
  │──── seq=92, 8 bytes data ────────→│  (retransmission)
  │                                   │── ACK=100
  │←──────────────────────────────────│
  │                                   │
```

**Scenario 2: Premature timeout (everything works, just slow)**
```
Host A                              Host B
  │                                   │
  │──── seq=92, 8 bytes ────────────→│
  │──── seq=100, 20 bytes ──────────→│
  │                                   │── ACK=100 (for first segment)
  │   ... timeout for seq=92 ...      │
  │                                   │── ACK=120 (for second segment)
  │──── seq=92, 8 bytes ────────────→│  (unnecessary retransmission!)
  │                                   │
  │←── ACK=100 (delayed arrival) ────│
  │←── ACK=120 ─────────────────────│
  │←── ACK=120 (for retransmission) ─│  (duplicate ACK, harmless)
  │                                   │
```

**Scenario 3: Cumulative ACK saves the day**
```
Host A                              Host B
  │                                   │
  │──── seq=92, 8 bytes ────────────→│
  │──── seq=100, 20 bytes ──────────→│
  │                                   │
  │←── ACK=120 ─────────────────────│  Cumulative! Covers BOTH segments!
  │         (ACK=100 was lost)        │  
  │                                   │
  │   No retransmission needed!       │
```

This last scenario shows the beauty of cumulative ACKs: even if ACK=100 is lost, ACK=120 tells the sender that everything up to byte 120 has been received.

### Fast Retransmit — Don't Wait for the Timer

Timeouts can be long (especially after exponential backoff). TCP uses **fast retransmit** as a shortcut:

**Rule:** If the sender receives **3 duplicate ACKs** for the same segment, retransmit immediately without waiting for the timer.

```
Sender sends: seq=100, seq=200, seq=300, seq=400, seq=500

Receiver gets:
  seq=100 ✓ → ACK=200
  seq=200 ✗ → LOST!
  seq=300 ✓ → ACK=200  (duplicate ACK #1 — "still need 200!")
  seq=400 ✓ → ACK=200  (duplicate ACK #2)
  seq=500 ✓ → ACK=200  (duplicate ACK #3)

Sender receives 3 duplicate ACKs for 200:
  → IMMEDIATELY retransmit seq=200 (don't wait for timeout!)

Receiver gets seq=200 → now has everything → ACK=600
```

**Why 3 duplicates, not 1 or 2?**
- 1-2 duplicate ACKs could be caused by normal **packet reordering** in the network
- 3 duplicates strongly suggests the segment is actually **lost**
- This threshold is a balance between reacting quickly and avoiding unnecessary retransmissions

### TCP ACK Generation Rules (RFC 5681)

The receiver follows these rules for generating ACKs:

| Event at Receiver                                   | TCP Receiver Action                                     |
| --------------------------------------------------- | ------------------------------------------------------- |
| In-order segment, no gap, everything else ACKed     | Delayed ACK: wait up to 500ms for another segment. If no more, send ACK. |
| In-order segment, no gap, one delayed ACK pending   | Immediately send single cumulative ACK for both segments|
| Out-of-order segment (gap detected)                 | Immediately send duplicate ACK indicating expected byte |
| Segment that fills a gap (partially or fully)       | Immediately send ACK if segment starts at lower end of gap |

**Delayed ACK:** TCP doesn't ACK every single segment instantly. It waits briefly hoping to piggyback the ACK on outgoing data, or to ACK two segments at once. This reduces the number of ACK packets.

## 5.7 TCP Flow Control

### The Problem

The sender might transmit data faster than the receiver can process it. The receiver has a finite receive buffer:

```
┌─────────────────────────────────────────────┐
│   Receive Buffer (e.g., 64 KB)              │
│                                             │
│  [Data waiting to be read by app] [Free]    │
│  ├────── used ──────┤├──── rwnd ────┤       │
│                                             │
└─────────────────────────────────────────────┘
```

If the buffer fills up, new segments are dropped. That triggers retransmissions, which waste bandwidth.

### The Solution — Receive Window (rwnd)

The receiver advertises how much free buffer space it has in the **Window Size** field of every TCP segment it sends:

$$\text{rwnd} = \text{RcvBuffer} - [\text{LastByteRcvd} - \text{LastByteRead}]$$

- `RcvBuffer` = total buffer size
- `LastByteRcvd - LastByteRead` = data in buffer not yet consumed by the app

**The sender's rule:**
$$\text{LastByteSent} - \text{LastByteAcked} \leq \text{rwnd}$$

The sender ensures the amount of unACKed data in flight never exceeds `rwnd`.

### Example

```
Step 1: Receiver buffer = 10 KB, empty → rwnd = 10240 bytes
        Receiver tells sender: "Window = 10240"
        
Step 2: Sender sends 4 KB → 4096 bytes in flight
        
Step 3: Receiver gets 4 KB. App reads 1 KB.
        Buffer used = 3 KB → rwnd = 10240 - 3072 = 7168 bytes
        Receiver tells sender: "Window = 7168"
        
Step 4: Sender sends 7 KB (staying within rwnd)

Step 5: Receiver buffer nearly full → rwnd = 0
        Receiver tells sender: "Window = 0"
        
Step 6: Sender STOPS sending data (except probe segments)
```

### Zero Window and Persist Timer

When `rwnd = 0`:
- Sender stops sending data
- **Problem:** If the receiver's update saying "rwnd > 0" is lost, both sides will wait forever (deadlock!)
- **Solution: Persist Timer** — sender periodically sends tiny **probe segments** (1 byte) to trigger the receiver to re-advertise its window
- These probes are sent with exponential backoff (initially every 500ms, doubling up to 60 seconds)

### Window Scaling

The window field is 16 bits → max value = 65535 bytes (64 KB). For high-speed networks, this is too small.

**TCP Window Scale option** (negotiated during handshake):
- A scale factor S (0-14) is sent during the SYN
- Actual window = Window field × 2^S
- Maximum possible window = 65535 × 2^14 = **1 GB**

## 5.8 TCP and Full-Duplex Communication

Remember: TCP is **full-duplex**. Both sides simultaneously maintain:

- Their own sequence numbers (tracking what they send)
- Their own ACK numbers (tracking what they've received)
- Their own send and receive buffers
- Their own rwnd (receiver window they advertise)

```
Host A                                Host B
┌──────────────┐                ┌──────────────┐
│ Send Buffer  │──── data ────→│Receive Buffer │
│              │                │              │
│Receive Buffer│←── data ──────│ Send Buffer  │
└──────────────┘                └──────────────┘

Host A has: seq_A, ack_A (= next byte A expects from B), rwnd_A
Host B has: seq_B, ack_B (= next byte B expects from A), rwnd_B
```

---

---

# 6. Principles of Congestion Control

## 6.1 What Is Congestion?

**Congestion** occurs when too much data is injected into the network, exceeding the capacity of links or routers.

| Flow Control                              | Congestion Control                           |
| ----------------------------------------- | -------------------------------------------- |
| Prevents overwhelming the **receiver**    | Prevents overwhelming the **network**        |
| End-to-end (sender ↔ receiver)            | Sender ↔ network                             |
| Uses `rwnd` (receiver's buffer space)     | Uses `cwnd` (sender's estimate of capacity)  |

**Congestion is a network-wide problem, not a single link problem.**

## 6.2 Costs of Congestion (Why It's Bad)

Kurose & Ross describe three increasingly realistic scenarios:

### Scenario 1: Two Senders, Infinite Buffer Router

```
Host A ──→ ┌────────────┐ ──→ Host B
           │   Router   │
Host C ──→ │ (infinite  │ ──→ Host D
           │  buffer)   │
           └────────────┘
           Link capacity: R
```

- Each sender sends at rate λ (lambda)
- Max throughput per connection: R/2 (shared between two flows)
- As λ → R/2: **delay goes to infinity** (queue grows without bound)
- Even with infinite buffers, **delay** becomes the cost

**Lesson:** Even without loss, congestion causes large queuing delays.

### Scenario 2: Finite Buffer Router (Realistic)

Now the router has a **finite buffer**. When it's full, packets are **dropped**.

New costs:
1. **Retransmissions** for lost packets → sender must send more data than the application generates
2. **Unnecessary retransmissions** due to premature timeouts → wasted bandwidth
3. For every lost packet, all the upstream link capacity used to forward it to the point of loss is **wasted**

**"Goodput"** = the rate at which useful (unique, non-duplicate) data arrives at the receiver
- Goodput ≤ Throughput (because retransmissions add to throughput but not goodput)

### Scenario 3: Multi-Hop Paths

When there are multiple hops:
- A packet dropped at hop 3 has already consumed resources at hops 1 and 2 → wasted!
- Congestion can cause **throughput collapse**: as load increases, actual useful throughput can **decrease**

```
    Load vs Throughput:
    
    Throughput
    ↑          ╱╲
    │        ╱    ╲
    │      ╱        ╲  ← Throughput can DROP!
    │    ╱
    │  ╱
    │╱
    └───────────────────→ Offered Load
         Light    Heavy
```

## 6.3 Approaches to Congestion Control

### End-to-End Congestion Control (TCP's Approach)

- Network provides **no explicit feedback** about congestion
- Sender infers congestion from **packet loss** and **delays**
- TCP uses this approach: if a packet is lost, the network must be congested → slow down!

### Network-Assisted Congestion Control

- Routers **explicitly notify** senders about congestion
- Examples:
  - **ECN (Explicit Congestion Notification):** Router marks packets' IP header when congested. Receiver echoes this marking to sender. Sender slows down.
  - **ATM ABR:** Routers send special control cells with explicit rate information.

Modern TCP actually uses **both**: loss-based inference + ECN support.

---

---

# 7. TCP Congestion Control

## 7.1 Overview

TCP congestion control is one of the most important algorithms in the Internet. It's the reason the Internet doesn't constantly collapse under load.

**Core idea:** Each TCP sender maintains a **congestion window (cwnd)** that limits how fast it can send:

$$\text{Sending Rate} \approx \frac{\text{cwnd}}{\text{RTT}} \text{ bytes/sec}$$

$$\text{Actual limit:} \quad \text{LastByteSent} - \text{LastByteAcked} \leq \min(\text{cwnd}, \text{rwnd})$$

The sender adjusts `cwnd` based on perceived network conditions:
- **No loss → increase cwnd** (network has capacity, be more aggressive)
- **Loss detected → decrease cwnd** (network is congested, back off)

This is a distributed, decentralized algorithm — every TCP sender independently adjusts its rate!

## 7.2 The Three Phases

TCP congestion control has three main phases:

```
       ┌─────────────┐
       │  Slow Start  │ (exponential growth)
       └──────┬───────┘
              │ cwnd reaches ssthresh
              ▼
     ┌────────────────┐
     │  Congestion    │ (linear growth)
     │  Avoidance     │
     └───────┬────────┘
             │ loss detected
             ▼
    ┌─────────────────┐
    │ React to Loss   │ (timeout or 3 dup ACKs)
    └─────────────────┘
```

## 7.3 Phase 1: Slow Start

**When:** Connection first starts, or after a timeout.

**Algorithm:**
1. Set `cwnd = 1 MSS` (e.g., ~1460 bytes)
2. For every ACK received: `cwnd = cwnd + 1 MSS`
3. This effectively **doubles** cwnd every RTT

```
RTT 1: cwnd = 1 MSS → send 1 segment → get 1 ACK → cwnd = 2
RTT 2: cwnd = 2 MSS → send 2 segments → get 2 ACKs → cwnd = 4
RTT 3: cwnd = 4 MSS → send 4 segments → get 4 ACKs → cwnd = 8
RTT 4: cwnd = 8 MSS → send 8 segments → get 8 ACKs → cwnd = 16
```

**Growth: 1 → 2 → 4 → 8 → 16 → ... (exponential!)**

Despite the name "slow start," this grows very quickly. The name is relative — compared to just blasting at full speed immediately, it "starts slow."

**When does slow start end?**

| Condition                       | Action                                          |
| ------------------------------- | ----------------------------------------------- |
| `cwnd ≥ ssthresh`               | Switch to **Congestion Avoidance** (linear growth)|
| Timeout                         | Set `ssthresh = cwnd/2`, reset `cwnd = 1 MSS`, restart slow start |
| 3 duplicate ACKs                | Set `ssthresh = cwnd/2`, `cwnd = ssthresh + 3 MSS`, enter **Fast Recovery** |

## 7.4 Phase 2: Congestion Avoidance

**When:** `cwnd ≥ ssthresh` (we're getting close to the network's capacity, be cautious).

**Algorithm:**
- For each RTT (approximately): `cwnd = cwnd + 1 MSS`
- More precisely: For each ACK received: `cwnd = cwnd + MSS × (MSS / cwnd)`

**This is linear growth**: +1 MSS per RTT instead of doubling.

```
RTT 5: cwnd = 16 MSS → send 16 segments → cwnd becomes 17 (+1)
RTT 6: cwnd = 17 MSS → send 17 segments → cwnd becomes 18 (+1)
RTT 7: cwnd = 18 MSS → send 18 segments → cwnd becomes 19 (+1)
```

**Growth: 16 → 17 → 18 → 19 → ... (linear, cautious probing)**

The sender is carefully probing for more bandwidth. This continues until a loss is detected.

## 7.5 Responding to Loss

TCP treats loss as a sign of congestion. But it responds differently depending on HOW the loss was detected:

### Loss Detected by Timeout (Severe Congestion)

A timeout means NO ACKs are getting through — the network may be severely congested.

**Response (aggressive cutback):**
1. `ssthresh = cwnd / 2`
2. `cwnd = 1 MSS`
3. Re-enter **Slow Start**

This is a drastic reset because the situation seems dire.

### Loss Detected by 3 Duplicate ACKs (Mild Congestion)

Three duplicate ACKs mean the network is still delivering SOME packets (the duplicates got through). Congestion exists but isn't catastrophic.

**Response (moderate cutback):**
1. `ssthresh = cwnd / 2`
2. `cwnd = ssthresh + 3 MSS`
3. Enter **Fast Recovery**

The "+3" accounts for the 3 segments that the duplicate ACKs indicate were received.

## 7.6 Phase 3: Fast Recovery

Fast Recovery is entered after fast retransmit (3 duplicate ACKs).

**Algorithm:**
1. Retransmit the lost segment
2. Set `cwnd = ssthresh + 3 MSS`
3. For each **additional** duplicate ACK received: `cwnd = cwnd + 1 MSS`
   (Each duplicate ACK means another segment left the network, so we can send more)
4. When a **new ACK** arrives (acknowledging the retransmitted segment):
   - `cwnd = ssthresh`
   - Enter **Congestion Avoidance**

```
Fast Recovery example:
  cwnd was 20 MSS when 3 dup ACKs detected
  ssthresh = 10 MSS
  cwnd = 10 + 3 = 13 MSS
  
  Each additional dup ACK: cwnd = 14, 15, 16, ...
  New ACK arrives: cwnd = 10 MSS (= ssthresh)
  Continue with Congestion Avoidance: 10 → 11 → 12 → ...
```

**Important:** If a timeout occurs during Fast Recovery:
- `ssthresh = cwnd / 2`
- `cwnd = 1 MSS`
- Go back to Slow Start (same as normal timeout behavior)

## 7.7 TCP Reno vs TCP Tahoe

Two historical versions of TCP that are important for understanding:

| Event               | TCP Tahoe                        | TCP Reno                              |
| -------------------- | -------------------------------- | ------------------------------------- |
| 3 Duplicate ACKs     | `ssthresh = cwnd/2, cwnd = 1`   | `ssthresh = cwnd/2, cwnd = ssthresh + 3` |
|                      | Restart Slow Start               | Enter Fast Recovery                   |
| Timeout              | `ssthresh = cwnd/2, cwnd = 1`   | `ssthresh = cwnd/2, cwnd = 1`        |
|                      | Restart Slow Start               | Restart Slow Start                    |

**Key difference:** Tahoe always resets to `cwnd = 1`. Reno is smarter — it uses Fast Recovery after 3 dup ACKs to avoid starting from scratch.

**Modern TCP uses Reno's approach** (or newer variants like CUBIC, BBR).

## 7.8 AIMD — The Heart of TCP's Strategy

TCP's overall strategy is captured by **AIMD (Additive Increase, Multiplicative Decrease)**:

- **Additive Increase:** During congestion avoidance, increase cwnd by 1 MSS per RTT (linear growth, cautious probing)
- **Multiplicative Decrease:** On loss, cut cwnd in half (aggressive cutback)

This creates TCP's signature **sawtooth pattern**:

```
cwnd (in MSS)
  24 │            ╱╲
  20 │          ╱    ╲
  16 │        ╱        ╲            ╱╲
  12 │      ╱            ╲        ╱    ╲
   8 │    ╱                ╲    ╱        ╲
   4 │  ╱                    ╲╱            ╲
   1 │╱                                     ╲
     └──────────────────────────────────────────→ time
            loss          loss          loss
       (Reno: half)   (Reno: half)   (Timeout: 1 MSS)
```

**Why AIMD?**
- The additive increase probes cautiously for bandwidth
- The multiplicative decrease quickly frees up capacity when congestion occurs
- AIMD has been mathematically proven to converge to a **fair** allocation between competing flows

## 7.9 TCP Fairness

### Is TCP Fair?

**Ideally yes.** If K TCP connections share a bottleneck link of capacity R, each should get R/K.

**Why AIMD leads to fairness:**

Consider two connections sharing a link:
```
Connection 1 throughput
        ↑
     R  │╲  equal share line
        │  ╲     ╱
        │   ╲  ╱  ← AIMD converges here
        │    ╳
        │  ╱  ╲
        │╱     ╲
        └────────────→ Connection 2 throughput
        0            R
```

- Both increase linearly (move diagonally toward the "full bandwidth" line)
- When they hit the capacity: loss → both multiplicatively decrease (move toward the origin along a line through the current point)
- Over many cycles, they converge to the equal share point

### Fairness Caveats

**UDP doesn't play fair:**
- UDP has no congestion control → it sends at whatever rate the app wants
- UDP flows can crowd out TCP flows, which back off when they detect congestion
- This is why there's an ongoing debate about congestion control for UDP (QUIC, for example, implements its own)

**Parallel TCP connections aren't fair:**
- A web browser that opens 10 parallel TCP connections to a server gets 10× the share of a single-connection app
- If a link has capacity R and 9 existing connections: each gets R/9
- Browser opens 10 new connections: now each of 19 gets R/19
- Browser's total: 10 × R/19 ≈ R/2 (half the bandwidth!)

### TCP and the Network-Assisted Approach: ECN

Modern TCP supports **ECN (Explicit Congestion Notification)**:

```
Before ECN: Loss = congestion signal (destructive)
With ECN:   Router marks packets before dropping them (non-destructive warning)
```

**How ECN works:**
1. During handshake, both sides negotiate ECN support (via SYN/SYN-ACK flags)
2. When a router's queue is getting full, it sets the **CE (Congestion Experienced)** bits in the IP header instead of dropping the packet
3. The receiver sees the CE marking → sets the **ECE (ECN-Echo)** flag in the TCP ACK back to the sender
4. Sender sees ECE → reduces cwnd (same as if it detected a loss via 3 dup ACKs)
5. Sender sets **CWR (Congestion Window Reduced)** flag to acknowledge to the receiver

**Benefit:** The sender can slow down BEFORE packets are lost, leading to better throughput and fewer retransmissions.

## 7.10 Complete TCP Congestion Control Summary

Here is the complete algorithm as a step-by-step reference:

```
INITIALIZE:
  cwnd = 1 MSS
  ssthresh = 64 KB (or receiver's advertised window)
  state = SLOW_START

SLOW_START:
  On each ACK:
    cwnd = cwnd + 1 MSS    (doubles every RTT)
  If cwnd >= ssthresh:
    state = CONGESTION_AVOIDANCE
  If timeout:
    ssthresh = cwnd / 2
    cwnd = 1 MSS
    state = SLOW_START
  If 3 dup ACKs:
    ssthresh = cwnd / 2
    cwnd = ssthresh + 3 MSS
    Retransmit lost segment
    state = FAST_RECOVERY

CONGESTION_AVOIDANCE:
  On each ACK:
    cwnd = cwnd + MSS × (MSS / cwnd)    (~1 MSS per RTT)
  If timeout:
    ssthresh = cwnd / 2
    cwnd = 1 MSS
    state = SLOW_START
  If 3 dup ACKs:
    ssthresh = cwnd / 2
    cwnd = ssthresh + 3 MSS
    Retransmit lost segment
    state = FAST_RECOVERY

FAST_RECOVERY:
  On each additional dup ACK:
    cwnd = cwnd + 1 MSS
  On new ACK:
    cwnd = ssthresh
    state = CONGESTION_AVOIDANCE
  If timeout:
    ssthresh = cwnd / 2
    cwnd = 1 MSS
    state = SLOW_START
```

## 7.11 Macroscopic Throughput of TCP

The average throughput of a TCP connection can be approximated:

$$\text{Average Throughput} = \frac{0.75 \times W}{\text{RTT}}$$

Where $W$ = window size (in bytes) when loss occurs.

More precisely (given loss probability $L$):

$$\text{Average Throughput} = \frac{1.22 \times MSS}{RTT \times \sqrt{L}}$$

This shows that TCP throughput is:
- **Directly proportional to MSS** (bigger segments → more throughput per ACK)
- **Inversely proportional to RTT** (farther hosts → less throughput)
- **Inversely proportional to √L** (more loss → less throughput)

This is why transfers to distant servers are slower — not because of bandwidth, but because of TCP's congestion control reacting to the long RTT.

---

---

# 8. Evolution of Transport-Layer Functionality

## 8.1 Why TCP Has Evolved

The Internet has changed dramatically since TCP was first designed:
- Link speeds went from Kbps to 100+ Gbps
- RTTs span from <1ms (data centers) to 250ms (satellite)
- New applications (video streaming, gaming) have different needs
- Middleboxes (firewalls, NATs) can interfere with TCP extensions

## 8.2 QUIC — A Modern Alternative

**QUIC (Quick UDP Internet Connections)** is a transport protocol developed by Google, now standardized as HTTP/3.

**Key design:** QUIC runs on top of **UDP** but implements:
- Reliable data transfer
- Congestion control
- Connection establishment
- Encryption (TLS 1.3 built-in)

**Why not just improve TCP?**
- TCP is implemented in operating system kernels → slow to update
- Middleboxes (firewalls, NATs) interfere with new TCP features
- QUIC runs in user space → can be updated with app updates

### QUIC vs TCP

| Feature                  | TCP                          | QUIC                                  |
| ------------------------ | ---------------------------- | ------------------------------------- |
| **Runs over**            | IP directly                  | UDP (for NAT/firewall traversal)      |
| **Handshake**            | TCP handshake + TLS handshake (2-3 RTT) | Combined handshake (0-1 RTT!) |
| **Encryption**           | Optional (TLS on top)        | Built-in (always encrypted)           |
| **Head-of-line blocking**| Yes (one lost packet blocks all) | No (independent streams)          |
| **Connection migration** | No (tied to IP:port 4-tuple) | Yes (uses Connection ID)             |
| **Multiplexing**         | Separate TCP connections     | Multiple streams in one connection    |
| **Implementation**       | OS kernel                    | User space (easy to update)           |

### QUIC's Connection Handshake

```
TCP + TLS (2-3 RTT before data):        QUIC (0-1 RTT before data):
  Client → Server: SYN                    Client → Server: Client Hello + 
  Server → Client: SYN-ACK                           Connection Setup + Data!
  Client → Server: ACK                    Server → Client: Server Hello +
  Client → Server: TLS ClientHello                    Connection Setup + Data!
  Server → Client: TLS ServerHello
  Client → Server: TLS Finished           (For repeat connections: 0-RTT!)
  Finally: Send data!
```

### QUIC Eliminates Head-of-Line Blocking

**TCP problem:** If you multiplex HTTP/2 streams over one TCP connection and a packet from Stream A is lost, ALL streams (A, B, C) are blocked waiting for the retransmission — even though B and C's data arrived fine.

**QUIC solution:** Each stream is independent. Loss in Stream A only blocks Stream A. Streams B and C continue normally.

```
TCP (HTTP/2):                       QUIC (HTTP/3):
Stream A: pkt1 ✓ pkt2 ✗ pkt3 ✓     Stream A: pkt1 ✓ pkt2 ✗ pkt3 ✓
Stream B: pkt1 ✓ pkt2 ✓             Stream B: pkt1 ✓ pkt2 ✓
Stream C: pkt1 ✓                    Stream C: pkt1 ✓

ALL streams blocked waiting         Only Stream A waits for pkt2
for Stream A's pkt2!                 B and C delivered immediately!
```

---

---

# 9. Summary & Key Takeaways

## The Transport Layer in a Nutshell

1. **Transport layer provides process-to-process communication** using port numbers (extending IP's host-to-host delivery)

2. **Multiplexing/Demultiplexing:**
   - UDP: 2-tuple (dest IP, dest port)
   - TCP: 4-tuple (src IP, src port, dest IP, dest port)

3. **UDP is simple:** Ports + checksum + nothing else. Perfect when speed > reliability.

4. **Reliable data transfer requires:** checksums, ACKs, sequence numbers, timers, and pipelining (built up from rdt 1.0 → 3.0 → GBN/SR)

5. **TCP is reliable, connection-oriented, byte-stream oriented, full-duplex:**
   - 3-way handshake to connect
   - Sequence numbers count bytes
   - Cumulative ACKs + SACK option for out-of-order segments
   - Timeout + fast retransmit (3 dup ACKs) for loss recovery
   - Flow control via receive window (rwnd)
   - 4-way handshake to disconnect

6. **TCP congestion control (AIMD):**
   - Slow Start → Congestion Avoidance → React to Loss
   - Additive Increase (+1 MSS/RTT), Multiplicative Decrease (halve on loss)
   - Fast Recovery avoids resetting to slow start on 3 dup ACKs
   - Leads to fair sharing of bandwidth

7. **QUIC** is the modern evolution: runs over UDP, eliminates head-of-line blocking, integrates encryption, achieves 0-1 RTT connection setup.

## The Big Equations to Remember

| Formula | Purpose |
| ------- | ------- |
| $\text{EstimatedRTT} = 0.875 \cdot \text{EstimatedRTT} + 0.125 \cdot \text{SampleRTT}$ | RTT smoothing |
| $\text{DevRTT} = 0.75 \cdot \text{DevRTT} + 0.25 \cdot |\text{SampleRTT} - \text{EstimatedRTT}|$ | RTT variability |
| $\text{TimeoutInterval} = \text{EstimatedRTT} + 4 \cdot \text{DevRTT}$ | Retransmission timeout |
| $\text{rwnd} = \text{RcvBuffer} - (\text{LastByteRcvd} - \text{LastByteRead})$ | Available receive window |
| $\text{Effective Window} = \min(\text{cwnd}, \text{rwnd})$ | What sender can actually send |
| $\text{Throughput} \approx \frac{0.75 \times W}{\text{RTT}}$ | Average TCP throughput |
| $\text{Utilization} = \frac{L/R}{\text{RTT} + L/R}$ | Stop-and-wait link utilization |

## TCP Congestion Control Cheat Sheet

```
┌──────────────────────────────────────────────────────────────────┐
│                    TCP CONGESTION CONTROL                        │
├─────────────┬──────────────────────┬────────────────────────────┤
│             │    3 Duplicate ACKs   │         Timeout            │
├─────────────┼──────────────────────┼────────────────────────────┤
│ ssthresh    │    cwnd / 2           │       cwnd / 2             │
│ cwnd        │    ssthresh + 3 MSS   │       1 MSS                │
│ Next state  │    Fast Recovery      │       Slow Start           │
├─────────────┴──────────────────────┴────────────────────────────┤
│ Slow Start:       cwnd + 1 MSS per ACK  (doubles each RTT)     │
│ Cong. Avoidance:  cwnd + MSS²/cwnd per ACK  (~+1 MSS per RTT) │
│ Fast Recovery:    cwnd + 1 MSS per dup ACK                      │
│                   New ACK → cwnd = ssthresh, go to Cong. Avoid. │
└──────────────────────────────────────────────────────────────────┘
```

---

---

# 10. Complete Glossary

| Term                            | Definition |
| ------------------------------- | ---------- |
| **ACK (Acknowledgment)**        | A message from the receiver confirming receipt of data. In TCP, ACK number = next byte expected. |
| **AIMD**                        | Additive Increase, Multiplicative Decrease — TCP's congestion avoidance strategy. |
| **ARQ**                         | Automatic Repeat reQuest — general protocol family using ACKs and retransmissions. |
| **Checksum**                    | A 16-bit error-detection value computed over a segment using one's complement arithmetic. |
| **Congestion**                  | When network load exceeds capacity, causing packet loss and delays. |
| **Congestion Avoidance**        | TCP phase where cwnd increases linearly (+1 MSS per RTT). |
| **Congestion Window (cwnd)**    | Sender's self-imposed limit on data in flight, based on perceived congestion. |
| **Cumulative ACK**              | An ACK that confirms receipt of ALL bytes up to the ACK number. |
| **cwnd**                        | Congestion window — see above. |
| **Delayed ACK**                 | Receiver waits up to 500ms before sending ACK, hoping to piggyback or batch ACKs. |
| **Demultiplexing**              | Delivering incoming segments to the correct application socket based on port numbers. |
| **DevRTT**                      | Estimated deviation of RTT; used to set a safety margin for the timeout. |
| **Duplicate ACK**               | An ACK for a segment that was already ACKed; indicates out-of-order delivery or loss. |
| **ECN**                         | Explicit Congestion Notification — routers mark packets instead of dropping them. |
| **Effective Window**            | min(cwnd, rwnd) — actual amount of data the sender can have in flight. |
| **Ephemeral Port**              | A temporary port (49152-65535) assigned by the OS to client applications. |
| **EstimatedRTT**                | Smoothed average of RTT measurements using EWMA. |
| **EWMA**                        | Exponential Weighted Moving Average — technique for smoothing measurements. |
| **Exponential Backoff**         | Doubling the timeout after each retransmission to avoid overwhelming a congested network. |
| **Fast Recovery**               | TCP state after 3 dup ACKs: cwnd = ssthresh + 3, inflate for each dup ACK. |
| **Fast Retransmit**             | Retransmit a segment immediately upon receiving 3 duplicate ACKs, without waiting for timeout. |
| **FIN**                         | TCP flag indicating the sender has finished sending data. |
| **Flow Control**                | Mechanism to prevent sender from overwhelming the receiver's buffer. |
| **Full-Duplex**                 | Both sides can send and receive data simultaneously. |
| **Go-Back-N (GBN)**            | Pipelined protocol where sender retransmits all packets from the lost one onward. Receiver discards out-of-order packets. |
| **Goodput**                     | The rate of useful (non-duplicate, non-retransmitted) data delivered to the application. |
| **Half-Close**                  | State where one direction of a TCP connection is closed but the other is still open. |
| **Header Length / Data Offset** | TCP field (4 bits) indicating the size of the TCP header in 32-bit words. |
| **ISN**                         | Initial Sequence Number — randomly chosen starting sequence number for a TCP connection. |
| **MSL**                         | Maximum Segment Lifetime — max time a segment can live in the network (~30s–2min). |
| **MSS**                         | Maximum Segment Size — max application data in one TCP segment (typically 1460 bytes). |
| **MTU**                         | Maximum Transmission Unit — max frame size at the data link layer (typically 1500 bytes for Ethernet). |
| **Multiplexing**                | Gathering data from multiple sockets, adding headers, and sending down to the network layer. |
| **NAK**                         | Negative Acknowledgment — tells sender the packet was corrupted. Not used in TCP. |
| **Persist Timer**               | Sender's timer to periodically probe a receiver that advertised rwnd = 0. |
| **Piggybacking**                | Including an ACK in a data segment going in the reverse direction. |
| **Pipelining**                  | Sending multiple packets without waiting for individual ACKs. |
| **Port Number**                 | 16-bit identifier (0-65535) for application processes. |
| **Pseudo-Header**               | Virtual header (src IP, dst IP, protocol, length) included in checksum calculation for extra protection. |
| **QUIC**                        | Modern transport protocol over UDP with built-in encryption, 0-RTT setup, and no head-of-line blocking. |
| **rdt**                         | Reliable data transfer — the abstract protocol developed step-by-step in the textbook. |
| **Receive Buffer**              | Memory at the receiver storing data between TCP receipt and application read. |
| **Receive Window (rwnd)**       | Amount of free space in receiver buffer; advertised to sender for flow control. |
| **RST**                         | TCP Reset flag — abruptly terminates a connection. |
| **RTT**                         | Round-Trip Time — time for a segment to reach the receiver and the ACK to come back. |
| **RTO**                         | Retransmission Timeout — the timer value after which a segment is retransmitted. |
| **SampleRTT**                   | Single measurement of RTT for one segment-ACK pair. |
| **SACK**                        | Selective Acknowledgment — TCP option listing byte ranges received out-of-order. |
| **Segment**                     | Transport-layer PDU = TCP/UDP header + application data. |
| **Selective Repeat (SR)**       | Pipelined protocol where only lost packets are retransmitted. Receiver buffers out-of-order packets. |
| **Send Buffer**                 | Memory at the sender storing data between application write and TCP send + ACK. |
| **Sequence Number**             | In TCP: the byte number of the first data byte in the segment. |
| **Slow Start**                  | TCP phase where cwnd doubles each RTT (exponential growth). |
| **Slow Start Threshold (ssthresh)** | The cwnd value at which TCP transitions from slow start to congestion avoidance. |
| **Socket**                      | The interface (endpoint) between the application and the transport layer. |
| **Stop-and-Wait**               | Sending one packet at a time, waiting for ACK before sending the next. |
| **SYN**                         | TCP Synchronize flag — used in the first two packets of the 3-way handshake. |
| **SYN Cookie**                  | Defense against SYN flood attacks: server encodes state in the SYN-ACK seq number. |
| **SYN Flood**                   | DoS attack where attacker sends many SYNs with fake IPs to exhaust server resources. |
| **TCP**                         | Transmission Control Protocol — reliable, ordered, connection-oriented transport protocol. |
| **TCP Reno**                    | TCP variant with Fast Recovery after 3 dup ACKs (doesn't reset cwnd to 1). |
| **TCP Tahoe**                   | Older TCP variant that always resets cwnd to 1 on any loss event. |
| **TIME_WAIT**                   | TCP state after sending final ACK in teardown; lasts 2×MSL. |
| **Timeout**                     | When retransmission timer expires, indicating probable packet loss. |
| **TTL**                         | Time to Live — IP header field decremented by each router; prevents infinite loops. |
| **UDP**                         | User Datagram Protocol — simple, connectionless, unreliable transport protocol. |
| **Welcoming Socket**            | The TCP server socket that listens for incoming connection requests. |
| **Window Scale**                | TCP option that allows receive window > 64 KB by applying a scale factor. |
| **Window Size**                 | TCP header field advertising receiver's available buffer space (rwnd). |

---

---

# 11. Self-Test Questions & Answers

### Basics

**Q1: What is the difference between network-layer delivery and transport-layer delivery?**
> Network layer (IP): host-to-host. Transport layer (TCP/UDP): process-to-process, using port numbers.

**Q2: What two services do BOTH TCP and UDP provide?**
> Multiplexing/demultiplexing and error checking (checksum).

**Q3: What does neither TCP nor UDP guarantee?**
> Timing guarantees, minimum bandwidth, or security (natively).

### Multiplexing/Demultiplexing

**Q4: How does UDP identify which socket to deliver to?**
> Using a 2-tuple: (destination IP, destination port).

**Q5: How does TCP identify which socket to deliver to?**
> Using a 4-tuple: (source IP, source port, destination IP, destination port).

**Q6: Why does a web server need the 4-tuple?**
> So it can maintain separate connections (sockets) for thousands of clients all connecting to port 80/443.

### UDP

**Q7: How many bytes is the UDP header?**
> 8 bytes (4 fields × 2 bytes each).

**Q8: Is the UDP checksum mandatory?**
> Optional in IPv4, mandatory in IPv6.

**Q9: What happens when UDP detects a checksum error?**
> The segment is silently discarded. No notification, no retransmission.

### Reliable Data Transfer

**Q10: What problem does rdt 2.0 solve that rdt 1.0 doesn't?**
> Bit errors (using checksum + ACK/NAK + retransmission).

**Q11: What problem does rdt 2.1 solve that rdt 2.0 doesn't?**
> Corrupted ACK/NAK (using sequence numbers to detect duplicates).

**Q12: What problem does rdt 3.0 solve that rdt 2.2 doesn't?**
> Packet loss (using a countdown timer for retransmission).

**Q13: Why is stop-and-wait inefficient?**
> Sender utilization = L/R ÷ (RTT + L/R), which is extremely low on high-speed, high-delay links.

**Q14: In Go-Back-N, what does the receiver do with out-of-order packets?**
> Discards them and re-sends ACK for the last in-order packet.

**Q15: In Selective Repeat, what does the receiver do with out-of-order packets?**
> Buffers them and sends an individual ACK for each.

**Q16: What is the max window size for GBN with k-bit sequence numbers?**
> N ≤ 2^k − 1

**Q17: What is the max window size for SR with k-bit sequence numbers?**
> N ≤ 2^(k−1)

### TCP

**Q18: What are the 3 steps of the TCP handshake?**
> SYN → SYN-ACK → ACK.

**Q19: Can the third packet (ACK) of the handshake carry data?**
> Yes!

**Q20: What do TCP sequence numbers count?**
> Bytes (not packets). The seq# = byte number of the first data byte in the segment.

**Q21: What does an ACK number of 500 mean?**
> "I have successfully received all bytes up to 499. Send me byte 500 next."

**Q22: What triggers TCP fast retransmit?**
> Receiving 3 duplicate ACKs for the same segment.

**Q23: What is the formula for TCP's retransmission timeout?**
> TimeoutInterval = EstimatedRTT + 4 × DevRTT

**Q24: What happens when the receiver's buffer is full (rwnd = 0)?**
> Sender stops sending data but periodically sends probe segments (1 byte) via the persist timer to trigger a window update.

**Q25: What is the difference between a FIN and a RST?**
> FIN = graceful close (orderly shutdown, lets other side finish). RST = abrupt reset (connection killed immediately, something went wrong).

### Congestion Control

**Q26: What is the difference between flow control and congestion control?**
> Flow control prevents overwhelming the receiver (uses rwnd). Congestion control prevents overwhelming the network (uses cwnd).

**Q27: What is cwnd set to at the start of slow start?**
> 1 MSS.

**Q28: How fast does cwnd grow during slow start?**
> Doubles every RTT (exponential growth).

**Q29: How fast does cwnd grow during congestion avoidance?**
> +1 MSS per RTT (linear growth).

**Q30: What does TCP do on a timeout?**
> ssthresh = cwnd/2, cwnd = 1 MSS, restart Slow Start.

**Q31: What does TCP do on 3 duplicate ACKs?**
> ssthresh = cwnd/2, cwnd = ssthresh + 3 MSS, enter Fast Recovery.

**Q32: What is AIMD?**
> Additive Increase (linear growth in congestion avoidance) + Multiplicative Decrease (halve cwnd on loss). This creates the sawtooth pattern and ensures fairness.

**Q33: What is the sending rate of a TCP connection?**
> Approximately cwnd/RTT bytes per second, limited by min(cwnd, rwnd).

**Q34: Is TCP fair? What about UDP?**
> TCP converges to fair shares via AIMD. UDP has no congestion control and can starve TCP flows.

### QUIC

**Q35: What protocol does QUIC run on top of?**
> UDP.

**Q36: What problem does QUIC solve that TCP can't?**
> Head-of-line blocking (one lost packet blocks all streams in TCP; QUIC has independent streams). Also: faster connection setup (0-1 RTT vs 2-3 RTT for TCP+TLS).

---

*Reference: Kurose, J.F. & Ross, K.W. — Computer Networking: A Top-Down Approach, 8th Edition, Chapter 3: Transport Layer.*
