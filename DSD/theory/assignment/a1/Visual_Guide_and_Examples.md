# Visual Guide and Worked Examples
## Assignment 1 - Digital System Design

This document provides additional visual diagrams, step-by-step calculations, and worked examples to help you understand the solutions better.

---

## 📐 Detailed Visual Diagrams

### Question 1: Complete Circuit Schematic

#### 2×4 Decoder Symbol and Internal Structure

```
        2×4 DECODER WITH ENABLE
        ========================

Symbol:                    Internal Logic:

  A₁ ──┐                   A₁  A₀  E
  A₀ ──┤  ┌────────┐        │   │  │
  E  ──┤──┤ 2×4    │        ▼   ▼  ▼
       │  │ DEC    │       ┌─────────┐
       │  │        │       │  Logic  │
       │  ├───── D₀│       │ Gates   │
       │  ├───── D₁│       └──┬─┬─┬─┬┘
       │  ├───── D₂│          │ │ │ │
       └──├───── D₃│          ▼ ▼ ▼ ▼
          └────────┘          D₀ D₁ D₂ D₃

Truth Table:
┌───┬────┬────┬────┬────┬────┬────┐
│ E │ A₁ │ A₀ │ D₃ │ D₂ │ D₁ │ D₀ │
├───┼────┼────┼────┼────┼────┼────┤
│ 0 │ X  │ X  │ 0  │ 0  │ 0  │ 0  │
│ 1 │ 0  │ 0  │ 0  │ 0  │ 0  │ 1  │ ← D₀ = E·A₁'·A₀'
│ 1 │ 0  │ 1  │ 0  │ 0  │ 1  │ 0  │ ← D₁ = E·A₁'·A₀
│ 1 │ 1  │ 0  │ 0  │ 1  │ 0  │ 0  │ ← D₂ = E·A₁·A₀'
│ 1 │ 1  │ 1  │ 1  │ 0  │ 0  │ 0  │ ← D₃ = E·A₁·A₀
└───┴────┴────┴────┴────┴────┴────┘
```

#### Complete Fuel Sensor Circuit - Detailed Schematic

