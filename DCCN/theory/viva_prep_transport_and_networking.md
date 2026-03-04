# DCCN Viva Preparation – Deep Dive

---

## 1. Transport Layer – Error Detection & Control

### How Does the Transport Layer Detect Errors?

The transport layer uses **checksums** to detect bit-level errors in segments.

**Process (TCP):**

1. Sender computes a **16-bit checksum** over the TCP header + data + pseudo-header (source IP, dest IP, protocol, segment length).
2. It takes all 16-bit words, sums them using **one's complement arithmetic**, then takes the **one's complement of the sum** → this is the checksum.
3. The checksum is placed in the TCP/UDP header.
4. Receiver recomputes the checksum over the received segment (including the checksum field).
5. If the result is all 1s (`0xFFFF`), **no error detected**. If not, the segment is **corrupted**.

**UDP also has a checksum** but it is **optional in IPv4** (mandatory in IPv6).

### What Happens When an Error is Detected? (Receiver Side)

- **TCP (reliable):** The receiver **silently discards** the corrupted segment. It does **NOT send a NACK**. Instead:

  - The receiver simply doesn't send an **ACK** for that segment.
  - The sender has a **retransmission timer**. If an ACK is not received within the timeout, it **retransmits** the segment.
  - Alternatively, the receiver may send **duplicate ACKs** for the last correctly received segment, triggering **fast retransmit** (after 3 duplicate ACKs).
- **UDP (unreliable):** The corrupted datagram is **silently dropped**. No retransmission, no notification. The application must handle it if needed.

### Viva Side Questions:

**Q: Does TCP use NACK (Negative Acknowledgment)?**
A: Standard TCP does **not** use NACKs. It relies on **timeout-based retransmission** and **duplicate ACK-based fast retransmit**. However, **Selective ACK (SACK)** is a TCP option that tells the sender exactly which segments are missing.

**Q: What is the difference between Go-Back-N and Selective Repeat?**

| Feature         | Go-Back-N (GBN)                                   | Selective Repeat (SR)             |
| --------------- | ------------------------------------------------- | --------------------------------- |
| Receiver buffer | Only accepts in-order                             | Buffers out-of-order              |
| Retransmission  | Retransmits ALL from lost segment onward          | Retransmits ONLY the lost segment |
| ACK type        | Cumulative ACK                                    | Individual ACK                    |
| Window size     | Sender window ≤ 2^m - 1                          | Sender + Receiver window ≤ 2^m   |
| Efficiency      | Lower (retransmits good packets too)              | Higher                            |
| TCP uses?       | TCP is closer to SR with cumulative ACKs (hybrid) | —                                |

**Q: What is the difference between Stop-and-Wait and Sliding Window?**

- **Stop-and-Wait:** Send 1 frame → wait for ACK → send next. Very slow, utilization = 1/(1+2a) where a = propagation/transmission delay ratio.
- **Sliding Window:** Send multiple frames (window size N) without waiting. Much higher throughput.

**Q: What is flow control vs congestion control?**

|                          | Flow Control                                       | Congestion Control                                 |
| ------------------------ | -------------------------------------------------- | -------------------------------------------------- |
| **Purpose**        | Prevent sender from overwhelming**receiver** | Prevent sender from overwhelming**network**  |
| **Mechanism**      | Receiver advertises**rwnd** (receive window) | Sender maintains**cwnd** (congestion window) |
| **Where**          | End-to-end (sender ↔ receiver)                    | Sender ↔ network                                  |
| **TCP algorithms** | rwnd in TCP header                                 | Slow start, congestion avoidance, fast recovery    |

**Actual sending window = min(rwnd, cwnd)**

**Q: What is TCP 3-way handshake?**

1. Client → Server: **SYN** (seq = x)
2. Server → Client: **SYN-ACK** (seq = y, ack = x+1)
3. Client → Server: **ACK** (seq = x+1, ack = y+1)

**Q: What is the 4-way connection termination?**

