# IPConfig Lab — Windows & Linux

## Table of Contents

1. [Step 1: ipconfig /all](#step-1-ipconfig-all)
2. [Step 2: ipconfig /displaydns](#step-2-ipconfig-displaydns)
3. [Step 3: ipconfig /flushdns](#step-3-ipconfig-flushdns)
4. [Command Mapping Summary](#command-mapping-summary)

---

## Step 1: `ipconfig /all`

### Windows Command

```cmd
ipconfig /all
```

### Linux Equivalent

```bash
ip addr show
```

### Observations (Linux Output)

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever

2: enp0s31f6: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether e4:b9:7a:6c:54:4e brd ff:ff:ff:ff:ff:ff

3: wlp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 98:3b:8f:04:b2:5d brd ff:ff:ff:ff:ff:ff
    inet 10.135.88.78/22 brd 10.135.91.255 scope global dynamic noprefixroute wlp2s0
       valid_lft 3490sec preferred_lft 3490sec
    inet6 fe80::b272:bf75:67f3:4cc9/64 scope link noprefixroute
       valid_lft forever preferred_lft forever

4: br-842c7a429ca2: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 62:dc:44:eb:7b:a0 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.1/16 brd 172.18.255.255 scope global br-842c7a429ca2
       valid_lft forever preferred_lft forever

5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 82:21:ed:e7:d2:ab brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
```

### Analysis

| Interface | Type | MAC Address | IPv4 Address | State | Notes |
|---|---|---|---|---|---|
| **lo** | Loopback (localhost) | `00:00:00:00:00:00` | `127.0.0.1/8` | UP | Used for localhost communication (`127.0.0.1`), always active |
| **enp0s31f6** | Ethernet (Wired) | `e4:b9:7a:6c:54:4e` | — | **DOWN** | No cable connected |
| **wlp2s0** | Wi-Fi (Wireless) | `98:3b:8f:04:b2:5d` | `10.135.88.78/22` | **UP** | Active connection, DHCP lease ~58 min |
| **br-842c7a429ca2** | Docker Bridge | `62:dc:44:eb:7b:a0` | `172.18.0.1/16` | DOWN | Custom Docker network |
| **docker0** | Docker Bridge | `82:21:ed:e7:d2:ab` | `172.17.0.1/16` | DOWN | Default Docker bridge |

### Windows vs Linux Comparison

| Information | Windows (`ipconfig /all`) | Linux (`ip addr show`) |
|---|---|---|
| Host Name | Shown | Not shown (use `hostname`) |
| DNS Suffix | Shown | Not shown (check `/etc/resolv.conf`) |
| Adapter Description | Human-readable name | Kernel-assigned name (e.g., `wlp2s0`) |
| Physical Address (MAC) | `E4-B9-7A-6C-54-4E` | `e4:b9:7a:6c:54:4e` (colon-separated) |
| DHCP Enabled | Explicitly shown | Indicated by `dynamic` keyword |
| IPv4 Address | Shown separately | Shown with CIDR notation (`/22`) |
| Subnet Mask | `255.255.252.0` | Expressed as CIDR prefix (`/22`) |
| Default Gateway | Shown | Not shown (use `ip route show`) |
| DNS Servers | Shown | Not shown (use `resolvectl status`) |

### Key Observations

1. **Active interface**: Only `wlp2s0` (Wi-Fi) is active with IP `10.135.88.78`
2. **Subnet**: `/22` = `255.255.252.0` — this means **1022 usable hosts** in the network
3. **Network range**: `10.135.88.0` to `10.135.91.255`
4. **Broadcast address**: `10.135.91.255`
5. **IPv6 link-local**: `fe80::b272:bf75:67f3:4cc9/64` — auto-configured, always present
6. **Ethernet is down**: `NO-CARRIER` means no physical cable is plugged in
7. **Docker interfaces**: Present but inactive (no containers running)

---

## Step 2: `ipconfig /displaydns`

### Windows Command

```cmd
ipconfig /displaydns
```

### Linux Equivalent

```bash
sudo resolvectl statistics    # Shows DNS cache statistics
resolvectl status              # Shows DNS server configuration
cat /etc/resolv.conf           # Shows resolver configuration file
```

### Observations (Linux Output)

#### DNS Cache Statistics (`sudo resolvectl statistics`)

```
Transactions
                   Current Transactions:    0
                     Total Transactions: 4527

Cache
                     Current Cache Size:   17
                             Cache Hits:  648
                           Cache Misses: 3659

Failure Transactions
                         Total Timeouts:   13
     Total Timeouts (Stale Data Served):    0
                Total Failure Responses:    3
Total Failure Responses (Stale Data Served):    0

DNSSEC Verdicts
                                 Secure:    0
                               Insecure:    0
                                  Bogus:    0
                          Indeterminate:    0
```

#### DNS Server Configuration (`resolvectl status`)

```
Global
         Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
  resolv.conf mode: stub

Link 3 (wlp2s0)
    Current Scopes: DNS
         Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 172.16.17.9
       DNS Servers: 172.16.17.9 8.8.8.8 10.100.100.51 172.16.17.32
        DNS Domain: cuilahore.edu.pk
```

#### Resolver Config (`/etc/resolv.conf`)

```
nameserver 127.0.0.53
options edns0 trust-ad
search cuilahore.edu.pk
```

### Analysis

| Metric | Value | Meaning |
|---|---|---|
| Cache Size | **17** | 17 DNS records currently cached |
| Cache Hits | **648** | 648 queries answered from cache (fast) |
| Cache Misses | **3659** | 3659 queries required external lookup |
| Hit Rate | **~15%** | Most queries are fresh lookups |
| Timeouts | **13** | 13 DNS queries failed due to timeout |
| Current DNS | `172.16.17.9` | University's DNS server (primary) |
| Backup DNS | `8.8.8.8` | Google's public DNS (fallback) |
| Search Domain | `cuilahore.edu.pk` | Auto-appended to short hostnames |
| DNSSEC | Not supported | DNS responses are not cryptographically verified |

### Windows vs Linux Comparison

| Feature | Windows (`ipconfig /displaydns`) | Linux (`resolvectl statistics`) |
|---|---|---|
| Individual cached records | **Yes** — shows each domain, TTL, IP | **No** — only aggregate stats |
| Cache size | Not shown directly | Shown (e.g., 17 entries) |
| Hit/miss ratio | Not shown | **Yes** — hits: 648, misses: 3659 |
| TTL per record | Shown for each entry | Not available in stats view |
| DNS server info | Not shown here (use `nslookup`) | Shown via `resolvectl status` |

### Key Observations

1. **DNS caching is active** via `systemd-resolved` (listening on `127.0.0.53`)
2. **17 entries cached** — relatively small cache, entries expire based on TTL
3. **4 DNS servers configured**: university DNS (`172.16.17.9`), Google DNS (`8.8.8.8`), and two internal servers
4. **Low cache hit rate (~15%)** — indicates diverse browsing or short TTL values
5. **13 timeouts** — some DNS queries didn't get a response (possible network issues)
6. **DNSSEC is disabled** — DNS responses are not verified for authenticity

---

## Step 3: `ipconfig /flushdns`

### Windows Command

```cmd
ipconfig /flushdns
```

### Linux Equivalent

```bash
sudo resolvectl flush-caches
```

### Observations (Linux Output)

#### Before Flush

```
Cache
    Current Cache Size:   17
            Cache Hits:  648
          Cache Misses: 3659
```

#### Flush Command

```bash
$ sudo resolvectl flush-caches
# (no output on success — silent confirmation)
```

#### After Flush (`sudo resolvectl statistics`)

```
Cache
    Current Cache Size:    0
            Cache Hits:  664
          Cache Misses: 3670
```

### Analysis

| Metric | Before Flush | After Flush | Change |
|---|---|---|---|
| Cache Size | **17** | **0** | All 17 entries cleared |
| Cache Hits | 648 | 664 | +16 (queries between steps) |
| Cache Misses | 3659 | 3670 | +11 (new lookups between steps) |
| Total Transactions | 4527 | 4554 | +27 total queries between steps |

### Windows vs Linux Comparison

| Feature | Windows (`ipconfig /flushdns`) | Linux (`sudo resolvectl flush-caches`) |
|---|---|---|
| Confirmation message | "Successfully flushed the DNS Resolver Cache" | Silent (no output = success) |
| Requires admin? | Yes (run as Administrator) | Yes (`sudo` required) |
| Effect | Clears all cached DNS entries | Clears all cached DNS entries |
| Verification | Run `ipconfig /displaydns` again | Run `sudo resolvectl statistics` |

### Key Observations

1. **Cache successfully cleared** — size dropped from 17 to 0
2. **Cumulative counters (hits/misses) are NOT reset** — only the cache itself is cleared
3. **Requires root privileges** — must use `sudo` on Linux
4. **Silent success** — unlike Windows which prints a confirmation, Linux gives no output on success
5. **Useful when**: DNS records have changed, troubleshooting stale DNS, or after modifying DNS settings

---

## Command Mapping Summary

| Step | Windows Command | Linux Command | Requires Admin/sudo? |
|---|---|---|---|
| Show all network config | `ipconfig /all` | `ip addr show` | No |
| Show DNS cache | `ipconfig /displaydns` | `sudo resolvectl statistics` | Yes |
| Flush DNS cache | `ipconfig /flushdns` | `sudo resolvectl flush-caches` | Yes |
| Show DNS servers | `nslookup` → check server | `resolvectl status` | No |
| Show resolver config | — | `cat /etc/resolv.conf` | No |
| Show default gateway | `ipconfig` | `ip route show` | No |

### Preferred Linux Commands

| Task | Preferred Command | Why |
|---|---|---|
| Network config | `ip addr show` | Modern, replaces deprecated `ifconfig` |
| DNS cache stats | `sudo resolvectl statistics` | Only option on systemd-resolved systems |
| DNS flush | `sudo resolvectl flush-caches` | Standard on Ubuntu/Debian |
| DNS lookup | `dig` | Most detailed output, widely used |
| Quick DNS check | `host` | Minimal, fast output |