```
                    FUEL SENSOR INDICATOR CIRCUIT
                    ==============================
                          (Using 5 Decoders)

Inputs: G[3:0] = G₃ G₂ G₁ G₀ (Fuel Level in Binary)
Outputs: F8, F4, F2, F1, R (Indicator Lights)

┌──────────────────────────────────────────────────────────────────────┐
│                        DECODER HIERARCHY                              │
│                                                                      │
│                          DECODER 1 (Master)                          │
│                          ===============                             │
│                Input: G₃(A₁), G₂(A₀), E=VCC(1)                      │
│                                                                      │
│    G₃ ────┐                                                         │
│    G₂ ────┤ ┌──────────────┐                                        │
│    VCC────┤─┤ DECODER 1    │                                        │
│           │ │  (2×4)       │                                        │
│           │ │              │                                        │
│           │ │   D1₀ ───────┼──► (0-3)  ──┐                          │
│           │ │   D1₁ ───────┼──► (4-7)  ──┼──┐                       │
│           │ │   D1₂ ───────┼──► (8-11) ──┼──┼──┐                    │
│           └─│   D1₃ ───────┼──► (12-15)──┼──┼──┼──┐                 │
│             └──────────────┘             │  │  │  │                 │
│                                          │  │  │  │                 │
├──────────────────────────────────────────┼──┼──┼──┼─────────────────┤
│                                          │  │  │  │                 │
│  DECODER 2 (Range 0-3)                   │  │  │  │                 │
│  ======================                   │  │  │  │                 │
│                                          │  │  │  │                 │
│  G₁ ────┐                                │  │  │  │                 │
│  G₀ ────┤ ┌──────────────┐              │  │  │  │                 │
│  D1₀────┤─┤ DECODER 2    │◄─────────────┘  │  │  │                 │
│         │ │  (2×4)       │                  │  │  │                 │
│         │ │              │                  │  │  │                 │
│         │ │   D2₀ ───────┼──► m₀ (0000)───┐ │  │  │                 │
│         │ │   D2₁ ───────┼──► m₁ (0001)───┼─┼──┼──┼─► R = D2₀+D2₁   │
│         │ │   D2₂ ───────┼──► m₂ (0010)   │ │  │  │                 │
│         └─│   D2₃ ───────┼──► m₃ (0011)   │ │  │  │                 │
│           └──────────────┘                 │ │  │  │                 │
│                                            │ │  │  │                 │
├────────────────────────────────────────────┼─┼──┼──┼─────────────────┤
│                                            │ │  │  │                 │
│  DECODER 3 (Range 4-7)                     │ │  │  │                 │
│  ======================                     │ │  │  │                 │
│                                            │ │  │  │                 │
│  G₁ ────┐                                  │ │  │  │                 │
│  G₀ ────┤ ┌──────────────┐                │ │  │  │                 │
│  D1₁────┤─┤ DECODER 3    │◄───────────────┘ │  │  │                 │
│         │ │  (2×4)       │                  │  │  │                 │
│         │ │              │                  │  │  │                 │
│         │ │   D3₀ ───────┼──► m₄ (0100)─────┼──┼──┼─┐               │
│         │ │   D3₁ ───────┼──► m₅ (0101)─────┼──┼──┼─┤               │
│         │ │   D3₂ ───────┼──► m₆ (0110)─────┼──┼──┼─┤               │
│         └─│   D3₃ ───────┼──► m₇ (0111)─────┼──┼──┼─┼─┐             │
│           └──────────────┘                  │  │  │ │ │             │
│                                             │  │  │ │ │             │
├─────────────────────────────────────────────┼──┼──┼─┼─┼─────────────┤
│                                             │  │  │ │ │             │
│  DECODER 4 (Range 8-11)                     │  │  │ │ │             │
│  =======================                     │  │  │ │ │             │
│                                             │  │  │ │ │             │
│  G₁ ────┐                                   │  │  │ │ │             │
│  G₀ ────┤ ┌──────────────┐                 │  │  │ │ │             │
│  D1₂────┤─┤ DECODER 4    │◄────────────────┘  │  │ │ │             │
│         │ │  (2×4)       │                    │  │ │ │             │
│         │ │              │                    │  │ │ │             │
│         │ │   D4₀ ───────┼──► m₈ (1000)───────┼──┼─┼─┼─┐           │
│         │ │   D4₁ ───────┼──► m₉ (1001)───────┼──┼─┼─┼─┤           │
│         │ │   D4₂ ───────┼──► m₁₀(1010)───────┼──┼─┼─┼─┼─┐         │
│         └─│   D4₃ ───────┼──► m₁₁(1011)───────┼──┼─┼─┼─┼─┤         │
│           └──────────────┘                    │  │ │ │ │ │         │
│                                               │  │ │ │ │ │         │
├───────────────────────────────────────────────┼──┼─┼─┼─┼─┼─────────┤
│                                               │  │ │ │ │ │         │
│  DECODER 5 (Range 12-15)                      │  │ │ │ │ │         │
│  ========================                      │  │ │ │ │ │         │
│                                               │  │ │ │ │ │         │
│  G₁ ────┐                                     │  │ │ │ │ │         │
│  G₀ ────┤ ┌──────────────┐                   │  │ │ │ │ │         │
│  D1₃────┤─┤ DECODER 5    │◄──────────────────┘  │ │ │ │ │         │
│         │ │  (2×4)       │                      │ │ │ │ │         │
│         │ │              │                      │ │ │ │ │         │
│         │ │   D5₀ ───────┼──► m₁₂(1100)─────────┼─┼─┼─┼─┼─┐       │
│         │ │   D5₁ ───────┼──► m₁₃(invalid)      │ │ │ │ │ │       │
│         │ │   D5₂ ───────┼──► m₁₄(invalid)      │ │ │ │ │ │       │
│         └─│   D5₃ ───────┼──► m₁₅(invalid)      │ │ │ │ │ │       │
│           └──────────────┘                      │ │ │ │ │ │       │
│                                                 │ │ │ │ │ │       │
└─────────────────────────────────────────────────┼─┼─┼─┼─┼─┼───────┘
                                                  │ │ │ │ │ │
        OUTPUT COMBINATION USING OR GATES         │ │ │ │ │ │
        ==================================         │ │ │ │ │ │
                                                  │ │ │ │ │ │
   ┌──────────────────────────────────────────────┘ │ │ │ │ │
   │                                                │ │ │ │ │
   │  OR Gate for R (Reserve indicator)             │ │ │ │ │
   │  ──────────────────────────────                │ │ │ │ │
   │  m₀ ──┐                                        │ │ │ │ │
   │  m₁ ──┤ ┌───┐                                  │ │ │ │ │
   └───────┴─┤OR ├───► R                            │ │ │ │ │
             └───┘                                  │ │ │ │ │
                                                    │ │ │ │ │
   ┌────────────────────────────────────────────────┘ │ │ │ │
   │                                                  │ │ │ │
   │  OR Gate for F1 (9 inputs)                       │ │ │ │
   │  ──────────────────────────                      │ │ │ │
   │  m₄  ──┐                                         │ │ │ │
   │  m₅  ──┤                                         │ │ │ │
   │  m₆  ──┤                                         │ │ │ │
   │  m₇  ──┤                                         │ │ │ │
   │  m₈  ──┤ ┌───┐                                   │ │ │ │
   │  m₉  ──┼─┤OR ├───► F1                            │ │ │ │
   │  m₁₀ ──┤ └───┘                                   │ │ │ │
   │  m₁₁ ──┤                                         │ │ │ │
   │  m₁₂ ──┘                                         │ │ │ │
   └──────────────────────────────────────────────────┘ │ │ │
                                                        │ │ │
      ┌─────────────────────────────────────────────────┘ │ │
      │                                                   │ │
      │  OR Gate for F2 (6 inputs)                        │ │
      │  ──────────────────────────                       │ │
      │  m₇  ──┐                                          │ │
      │  m₈  ──┤                                          │ │
      │  m₉  ──┤ ┌───┐                                    │ │
      │  m₁₀ ──┼─┤OR ├───► F2                             │ │
      │  m₁₁ ──┤ └───┘                                    │ │
      │  m₁₂ ──┘                                          │ │
      └───────────────────────────────────────────────────┘ │
                                                            │
         ┌────────────────────────────────────────────────┘ │
         │                                                  │
         │  OR Gate for F4 (3 inputs)                       │
         │  ──────────────────────────                      │
         │  m₁₀ ──┐                                         │
         │  m₁₁ ──┤ ┌───┐                                   │
         │  m₁₂ ──┴─┤OR ├───► F4                            │
         │          └───┘                                   │
         └──────────────────────────────────────────────────┘
                                                            │
            ┌───────────────────────────────────────────────┘
            │
            │  Direct Connection for F8 (1 input)
            │  ────────────────────────────────
            │  m₁₂ ───────────────────────────────► F8
            │
            └────────────────────────────────────────────────
```