1. A → B: **FIN**
2. B → A: **ACK** (B can still send data — half-close)
3. B → A: **FIN**
4. A → B: **ACK** (A enters TIME_WAIT for 2×MSL)

---

## 2. Application Layer → Transport Layer (Data Handoff)

### How Application Layer Gives Data to Transport Layer

1. Application creates data (e.g., HTTP request).
2. Application calls the **socket API** (e.g., `send()`, `write()`).
3. Data is placed into the **socket send buffer**.
4. Transport layer (TCP/UDP) takes data from the buffer:
   - **TCP:** Segments the data into MSS-sized chunks, adds TCP header (src port, dst port, seq #, ack #, flags, checksum, window size).
   - **UDP:** Wraps entire data block into a single datagram with UDP header (src port, dst port, length, checksum).
5. The segment/datagram is passed down to the **Network Layer**.

### Multiplexing and Demultiplexing

- **Multiplexing (sender):** Gathering data from multiple sockets, adding transport headers → sending down.
- **Demultiplexing (receiver):** Delivering received segments to the correct socket using port numbers.
  - **UDP demux:** uses only (dest IP, dest port) — 2-tuple.
  - **TCP demux:** uses (src IP, src port, dest IP, dest port) — 4-tuple. This is why a web server can have thousands of connections on port 80.

**Q: Why does TCP use a 4-tuple for demultiplexing?**
Because TCP is connection-oriented. Two different clients connecting to the same server port must be distinguished by their source IP and source port.

---

## 3. OSI Model vs TCP/IP Model – Exploded at Every Layer

### OSI Model (7 Layers)

| # | Layer                  | PDU              | Function                                                 | Protocols/Examples                                  | Devices               |
| - | ---------------------- | ---------------- | -------------------------------------------------------- | --------------------------------------------------- | --------------------- |
| 7 | **Application**  | Data             | User interface, resource sharing                         | HTTP, FTP, SMTP, DNS, POP3, IMAP, SNMP, Telnet, SSH | —                    |
| 6 | **Presentation** | Data             | Translation, encryption, compression                     | SSL/TLS, JPEG, MPEG, ASCII, EBCDIC                  | —                    |
| 5 | **Session**      | Data             | Session management (establish, maintain, terminate)      | NetBIOS, RPC, PPTP, SCP                             | —                    |
| 4 | **Transport**    | Segment/Datagram | End-to-end delivery, error/flow control                  | TCP, UDP, SCTP                                      | —                    |
| 3 | **Network**      | Packet           | Logical addressing, routing                              | IP, ICMP, ARP, RARP, OSPF, BGP                      | Router, L3 Switch     |
| 2 | **Data Link**    | Frame            | Physical addressing (MAC), error detection, media access | Ethernet (802.3), Wi-Fi (802.11), PPP, HDLC         | Switch, Bridge, NIC   |
| 1 | **Physical**     | Bits             | Bit transmission over physical medium                    | RS-232, RJ-45, Fiber optics, DSL, Hubs              | Hub, Repeater, Cables |

### TCP/IP Model (4 Layers)

| # | TCP/IP Layer             | Equivalent OSI | Key Protocols                     |
| - | ------------------------ | -------------- | --------------------------------- |
| 4 | **Application**    | 7 + 6 + 5      | HTTP, FTP, SMTP, DNS, SSH, Telnet |
| 3 | **Transport**      | 4              | TCP, UDP                          |
| 2 | **Internet**       | 3              | IP, ICMP, ARP, IGMP               |
| 1 | **Network Access** | 2 + 1          | Ethernet, Wi-Fi, PPP, Token Ring  |

### Key Differences

| Feature              | OSI                                | TCP/IP                         |
| -------------------- | ---------------------------------- | ------------------------------ |
| Layers               | 7                                  | 4                              |
| Developed by         | ISO                                | DARPA/DoD                      |
| Approach             | Theoretical (protocol-independent) | Practical (protocol-dependent) |
| Session/Presentation | Separate layers                    | Merged into Application        |
| Network Access       | Physical + Data Link separate      | Combined                       |
| Usage                | Reference/teaching model           | Actual Internet model          |

### Viva Side Questions:

**Q: Why was the OSI model not adopted as the Internet standard?**
A: TCP/IP was already deployed and working before OSI was finalized. OSI was seen as too complex and bureaucratic. "TCP/IP won the market, OSI won the textbook."

**Q: Where does ARP sit?**
A: ARP operates between Layer 2 and Layer 3. It resolves IP addresses to MAC addresses. In TCP/IP, it's in the Network Access layer. In OSI, it bridges Network and Data Link.

**Q: What is the difference between a segment, packet, and frame?**

- **Segment:** Transport layer PDU (TCP segment, UDP datagram)
- **Packet:** Network layer PDU (IP packet)
- **Frame:** Data Link layer PDU (Ethernet frame)
- **Bits:** Physical layer

---

## 4. Encapsulation & Decapsulation

### Encapsulation (Sender Side – Top to Bottom)

```
Application Data
       ↓ + [App header]
Transport: Segment = [TCP/UDP Header | Data]
       ↓ + [IP header]  
Network:   Packet  = [IP Header | TCP Header | Data]
       ↓ + [Frame header + trailer]
Data Link: Frame   = [Eth Header | IP Header | TCP Header | Data | FCS]
       ↓
Physical:  Bits    = 010110110100...
```

Each layer adds its own header (and sometimes trailer like FCS at Data Link).

### Decapsulation (Receiver Side – Bottom to Top)

```
Physical: Receives bits → assembles frame
Data Link: Strip frame header/trailer → extract packet, check FCS
Network:   Strip IP header → extract segment, check destination IP
Transport: Strip TCP/UDP header → extract data, verify checksum
Application: Process data
```

### Viva Side Questions:

**Q: What does the Ethernet frame trailer contain?**
A: **FCS (Frame Check Sequence)** — a 4-byte CRC-32 value for error detection at the Data Link layer.

**Q: What is the Ethernet frame structure?**| Preamble (7B) | SFD (1B) | Dest MAC (6B) | Src MAC (6B) | Type/Length (2B) | Data (46-1500B) | FCS (4B) |

- **Preamble:** 7 bytes of alternating 10101010 for clock synchronization
- **SFD (Start Frame Delimiter):** 10101011 — signals start of frame
- **Minimum data size = 46 bytes** (padded if less) — required for collision detection in CSMA/CD
- **MTU = 1500 bytes** (Maximum Transmission Unit for Ethernet)

**Q: What happens if data is less than 46 bytes?**
A: The Data Link layer **pads** the data with zeros to reach 46 bytes. This ensures minimum frame size of 64 bytes (excluding preamble/SFD) for proper collision detection.

---

## 5. Twisted Pair Cables – Use Cases

### Types of Twisted Pair

| Type                       | Shielding               | Use                                | Cost   |
| -------------------------- | ----------------------- | ---------------------------------- | ------ |
| **UTP** (Unshielded) | None                    | Most LANs, offices                 | Low    |
| **STP** (Shielded)   | Foil/braid around pairs | Industrial, high-interference      | High   |
| **FTP** (Foiled)     | Overall foil only       | Moderate interference environments | Medium |

### Categories

| Category        | Speed     | Bandwidth | Use                   |
| --------------- | --------- | --------- | --------------------- |
| Cat5            | 100 Mbps  | 100 MHz   | Legacy                |
| **Cat5e** | 1 Gbps    | 100 MHz   | Most common           |
| **Cat6**  | 1-10 Gbps | 250 MHz   | Modern LANs           |
| Cat6a           | 10 Gbps   | 500 MHz   | Data centers          |
| Cat7            | 10 Gbps   | 600 MHz   | Shielded, specialized |

### Straight-Through Cable

**Wiring:** Both ends use the **same standard** (T568A–T568A or T568B–T568B).

**Use cases — connecting UNLIKE devices:**

- PC → Switch
- PC → Hub
- Switch → Router
- Router → Switch

**Mnemonic:** Different device types = straight-through.

### Crossover Cable

**Wiring:** One end uses **T568A**, other end uses **T568B**. This swaps Tx and Rx pins.

**Pins crossed:** 1↔3, 2↔6 (for 100Mbps).

**Use cases — connecting LIKE devices:**

- PC → PC
- Switch → Switch
- Hub → Hub
- Router → Router (via Ethernet)
- Router → PC (both are DTE devices)

**Mnemonic:** Same device types = crossover.

### Viva Side Questions:

**Q: Why do we twist the wires?**
A: Twisting reduces **electromagnetic interference (EMI)** and **crosstalk** between adjacent pairs. The twists cause induced noise to cancel out (balanced signal).

**Q: What is the difference between T568A and T568B?**

| Pin | T568A        | T568B        |
| --- | ------------ | ------------ |
| 1   | White/Green  | White/Orange |
| 2   | Green        | Orange       |
| 3   | White/Orange | White/Green  |
| 4   | Blue         | Blue         |
| 5   | White/Blue   | White/Blue   |
| 6   | Orange       | Green        |
| 7   | White/Brown  | White/Brown  |
| 8   | Brown        | Brown        |

Only pairs 2 and 3 (orange and green) are swapped.

**Q: Do modern switches need crossover cables?**
A: No. Most modern switches support **Auto-MDI/MDI-X**, which automatically detects and adjusts pin configuration. Crossover cables are largely obsolete for modern equipment.

**Q: What is the maximum length of a Cat5e/Cat6 cable?**
A: **100 meters** (328 feet) for a single run without a repeater or switch.

**Q: What is RJ-45?**
A: The **8P8C** (8-position, 8-contact) connector used at the ends of twisted pair Ethernet cables. Technically "RJ-45" is a misnomer but universally used.

---

## 6. Switches – Cut-Through vs Store-and-Forward

### Store-and-Forward Switching

1. Switch receives the **entire frame**.
2. Checks the **FCS** (CRC) for errors.
3. If error → **drops the frame**.
4. If valid → looks up **destination MAC** in MAC address table → forwards out the correct port.

**Pros:** Error checking, reliable.
**Cons:** Higher latency (proportional to frame size).

### Cut-Through Switching

1. Switch reads only the first **6 bytes** of the frame (destination MAC address — which starts at byte 7 after preamble+SFD, so effectively after the first 14 bytes of the header).
2. **Immediately** starts forwarding the frame to the output port **before receiving the rest**.
3. **No error checking** (FCS hasn't arrived yet).

**Pros:** Very low, fixed latency (~12 microseconds).
**Cons:** Forwards corrupted/runt frames. Bad in noisy networks.

### Fragment-Free Switching (Modified Cut-Through)

1. Switch reads the first **64 bytes** (minimum frame size).
2. Since collisions are detected within 64 bytes, this filters out **collision fragments (runts)**.
3. Then forwards without waiting for the rest.

**Pros:** Filters runts, still faster than store-and-forward.
**Cons:** Doesn't catch all errors.

### Comparison Table

| Feature                 | Store-and-Forward | Cut-Through       | Fragment-Free  |
| ----------------------- | ----------------- | ----------------- | -------------- |
| Reads before forwarding | Entire frame      | 6B (dest MAC)     | 64B            |
| Error checking          | Full CRC          | None              | Runt filtering |
| Latency                 | High (variable)   | Low (fixed)       | Medium         |
| Forwards bad frames?    | No                | Yes               | Some           |
| Best for                | Reliable networks | Low-latency needs | Balanced       |

### Viva Side Questions:

**Q: How does a switch learn MAC addresses?**A: Through the **learning/flooding process:**

1. Frame arrives on port X with source MAC = AAA.
2. Switch records: MAC AAA → Port X in its **MAC address table** (CAM table).
3. If destination MAC is unknown → **floods** frame to all ports except source.
4. When reply comes back, it learns the other MAC too.
5. Entries have a **timeout** (default 300 seconds / 5 minutes on Cisco).

**Q: What is the difference between a switch and a hub?**

| Feature          | Hub                     | Switch                              |
| ---------------- | ----------------------- | ----------------------------------- |
| Layer            | Physical (L1)           | Data Link (L2)                      |
| Forwarding       | Broadcasts to all ports | Forwards to specific port           |
| Collision domain | One (shared)            | One per port (each port is its own) |
| Broadcast domain | One                     | One (same VLAN)                     |
| Intelligence     | None                    | MAC address table                   |
| Duplex           | Half-duplex             | Full-duplex                         |

**Q: What is a collision domain vs broadcast domain?**

- **Collision domain:** A network segment where frames can collide. Each switch port = separate collision domain. A hub = one big collision domain.
- **Broadcast domain:** A network segment where a broadcast reaches all devices. All ports on a switch (in the same VLAN) = one broadcast domain. A **router** separates broadcast domains.

---

## 7. Port Numbers

### Well-Known Ports (0–1023)

| Protocol              | Port | Transport               | Purpose                     |
| --------------------- | ---- | ----------------------- | --------------------------- |
| **FTP Data**    | 20   | TCP                     | Actual file transfer        |
| **FTP Control** | 21   | TCP                     | Commands (login, ls, cd)    |
| **SSH**         | 22   | TCP                     | Secure remote shell         |
| **Telnet**      | 23   | TCP                     | Unsecure remote shell       |
| **SMTP**        | 25   | TCP                     | Sending email               |
| **DNS**         | 53   | **UDP (and TCP)** | Name resolution             |
| **DHCP Server** | 67   | UDP                     | IP assignment (server)      |
| **DHCP Client** | 68   | UDP                     | IP assignment (client)      |
| **HTTP**        | 80   | TCP                     | Web browsing                |
| **POP3**        | 110  | TCP                     | Retrieving email            |
| **IMAP**        | 143  | TCP                     | Retrieving email (advanced) |
| **HTTPS**       | 443  | TCP                     | Secure web browsing         |

### Port Ranges

| Range        | Name              | Usage                                        |
| ------------ | ----------------- | -------------------------------------------- |
| 0–1023      | Well-known        | Assigned to standard protocols by IANA       |
| 1024–49151  | Registered        | Used by vendor applications                  |
| 49152–65535 | Dynamic/Ephemeral | Assigned by OS to client sockets temporarily |

### Viva Side Questions:

**Q: Why does FTP use two ports?**
A: FTP separates **control** (port 21 — commands like LIST, RETR) from **data** (port 20 — actual file bytes). This is called **out-of-band control**. In **active mode**, server connects FROM port 20 to client. In **passive mode**, server tells client a random high port to connect to (better for firewalls).

**Q: What is an ephemeral port?**
A: When a client opens a connection (e.g., web browser), the OS assigns a random high port (49152–65535) as the **source port**. This is ephemeral — it's temporary and released after the connection closes.

**Q: Can a port be used by both TCP and UDP simultaneously?**
A: Yes. TCP port 53 and UDP port 53 are independent. DNS uses both — UDP for normal queries, TCP for zone transfers or responses > 512 bytes.

---

## 8. DNS Uses UDP (and Sometimes TCP)

### Why DNS Primarily Uses UDP (Port 53)

1. DNS queries are **small** (typically < 512 bytes).
2. UDP has **no connection setup** overhead (no 3-way handshake) → faster.
3. DNS needs to be **fast** — it's queried before almost every internet request.
4. If a response is lost, the **DNS resolver simply retries** (application-level reliability).
5. DNS servers handle **millions of queries** — TCP would require maintaining state for each connection (expensive).

### When DNS Uses TCP (Port 53)

1. **Zone transfers** (AXFR/IXFR) — when secondary DNS servers replicate data from primary. Large data, must be reliable.
2. **Responses > 512 bytes** (or > 4096 bytes with EDNS0) — if the response is truncated (TC flag set), client retries over TCP.
3. **DNSSEC responses** — digital signatures make responses larger.

### DNS Resolution Process (Iterative)

```
Client → Local DNS Resolver → Root Server (.com?)
                             → TLD Server (.com → google.com NS?)  
                             → Authoritative Server (google.com → 142.250.x.x)
       ← IP Address returned to client
```

**Types of queries:**

- **Recursive:** Client asks resolver, resolver does ALL the work and returns final answer.
- **Iterative:** Resolver asks root, root says "ask TLD," resolver asks TLD, TLD says "ask auth NS," resolver asks auth NS.

### Viva Side Questions:

**Q: What is DNS caching and TTL?**
A: DNS resolvers **cache** responses to avoid repeated lookups. Each DNS record has a **TTL (Time To Live)** — the number of seconds the record can be cached. After TTL expires, the resolver must query again.

**Q: What is the difference between authoritative and non-authoritative answers?**

- **Authoritative:** Response comes directly from the DNS server that owns the zone file for that domain.
- **Non-authoritative:** Response comes from a cache (resolver has seen this before).

**Q: What are the 13 root servers?**
A: Named A through M (a.root-servers.net through m.root-servers.net). They use **anycast** — each "server" is actually hundreds of distributed instances worldwide.

---

## 9. Push vs Pull Protocols – SMTP and POP3

### SMTP (Simple Mail Transfer Protocol) — PUSH

- **Port:** 25 (unencrypted), 587 (submission with STARTTLS), 465 (SMTPS)
- **Type:** **PUSH protocol** — sender **pushes** email to the receiver's mail server.
- **Transport:** TCP (reliable delivery needed).
- **Direction:** Client → Server, Server → Server.

**SMTP Flow:**

```
Sender's MUA → Sender's Mail Server (SMTP PUSH)
                    ↓ SMTP PUSH
              Receiver's Mail Server (stores in mailbox)
                    ↓ POP3/IMAP PULL
              Receiver's MUA
```

**SMTP Commands:**

| Command    | Purpose                                             |
| ---------- | --------------------------------------------------- |
| HELO/EHLO  | Identify sender to server                           |
| MAIL FROM: | Specify sender address                              |
| RCPT TO:   | Specify recipient                                   |
| DATA       | Begin message body (end with `.` on its own line) |
| QUIT       | Close connection                                    |

**SMTP Response Codes:**

| Code | Meaning               |
| ---- | --------------------- |
| 220  | Server ready          |
| 250  | OK (action completed) |
| 354  | Start mail input      |
| 550  | Mailbox not found     |

### POP3 (Post Office Protocol v3) — PULL

- **Port:** 110 (unencrypted), 995 (POP3S with SSL)
- **Type:** **PULL protocol** — client **pulls** (downloads) email from the server.
- **Transport:** TCP.
- **Behavior:** Downloads messages and usually **deletes** them from server (download-and-delete mode). Can also be configured to keep copies.

**POP3 Phases:**

1. **Authorization:** USER + PASS commands.
2. **Transaction:** LIST, RETR (retrieve), DELE (mark for deletion).
3. **Update:** After QUIT, server actually deletes marked messages.

**POP3 Commands:**

| Command | Purpose                      |
| ------- | ---------------------------- |
| USER    | Username                     |
| PASS    | Password                     |
| STAT    | Mailbox status (count, size) |
| LIST    | List messages                |
| RETR n  | Retrieve message n           |
| DELE n  | Mark message n for deletion  |
| QUIT    | End session, apply deletions |

**POP3 Responses:** `+OK` (success) or `-ERR` (failure).

### POP3 vs IMAP

| Feature           | POP3                         | IMAP                              |
| ----------------- | ---------------------------- | --------------------------------- |
| Port              | 110 / 995                    | 143 / 993                         |
| Model             | Download & delete            | Keep on server                    |
| Multi-device      | Poor (mail on one device)    | Excellent (synced everywhere)     |
| Server storage    | Low (deleted after download) | High (always on server)           |
| Folder management | No                           | Yes (server-side folders)         |
| Offline access    | Full (downloaded)            | Limited (headers only by default) |
| Bandwidth         | High initial, low later      | Low initial, on-demand            |

### Why SMTP is Push and POP3 is Pull

- **SMTP is push** because the **sender initiates** — the sender's MUA connects to the server and pushes the email. The receiver doesn't ask for it.
- **POP3 is pull** because the **receiver initiates** — the receiver's MUA connects to the server and pulls/downloads emails on demand (e.g., "Check Mail" button).

### Viva Side Questions:

**Q: Can SMTP pull emails?**
A: No. SMTP is strictly a **push** protocol. It can only send/relay messages. To retrieve emails, you need POP3 or IMAP.

**Q: Why does SMTP use TCP, not UDP?**
A: Email must be delivered **reliably and completely**. TCP provides guaranteed delivery, ordered data, and error recovery. Losing parts of an email is unacceptable.

**Q: What is the difference between SMTP submission port 587 and port 25?**

- **Port 25:** Original SMTP, used for server-to-server relay. Often blocked by ISPs for clients (to prevent spam).
- **Port 587:** Submission port — used by email clients (MUA) to submit outgoing mail. Requires authentication (STARTTLS).

**Q: Does the sender's mail server use SMTP to send to the receiver's mail server?**A: Yes. SMTP is used in **two** hops:

1. Sender's client → sender's server (submission, port 587).
2. Sender's server → receiver's server (relay, port 25).

---

## 10. Quick-Fire Viva Questions

| Question                                      | Answer                                                                         |
| --------------------------------------------- | ------------------------------------------------------------------------------ |
| What layer does a router operate at?          | Layer 3 (Network)                                                              |
| What layer does a switch operate at?          | Layer 2 (Data Link)                                                            |
| What layer does a hub operate at?             | Layer 1 (Physical)                                                             |
| What is MAC address length?                   | 48 bits (6 bytes), written as XX:XX:XX:XX:XX:XX                                |
| What is IPv4 address length?                  | 32 bits (4 bytes)                                                              |
| What is IPv6 address length?                  | 128 bits (16 bytes)                                                            |
| TCP is connection-oriented or connectionless? | Connection-oriented                                                            |
| UDP is connection-oriented or connectionless? | Connectionless                                                                 |
| Which is faster, TCP or UDP?                  | UDP (no overhead)                                                              |
| What protocol does `ping` use?              | ICMP (Internet Control Message Protocol)                                       |
| What protocol does `traceroute` use?        | ICMP (or UDP on Linux)                                                         |
| What does ARP do?                             | Resolves IP address → MAC address                                             |
| What does RARP do?                            | Resolves MAC address → IP address (obsolete, replaced by DHCP)                |
| What is NAT?                                  | Network Address Translation — maps private IPs to a public IP                 |
| What is a default gateway?                    | The router IP that a host sends packets to for destinations outside its subnet |
| What is subnet mask used for?                 | To determine which part of IP is network vs host address                       |
| What does DHCP provide?                       | IP address, subnet mask, default gateway, DNS server                           |
| Is ARP Layer 2 or Layer 3?                    | It bridges both — uses IP (L3) to find MAC (L2)                               |
| What is full-duplex vs half-duplex?           | Full: simultaneous send/receive. Half: one direction at a time                 |
| What is CSMA/CD?                              | Carrier Sense Multiple Access/Collision Detection — Ethernet access method    |
| Where is CSMA/CD used?                        | Wired Ethernet (hubs). Not needed with switches (full-duplex, no collisions)   |
| What is CSMA/CA?                              | Collision Avoidance — used in Wi-Fi (802.11)                                  |
