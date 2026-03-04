# DNS Lab – Complete Linux Guide

## Table of Contents

1. [Introduction to DNS](#introduction-to-dns)
2. [Task 1: Get DNS Record](#task-1-get-dns-record)
3. [Task 2: Get Your System Address](#task-2-get-your-system-address)
4. [Task 3: Tracing DNS with Wireshark](#task-3-tracing-dns-with-wireshark)
5. [Linux vs Windows Command Comparison](#linux-vs-windows-command-comparison)

---

## Introduction to DNS

The **Domain Name System (DNS)** is often called the "phonebook of the Internet." Humans access websites using domain names like `www.google.com`, but computers communicate using **IP addresses** (e.g., `142.250.185.4`). DNS translates human-readable domain names into machine-readable IP addresses.

### Why DNS Matters

- Without DNS, you would have to memorize IP addresses for every website.
- DNS is a **hierarchical, distributed database** — no single server holds all records.
- Your computer first asks a **local DNS resolver** (usually provided by your ISP or configured manually), which then queries the DNS hierarchy on your behalf.

### DNS Record Types

| Type            | Purpose                                     | Example                                        |
| --------------- | ------------------------------------------- | ---------------------------------------------- |
| **A**     | Maps hostname → IPv4 address               | `www.google.com → 142.250.185.4`            |
| **AAAA**  | Maps hostname → IPv6 address               | `www.google.com → 2607:f8b0:...`            |
| **NS**    | Nameserver responsible for a domain         | `google.com → ns1.google.com`               |
| **MX**    | Mail exchange server for a domain           | `google.com → smtp.google.com`              |
| **CNAME** | Canonical name (alias) for another domain   | `mail.google.com → googlemail.l.google.com` |
| **SOA**   | Start of Authority — admin info for a zone | Serial number, refresh intervals               |
| **TXT**   | Arbitrary text (SPF, DKIM, verification)    | `v=spf1 include:_spf.google.com`             |

---

## Task 1: Get DNS Record

### Tool: `nslookup` / `dig` / `host`

On Linux, you have **three** main DNS lookup tools. Windows only ships with `nslookup`.

| Tool         | Available On    | Detail Level  | Recommended                    |
| ------------ | --------------- | ------------- | ------------------------------ |
| `nslookup` | Windows + Linux | Basic         | For cross-platform familiarity |
| `dig`      | Linux (+ macOS) | Very detailed | **Yes — most powerful** |
| `host`     | Linux (+ macOS) | Moderate      | Quick lookups                  |

### Installing the Tools (if not already present)

```bash
# On Debian/Ubuntu-based systems
sudo apt update && sudo apt install dnsutils -y

# On Fedora/RHEL-based systems
sudo dnf install bind-utils -y

# On Arch-based systems
sudo pacman -S bind-tools
```

> **Why install `dnsutils` / `bind-utils`?**
> These packages provide `nslookup`, `dig`, and `host`. On minimal Linux installations, they may not be pre-installed.

---

### Step 1: Basic DNS Lookup

#### Windows Command

```cmd
nslookup www.google.com
```

#### Linux Equivalent Commands

**Option A — `nslookup` (same as Windows):**

```bash
nslookup www.google.com
```

**Option B — `dig` (Linux-preferred, more detailed):**

```bash
dig www.google.com
```

**Option C — `host` (quick and clean):**

```bash
host www.google.com
```

#### What Each Command Does

- Sends a DNS **A record** query (hostname → IPv4) to your configured DNS resolver.
- The resolver looks up the IP address(es) for `www.google.com`.
- Returns the resolved IP address(es) and the DNS server that answered.

#### Expected Output (Linux — `nslookup`)

```
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   www.google.com
Address: 142.250.185.4
Name:   www.google.com
Address: 2607:f8b0:4004:800::2004
```

#### Expected Output (Linux — `dig`)

```
; <<>> DiG 9.18.x <<>> www.google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;www.google.com.                IN      A

;; ANSWER SECTION:
www.google.com.         300     IN      A       142.250.185.4

;; Query time: 12 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Sat Feb 21 10:00:00 PKT 2026
;; MSG SIZE  rcvd: 59
```

#### Key Observations

| Field                        | Meaning                                                                     |
| ---------------------------- | --------------------------------------------------------------------------- |
| `Server: 127.0.0.53`       | Your local DNS resolver (on Linux,`systemd-resolved` listens here)        |
| `Non-authoritative answer` | The answer came from cache, not directly from Google's authoritative DNS    |
| `Address: 142.250.185.4`   | The resolved IPv4 address                                                   |
| `Query time: 12 msec`      | How long the lookup took (only shown in `dig`)                            |
| `flags: qr rd ra`          | `qr`=query response, `rd`=recursion desired, `ra`=recursion available |

> **Why `127.0.0.53` on Linux?**
> Modern Ubuntu/Debian systems use `systemd-resolved` as a local caching DNS stub resolver. It listens on `127.0.0.53` and forwards queries to your actual DNS server. Windows doesn't have this — it directly contacts the configured DNS server.

---

### Step 2: Query NS (Nameserver) Records

#### Windows Command

```cmd
nslookup -type=NS www.google.com
```

#### Linux Equivalent Commands

```bash
# nslookup (same as Windows but use dash or hyphen)
nslookup -type=NS www.google.com

# dig (preferred on Linux)
dig NS www.google.com

# host
host -t NS google.com
```

#### What This Does

- Queries for **NS records** — these tell you which DNS servers are **authoritative** (officially responsible) for the domain.
- Authoritative nameservers hold the actual, original DNS records for a domain.

#### Expected Output (`dig NS google.com`)

```
;; ANSWER SECTION:
google.com.     21600   IN      NS      ns1.google.com.
google.com.     21600   IN      NS      ns2.google.com.
google.com.     21600   IN      NS      ns3.google.com.
google.com.     21600   IN      NS      ns4.google.com.
```

#### Key Observations

- Google uses **4 nameservers** (`ns1` through `ns4`) for redundancy.
- The TTL `21600` means this record is cached for 6 hours (21600 seconds).
- These are the servers that hold the **authoritative** (official) DNS records for `google.com`.

> **Application:** If you're setting up a domain, you must configure NS records at your registrar to point to your DNS provider's nameservers.

---

### Step 3: Query a Specific DNS Server

#### Windows Command

```cmd
nslookup www.hotmail.com 8.8.8.8
```

#### Linux Equivalent Commands

```bash
# nslookup — same syntax as Windows
nslookup www.hotmail.com 8.8.8.8

# dig — use @ to specify DNS server
dig @8.8.8.8 www.hotmail.com

# host — server specified at the end
host www.hotmail.com 8.8.8.8
```

#### What This Does

- Instead of using your default DNS resolver, this sends the query **directly** to Google's public DNS server (`8.8.8.8`).
- Useful for:
  - **Troubleshooting** — check if your local DNS is returning stns lnsdnjsadnsajkfnsafale/wrong results
  - **Comparing** responses from different DNS providers
  - **Bypassing** potentially censored or filtered DNS

#### Common Public DNS Servers

| Provider   | IPv4 Primary       | IPv4 Secondary      | Why Use It                         |
| ---------- | ------------------ | ------------------- | ---------------------------------- |
| Google     | `8.8.8.8`        | `8.8.4.4`         | Fast, reliable, globally available |
| Cloudflare | `1.1.1.1`        | `1.0.0.1`         | Privacy-focused, fastest           |
| OpenDNS    | `208.67.222.222` | `208.67.220.220`  | Family/security filtering          |
| Quad9      | `9.9.9.9`        | `149.112.112.112` | Blocks malicious domains           |

#### Example: Compare Results from Different DNS Servers

```bash
# Query your default DNS
dig www.hotmail.com

# Query Google DNS
dig @8.8.8.8 www.hotmail.com

# Query Cloudflare DNS
dig @1.1.1.1 www.hotmail.com
```

---

## Task 2: Get Your System Address

### Tool: `ip` / `ifconfig` / `nmcli` (Linux) vs `ipconfig` (Windows)

> **Critical Difference:** Windows uses `ipconfig`. Linux uses `ip`, `ifconfig`, or `nmcli`. The commands are **completely different** — don't confuse them!

---

### Step 1: Show Full Network Configuration

#### Windows Command

```cmd
ipconfig /all
```

#### Linux Equivalent Commands

**Option A — `ip` (modern, recommended):**

```bash
# Show all interface addresses
ip addr show

# Short form
ip a
```

**Option B — `ifconfig` (legacy, still widely used):**

```bash
ifconfig -a
```

**Option C — `nmcli` (NetworkManager — for desktop Linux):**

```bash
nmcli device show
```

**Option D — Get DNS server info specifically:**

```bash
# systemd-resolved systems (Ubuntu 18.04+)
resolvectl status

# Or check resolv.conf
cat /etc/resolv.conf

# Or using nmcli
nmcli dev show | grep DNS
```

#### Why Multiple Commands on Linux?

| Command                  | Purpose                                 | Installed By Default?  |
| ------------------------ | --------------------------------------- | ---------------------- |
| `ip addr`              | Show IP addresses, interfaces, MAC      | Yes (iproute2)         |
| `ifconfig`             | Legacy equivalent of `ip addr`        | Sometimes (net-tools)  |
| `nmcli`                | NetworkManager CLI (Wi-Fi, connections) | Yes on desktop distros |
| `resolvectl`           | DNS resolver status (systemd)           | Yes on systemd distros |
| `cat /etc/resolv.conf` | Raw DNS configuration file              | Always                 |

> **Why so many?** Linux separates concerns — networking, DNS, and connection management are handled by different subsystems. Windows bundles everything into `ipconfig`.

#### Key Information to Note

```bash
# Get your IP address
ip -4 addr show | grep inet

# Get your default gateway
ip route show default

# Get your DNS servers
resolvectl status | grep "DNS Servers"
# OR
cat /etc/resolv.conf | grep nameserver

# Get your MAC address
ip link show | grep ether
```

#### Expected Output (`ip addr show`)

```
2: wlp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether aa:bb:cc:dd:ee:ff brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.105/24 brd 192.168.1.255 scope global dynamic wlp3s0
    inet6 fe80::abcd:1234:5678:9abc/64 scope link
```

| Field                     | Meaning                 | Windows Equivalent             |
| ------------------------- | ----------------------- | ------------------------------ |
| `wlp3s0`                | Interface name (Wi-Fi)  | "Wireless LAN adapter Wi-Fi"   |
| `link/ether aa:bb:...`  | MAC address             | "Physical Address"             |
| `inet 192.168.1.105/24` | IPv4 address + subnet   | "IPv4 Address" + "Subnet Mask" |
| `inet6 fe80::...`       | IPv6 link-local address | "Link-local IPv6 Address"      |

---

### Step 2: Display DNS Cache

#### Windows Command

```cmd
ipconfig /displaydns
```

#### Linux Equivalent Commands

```bash
# If using systemd-resolved (Ubuntu, Fedora, etc.)
resolvectl statistics

# To see cached entries (requires debug mode or nscd)
sudo systemd-resolve --statistics   # older syntax

# If using nscd (Name Service Cache Daemon)
sudo nscd -g
```

#### Why This Is Different on Linux

| Aspect           | Windows                             | Linux                                          |
| ---------------- | ----------------------------------- | ---------------------------------------------- |
| DNS Caching      | Built-in Windows DNS Client service | `systemd-resolved` or `nscd` (optional)    |
| View Cache       | `ipconfig /displaydns`            | `resolvectl statistics` (limited)            |
| Cache Visibility | Shows all cached records with TTL   | Only shows statistics (hits/misses) by default |

> **Important:** Linux's `systemd-resolved` doesn't easily expose individual cached DNS entries like Windows does. You can see **statistics** (cache size, hits, misses) but not the actual cached domains. This is a privacy/security design choice.

#### Workaround: Monitor DNS Queries in Real-Time

```bash
# Watch DNS queries as they happen (requires root)
sudo tcpdump -i any port 53 -l

# Or use journalctl to see resolved queries
sudo journalctl -u systemd-resolved -f
```

---

### Step 3: Flush DNS Cache

#### Windows Command

```cmd
ipconfig /flushdns
```

#### Linux Equivalent Commands

```bash
# systemd-resolved (Ubuntu 18.04+, Fedora, etc.)
sudo resolvectl flush-caches
# OR (older syntax)
sudo systemd-resolve --flush-caches

# If using nscd
sudo systemctl restart nscd

# If using dnsmasq (some distros)
sudo systemctl restart dnsmasq

# Verify cache was flushed
resolvectl statistics
```

#### What Flushing DNS Cache Does

- **Clears all stored DNS records** from your system's local cache.
- Forces your computer to make **fresh DNS queries** for every domain.
- Useful when:
  - A website changed its IP address and you're still reaching the old one.
  - You changed DNS server settings and want immediate effect.
  - You're **debugging DNS** and want to start clean.
  - A website was previously unreachable and DNS cached the failure.

#### Verification After Flushing

```bash
# Check that cache size is 0
resolvectl statistics
```

Expected output after flush:

```
DNSSEC supported by current servers: no

Transactions
Current Transactions: 0
  Total Transactions: 125

Cache
  Current Cache Size: 0        <-- This should be 0
          Cache Hits: 50
        Cache Misses: 75

...
```

---

## Task 3: Tracing DNS with Wireshark

### Prerequisites on Linux

```bash
# Install Wireshark
sudo apt install wireshark -y        # Debian/Ubuntu
sudo dnf install wireshark -y        # Fedora
sudo pacman -S wireshark-qt -y       # Arch

# Allow non-root users to capture packets
sudo usermod -aG wireshark $USER

# IMPORTANT: Log out and log back in for group changes to take effect
# Or run: newgrp wireshark
```

> **Windows vs Linux:** On Windows, Wireshark installs Npcap for packet capture. On Linux, it uses the native **libpcap** library and needs elevated privileges or group membership.

---

### Step 1: Prepare for Capture

```bash
# 1. Flush DNS cache
sudo resolvectl flush-caches

# 2. Clear browser cache
#    In Firefox: Ctrl+Shift+Delete → select "Cache" → Clear
#    In Chrome: Ctrl+Shift+Delete → select "Cached images and files" → Clear

# 3. Get your IP address (note this for the Wireshark filter)
ip -4 addr show | grep "inet " | grep -v 127.0.0.1
#    Example output: inet 192.168.1.105/24 ...
#    Your IP is: 192.168.1.105

# 4. Open Wireshark
wireshark &
```

### Step 2: Configure Wireshark Filter

In the Wireshark **display filter** bar, enter:

```
ip.addr == 192.168.1.105
```

*(Replace `192.168.1.105` with YOUR IP address from step 3)*

> **Better filter for DNS-specific analysis:**
>
> ```
> dns
> ```
>
> or combine both:
>
> ```
> ip.addr == 192.168.1.105 && dns
> ```

### Step 3: Capture and Analyse

1. **Start** packet capture (click the blue shark fin button or press `Ctrl+E`).
2. Open your browser and visit: **http://www.ietf.org**
3. **Stop** capture (click the red square or `Ctrl+E` again).
4. Apply the `dns` filter to isolate DNS packets.

### Step 4: Answer the Analysis Questions

#### Q1: Are DNS messages sent over UDP or TCP?

**How to check:** Look at the **Protocol** column in Wireshark for DNS packets.

**Answer:** DNS query and response messages are sent over **UDP** (User Datagram Protocol).

| Protocol | When Used for DNS                                                                     |
| -------- | ------------------------------------------------------------------------------------- |
| UDP      | Default — all standard queries (port 53)                                             |
| TCP      | Only when response exceeds 512 bytes, zone transfers (AXFR), or DNS-over-TCP fallback |

> DNS uses UDP because queries and responses are **small** and the overhead of TCP's three-way handshake would be unnecessary. UDP is faster since it's connectionless (no SYN/ACK).

---

#### Q2: Destination port for query? Source port for response?

**How to check:** Click on a DNS query packet → expand **User Datagram Protocol** section.

**Answer:**

- DNS Query: **Destination port = 53** (the well-known DNS port)
- DNS Response: **Source port = 53** (the server responds from port 53)

The client uses a random **ephemeral port** (e.g., 49152–65535) as source, and the server's response goes back to that same ephemeral port.

```
Query:    Client:54321 → Server:53
Response: Server:53    → Client:54321
```

---

#### Q3: What IP is the DNS query sent to? Is it the same as your local DNS?

**How to check:**

- In Wireshark: look at the **Destination** column of the DNS query packet.
- In terminal: run `cat /etc/resolv.conf` or `resolvectl status`.

**Answer:** The DNS query is sent to your configured DNS server. On Linux with `systemd-resolved`, the query first goes to `127.0.0.53` (the local stub resolver), which then forwards it to the actual upstream DNS server.

```bash
# To see the actual upstream DNS server
resolvectl status | grep "DNS Servers"
```

In Wireshark, you may see traffic to `127.0.0.53` or directly to your upstream DNS (e.g., `192.168.1.1` or `8.8.8.8` depending on configuration).

> **Windows difference:** Windows sends DNS queries directly to the configured DNS server (no local stub resolver by default).

---

#### Q4: What type of DNS query? Does it contain answers?

**How to check:** Click on DNS query packet → expand **Domain Name System (query)** → look at **Queries** section.

**Answer:**

- **Type:** `A` (Address record — requesting IPv4 address for `www.ietf.org`)
- **Answers:** The **query** message contains **0 answers**. Only the **response** contains answers. This is how DNS works — the client asks, the server answers.

```
Queries
    www.ietf.org: type A, class IN
        Name: www.ietf.org
        Type: A (Host Address) (1)
        Class: IN (0x0001)
```

---

#### Q5: How many answers in the DNS response?

**How to check:** Click on the DNS **response** packet → expand **Answers** section.

**Answer:** The response may contain **multiple answers** (the exact number depends on the current DNS configuration of ietf.org). Typically you'll see:

- **CNAME record(s):** `www.ietf.org` may be an alias (CNAME) pointing to another hostname (e.g., a CDN like `www.ietf.org.cdn.cloudflare.net`).
- **A record(s):** The final IPv4 address(es) of the server.

Example:

```
Answers:
  www.ietf.org: type CNAME, class IN, cname www.ietf.org.cdn.cloudflare.net
  www.ietf.org.cdn.cloudflare.net: type A, class IN, addr 104.16.44.99
  www.ietf.org.cdn.cloudflare.net: type A, class IN, addr 104.16.45.99
```

---

#### Q6: Does the TCP SYN destination match a DNS response IP?

**How to check:**

1. Find the first **TCP SYN** packet after the DNS response (filter: `tcp.flags.syn == 1`).
2. Check its **Destination IP**.
3. Compare with the IP addresses in the DNS response's **Answer** section.

**Answer:** **Yes.** The TCP SYN packet's destination IP matches one of the A record IP addresses from the DNS response. This confirms the workflow:

```
1. Browser asks DNS: "What is the IP of www.ietf.org?"
2. DNS responds: "It's 104.16.44.99"
3. Browser opens TCP connection (SYN) to 104.16.44.99:80
4. HTTP request is sent over this TCP connection
```

---

## Linux vs Windows Command Comparison

### Complete Reference Table

| Task                                | Windows Command              | Linux Command (Recommended)      | Linux Alternative               |
| ----------------------------------- | ---------------------------- | -------------------------------- | ------------------------------- |
| **DNS lookup**                | `nslookup www.google.com`  | `dig www.google.com`           | `nslookup www.google.com`     |
| **NS record query**           | `nslookup -type=NS domain` | `dig NS domain`                | `nslookup -type=NS domain`    |
| **Query specific DNS server** | `nslookup domain 8.8.8.8`  | `dig @8.8.8.8 domain`          | `nslookup domain 8.8.8.8`     |
| **MX record query**           | `nslookup -type=MX domain` | `dig MX domain`                | `host -t MX domain`           |
| **Show all network info**     | `ipconfig /all`            | `ip addr show`                 | `ifconfig -a`                 |
| **Show IP address only**      | `ipconfig`                 | `ip -4 addr show`              | `hostname -I`                 |
| **Show DNS servers**          | `ipconfig /all` (find DNS) | `resolvectl status`            | `cat /etc/resolv.conf`        |
| **Show default gateway**      | `ipconfig /all`            | `ip route show default`        | `route -n`                    |
| **Show MAC address**          | `ipconfig /all`            | `ip link show`                 | `ifconfig`                    |
| **Display DNS cache**         | `ipconfig /displaydns`     | `resolvectl statistics`        | `sudo nscd -g`                |
| **Flush DNS cache**           | `ipconfig /flushdns`       | `sudo resolvectl flush-caches` | `sudo systemctl restart nscd` |
| **Trace route**               | `tracert domain`           | `traceroute domain`            | `mtr domain`                  |
| **Ping**                      | `ping domain`              | `ping -c 4 domain`             | same                            |
| **ARP table**                 | `arp -a`                   | `ip neigh show`                | `arp -a`                      |
| **Packet capture**            | Wireshark (Npcap)            | Wireshark (libpcap) /`tcpdump` | `tshark` (CLI Wireshark)      |

### Key Differences Explained

#### 1. `ipconfig` vs `ip` / `ifconfig`

| Aspect       | Windows `ipconfig`       | Linux `ip addr`                     |
| ------------ | -------------------------- | ------------------------------------- |
| Package      | Built-in                   | `iproute2` (built-in)               |
| Scope        | IP + DNS + DHCP all-in-one | Only IP/interface info                |
| DNS info     | Included in output         | Separate command (`resolvectl`)     |
| Flushing DNS | `ipconfig /flushdns`     | `resolvectl flush-caches`           |
| Renew DHCP   | `ipconfig /renew`        | `sudo dhclient -r && sudo dhclient` |

> **Why different?** Linux follows the **Unix philosophy** — each tool does one thing well. Windows prefers consolidated tools.

#### 2. `nslookup` vs `dig`

| Aspect           | `nslookup`               | `dig`                            |
| ---------------- | -------------------------- | ---------------------------------- |
| Available on     | Windows + Linux            | Linux + macOS                      |
| Output detail    | Basic                      | Very detailed (flags, TTL, timing) |
| Scriptability    | Harder to parse            | Easy to parse (`+short` flag)    |
| Deprecated?      | Considered legacy on Linux | Preferred on Linux                 |
| Interactive mode | Yes                        | No                                 |

```bash
# dig with +short for clean output (no Windows equivalent)
dig +short www.google.com
# Output: 142.250.185.4

# dig with trace (shows full DNS resolution path)
dig +trace www.google.com
# Shows: root → .com → google.com → www.google.com
```

#### 3. DNS Cache Architecture

```
WINDOWS:
┌──────────┐     ┌─────────────────┐     ┌────────────┐
│ Browser  │────→│ Windows DNS     │────→│ ISP DNS    │
│          │     │ Client Service  │     │ Server     │
└──────────┘     │ (caches locally)│     └────────────┘
                 └─────────────────┘

LINUX (with systemd-resolved):
┌──────────┐     ┌─────────────────┐     ┌────────────┐
│ Browser  │────→│ systemd-resolved│────→│ ISP DNS    │
│          │     │ (127.0.0.53)    │     │ Server     │
└──────────┘     │ (caches locally)│     └────────────┘
                 └─────────────────┘
```

Both architectures serve the same purpose — cache DNS responses locally to speed up future lookups. The difference is in implementation and visibility.

---

## Quick Command Cheat Sheet for This Lab

```bash
# ============ TASK 1 ============
# Basic DNS lookup
dig www.google.com

# NS record query
dig NS google.com

# Query through Google DNS
dig @8.8.8.8 www.hotmail.com

# ============ TASK 2 ============
# Show network info
ip addr show

# Show DNS servers
resolvectl status

# Show DNS cache stats
resolvectl statistics

# Flush DNS cache
sudo resolvectl flush-caches

# ============ TASK 3 ============
# Get your IP for Wireshark filter
ip -4 addr show | grep "inet " | grep -v 127.0.0.1

# Flush DNS before capture
sudo resolvectl flush-caches

# Open Wireshark
wireshark &

# Alternative: CLI packet capture for DNS
sudo tcpdump -i any port 53 -vv
```

---

## Troubleshooting

| Problem                                           | Solution                                                                               |
| ------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `dig: command not found`                        | `sudo apt install dnsutils`                                                          |
| `resolvectl: command not found`                 | Your distro may not use systemd-resolved. Try `cat /etc/resolv.conf`                 |
| Wireshark shows no packets                        | Run with `sudo wireshark` or add user to `wireshark` group                         |
| DNS queries go to `127.0.0.53`                  | Normal on Ubuntu — this is the systemd-resolved stub                                  |
| `nslookup` gives different results than `dig` | They may use different resolver libraries;`dig` is more reliable                     |
| Can't flush DNS cache                             | Check which caching service you use:`systemctl status systemd-resolved nscd dnsmasq` |

---

*Lab prepared for Linux users — DCCN Spring 2026*