#### Step-by-Step Example: G = 10 (1010₂)

Let's trace through the circuit when fuel level is 10:

```
Input: G = 10₁₀ = 1010₂
       G₃G₂G₁G₀ = 1010

Step 1: DECODER 1 (Master Decoder)
────────────────────────────────
Inputs: A₁=G₃=1, A₀=G₂=0, E=1
Output: D1₂ = 1 (since A₁=1, A₀=0)
        D1₀, D1₁, D1₃ = 0

Step 2: DECODER 4 is enabled (by D1₂=1)
────────────────────────────────────
Inputs: A₁=G₁=1, A₀=G₀=0, E=D1₂=1
Output: D4₂ = 1 (since A₁=1, A₀=0)
        This represents m₁₀ (minterm 10)

Step 3: All other decoders disabled
────────────────────────────────
DEC 2: E=D1₀=0 → all outputs = 0
DEC 3: E=D1₁=0 → all outputs = 0
DEC 5: E=D1₃=0 → all outputs = 0

Step 4: Output Computation
──────────────────────
R  = D2₀ + D2₁ = 0 + 0 = 0  ✓
F1 = D3₀+D3₁+D3₂+D3₃+D4₀+D4₁+D4₂+D4₃+D5₀
   = 0+0+0+0+0+0+1+0+0 = 1  ✓
F2 = D3₃+D4₀+D4₁+D4₂+D4₃+D5₀
   = 0+0+0+1+0+0 = 1  ✓
F4 = D4₂+D4₃+D5₀
   = 1+0+0 = 1  ✓
F8 = D5₀ = 0  ✓

Result: F8=0, F4=1, F2=1, F1=1, R=0

This matches row for G=10: Shows 3 indicators (F1, F2, F4)
representing fuel level ≤ 11 (above 75%)
```

