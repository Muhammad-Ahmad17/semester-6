# Pre-Lab Reading Guide: TCP, UDP & ICMP

### *Beginner-Friendly Edition — Based on Kurose & Ross, Chapter 3*

---

## Table of Contents

1. [The Big Picture — Why Do We Need These Protocols?](#1-the-big-picture)
2. [Transport Layer Basics](#2-transport-layer-basics)
3. [UDP — User Datagram Protocol](#3-udp--user-datagram-protocol)
4. [TCP — Transmission Control Protocol](#4-tcp--transmission-control-protocol)
5. [ICMP — Internet Control Message Protocol](#5-icmp--internet-control-message-protocol)
6. [Side-by-Side Comparison](#6-side-by-side-comparison)
7. [Key Terms Glossary](#7-key-terms-glossary)

---

## 1. The Big Picture

Imagine you want to send a letter to a friend:

- **IP (Internet Protocol)** is like the postal service — it knows the *address* (IP address) but doesn't guarantee the letter arrives, arrives in order, or arrives undamaged.
- **TCP** is like registered mail — it guarantees delivery, correct order, and no damage. If something goes wrong, it re-sends.
- **UDP** is like dropping a postcard in a mailbox — fast and simple, but no guarantee it arrives. No tracking.
- **ICMP** is like the postal service sending *you* a notification saying "that address doesn't exist" or "road blocked." It's a *helper* protocol for reporting errors and diagnostics.

All three work **on top of IP** but serve very different purposes.

---

## 2. Transport Layer Basics

### Where Does the Transport Layer Sit?

```
┌─────────────────────┐
│   Application Layer  │  ← Your apps (browser, email, games)
├─────────────────────┤
│   Transport Layer    │  ← TCP & UDP live here
├─────────────────────┤
│   Network Layer      │  ← IP & ICMP live here
├─────────────────────┤
│   Data Link Layer    │  ← Ethernet, Wi-Fi
├─────────────────────┤
│   Physical Layer     │  ← Cables, radio waves
└─────────────────────┘
```

> **Note:** ICMP is technically a *Network Layer* protocol (it sits inside IP packets), but we study it alongside TCP/UDP because they all work together.

### What Does the Transport Layer Do?

The transport layer provides **logical communication between application processes** running on different hosts. Think of it this way:

- **Network Layer (IP):** Gets data from **Host A** to **Host B** (house to house).
- **Transport Layer (TCP/UDP):** Gets data from **Process X on Host A** to **Process Y on Host B** (person to person inside those houses).

### Ports — How Processes Are Identified

Every application on your computer uses a **port number** (0–65535) to send/receive data.

| Port Range     | Name             | Examples                                    |
| -------------- | ---------------- | ------------------------------------------- |
| 0 – 1023      | Well-Known Ports | HTTP (80), HTTPS (443), DNS (53), SMTP (25) |
| 1024 – 49151  | Registered Ports | MySQL (3306), PostgreSQL (5432)             |
| 49152 – 65535 | Dynamic/Private  | Assigned temporarily by your OS to apps     |

When your browser opens `google.com`, your OS says:

- **Destination port:** 443 (HTTPS on Go| col1 | col2 | col3 |
  | ---- | ---- | ---- |
  |      |      |      |
  |      |      |      |

  ogle's server)
- **Source port:** 52314 (random high port your OS picks for the browser)

### Multiplexing & Demultiplexing

These are fancy words for a simple concept:

- **Multiplexing (at sender):** Multiple apps hand data to the transport layer → transport layer labels each with the correct port and sends it down.
- **Demultiplexing (at receiver):** Transport layer receives data → looks at the destination port → delivers to the right app.

```
App A (port 80)  ──┐                          ┌── App A (port 80)
App B (port 443) ──┤──  Transport Layer  ──────┤── App B (port 443)
App C (port 53)  ──┘      (mux/demux)         └── App C (port 53)
```

---

## 3. UDP — User Datagram Protocol

### What Is UDP?

UDP is the **simplest** transport protocol. It does almost nothing on top of IP — just adds port numbers and an optional checksum. That's it.

**Think of UDP as:** "Here's the data. Good luck."

### Why Would Anyone Use UDP?

Because sometimes you **want** simplicity and speed:

| Scenario             | Why UDP?                                                         |
| -------------------- | ---------------------------------------------------------------- |
| Video streaming      | A lost frame is better than pausing to re-request it             |
| Online gaming        | Speed > perfection; old data is useless anyway                   |
| DNS queries          | Tiny request, tiny response — overhead of TCP setup is wasteful |
| Voice over IP (VoIP) | Real-time; can't wait for retransmissions                        |
| IoT sensor data      | Lightweight devices, simple protocol                             |

### UDP Segment Structure (Header = Only 8 Bytes!)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─────────────────────┼─────────────────────┤
│    Source Port (16)  │  Destination Port (16) │
├─────────────────────┼─────────────────────┤
│     Length (16)      │    Checksum (16)     │
├─────────────────────┴─────────────────────┤
│              Application Data              │
│                   ...                      │
└────────────────────────────────────────────┘
```

Four fields, each 16 bits (2 bytes):

| Field                 | Size    | Purpose                                               |
| --------------------- | ------- | ----------------------------------------------------- |
| **Source Port** | 16 bits | Port of the sending application                       |
| **Dest Port**   | 16 bits | Port of the receiving application                     |
| **Length**      | 16 bits | Total length of UDP segment (header + data) in bytes  |
| **Checksum**    | 16 bits | Error detection (optional in IPv4, mandatory in IPv6) |

### UDP Checksum — How It Works (Step by Step)

The checksum catches **bit errors** (flipped bits during transmission).

**Sender side:**

1. Take the UDP header + data + a pseudo-header (source IP, dest IP, protocol number, UDP length).
2. Split into 16-bit words.
3. Add all 16-bit words using **one's complement addition** (if there's a carry out of the MSB, wrap it around and add it to the LSB).
4. Take the **one's complement** (flip all bits) of the final sum → that's the checksum.

**Receiver side:**

1. Add all 16-bit words of the received segment (including the checksum).
2. If the result is `1111111111111111` (all 1s), **no error** detected.
3. If any bit is 0, **error detected** → segment is discarded silently.

**Example:**

```
Word 1:  0110011001100000
Word 2:  0101010101010101
Word 3:  1000111100001100
─────────────────────────
Sum:     0100101011000010   (with wraparound carry)
Checksum:1011010100111101   (one's complement of sum)
```

> **Limitation:** The checksum can detect errors but CANNOT correct them. Also, some errors can cancel out (very rare).

### What UDP Does NOT Provide

- ❌ No guaranteed delivery (packets can be lost)
- ❌ No ordering (packets can arrive out of order)
- ❌ No connection setup (no handshake)
- ❌ No flow control (sender can overwhelm receiver)
- ❌ No congestion control (sender can flood the network)

---

## 4. TCP — Transmission Control Protocol

### What Is TCP?

TCP is a **reliable, connection-oriented, byte-stream** protocol. It guarantees that data arrives correctly, in order, and without duplication.

**Think of TCP as:** "I'll make absolutely sure your data gets there perfectly, even if I have to resend it 10 times."

### TCP's Key Properties

| Property                       | What It Means                                                        |
| ------------------------------ | -------------------------------------------------------------------- |
| **Connection-oriented**  | Must establish a connection before sending data (3-way handshake)    |
| **Reliable delivery**    | Every byte sent will be received (or sender is notified of failure)  |
| **In-order delivery**    | Data arrives in the same order it was sent                           |
| **Byte-stream oriented** | TCP sees data as a continuous stream of bytes, not discrete messages |
| **Full-duplex**          | Both sides can send and receive simultaneously                       |
| **Flow control**         | Prevents sender from overwhelming the receiver                       |
| **Congestion control**   | Prevents sender from overwhelming the network                        |

### TCP Segment Structure (Header = 20–60 Bytes)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─────────────────────┼─────────────────────┤
│    Source Port (16)  │  Destination Port (16) │
├─────────────────────────────────────────────┤
│                Sequence Number (32)          │
├─────────────────────────────────────────────┤
│             Acknowledgment Number (32)       │
├────────┼────┼──────┼───────────────────────┤
│Data    │Res │Flags │     Window Size (16)    │
│Offset  │(4) │(6)   │                         │
│(4 bits)│    │      │                         │
├─────────────────────┼─────────────────────┤
│    Checksum (16)    │  Urgent Pointer (16)  │
├─────────────────────┴─────────────────────┤
│          Options (0–40 bytes)              │
├────────────────────────────────────────────┤
│              Application Data              │
└────────────────────────────────────────────┘
```

Let's break down each field:

| Field                      | Size     | Purpose                                                               |
| -------------------------- | -------- | --------------------------------------------------------------------- |
| **Source Port**      | 16 bits  | Sender's port number                                                  |
| **Destination Port** | 16 bits  | Receiver's port number                                                |
| **Sequence Number**  | 32 bits  | Byte number of the first byte in this segment's data                  |
| **ACK Number**       | 32 bits  | The next byte number the receiver expects (cumulative acknowledgment) |
| **Data Offset**      | 4 bits   | Size of TCP header in 32-bit words (min 5 = 20 bytes)                 |
| **Flags**            | 6 bits   | Control bits (see below)                                              |
| **Window Size**      | 16 bits  | How many bytes the receiver is willing to accept (flow control)       |
| **Checksum**         | 16 bits  | Error detection (same method as UDP but mandatory)                    |
| **Urgent Pointer**   | 16 bits  | Points to urgent data (rarely used)                                   |
| **Options**          | Variable | Optional features like MSS, Window Scaling, SACK, Timestamps          |

### TCP Flags — The 6 Control Bits

Each flag is 1 bit (on or off):

| Flag          | Name           | When Is It Set?                                     |
| ------------- | -------------- | --------------------------------------------------- |
| **SYN** | Synchronize    | Connection setup (first two packets of handshake)   |
| **ACK** | Acknowledgment | Almost always set after handshake; confirms receipt |
| **FIN** | Finish         | Sender wants to close the connection                |
| **RST** | Reset          | Abort the connection immediately (something wrong)  |
| **PSH** | Push           | Deliver data to app immediately, don't buffer       |
| **URG** | Urgent         | Urgent data present (check Urgent Pointer field)    |

### The 3-Way Handshake — How TCP Connects

Before any data is sent, TCP establishes a connection:

```
    Client                          Server
      │                               │
      │──── SYN (seq=x) ────────────→│   Step 1: "Hey, I want to connect"
      │                               │            Client picks random seq # x
      │                               │
      │←── SYN-ACK (seq=y, ack=x+1) ─│   Step 2: "OK, I'm ready too"
      │                               │            Server picks random seq # y
      │                               │            Acknowledges client's SYN
      │                               │
      │──── ACK (seq=x+1, ack=y+1) ──→│   Step 3: "Great, let's go"
      │                               │            Connection established!
      │                               │
```

**Why 3 steps? Why not 2?**

- With only 2 steps, the server has no confirmation that the client received the server's SYN. Old duplicate SYN packets could cause "half-open" connections, wasting server resources.
- The 3rd step confirms both sides are synchronized and ready.

**Real-life analogy:**

- You: "Can you hear me?" (SYN)
- Friend: "Yes, can you hear me?" (SYN-ACK)
- You: "Yes!" (ACK)
- Now both of you know the other can hear.

### Sequence and Acknowledgment Numbers — The Heart of TCP

This is where most beginners get confused. Let's go slow.

**Sequence Number:** Counts *bytes*, not packets.

Example: You want to send "Hello World" (11 bytes), and your initial sequence number is 100:

```
Segment 1: seq=100, data="Hello" (5 bytes)     → bytes 100-104
Segment 2: seq=105, data=" Worl" (5 bytes)      → bytes 105-109
Segment 3: seq=110, data="d"     (1 byte)       → byte  110
```

**Acknowledgment Number:** "I've received everything up to byte X. Send me byte X next."

```
After receiving Segment 1: ACK = 105  ("I got bytes 100-104, send byte 105 next")
After receiving Segment 2: ACK = 110  ("I got bytes 105-109, send byte 110 next")
After receiving Segment 3: ACK = 111  ("I got byte 110, send byte 111 next")
```

This is called **cumulative acknowledgment** — the ACK number tells the sender that ALL bytes before that number have been received.

### TCP Reliable Data Transfer — How TCP Handles Lost/Corrupted Data

TCP uses multiple mechanisms to ensure reliability:

#### Mechanism 1: Timeout-Based Retransmission

```
Sender sends segment (seq=100) → starts a TIMER
  │
  │ ← No ACK received before timer expires
  │
  ▼
Sender RETRANSMITS the same segment (seq=100)
```

**How long is the timer?**

- TCP estimates the Round-Trip Time (RTT) — the time for a packet to travel to the receiver and back.
- Timeout = EstimatedRTT + 4 × DevRTT (safety margin)
- If timeout happens, TCP **doubles** the timeout for the next retry (exponential backoff).

#### Mechanism 2: Fast Retransmit (3 Duplicate ACKs)

Sometimes the timer is too slow. TCP has a faster way:

```
Sender sends: seq=100, seq=200, seq=300, seq=400, seq=500

Receiver gets: 100  ✓ → ACK 200
               200  ✗ → LOST!
               300  ✓ → ACK 200  (duplicate ACK #1 — "I still need 200!")
               400  ✓ → ACK 200  (duplicate ACK #2)
               500  ✓ → ACK 200  (duplicate ACK #3)

Sender receives 3 duplicate ACKs for 200 → IMMEDIATELY retransmits seq=200
(without waiting for the timer to expire)
```

**Why 3 duplicates?** One or two could be caused by normal packet reordering. Three strongly suggests a loss.

### TCP Flow Control — Don't Overwhelm the Receiver

The receiver has a **receive buffer** of limited size. If the sender sends too fast, the buffer overflows and data is lost.

**Solution: Receive Window (rwnd)**

```
Receiver → Sender: "My buffer has 5000 bytes free" (rwnd = 5000)

Sender: "OK, I'll send at most 5000 bytes before waiting for an ACK"

Receiver processes some data, buffer now has 8000 bytes free
Receiver → Sender: "rwnd = 8000"

Sender: "Great, I can send more now"
```

The `rwnd` value is sent in every TCP segment's **Window Size** field.

**Edge case — Zero Window:**
If `rwnd = 0`, the sender stops sending. But then how does the sender know when the receiver is ready again? → The sender periodically sends **probe segments** (1 byte) to trigger an updated window.

### TCP Congestion Control — Don't Overwhelm the Network

Even if the receiver can handle more data, the **network** might be congested (too many packets). TCP has built-in mechanisms:

#### The Congestion Window (cwnd)

- The sender maintains `cwnd` — the max amount of data it can have in the network.
- **Actual sending rate = min(rwnd, cwnd)** — limited by the tighter constraint.

#### Phase 1: Slow Start (Exponential Growth)

```
Start: cwnd = 1 MSS (e.g., 1 segment ≈ 1460 bytes)

Round 1: Send 1 segment → get 1 ACK → cwnd = 2 MSS
Round 2: Send 2 segments → get 2 ACKs → cwnd = 4 MSS
Round 3: Send 4 segments → get 4 ACKs → cwnd = 8 MSS
...doubles every RTT!
```

**"Slow start" is actually not slow at all** — it grows exponentially. The name is historical (compared to just blasting data immediately).

Growth continues until:

- `cwnd` reaches the **slow start threshold (ssthresh)** → switch to congestion avoidance
- A packet loss is detected → respond to congestion

#### Phase 2: Congestion Avoidance (Linear Growth)

Once `cwnd ≥ ssthresh`:

```
Each RTT: cwnd = cwnd + 1 MSS (linear increase)
```

This is much more cautious growth — probing for available bandwidth slowly.

#### What Happens on Packet Loss?

| Event                      | Action                                                      |
| -------------------------- | ----------------------------------------------------------- |
| **Timeout**          | ssthresh = cwnd/2, cwnd = 1 MSS, go back to Slow Start      |
| **3 Duplicate ACKs** | ssthresh = cwnd/2, cwnd = ssthresh + 3, enter Fast Recovery |

This is called **AIMD — Additive Increase, Multiplicative Decrease**:

- **Additive Increase:** Grow linearly during congestion avoidance (+1 MSS per RTT)
- **Multiplicative Decrease:** Halve the window on loss (cwnd/2)

AIMD creates TCP's characteristic "sawtooth" pattern:

```
cwnd
 ↑        /\      /\      /\
 │       /  \    /  \    /  \
 │      /    \  /    \  /    \
 │     /      \/      \/      \
 │    /
 └──────────────────────────────→ time
       loss   loss    loss
```

### TCP Connection Termination — The 4-Way Handshake

Either side can initiate closing:

```
    Client                          Server
      │                               │
      │──── FIN ─────────────────────→│  Step 1: "I'm done sending"
      │                               │
      │←── ACK ──────────────────────│  Step 2: "OK, noted" 
      │                               │          (Server can still send data!)
      │                               │
      │←── FIN ──────────────────────│  Step 3: "I'm done too"
      │                               │
      │──── ACK ─────────────────────→│  Step 4: "OK, connection closed"
      │                               │
      │   [TIME_WAIT: 2×MSL]          │  Client waits before fully closing
      │                               │
```

**Why TIME_WAIT?**

- To make sure the final ACK reaches the server. If it's lost, the server will re-send its FIN, and the client can re-send the ACK.
- To let old duplicate packets from this connection expire so they don't interfere with a new connection on the same ports.
- **MSL = Maximum Segment Lifetime** (typically 30 seconds to 2 minutes).

---

## 5. ICMP — Internet Control Message Protocol

### What Is ICMP?

ICMP is a **helper protocol** used by network devices to send error messages and diagnostic information. It works at the **Network Layer** (inside IP packets).

**ICMP is NOT used to send application data.** It's used by the network itself to communicate problems.

**Think of ICMP as:** A traffic officer telling you "this road is closed" or "you took a wrong turn."

### When Does ICMP Kick In?

| Situation                            | ICMP Message                |
| ------------------------------------ | --------------------------- |
| Destination host is unreachable      | Destination Unreachable     |
| Packet's TTL (time to live) expired  | Time Exceeded               |
| Router can't fragment a large packet | Fragmentation Needed        |
| You run `ping` command             | Echo Request / Echo Reply   |
| You run `traceroute` command       | Uses Time Exceeded messages |
| Network is congested                 | Source Quench (deprecated)  |
| A better route exists                | Redirect                    |

### ICMP Message Structure

ICMP messages are carried **inside IP packets**:

```
┌──────────────────────────────────────────┐
│            IP Header (20 bytes)           │
│  Protocol field = 1 (means ICMP)         │
├──────────────────────────────────────────┤
│     Type (8 bits)  │  Code (8 bits)      │
├────────────────────┴─────────────────────┤
│           Checksum (16 bits)              │
├──────────────────────────────────────────┤
│     Type-Specific Data (variable)         │
│  (often includes the header + first 8    │
│   bytes of the packet that caused the    │
│   error — so sender can identify which   │
│   packet had the problem)                │
└──────────────────────────────────────────┘
```

### Common ICMP Message Types

| Type | Code | Name                     | Description                                   |
| ---- | ---- | ------------------------ | --------------------------------------------- |
| 0    | 0    | Echo Reply               | Response to ping                              |
| 3    | 0    | Net Unreachable          | Destination network doesn't exist             |
| 3    | 1    | Host Unreachable         | Destination host doesn't exist or is down     |
| 3    | 3    | Port Unreachable         | No app listening on that port (UDP only)      |
| 3    | 4    | Fragmentation Needed     | Packet too big + DF flag set                  |
| 4    | 0    | Source Quench            | "Slow down!" (deprecated, rarely used now)    |
| 5    | 0    | Redirect                 | "Use a different router for this destination" |
| 8    | 0    | Echo Request             | Ping request                                  |
| 11   | 0    | TTL Exceeded             | Packet's TTL reached 0 (used by traceroute)   |
| 11   | 1    | Fragment Reassembly Time | Not all fragments arrived in time             |

### Ping — How It Works

`ping google.com` sends ICMP Echo Request messages:

```
Your PC ──── Echo Request (Type 8) ────→ google.com
Your PC ←── Echo Reply   (Type 0) ──── google.com

Round-Trip Time (RTT): 15 ms
```

**What ping tells you:**

- Is the host reachable? (If you get replies: yes)
- How long does a round trip take? (RTT in milliseconds)
- Is there packet loss? (If some requests get no reply)

**Sample output:**

```
$ ping google.com
PING google.com (142.250.80.46) 56(84) bytes of data.
64 bytes from 142.250.80.46: icmp_seq=1 ttl=117 time=12.3 ms
64 bytes from 142.250.80.46: icmp_seq=2 ttl=117 time=11.8 ms
64 bytes from 142.250.80.46: icmp_seq=3 ttl=117 time=13.1 ms

--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 11.8/12.4/13.1/0.5 ms
```

### Traceroute — How It Uses ICMP

`traceroute google.com` discovers every router between you and the destination:

**Trick:** It sends packets with increasing TTL values:

```
Step 1: Send packet with TTL=1
        → First router decrements TTL to 0 → sends back ICMP "Time Exceeded"
        → Now you know Router 1's IP and RTT

Step 2: Send packet with TTL=2
        → Router 1 decrements TTL to 1, forwards it
        → Router 2 decrements TTL to 0 → sends back ICMP "Time Exceeded"
        → Now you know Router 2's IP and RTT

Step 3: Send packet with TTL=3
        → ... same pattern ...

Last Step: TTL is high enough → packet reaches destination
           → Destination sends back ICMP "Port Unreachable" (Linux traceroute)
              or ICMP "Echo Reply" (Windows tracert)
           → You know the full path!
```

**Sample output:**

```
$ traceroute google.com
 1  192.168.1.1      1.2 ms   ← Your home router
 2  10.0.0.1         5.4 ms   ← ISP router
 3  72.14.215.85    10.2 ms   ← Google's network
 4  142.250.80.46   12.1 ms   ← google.com (destination)
```

### TTL (Time to Live) — Why It Exists

- Every IP packet has a TTL field (8 bits, max value 255).
- **Each router decrements TTL by 1** when forwarding.
- If TTL reaches 0, the router **drops the packet** and sends ICMP Time Exceeded back to the sender.

**Why?** To prevent packets from looping forever if there's a routing error/loop.

```
Routing Loop Without TTL:
  Router A → Router B → Router C → Router A → Router B → ... (forever!)

With TTL:
  Router A (TTL=64) → Router B (TTL=63) → ... → some router (TTL=0) → DROP + ICMP
```

---

## 6. Side-by-Side Comparison

### TCP vs UDP

| Feature                       | TCP                             | UDP                          |
| ----------------------------- | ------------------------------- | ---------------------------- |
| **Connection**          | Connection-oriented (handshake) | Connectionless               |
| **Reliability**         | Guaranteed delivery             | Best-effort (no guarantee)   |
| **Ordering**            | In-order delivery               | No ordering                  |
| **Speed**               | Slower (more overhead)          | Faster (minimal overhead)    |
| **Header size**         | 20–60 bytes                    | 8 bytes                      |
| **Flow control**        | Yes (receive window)            | No                           |
| **Congestion ctrl**     | Yes (slow start, AIMD)          | No                           |
| **Error detection**     | Mandatory checksum              | Optional checksum (IPv4)     |
| **Data boundary**       | Byte stream (no boundaries)     | Message-oriented (preserved) |
| **Broadcast/Multicast** | No                              | Yes                          |
| **Use cases**           | Web, email, file transfer, SSH  | DNS, streaming, gaming, VoIP |

### TCP vs UDP vs ICMP

| Aspect                      | TCP                    | UDP                 | ICMP                        |
| --------------------------- | ---------------------- | ------------------- | --------------------------- |
| **Layer**             | Transport (Layer 4)    | Transport (Layer 4) | Network (Layer 3)           |
| **IP Protocol #**     | 6                      | 17                  | 1                           |
| **Purpose**           | Reliable data transfer | Fast data transfer  | Error reporting/diagnostics |
| **Uses ports?**       | Yes                    | Yes                 | No (uses type & code)       |
| **Carries app data?** | Yes                    | Yes                 | No (only control info)      |

---

## 7. Key Terms Glossary

| Term                              | Definition                                                                                      |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Segment**                 | Transport layer PDU (TCP/UDP header + data)                                                     |
| **Datagram**                | Often used for UDP segments or IP packets                                                       |
| **MSS**                     | Maximum Segment Size — largest chunk of data TCP puts in one segment (typically 1460 bytes)    |
| **MTU**                     | Maximum Transmission Unit — largest frame the data link layer accepts (typically 1500 bytes)   |
| **RTT**                     | Round-Trip Time — time for a packet to go out and an ACK to come back                          |
| **rwnd**                    | Receive Window — how many bytes the receiver can accept (flow control)                         |
| **cwnd**                    | Congestion Window — how many bytes the sender can inject into the network (congestion control) |
| **ssthresh**                | Slow Start Threshold — point where slow start switches to congestion avoidance                 |
| **MSL**                     | Maximum Segment Lifetime — max time a segment can exist in the network (~30s–2min)            |
| **TTL**                     | Time to Live — hop counter in IP header; decremented by each router                            |
| **SYN**                     | Synchronize flag — used in connection establishment                                            |
| **ACK**                     | Acknowledgment flag/number — confirms receipt of data                                          |
| **FIN**                     | Finish flag — used in connection termination                                                   |
| **RST**                     | Reset flag — abruptly terminates a connection                                                  |
| **AIMD**                    | Additive Increase, Multiplicative Decrease — TCP's congestion avoidance strategy               |
| **Fast Retransmit**         | Retransmit after 3 duplicate ACKs instead of waiting for timeout                                |
| **3-Way Handshake**         | SYN → SYN-ACK → ACK connection setup                                                          |
| **4-Way Termination**       | FIN → ACK → FIN → ACK connection teardown                                                    |
| **Cumulative ACK**          | ACK number means "I have everything up to this byte"                                            |
| **Selective ACK (SACK)**    | TCP option that tells sender exactly which blocks were received (out of order)                  |
| **Checksum**                | 16-bit error detection code computed using one's complement arithmetic                          |
| **Pseudo-header**           | Fake header (src IP, dst IP, protocol, length) included in checksum for extra protection        |
| **Pipelining**              | Sending multiple packets without waiting for individual ACKs (sliding window)                   |
| **Go-Back-N**               | On loss, retransmit the lost packet and ALL subsequent packets                                  |
| **Selective Repeat**        | On loss, retransmit ONLY the lost packet                                                        |
| **Echo Request/Reply**      | ICMP messages used by `ping`                                                                  |
| **Time Exceeded**           | ICMP message sent when TTL reaches 0 (used by `traceroute`)                                   |
| **Destination Unreachable** | ICMP message sent when a host/port/network can't be reached                                     |

---

## Quick Self-Test Questions

1. **What port number does HTTP use?** → 80
2. **How many bytes is a UDP header?** → 8
3. **What are the 3 steps of TCP's handshake?** → SYN, SYN-ACK, ACK
4. **What triggers TCP fast retransmit?** → 3 duplicate ACKs
5. **What ICMP type is Echo Request?** → Type 8
6. **What ICMP type is Echo Reply?** → Type 0
7. **What command uses ICMP Echo?** → `ping`
8. **What command uses ICMP Time Exceeded?** → `traceroute`
9. **What is the formula for TCP sending rate?** → min(rwnd, cwnd)
10. **Does UDP provide reliable delivery?** → No
11. **What is TTL and why does it exist?** → Time to Live; prevents infinite routing loops
12. **What happens when TCP's cwnd reaches ssthresh?** → Switches from slow start to congestion avoidance (linear growth)

---

*Reference: Kurose, J.F. & Ross, K.W. — Computer Networking: A Top-Down Approach, Chapter 3 (Transport Layer) and Section on ICMP in Chapter 5 (Network Layer: Control Plane).*
