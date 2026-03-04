# Lab 4 — Complete Guide (Router-PT & Switch-PT)

## Reproduce Basic Device Configuration Sequence to Ensure Device Connectivity in Layer 3 Devices using Cisco Packet Tracer

> This guide matches **your exact topology** — device names, interface labels, and cable types as shown in your diagram.

---

## Table of Contents

1. [Understanding the Topology](#1-understanding-the-topology)
2. [Step-by-Step: Building the Topology](#2-step-by-step-building-the-topology)
3. [Task 1: Cable the Network](#3-task-1-cable-the-network)
4. [Task 2: Basic IOS CLI Operations](#4-task-2-basic-ios-cli-operations)
5. [Task 3: Configure Router0](#5-task-3-configure-router0)
6. [Task 4: Configure Router1](#6-task-4-configure-router1)
7. [Task 5: Configure PCs](#7-task-5-configure-pcs)
8. [Task 6: Verify and Test](#8-task-6-verify-and-test)
9. [Task 7: Reflection](#9-task-7-reflection)
10. [Task 8: Create Startup Config File](#10-task-8-create-startup-config-file)
11. [Task 9: Reload Router from Saved Config](#11-task-9-reload-router-from-saved-config)
12. [Quick Reference: IOS Commands](#12-quick-reference-ios-commands)
13. [Answers to Lab Questions](#13-answers-to-lab-questions)

---

## 1. Understanding the Topology

### Your Exact Topology

```
   Network 1 (LAN)            WAN Link (Serial)             Network 3 (LAN)
   192.168.1.0/24             192.168.2.0/24                192.168.3.0/24

 ┌──────┐ Fa0  Fa0/1┌──────────┐Fa1/1   Fa0/0┌──────────┐Se2/0(DCE⊕) Se2/0┌──────────┐Fa0/0  Fa0 ┌──────┐
 │ PC0  │───────────│ Switch0  │──────────────│ Router0  │══════════════════│ Router1  │─ ─ ─ ─ ─ ─│ PC1  │
 └──────┘           │(Switch-PT│              │(Router-PT│                  │(Router-PT│            └──────┘
 GW:.1.1            └──────────┘              │Fa0/0:.1.1│                  │Se2/0:.2.2│            GW:.3.1
                                              │Se2/0:.2.1│                  │Fa0/0:.3.1│
                                              └──────────┘                  └──────────┘

  ── solid line  = Copper Straight-Through
  ══ red line    = Serial DCE  (Router0 clicked first; ⊕ = DCE/clock side)
  ─ ─ dashed line = Copper Cross-Over (Router1 direct to PC1, no switch on PC1 side)
```

### Devices (5 total)

| # | Device            | Type       | Model in PT         |
| - | ----------------- | ---------- | ------------------- |
| 1 | **Router0** | Router     | **Router-PT** |
| 2 | **Router1** | Router     | **Router-PT** |
| 3 | **Switch0** | Switch     | **Switch-PT** |
| 4 | **PC0**     | End Device | Generic PC-PT       |
| 5 | **PC1**     | End Device | Generic PC-PT       |

### Addressing Table

| Device  | Interface | IP Address   | Subnet Mask   | Default Gateway |
| ------- | --------- | ------------ | ------------- | --------------- |
| Router0 | Fa0/0     | 192.168.1.1  | 255.255.255.0 | N/A             |
| Router0 | Se2/0     | 192.168.2.1  | 255.255.255.0 | N/A             |
| Router1 | Se2/0     | 192.168.2.2  | 255.255.255.0 | N/A             |
| Router1 | Fa0/0     | 192.168.3.1  | 255.255.255.0 | N/A             |
| PC0     | Fa0       | 192.168.1.10 | 255.255.255.0 | 192.168.1.1     |
| PC1     | Fa0       | 192.168.3.10 | 255.255.255.0 | 192.168.3.1     |

### Cable Types

| # | Connection                             | Cable Type                        | Why?                                             |
| - | -------------------------------------- | --------------------------------- | ------------------------------------------------ |
| 1 | PC0 `Fa0` → Switch0 `Fa0/1`       | **Copper Straight-Through** | Different device types (PC ↔ switch)            |
| 2 | Switch0 `Fa1/1` → Router0 `Fa0/0` | **Copper Straight-Through** | Different device types (switch ↔ router)        |
| 3 | Router0 `Se2/0` → Router1 `Se2/0` | **Serial DCE**              | WAN serial link; Router0 = DCE (⊕ clock symbol) |
| 4 | Router1 `Fa0/0` → PC1 `Fa0`       | **Copper Cross-Over**       | Direct router ↔ PC, no switch in between        |

> **CRITICAL — Router0 is DCE:**
> The ⊕ clock symbol on Router0's Se2/0 in your diagram means Router0 is the DCE side.
> You MUST click **Router0 first** when placing the Serial DCE cable, and you MUST run
> `clock rate 64000` on Router0's Se2/0 interface. Router1 does NOT need clock rate.

---

## 2. Step-by-Step: Building the Topology

### Step 2.1: Open Packet Tracer

Open Packet Tracer, log in, and start with an empty workspace.

### Step 2.2: Add Router0 (Router-PT)

1. Bottom panel → **Network Devices** → **Routers**
2. Select **Router-PT**
3. Click on the workspace — this is **Router0**

### Step 2.3: Add Router1 (Router-PT)

1. Same category → **Router-PT**
2. Click to the **right of Router0** — this is **Router1**

### Step 2.4: Add Switch0 (Switch-PT)

1. Bottom panel → **Network Devices** → **Switches**
2. Select **Switch-PT**
3. Place it **to the left of Router0** — this is **Switch0**

### Step 2.5: Add PC0

1. Bottom panel → **End Devices** → **PC-PT**
2. Place it **to the left of Switch0** — this is **PC0**

### Step 2.6: Add PC1

1. Same → **End Devices** → **PC-PT**
2. Place it **to the right of Router1** — this is **PC1**

### Step 2.7: Rename the Devices

Click each device → **Config** tab → set **Display Name**:

| Device       | Set Display Name to |
| ------------ | ------------------- |
| First PC     | `PC0`             |
| Switch       | `Switch0`         |
| Left Router  | `Router0`         |
| Right Router | `Router1`         |
| Second PC    | `PC1`             |

> Final layout (left → right):
>
> ```
> [PC0]  [Switch0]  [Router0] ══serial══ [Router1]  [PC1]
> ```

---

## 3. Task 1: Cable the Network

Open: bottom panel → **Connections** (lightning bolt icon)

### Cable 1 — PC0 to Switch0 (Straight-Through)

1. Select **Copper Straight-Through**
2. Click **PC0** → select `Fa0`
3. Click **Switch0** → select `Fa0/1`
4. ✅ Both lights turn **green** (Switch-PT ports auto-activate)

### Cable 2 — Switch0 to Router0 (Straight-Through)

1. Select **Copper Straight-Through**
2. Click **Switch0** → select `Fa1/1`
3. Click **Router0** → select `Fa0/0`
4. Switch side → 🟢; Router side → 🔴 (router interfaces are shutdown by default — normal!)

### Cable 3 — Router0 Se2/0 to Router1 Se2/0 (Serial DCE)

> This is the **red cable** in your diagram.

1. Select **Serial DCE** cable
2. **Click Router0 FIRST** → select `Se2/0`  ← Router0 = DCE (⊕ clock symbol)
3. Click **Router1** → select `Se2/0`
4. Both sides 🔴 red — serial interfaces shutdown, needs `no shutdown` + `clock rate`

> **Why click Router0 first?**
> Whichever router you click first when placing a Serial DCE cable becomes the DCE side.
> The ⊕ clock symbol confirms Router0 is DCE.

### Cable 4 — Router1 Fa0/0 to PC1 (Cross-Over, Direct)

> Dashed line in your diagram = Crossover. No switch on PC1 side.

1. Select **Copper Cross-Over**
2. Click **Router1** → select `Fa0/0`
3. Click **PC1** → select `Fa0`
4. Both sides 🔴 red (router Fa0/0 shutdown, no switch to auto-activate PC1 side)

### Connection Summary

```
PC0(Fa0) ──straight──► Switch0(Fa0/1)
Switch0(Fa1/1) ──straight──► Router0(Fa0/0)
Router0(Se2/0) ══Serial DCE══ Router1(Se2/0)    ← red cable, Router0=DCE
Router1(Fa0/0) ─ ─crossover─ ─► PC1(Fa0)
```

**Link light status at this stage:**

- PC0 ↔ Switch0:       🟢🟢 Green
- Switch0 ↔ Router0:   🟢🔴 (switch green, router red — normal)
- Router0 ↔ Router1:   🔴🔴 Red
- Router1 ↔ PC1:       🔴🔴 Red

> All lights turn **green** after running `no shutdown` on all router interfaces.

---

## 4. Task 2: Basic IOS CLI Operations

### Step 4.1: Open Router0 CLI

1. Click **Router0** in the workspace
2. In the popup, click the **CLI** tab
3. Press **Enter** if prompted

You'll see:

```
Router>
```

This is **User EXEC mode** — limited, view-only.

### Step 4.2: Enter Privileged EXEC Mode

```
Router> enable
Router#
```

The `#` means **Privileged EXEC mode** — full access.

### Step 4.3: Enter Global Configuration Mode

```
Router# configure terminal
Router(config)#
```

---

## 5. Task 3: Configure Router0

Click **Router0** → **CLI** tab. Run commands one by one:

### Step 5.1: Set Hostname

```
Router> enable
Router# configure terminal
Router(config)# hostname Router0
Router0(config)#
```

> Prompt changes from `Router(config)#` to `Router0(config)#`

### Step 5.2: Disable DNS Lookup

```
Router0(config)# no ip domain-lookup
```

> Prevents ~30-second delays when mistyped commands are treated as DNS hostname lookups.

### Step 5.3: Set Enable Secret Password

```
Router0(config)# enable secret class
```

> `enable secret` stores the password **encrypted** (MD5). More secure than `enable password` (plain text). If both are set, `enable secret` takes priority.

### Step 5.4: Set Console Password

```
Router0(config)# line console 0
Router0(config-line)# password cisco
Router0(config-line)# login
Router0(config-line)# exit
Router0(config)#
```

### Step 5.5: Set VTY (Telnet) Password

```
Router0(config)# line vty 0 4
Router0(config-line)# password cisco
Router0(config-line)# login
Router0(config-line)# exit
Router0(config)#
```

### Step 5.6: Configure Fa0/0 — LAN Side (connects to Switch0)

```
Router0(config)# interface fastethernet 0/0
Router0(config-if)# ip address 192.168.1.1 255.255.255.0
Router0(config-if)# description LAN - Connected to Switch0
Router0(config-if)# no shutdown
Router0(config-if)# exit
```

> You'll see:
>
> ```
> %LINK-5-CHANGED: Interface FastEthernet0/0, changed state to up
> %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/0, changed state to up
> ```
>
> The Switch0 ↔ Router0 link lights both turn **green**.

### Step 5.7: Configure Se2/0 — WAN Side (connects to Router1)

```
Router0(config)# interface serial 2/0
Router0(config-if)# ip address 192.168.2.1 255.255.255.0
Router0(config-if)# clock rate 64000
Router0(config-if)# description WAN - Serial link to Router1 (DCE)
Router0(config-if)# no shutdown
Router0(config-if)# exit
```

> **Why `clock rate 64000` on Router0?**
>
> - Router0 is the **DCE** side (⊕ symbol in your diagram).
> - DCE provides the clock signal that the DTE (Router1) uses to synchronize transmission.
> - `64000` sets the link speed to 64,000 bps.
> - **Only Router0 (DCE) needs this command.** Router1 does NOT.
> - Without `clock rate`, the serial link stay `up/down` and will not pass traffic.

### Step 5.8: Save Configuration

```
Router0(config)# exit
Router0# copy running-config startup-config
```

Press **Enter** when prompted.

> Short version: `Router0# wr`
> `running-config` = current settings in RAM (lost on reboot)
> `startup-config` = saved in NVRAM (survives reboot)

---

## 6. Task 4: Configure Router1

Click **Router1** → **CLI** tab. Run:

```
Router> enable
Router# configure terminal

! Step 1: Hostname
Router(config)# hostname Router1

! Step 2: Disable DNS lookup
Router1(config)# no ip domain-lookup

! Step 3: Enable secret
Router1(config)# enable secret class

! Step 4: Console password
Router1(config)# line console 0
Router1(config-line)# password cisco
Router1(config-line)# login
Router1(config-line)# exit

! Step 5: VTY password
Router1(config)# line vty 0 4
Router1(config-line)# password cisco
Router1(config-line)# login
Router1(config-line)# exit

! Step 6: Configure Se2/0 — WAN side (connects to Router0)
Router1(config)# interface serial 2/0
Router1(config-if)# ip address 192.168.2.2 255.255.255.0
Router1(config-if)# description WAN - Serial link to Router0 (DTE)
Router1(config-if)# no shutdown
Router1(config-if)# exit

! Step 7: Configure Fa0/0 — LAN side (connects directly to PC1)
Router1(config)# interface fastethernet 0/0
Router1(config-if)# ip address 192.168.3.1 255.255.255.0
Router1(config-if)# description LAN - Direct link to PC1
Router1(config-if)# no shutdown
Router1(config-if)# exit

! Step 8: Save
Router1(config)# exit
Router1# copy running-config startup-config
```

> **Router1 does NOT use `clock rate`** — Router1 is the **DTE** side (receives the clock signal from Router0 which is DCE).

---

## 7. Task 5: Configure PCs

### Step 7.1: Configure PC0

1. Click **PC0** → **Desktop** tab → **IP Configuration**
2. Select **Static**
3. Enter:
   - **IP Address:** `192.168.1.10`
   - **Subnet Mask:** `255.255.255.0`
   - **Default Gateway:** `192.168.1.1`  ← Router0's Fa0/0
4. Close the window

### Step 7.2: Configure PC1

1. Click **PC1** → **Desktop** tab → **IP Configuration**
2. Select **Static**
3. Enter:
   - **IP Address:** `192.168.3.10`
   - **Subnet Mask:** `255.255.255.0`
   - **Default Gateway:** `192.168.3.1`  ← Router1's Fa0/0
4. Close the window

> **Default Gateway:** The IP of the router interface on the same network as the PC. The PC sends all traffic for other networks through this address.

---

## 8. Task 6: Verify and Test

### Step 8.1: Check Routing Tables

**On Router0:**

```
Router0# show ip route
```

Expected:

```
C    192.168.1.0/24 is directly connected, FastEthernet0/0
C    192.168.2.0/24 is directly connected, Serial2/0
```

**On Router1:**

```
Router1# show ip route
```

Expected:

```
C    192.168.2.0/24 is directly connected, Serial2/0
C    192.168.3.0/24 is directly connected, FastEthernet0/0
```

> **C** = Directly Connected — the router knows about these networks automatically.

### Step 8.2: Verify Interface Status

**On Router0:**

```
Router0# show ip interface brief
```

Expected:

```
Interface          IP-Address      OK? Method Status    Protocol
FastEthernet0/0    192.168.1.1     YES manual up        up
Serial2/0          192.168.2.1     YES manual up        up
```

**On Router1:**

```
Router1# show ip interface brief
```

Expected:

```
Interface          IP-Address      OK? Method Status    Protocol
FastEthernet0/0    192.168.3.1     YES manual up        up
Serial2/0          192.168.2.2     YES manual up        up
```

> Both **Status** and **Protocol** must say `up up`.
> If Serial shows `up/down` → `clock rate` is missing on Router0.
> If Serial shows `down/down` → `no shutdown` not run, or cable problem.

### Step 8.3: Test Pings (Directly Connected)

**From Router0, ping PC0:**

```
Router0# ping 192.168.1.10
```

Expected: `!!!!!`

**From PC0, ping its default gateway:**
Click **PC0** → **Desktop** → **Command Prompt**

```
ping 192.168.1.1
```

Expected: 4 replies, 0% loss

**From Router0, ping Router1 serial interface:**

```
Router0# ping 192.168.2.2
```

Expected: `!!!!!`

**From PC1, ping its default gateway:**
Click **PC1** → **Desktop** → **Command Prompt**

```
ping 192.168.3.1
```

Expected: 4 replies, 0% loss

---

## 9. Task 7: Reflection

### Test Cross-Network Pings

**From PC0, ping PC1:**

```
C:\> ping 192.168.3.10
```

**Result:** ❌ FAIL — Request timed out

**From PC0, ping Router1 WAN interface:**

```
C:\> ping 192.168.2.2
```

**Result:** ❌ FAIL

**From PC1, ping Router0:**

```
C:\> ping 192.168.2.1
```

**Result:** ❌ FAIL

### Why Do These Pings Fail?

> Router0 knows only about `192.168.1.0/24` and `192.168.2.0/24`.
> Router1 knows only about `192.168.2.0/24` and `192.168.3.0/24`.
> Neither router has a route to the other's LAN network.
> **Static routes or a dynamic routing protocol** must be configured for end-to-end connectivity.
> This will be covered in a later lab.

---

## 10. Task 8: Create Startup Config File

### Step 10.1: View Running Config

```
Router0# show running-config
```

### Step 10.2: Save to a Text File

1. Select all output from `show running-config` in the CLI window
2. Copy (Ctrl+C)
3. Open a text editor (`gedit`, `nano`, or VS Code)
4. Paste and edit:
   - Add `no shutdown` after each interface section
   - Replace the encrypted `enable secret` hash line with `enable secret class`
   - Remove any `mac-address` lines from interfaces
5. Save as `start.txt`

---

## 11. Task 9: Reload Router from Saved Config

### Step 11.1: Erase Startup Config

```
Router0# erase startup-config
```

Press **Enter** to confirm.

### Step 11.2: Reload

```
Router0# reload
```

- Confirm the reload
- Answer **no** if asked to save running config
- Answer **no** to AutoInstall after reboot

### Step 11.3: Verify After Reboot

```
Router> enable
Router# show running-config
Router# show startup-config
```

> `startup-config is not present` — expected, we erased it.

### Step 11.4: Restore Config

```
Router# configure terminal
```

Paste contents of `start.txt` into the CLI.

### Step 11.5: Save

```
Router0# copy running-config startup-config
```

---

## 12. Quick Reference: IOS Commands

### Navigation Modes

| Mode             | Prompt                   | How to Enter                          |
| ---------------- | ------------------------ | ------------------------------------- |
| User EXEC        | `Router>`              | Default on login                      |
| Privileged EXEC  | `Router#`              | `enable`                            |
| Global Config    | `Router(config)#`      | `configure terminal`                |
| Interface Config | `Router(config-if)#`   | `interface fastethernet 0/0`        |
| Line Config      | `Router(config-line)#` | `line console 0` / `line vty 0 4` |

### Going Back

| From → To           | Command                 |
| -------------------- | ----------------------- |
| Privileged → User   | `disable`             |
| Config → Privileged | `exit` or `Ctrl+Z`  |
| Interface → Global  | `exit`                |
| Any → Privileged    | `Ctrl+Z` (or `end`) |

### Keyboard Shortcuts

| Shortcut | Action                    |
| -------- | ------------------------- |
| Ctrl+A   | Move to beginning of line |
| Ctrl+E   | Move to end of line       |
| Ctrl+Z   | Exit to privileged mode   |
| Ctrl+U   | Erase entire line         |
| Ctrl+W   | Erase one word            |
| Tab      | Auto-complete command     |
| `?`    | Show available commands   |

### Most Used Commands

```
show running-config                     → Current config (RAM)
show startup-config                     → Saved config (NVRAM)
show ip route                           → Routing table
show ip interface brief                 → Quick interface status
copy running-config startup-config      → Save configuration
ping <ip-address>                       → Test connectivity
```

---

## 13. Answers to Lab Questions

### Task 1 — Cable Types

| Connection                             | Cable Used              |
| -------------------------------------- | ----------------------- |
| PC0 `Fa0` → Switch0 `Fa0/1`       | Copper Straight-Through |
| Switch0 `Fa1/1` → Router0 `Fa0/0` | Copper Straight-Through |
| Router0 `Se2/0` → Router1 `Se2/0` | **Serial DCE**    |
| Router1 `Fa0/0` → PC1 `Fa0`       | Copper Cross-Over       |

### Task 3 — Configuration Q&A

| Question                                                | Answer                                                                                                                   |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Command to enter privileged EXEC mode                   | `enable`                                                                                                               |
| Observation after `hostname Router0`                  | Prompt changes from `Router(config)#` to `Router0(config)#`                                                          |
| Why disable DNS lookup in lab?                          | Prevents ~30-second delays when mistyped commands try to resolve as hostnames                                            |
| Effect of disabling DNS in production                   | Router CLI cannot resolve hostnames (e.g.,`ping google.com` won't work from CLI)                                       |
| `enable secret` vs `enable password`                | `enable secret` = encrypted (MD5); `enable password` = plain text. `secret` overrides `password` if both are set |
| What is `clock rate`, and which router needs it?      | Sets serial link speed. Only**Router0 (DCE side)** needs it. Router1 (DTE) does not                                |
| Why no `clock rate` on Router1?                       | Router1 is DTE — it receives the clock signal from Router0 (DCE)                                                        |
| Why add interface descriptions?                         | Documents what each interface connects to; useful in large networks for troubleshooting                                  |
| Short version of `copy running-config startup-config` | `wr` or `copy run start`                                                                                             |

### Task 5 Answer

| Question                        | Answer                                                                                                                                                      |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Significance of default gateway | The router interface IP on the PC's own network. The PC forwards all remote traffic through this address. Without it, the PC cannot reach any other network |

### Task 7 Answer

| Question                         | Answer                                                                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Why do cross-network pings fail? | Router0 has no route to `192.168.3.0/24`; Router1 has no route to `192.168.1.0/24`. Static or dynamic routes must be added |

---

## Troubleshooting

| Problem                                     | Solution                                                                         |
| ------------------------------------------- | -------------------------------------------------------------------------------- |
| Router Fa0/0 link stays red                 | Run `no shutdown` on that interface; verify cable is Straight-Through          |
| Serial shows `up/down` in interface brief | `clock rate` missing — run `clock rate 64000` on Router0 `Se2/0`          |
| Serial shows `down/down`                  | Check `no shutdown` on both Router0 and Router1 Se2/0; verify Serial DCE cable |
| Ping to default gateway fails               | Check PC IP/gateway are on the same subnet; verify `show ip interface brief`   |
| "Invalid input detected" error              | Wrong CLI mode — use `?` to see available commands                            |
| Prompt shows `Router>` not `Router0>`   | Hostname not set yet, or config was erased                                       |

---

## Visual Summary

```
     192.168.1.0/24            192.168.2.0/24            192.168.3.0/24
     (LAN — PC0 side)          (WAN — Serial)            (LAN — PC1 side)

 ┌──────────┐  ┌──────────────┐  ┌──────────────┐       ┌──────────────┐  ┌──────────┐
 │   PC0    │  │   Switch0    │  │   Router0    │ DCE⊕  │   Router1    │  │   PC1    │
 │192.168   │──│  (Switch-PT) │──│  (Router-PT) │═══════│  (Router-PT) │──│192.168   │
 │.1.10     │  │              │  │ Fa0/0: .1.1  │Se2/0  │Se2/0  Fa0/0 │  │.3.10     │
 │GW: .1.1  │  │              │  │ Se2/0: .2.1  │  .2.2 │.2.2    .3.1 │  │GW: .3.1  │
 └──────────┘  └──────────────┘  └──────────────┘       └──────────────┘  └──────────┘
  Fa0   Fa0/1    Fa1/1  Fa0/0                                 Fa0/0  Fa0
  └─straight─────┘└──straight──┘                              └─crossover─┘

  Cable 1: PC0(Fa0) → Switch0(Fa0/1)        = Copper Straight-Through  ──
  Cable 2: Switch0(Fa1/1) → Router0(Fa0/0)  = Copper Straight-Through  ──
  Cable 3: Router0(Se2/0) → Router1(Se2/0)  = Serial DCE  ══ (red, ⊕ on Router0)
  Cable 4: Router1(Fa0/0) → PC1(Fa0)        = Copper Cross-Over  ─ ─
```

---

*Guide for CPE314 Lab 4 — Spring 2025 | Matches your exact Packet Tracer diagram*