---

## Question 2: Photo Booth FSM - Detailed Examples

### Example Scenario 1: Insert 25¢ (Quarter)

```
Cycle-by-Cycle Operation:
─────────────────────────

Initial State: S0 (0¢)
Outputs: P=0, RN=0, RD=0, RT=0

Clock Cycle 1:
─────────────
User inserts: Q (quarter, 25¢)
Current State: S0
Inputs: N=0, D=0, Q=1

FSM Logic:
- From S0, Q=1 → Go to S0 (complete transaction)
- Output: P=1 (Print photo)
- Change: 0¢ (exact amount)

Next Clock Cycle:
State: S0 (reset)
Outputs: P=0, RN=0, RD=0, RT=0
Ready for next customer
```

### Example Scenario 2: Insert N, N, N, N, N (5 Nickels)

```
Cycle-by-Cycle Operation:
─────────────────────────

Cycle 1: Insert N (5¢)
────────────────────
Current: S0 (0¢)
Input: N=1, D=0, Q=0
Action: S0 → S5
Output: P=0, RN=0, RD=0, RT=0
Total: 5¢

Cycle 2: Insert N (5¢)
────────────────────
Current: S5 (5¢)
Input: N=1, D=0, Q=0
Action: S5 → S10
Output: P=0, RN=0, RD=0, RT=0
Total: 10¢

Cycle 3: Insert N (5¢)
────────────────────
Current: S10 (10¢)
Input: N=1, D=0, Q=0
Action: S10 → S15
Output: P=0, RN=0, RD=0, RT=0
Total: 15¢

Cycle 4: Insert N (5¢)
────────────────────
Current: S15 (15¢)
Input: N=1, D=0, Q=0
Action: S15 → S20
Output: P=0, RN=0, RD=0, RT=0
Total: 20¢

Cycle 5: Insert N (5¢)
────────────────────
Current: S20 (20¢)
Input: N=1, D=0, Q=0
Action: S20 → S0 (complete!)
Output: P=1 (Print!), RN=0, RD=0, RT=0
Total: 25¢ (exact)
Change: 0¢

Cycle 6: Ready for next customer
─────────────────────────────
Current: S0 (0¢)
Output: P=0, RN=0, RD=0, RT=0
```

### Example Scenario 3: Insert D, D, N (Dime, Dime, Nickel)

```
Cycle 1: Insert D (10¢)
────────────────────
Current: S0 (0¢)
Input: N=0, D=1, Q=0
Action: S0 → S10
Total: 10¢

Cycle 2: Insert D (10¢)
────────────────────
Current: S10 (10¢)
Input: N=0, D=1, Q=0
Action: S10 → S20
Total: 20¢

Cycle 3: Insert N (5¢)
────────────────────
Current: S20 (20¢)
Input: N=1, D=0, Q=0
Action: S20 → S0
Output: P=1, RN=0, RD=0, RT=0
Total: 25¢ (exact)
Change: 0¢
```

### Example Scenario 4: Insert Q, D (Over-payment)

```
Cycle 1: Insert Q (25¢)
────────────────────
Current: S0 (0¢)
Input: N=0, D=0, Q=1
Action: S0 → S0
Output: P=1, RN=0, RD=0, RT=0
Total: 25¢ (exact)
Change: 0¢

Machine completes and resets!
Note: Next coin (D) would start new transaction
```

### Example Scenario 5: Insert D, Q (Overpayment with change)

```
Cycle 1: Insert D (10¢)
────────────────────
Current: S0 (0¢)
Input: N=0, D=1, Q=0
Action: S0 → S10
Total: 10¢

Cycle 2: Insert Q (25¢)
────────────────────
Current: S10 (10¢)
Input: N=0, D=0, Q=1
Action: S10 → S0
Output: P=1, RN=0, RD=1, RT=0
Total: 35¢
Change: 10¢ (one dime returned)
```

### Complete State Transition Table with Examples

```
┌─────────┬───────┬───────┬─────────┬────────────────┬──────────────┐
│ Current │ Coin  │ Amount│  Next   │    Outputs     │   Physical   │
│  State  │Insert │ Added │  State  │  P RN RD RT    │   Action     │
├─────────┼───────┼───────┼─────────┼────────────────┼──────────────┤
│   S0    │   N   │  +5¢  │   S5    │  0  0  0  0    │ Collect      │
│   S0    │   D   │ +10¢  │  S10    │  0  0  0  0    │ Collect      │
│   S0    │   Q   │ +25¢  │   S0    │  1  0  0  0    │ Print, exact │
├─────────┼───────┼───────┼─────────┼────────────────┼──────────────┤
│   S5    │   N   │ +5¢   │  S10    │  0  0  0  0    │ Collect (10¢)│
│   S5    │   D   │ +10¢  │  S15    │  0  0  0  0    │ Collect (15¢)│
│   S5    │   Q   │ +25¢  │   S0    │  1  1  0  0    │ Print, ret 5¢│
├─────────┼───────┼───────┼─────────┼────────────────┼──────────────┤
│  S10    │   N   │ +5¢   │  S15    │  0  0  0  0    │ Collect (15¢)│
│  S10    │   D   │ +10¢  │  S20    │  0  0  0  0    │ Collect (20¢)│
│  S10    │   Q   │ +25¢  │   S0    │  1  0  1  0    │ Print,ret 10¢│
├─────────┼───────┼───────┼─────────┼────────────────┼──────────────┤
│  S15    │   N   │ +5¢   │  S20    │  0  0  0  0    │ Collect (20¢)│
│  S15    │   D   │ +10¢  │   S0    │  1  0  0  0    │ Print, exact │
│  S15    │   Q   │ +25¢  │   S0    │  1  1  1  0    │ Print,ret 15¢│
├─────────┼───────┼───────┼─────────┼────────────────┼──────────────┤
│  S20    │   N   │ +5¢   │   S0    │  1  0  0  0    │ Print, exact │
│  S20    │   D   │ +10¢  │   S0    │  1  1  0  0    │ Print, ret 5¢│
│  S20    │   Q   │ +25¢  │   S0    │  1  0  0  1    │ Print,ret 20¢│
└─────────┴───────┴───────┴─────────┴────────────────┴──────────────┘
```

---

## Question 3: Sequence Generator FSM - Timing Diagrams

### Part (a): Stop/Reset Behavior - Timing Diagram

```
                Timing Diagram for Part (a)
                ============================

Clock:   ──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──
           └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──

Input S: ─────────┐                    ┌─────────┐
                  └────────────────────┘         └─────────────────

State:   St0  St1  St0  St0  St0  St1  St2  St3  St0  St0  St1

Output
 x:      ────────────────────────────────────┐        ┌─────────────
                                             └────────┘

 y:      ──────────────────────────────────────┐  ┌──────────────────
                                               └──┘

 z:      ─────┐              ┌─────────────┐              ┌──────────
              └──────────────┘             └──────────────┘

xyz:     000  001  000  000  000  001  010  100  000  000  001

Analysis:
─────────
Cycle 0: Start in St0, xyz=000
Cycle 1: S=0 → advance to St1, xyz=001
Cycle 2: S=1 → reset to St0, xyz=000  ← RESET!
Cycle 3: S=1 → stay in St0, xyz=000
Cycle 4: S=0 → advance to St1, xyz=001
Cycle 5: S=0 → advance to St2, xyz=010
Cycle 6: S=0 → advance to St3, xyz=100
Cycle 7: S=1 → reset to St0, xyz=000  ← RESET!
Cycle 8: S=0 → advance to St1, xyz=001

Key Observation: Whenever S=1, sequence resets to 000
                When S returns to 0, sequence starts fresh from 000
```

### Part (b): 3-Cycle Postpone - Timing Diagram

```
                Timing Diagram for Part (b)
                ============================

Clock:   ──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──
           └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──

Input S: ──────┐                             ┌──────────────────────
               └─────────────────────────────┘

State:   St0  St1  Ps1  Ps2  Ps3  Ps3  Ps3  St2  St3  St0  St1

Output
 x:      ────────────────────────────────────────┐        ┌──────────
                                                 └────────┘

 y:      ──────────────────────────────────┐  ┌───────────────────
                                           └──┘

 z:      ─────┐                                         ┌───────────
              └─────────────────────────────────────────┘

xyz:     000  001  001  001  001  001  001  010  100  000  001
              ↑                             ↑
           S=1 (pause)                   S=0 (resume)
         Enter Pause1                    After 3 cycles,
                                        continue sequence

Analysis:
─────────
Cycle 0: Start in St0, xyz=000
Cycle 1: S=0 → St1, xyz=001
Cycle 2: S=1 → Pause1, xyz=001 (output frozen)
Cycle 3: → Pause2, xyz=001 (count: 1)
Cycle 4: → Pause3, xyz=001 (count: 2)
Cycle 5: S still 1 → Pause3, xyz=001 (count: 3)
Cycle 6: S still 1 → Pause3, xyz=001 (count: 4)
Cycle 7: S=0 → Resume! → St2, xyz=010  ← CONTINUE!
Cycle 8: S=0 → St3, xyz=100
Cycle 9: S=0 → St0, xyz=000
Cycle 10: S=0 → St1, xyz=001

Key Observation: Output stays constant during pause
                Sequence CONTINUES from where it left off
                Minimum 3 cycles pause enforced
```

### Part (c): 30-Cycle Postpone with Counter

```
                Timing Diagram for Part (c)
                ============================
                (Showing key cycles only)

Clock:   ──┐  ┌──┐  ┌──┐  ... ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐
           └──┘  └──┘  └──┘     └──┘  └──┘  └──┘  └──┘  └──┘
Cycle:     0    1    2    ...   29   30   31   32   33

Input S: ──────┐                                  ┌──────────
               └──────────────────────────────────┘

State:   St0  St1  Ps   Ps   ... Ps   Ps   Ps   St2  St3

Counter: 0    0    1    2    ... 28   29   30   0    0

cnt_done:─────────────────────────────┐           ┌──────────
                                      └───────────┘

xyz:     000  001  001  001  ... 001  001  001  010  100

Analysis:
─────────
Cycle 0: St0, xyz=000, counter=0
Cycle 1: St1, xyz=001, counter=0
Cycle 2: S=1 → Pause, xyz=001, counter starts (=1)
Cycle 3: Pause, xyz=001, counter=2
...
Cycle 30: Pause, xyz=001, counter=29
Cycle 31: Pause, xyz=001, counter=30 → cnt_done=1
Cycle 32: S=0 AND cnt_done=1 → Resume! St2, xyz=010
Cycle 33: St3, xyz=100

Counter Logic:
──────────────
  ┌──────────────┐
  │  5-bit       │  count
  │  Counter  ───┼────► [4:0]
  │  (74163)     │         │
  └──┬────┬──────┘         ▼
     │    │          ┌──────────┐
  clk│ rst│          │ count≥30?│
                     └─────┬────┘
                           │
                           ▼
                       cnt_done

When in Pause state:
- Counter increments each clock cycle
- When count reaches 30, cnt_done=1
- If S=0 AND cnt_done=1, resume sequence
- If S still 1, stay in pause
```

---

## Karnaugh Maps for Simplification

### Question 1: K-maps for Output Functions

#### K-map for F1

```
       G₁G₀
G₃G₂   00  01  10  11
────┼────┼────┼────┼────┐
 00 │ 0  │ 0  │ 0  │ 0  │
────┼────┼────┼────┼────┤
 01 │ 1  │ 1  │ 1  │ 1  │ ← All 1's (G₂=1)
────┼────┼────┼────┼────┤
 10 │ 1  │ 1  │ 1  │ 1  │ ← All 1's (G₃=1)
────┼────┼────┼────┼────┤
 11 │ 1  │ X  │ X  │ X  │
────┴────┴────┴────┴────┘

Groups:
━━━━━━
□ Second row (G₃=0, G₂=1): 4 cells → G₃'·G₂
□ Third row (G₃=1, G₂=0): 4 cells → G₃·G₂'
□ Fourth row (G₃=1, G₂=1): 4 cells → G₃·G₂

Simplified: F1 = G₃'·G₂ + G₃·G₂' + G₃·G₂
                = G₂ + G₃
```

#### K-map for F2

```
       G₁G₀
G₃G₂   00  01  10  11
────┼────┼────┼────┼────┐
 00 │ 0  │ 0  │ 0  │ 0  │
────┼────┼────┼────┼────┤
 01 │ 0  │ 0  │ 0  │ 1  │ ← m₇
────┼────┼────┼────┼────┤
 10 │ 1  │ 1  │ 1  │ 1  │ ← m₈,m₉,m₁₀,m₁₁
────┼────┼────┼────┼────┤
 11 │ 1  │ X  │ X  │ X  │ ← m₁₂
────┴────┴────┴────┴────┘

Groups:
━━━━━━
□ Third row: G₃·G₂' (covers m₈-m₁₁)
□ Cell (01,11): G₃'·G₂·G₁·G₀ (m₇)
□ Can also group with (11,00): needs more terms

Simplified: F2 = G₃·G₂' + G₂·G₁·G₀ + G₃·G₂·G₁'·G₀'
```

#### K-map for R

```
       G₁G₀
G₃G₂   00  01  10  11
────┼────┼────┼────┼────┐
 00 │ 1  │ 1  │ 0  │ 0  │ ← m₀, m₁
────┼────┼────┼────┼────┤
 01 │ 0  │ 0  │ 0  │ 0  │
────┼────┼────┼────┼────┤
 10 │ 0  │ 0  │ 0  │ 0  │
────┼────┼────┼────┼────┤
 11 │ 0  │ X  │ X  │ X  │
────┴────┴────┴────┴────┘

Groups:
━━━━━━
□ Cells (00,00) and (00,01): G₃'·G₂'·G₁'

Simplified: R = G₃'·G₂'·G₁'
```

---

## Implementation Tips

### Best Practices:

1. **Always verify truth tables** - Check several test cases manually
2. **Use consistent notation** - Stick to one style for state encoding
3. **Draw clear diagrams** - Make transitions and outputs obvious
4. **Minimize logic** - Use K-maps or Boolean algebra
5. **Test edge cases** - What happens at boundaries (e.g., fuel=2, fuel=12)?

### Common Mistakes to Avoid:

❌ **Forgetting initial state** - Always mark which state FSM starts in
❌ **Incorrect state encoding** - Ensure each state has unique binary code
❌ **Missing transitions** - Every state must have transition for every input combination
❌ **Wrong output timing** - Outputs change on clock edge in synchronous FSMs
❌ **Decoder enable ignored** - When enable=0, ALL decoder outputs are 0

---

## Summary

This visual guide provides:
✅ Detailed circuit schematics with component connections
✅ Step-by-step trace-through examples
✅ Timing diagrams showing FSM behavior over time
✅ K-maps for Boolean minimization
✅ Common pitfalls and best practices

Use these diagrams alongside the main solution document for complete understanding!

**Good luck with your assignment! 🎓**
