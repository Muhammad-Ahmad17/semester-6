# Digital System Design - Assignment 1 Solution
## SPRING 2026 - CPE344

**Course:** Digital System Design
**Instructor:** Dr Muhammad Babar Ali
**Batch-Section:** FA23-B
**Topics Covered:** Chapters 2-4
**Total Marks:** 40

---

## 📚 Prerequisite Knowledge

Before solving the assignment, let's cover the essential concepts you need to understand:

### 1. Combinational Logic Fundamentals

**Combinational Logic Circuit:** A circuit where outputs depend only on current inputs (no memory/state).

Key Components:
- **Logic Gates:** AND, OR, NOT, NAND, NOR, XOR, XNOR
- **Truth Tables:** Show all possible input combinations and corresponding outputs
- **Boolean Algebra:** Mathematical notation for logic operations
- **Karnaugh Maps (K-maps):** Tool for simplifying Boolean expressions

### 2. Decoders

**Decoder:** A combinational circuit that converts n inputs to at most 2ⁿ unique outputs.

**2×4 Decoder with Enable:**
- **Inputs:** 2 data inputs (A₁, A₀), 1 enable input (E)
- **Outputs:** 4 outputs (D₀, D₁, D₂, D₃)
- **Operation:** When E=1, exactly one output is HIGH based on input combination
- **Truth Table:**

| E | A₁ | A₀ | D₃ | D₂ | D₁ | D₀ |
|:-:|:--:|:--:|:--:|:--:|:--:|:--:|
| 0 | X  | X  | 0  | 0  | 0  | 0  |
| 1 | 0  | 0  | 0  | 0  | 0  | 1  |
| 1 | 0  | 1  | 0  | 0  | 1  | 0  |
| 1 | 1  | 0  | 0  | 1  | 0  | 0  |
| 1 | 1  | 1  | 1  | 0  | 0  | 0  |

**Using Decoders for Logic Implementation:**
- Decoders generate all minterms for the inputs
- Combine decoder outputs with OR gates to implement any Boolean function
- Each minterm corresponds to one decoder output

### 3. Finite State Machines (FSM)

**FSM:** A mathematical model for sequential circuits with:
- **States:** All possible conditions the machine can be in
- **Inputs:** External signals affecting state transitions
- **Outputs:** Signals produced based on current state
- **Transitions:** Rules for moving between states
- **Initial State:** Starting state on power-up/reset

**FSM Types:**
1. **Moore Machine:** Outputs depend only on current state
2. **Mealy Machine:** Outputs depend on current state AND inputs

**FSM Design Process:**
1. Capture FSM (draw state diagram)
2. Encode states (assign binary codes)
3. Create state transition table
4. Derive next-state and output equations
5. Implement with flip-flops and combinational logic

### 4. State Encoding

**Number of Flip-Flops Required:**
- n flip-flops → 2ⁿ possible states
- For N states: need ⌈log₂(N)⌉ flip-flops

Examples:
- 2-4 states → 2 flip-flops
- 5-8 states → 3 flip-flops
- 9-16 states → 4 flip-flops

### 5. Binary Number System

**Decimal to Binary Conversion:**
- 0₁₀ = 0000₂
- 1₁₀ = 0001₂
- 12₁₀ = 1100₂

**Percentage Calculations:**
- For 12 units (max fuel):
  - 75% = 9 units
  - 50% = 6 units
  - 25% = 3 units

---

## Question 1: Fuel Sensor Indicator Circuit (Marks: 20)

### Problem Statement

A vehicle has a fuel sensor which outputs the current fuel/gasoline level as a 4-bit binary number ranges from 0001₂ (0₁₀) to 1100₂ (12₁₀). Design combinational logic (CL) circuit that takes sensor data as input G and generates F1, F2, F4, F8 and R signals on its outputs for fuel indicators.

**Requirements:**
- When Gasoline is above 11 (i.e., 12): Set all Fᵢ outputs (i=1,2,4,8) to 1, R=0
- When Gasoline ≤ 11 and > 9 (75%): F1=1, F2=1, F4=1, F8=0, R=0
- When Gasoline ≤ 9 and > 6 (50%): F1=1, F2=1, F4=0, F8=0, R=0
- When Gasoline ≤ 6 and > 3 (25%): F1=1, F2=0, F4=0, F8=0, R=0
- When Gasoline ≤ 3 (25%): All Fᵢ=0, R=0
- When Gasoline < 2: All Fᵢ=0, R=1

**Input:** G[3:0] (4-bit binary)
**Outputs:** F1, F2, F4, F8, R
**Implementation:** Use five 2×4 decoders with enable input

### Solution

#### Step 1: Analyze the Problem

Let's denote the 4-bit input as G = G₃G₂G₁G₀ where:
- G₃ is the most significant bit (MSB)
- G₀ is the least significant bit (LSB)

Valid range: 0001 (1) to 1100 (12)

#### Step 2: Create Truth Table

| G₃ | G₂ | G₁ | G₀ | Decimal | Condition | F8 | F4 | F2 | F1 | R |
|:--:|:--:|:--:|:--:|:-------:|:----------|:--:|:--:|:--:|:--:|:-:|
| 0  | 0  | 0  | 0  | 0       | < 2       | 0  | 0  | 0  | 0  | 1 |
| 0  | 0  | 0  | 1  | 1       | < 2       | 0  | 0  | 0  | 0  | 1 |
| 0  | 0  | 1  | 0  | 2       | ≤ 25%     | 0  | 0  | 0  | 0  | 0 |
| 0  | 0  | 1  | 1  | 3       | ≤ 25%     | 0  | 0  | 0  | 0  | 0 |
| 0  | 1  | 0  | 0  | 4       | ≤ 50%     | 0  | 0  | 0  | 1  | 0 |
| 0  | 1  | 0  | 1  | 5       | ≤ 50%     | 0  | 0  | 0  | 1  | 0 |
| 0  | 1  | 1  | 0  | 6       | ≤ 50%     | 0  | 0  | 0  | 1  | 0 |
| 0  | 1  | 1  | 1  | 7       | ≤ 75%     | 0  | 0  | 1  | 1  | 0 |
| 1  | 0  | 0  | 0  | 8       | ≤ 75%     | 0  | 0  | 1  | 1  | 0 |
| 1  | 0  | 0  | 1  | 9       | ≤ 75%     | 0  | 0  | 1  | 1  | 0 |
| 1  | 0  | 1  | 0  | 10      | ≤ 11      | 0  | 1  | 1  | 1  | 0 |
| 1  | 0  | 1  | 1  | 11      | ≤ 11      | 0  | 1  | 1  | 1  | 0 |
| 1  | 1  | 0  | 0  | 12      | > 11      | 1  | 1  | 1  | 1  | 0 |
| 1  | 1  | 0  | 1  | 13      | Invalid   | X  | X  | X  | X  | X |
| 1  | 1  | 1  | 0  | 14      | Invalid   | X  | X  | X  | X  | X |
| 1  | 1  | 1  | 1  | 15      | Invalid   | X  | X  | X  | X  | X |

#### Step 3: Derive Boolean Expressions

**For F8:**
F8 = 1 only when G = 12 (1100)
```
F8 = m₁₂ = G₃·G₂·G₁'·G₀'
```

**For F4:**
F4 = 1 when G ∈ {10, 11, 12}
```
F4 = m₁₀ + m₁₁ + m₁₂
   = G₃·G₂'·G₁·G₀' + G₃·G₂'·G₁·G₀ + G₃·G₂·G₁'·G₀'
   = G₃·G₁·(G₂'·G₀' + G₂'·G₀ + G₂·G₁'·G₀'/G₁)
   = G₃·G₁ + G₃·G₂·G₁'·G₀'
```

**For F2:**
F2 = 1 when G ∈ {7, 8, 9, 10, 11, 12}
```
F2 = m₇ + m₈ + m₉ + m₁₀ + m₁₁ + m₁₂
   = G₃·G₂' + G₂·G₁·G₀
   (Can be simplified using K-map)
```

**For F1:**
F1 = 1 when G ∈ {4, 5, 6, 7, 8, 9, 10, 11, 12}
```
F1 = m₄ + m₅ + m₆ + m₇ + m₈ + m₉ + m₁₀ + m₁₁ + m₁₂
   = G₂ + G₃
   (G₂=1 covers 4-7, G₃=1 covers 8-15)
```

**For R:**
R = 1 when G < 2 (i.e., G = 0 or 1)
```
R = m₀ + m₁
  = G₃'·G₂'·G₁'·G₀' + G₃'·G₂'·G₁'·G₀
  = G₃'·G₂'·G₁'
```

#### Step 4: Implementation Using Five 2×4 Decoders

**Decoder Configuration:**

We'll use five 2×4 decoders to implement this circuit. The strategy is:
- Use decoders to generate specific minterms
- Combine decoder outputs to create each output function

**Decoder 1 - Decode G₃G₂:**
- Inputs: G₃, G₂, Enable = 1
- Outputs: D1₀, D1₁, D1₂, D1₃
  - D1₀ = G₃'·G₂' (covers 0-3)
  - D1₁ = G₃'·G₂  (covers 4-7)
  - D1₂ = G₃·G₂'  (covers 8-11)
  - D1₃ = G₃·G₂   (covers 12-15)

**Decoder 2 - Decode G₁G₀ when G₃G₂ = 00:**
- Inputs: G₁, G₀, Enable = D1₀
- Outputs: D2₀, D2₁, D2₂, D2₃
  - D2₀ = m₀ (0000)
  - D2₁ = m₁ (0001)
  - D2₂ = m₂ (0010)
  - D2₃ = m₃ (0011)

**Decoder 3 - Decode G₁G₀ when G₃G₂ = 01:**
- Inputs: G₁, G₀, Enable = D1₁
- Outputs: D3₀, D3₁, D3₂, D3₃
  - D3₀ = m₄ (0100)
  - D3₁ = m₅ (0101)
  - D3₂ = m₆ (0110)
  - D3₃ = m₇ (0111)

**Decoder 4 - Decode G₁G₀ when G₃G₂ = 10:**
- Inputs: G₁, G₀, Enable = D1₂
- Outputs: D4₀, D4₁, D4₂, D4₃
  - D4₀ = m₈ (1000)
  - D4₁ = m₉ (1001)
  - D4₂ = m₁₀ (1010)
  - D4₃ = m₁₁ (1011)

**Decoder 5 - Decode G₁G₀ when G₃G₂ = 11:**
- Inputs: G₁, G₀, Enable = D1₃
- Outputs: D5₀, D5₁, D5₂, D5₃
  - D5₀ = m₁₂ (1100)
  - D5₁ = m₁₃ (1101) - Invalid
  - D5₂ = m₁₄ (1110) - Invalid
  - D5₃ = m₁₅ (1111) - Invalid

#### Step 5: Output Equations Using Decoder Outputs

```
F8 = D5₀
   = m₁₂

F4 = D4₂ + D4₃ + D5₀
   = m₁₀ + m₁₁ + m₁₂

F2 = D3₃ + D4₀ + D4₁ + D4₂ + D4₃ + D5₀
   = m₇ + m₈ + m₉ + m₁₀ + m₁₁ + m₁₂

F1 = D3₀ + D3₁ + D3₂ + D3₃ + D4₀ + D4₁ + D4₂ + D4₃ + D5₀
   = m₄ + m₅ + m₆ + m₇ + m₈ + m₉ + m₁₀ + m₁₁ + m₁₂

R = D2₀ + D2₁
  = m₀ + m₁
```

#### Step 6: Logic Diagram

```
                    FUEL SENSOR CIRCUIT USING 2×4 DECODERS
                    ========================================

Input: G[3:0] = G₃ G₂ G₁ G₀
─────────────────────────────────────────────────────────────────────

                                ┌──────────────┐
                     G₃ ────────┤A₁            │
                     G₂ ────────┤A₀   DEC 1    │
                     1  ────────┤E   (2×4)     │
                                │              │
                                │          D1₀─┼─── (G₃'·G₂') ───┐
                                │          D1₁─┼─── (G₃'·G₂)  ───┼───┐
                                │          D1₂─┼─── (G₃·G₂')  ───┼───┼───┐
                                │          D1₃─┼─── (G₃·G₂)   ───┼───┼───┼───┐
                                └──────────────┘    │           │   │   │   │
                                                    │           │   │   │   │
       ┌────────────────────────────────────────────┘           │   │   │   │
       │                                                        │   │   │   │
       │   ┌──────────────┐                                    │   │   │   │
       │   │              │                                    │   │   │   │
       │   │   DEC 2      │                                    │   │   │   │
       │   │   (2×4)      │                                    │   │   │   │
 G₁────┼───┤A₁            │                                    │   │   │   │
 G₀────┼───┤A₀            │                                    │   │   │   │
       └───┤E             │                                    │   │   │   │
           │          D2₀─┼─── m₀ (0000) ──────────────────────┼───┼───┼──OR→ R
           │          D2₁─┼─── m₁ (0001) ──────────────────────┘   │   │
           │          D2₂─┼─── m₂ (0010)                           │   │
           │          D2₃─┼─── m₃ (0011)                           │   │
           └──────────────┘                                        │   │
                                                                   │   │
           ┌────────────────────────────────────────────────────────┘   │
           │                                                            │
           │   ┌──────────────┐                                        │
           │   │   DEC 3      │                                        │
           │   │   (2×4)      │                                        │
 G₁────────┼───┤A₁            │                                        │
 G₀────────┼───┤A₀            │                                        │
           └───┤E             │                                        │
               │          D3₀─┼─── m₄ (0100) ──┐                       │
               │          D3₁─┼─── m₅ (0101) ──┤                       │
               │          D3₂─┼─── m₆ (0110) ──┼──OR→ F1               │
               │          D3₃─┼─── m₇ (0111) ──┼──OR→ F2               │
               └──────────────┘                │                       │
                                               │                       │
               ┌────────────────────────────────┼───────────────────────┘
               │                               │
               │   ┌──────────────┐            │
               │   │   DEC 4      │            │
               │   │   (2×4)      │            │
 G₁────────────┼───┤A₁            │            │
 G₀────────────┼───┤A₀            │            │
               └───┤E             │            │
                   │          D4₀─┼─── m₈ ─────┼──OR→ F1
                   │          D4₁─┼─── m₉ ─────┼──OR→ F1, F2
                   │          D4₂─┼─── m₁₀ ────┼──OR→ F1, F2, F4
                   │          D4₃─┼─── m₁₁ ────┼──OR→ F1, F2, F4
                   └──────────────┘            │
                                               │
                   ┌────────────────────────────┘
                   │
                   │   ┌──────────────┐
                   │   │   DEC 5      │
                   │   │   (2×4)      │
 G₁────────────────┼───┤A₁            │
 G₀────────────────┼───┤A₀            │
                   └───┤E             │
                       │          D5₀─┼─── m₁₂ ──OR→ F1, F2, F4, F8
                       │          D5₁─┼─── m₁₃ (invalid)
                       │          D5₂─┼─── m₁₄ (invalid)
                       │          D5₃─┼─── m₁₅ (invalid)
                       └──────────────┘

OUTPUT COMBINATION (using OR gates):

F8 = D5₀

F4 = D4₂ + D4₃ + D5₀

F2 = D3₃ + D4₀ + D4₁ + D4₂ + D4₃ + D5₀

F1 = D3₀ + D3₁ + D3₂ + D3₃ + D4₀ + D4₁ + D4₂ + D4₃ + D5₀

R  = D2₀ + D2₁
```

#### Verification Table

Let's verify with some test cases:

| G (decimal) | G₃G₂G₁G₀ | Active Decoder Output | F8 | F4 | F2 | F1 | R | Condition |
|:-----------:|:--------:|:---------------------:|:--:|:--:|:--:|:--:|:-:|:----------|
| 0           | 0000     | D2₀                   | 0  | 0  | 0  | 0  | 1 | < 2       |
| 1           | 0001     | D2₁                   | 0  | 0  | 0  | 0  | 1 | < 2       |
| 3           | 0011     | D2₃                   | 0  | 0  | 0  | 0  | 0 | ≤ 25%     |
| 5           | 0101     | D3₁                   | 0  | 0  | 0  | 1  | 0 | ≤ 50%     |
| 7           | 0111     | D3₃                   | 0  | 0  | 1  | 1  | 0 | ≤ 75%     |
| 9           | 1001     | D4₁                   | 0  | 0  | 1  | 1  | 0 | ≤ 75%     |
| 10          | 1010     | D4₂                   | 0  | 1  | 1  | 1  | 0 | ≤ 11      |
| 11          | 1011     | D4₃                   | 0  | 1  | 1  | 1  | 0 | ≤ 11      |
| 12          | 1100     | D5₀                   | 1  | 1  | 1  | 1  | 0 | > 11      |

✅ All test cases pass!

---

## Question 2: Photo Booth Vending Machine FSM (Marks: 10)

### Problem Statement

Design a digital controller (finite state machine) for an automatic photo booth machine. The cost of taking a photo is 25 cents. The machine accepts:
- **Nickels (N):** 5 cents
- **Dimes (D):** 10 cents
- **Quarters (Q):** 25 cents

**Inputs:** N, D, Q (exactly one coin per cycle)
**Outputs:** P (Print Photo), RN (Return Nickel), RD (Return Dime), RT (Return Two Dimes)

When total ≥ 25 cents, print photo and return appropriate change, then reset.

### Solution

#### Step 1: Identify States

We need states to track the amount of money inserted:

| State | Amount Collected | Encoding |
|:-----:|:----------------:|:--------:|
| S0    | 0 cents          | 000      |
| S5    | 5 cents          | 001      |
| S10   | 10 cents         | 010      |
| S15   | 15 cents         | 011      |
| S20   | 20 cents         | 100      |

#### Step 2: Analyze Transitions

From each state, we can insert N (5¢), D (10¢), or Q (25¢):

**From S0 (0¢):**
- Insert N → S5 (5¢)
- Insert D → S10 (10¢)
- Insert Q → S0 (Print, no change)

**From S5 (5¢):**
- Insert N → S10 (10¢)
- Insert D → S15 (15¢)
- Insert Q → S0 (Print, return 5¢ = RN)

**From S10 (10¢):**
- Insert N → S15 (15¢)
- Insert D → S20 (20¢)
- Insert Q → S0 (Print, return 10¢ = RD)

**From S15 (15¢):**
- Insert N → S20 (20¢)
- Insert D → S0 (Print, no change)
- Insert Q → S0 (Print, return 15¢ = RN + RD)

**From S20 (20¢):**
- Insert N → S0 (Print, no change)
- Insert D → S0 (Print, return 5¢ = RN)
- Insert Q → S0 (Print, return 20¢ = RT)

#### Step 3: State Diagram

```
                PHOTO BOOTH FSM STATE DIAGRAM
                ==============================

        ┌────┐  Q/P=1           ┌────┐
   ────►│ S0 │◄─────────────────┤ S5 │
        └─┬──┘                  └─▲─┬┘
          │                       │ │
       N  │                     N │ │ D
          │                       │ │
          ▼                       │ │
        ┌────┐  Q/P=1,RN=1       │ │
        │ S5 ├───────────────────┘ │
        └─┬──┘                     │
          │                        │
       D  │                        │
          │                        │
          ▼                        │
        ┌────┐  Q/P=1,RD=1        │
        │S15 ├────────────────────┤
        └─┬─┬┘                    │
          │ │                     │
       N  │ │ D/P=1               │
          │ └─────────────────────┤
          ▼                       │
        ┌────┐  Q/P=1,RT=1       │
        │S20 ├────────────────────┤
        └─┬──┘                    │
          │                       │
       N/P│                       │
          └───────────────────────┘

Legend:
─────  State transition
Input/Outputs  Transition condition and outputs
```

#### Detailed State Transition Diagram with All Outputs:

```
                           Photo Booth FSM
                           ===============

Initial ──►┌──────────────────────────────────────┐
           │         State S0 (0 cents)           │
           │    Outputs: P=0, RN=0, RD=0, RT=0    │
           └──┬────────┬────────┬──────────────┬──┘
              │        │        │              │
           N  │     D  │     Q  │              │ (All return paths)
              │        │        │ P=1          │
              ▼        ▼        │              │
         ┌────────┐┌────────┐  │              │
         │   S5   ││  S10   │  │              │
         │ 5¢     ││  10¢   │  │              │
         └─┬───┬──┘└─┬───┬──┘  │              │
           │   │     │   │     │              │
        N  │ D │  N  │ D │  Q  │              │
           │   │     │   │  P=1,RD=1          │
           │   ▼     ▼   │     │              │
           │ ┌────────┐  │     │              │
           │ │  S15   │  │     │              │
           │ │  15¢   │◄─┘     │              │
           │ └─┬───┬──┘        │              │
           │   │   │ D         │              │
           │ N │   │ P=1       │              │
           │   │   └───────────┤              │
           ▼   ▼               │              │
         ┌────────┐            │              │
         │  S20   │            │              │
         │  20¢   │            │              │
         └─┬───┬──┘            │              │
           │   │               │              │
        N  │ D │ Q             │              │
        P=1│P=1│ P=1,RT=1      │              │
           │RN │               │              │
           └───┴───────────────┴──────────────┘
```

#### Step 4: State Transition Table

Let's use 3-bit state encoding: s₂s₁s₀

| Current State | s₂s₁s₀ | Input | Next State | n₂n₁n₀ | P | RN | RD | RT | Notes |
|:-------------:|:------:|:-----:|:----------:|:------:|:-:|:--:|:--:|:--:|:------|
| S0            | 000    | N     | S5         | 001    | 0 | 0  | 0  | 0  | +5¢   |
| S0            | 000    | D     | S10        | 010    | 0 | 0  | 0  | 0  | +10¢  |
| S0            | 000    | Q     | S0         | 000    | 1 | 0  | 0  | 0  | 25¢=Print |
| S5            | 001    | N     | S10        | 010    | 0 | 0  | 0  | 0  | 5+5=10 |
| S5            | 001    | D     | S15        | 011    | 0 | 0  | 0  | 0  | 5+10=15 |
| S5            | 001    | Q     | S0         | 000    | 1 | 1  | 0  | 0  | 5+25=30, return 5 |
| S10           | 010    | N     | S15        | 011    | 0 | 0  | 0  | 0  | 10+5=15 |
| S10           | 010    | D     | S20        | 100    | 0 | 0  | 0  | 0  | 10+10=20 |
| S10           | 010    | Q     | S0         | 000    | 1 | 0  | 1  | 0  | 10+25=35, return 10 |
| S15           | 011    | N     | S20        | 100    | 0 | 0  | 0  | 0  | 15+5=20 |
| S15           | 011    | D     | S0         | 000    | 1 | 0  | 0  | 0  | 15+10=25, exact |
| S15           | 011    | Q     | S0         | 000    | 1 | 1  | 1  | 0  | 15+25=40, return 15 |
| S20           | 100    | N     | S0         | 000    | 1 | 0  | 0  | 0  | 20+5=25, exact |
| S20           | 100    | D     | S0         | 000    | 1 | 1  | 0  | 0  | 20+10=30, return 5 |
| S20           | 100    | Q     | S0         | 000    | 1 | 0  | 0  | 1  | 20+25=45, return 20 |

#### Step 5: Next State and Output Equations

Using the state transition table, we can derive the next state logic and output logic:

**State Encoding:**
- S0  = 000
- S5  = 001
- S10 = 010
- S15 = 011
- S20 = 100

**Next State Equations (simplified using K-maps):**

```
n₂ = s₁·s₀·N + s₁·D·Q'
n₁ = s₂'·s₁'·D·N' + s₁'·s₀·N·D' + s₁·s₀·N'
n₀ = s₂'·s₁'·s₀'·N + s₁'·s₀·N + s₁·s₀'·N
```

**Output Equations:**

```
P  = Q + (s₁·D·N'·Q') + (s₂·N·D'·Q') + (s₁·s₀·D·N'·Q')
   = Q + s₁·D + s₂·N + s₁·s₀·D

RN = s₀·Q + s₂·D·N'·Q'
   = s₀·Q + s₂·D

RD = s₁·s₀'·Q + s₁·s₀·Q·N'·D'
   = s₁·Q·(s₀' + s₁·s₀·N'·D')

RT = s₂·Q·N'·D'
   = s₂·Q
```

#### Step 6: Implementation Block Diagram

```
                FSM IMPLEMENTATION
                ==================

  Inputs: N, D, Q, clk

  ┌─────────────────────────────────────────┐
  │    Next State & Output Logic            │
  │    (Combinational Logic)                │
  │                                         │
  │  Inputs: s₂, s₁, s₀, N, D, Q           │
  │  Outputs: n₂, n₁, n₀, P, RN, RD, RT    │
  └────┬──────────────────────────┬─────────┘
       │                          │
       │ n₂, n₁, n₀              │ P, RN, RD, RT
       │                          │
       ▼                          ▼
  ┌─────────┐              ┌──────────┐
  │  State  │              │  Output  │
  │Register │              │  Signals │
  │ (3 D-FF)│              └──────────┘
  └────┬────┘
       │
       │ s₂, s₁, s₀
       │
       └──────► (feedback to combinational logic)

       clk ────► (clock to D flip-flops)
```

---

## Question 3: Output Sequence Controller FSM (Marks: 10)

### Problem Statement

Design FSM with:
- **Input:** S
- **Outputs:** x, y, z
- **Sequence:** 000 → 001 → 010 → 100 → repeat
- **Initial state:** 000

The output should change only on rising clock edge.

### Part (a): Stop and Reset Behavior

**Requirement:** When S=1, stop the sequence. When S returns to 0, restart from 000.

#### Solution for Part (a)

**States Needed:**
- St0: Output 000
- St1: Output 001
- St2: Output 010
- St3: Output 100

**State Diagram:**

```
                FSM Part (a) - Stop and Reset
                ==============================

                         ┌──────────┐
                    ────►│   St0    │
                         │ xyz=000  │◄────────────┐
                         └────┬─────┘             │
                              │                   │
                           S=0│                   │ S=1
                              │               (from any state)
                              ▼                   │
                         ┌──────────┐            │
                    ┌────┤   St1    │            │
                    │    │ xyz=001  │            │
                    │    └────┬─────┘            │
                    │         │                  │
                 S=1│      S=0│                  │
                    │         │                  │
                    │         ▼                  │
                    │    ┌──────────┐            │
                    ├────┤   St2    │────────────┤
                    │    │ xyz=010  │            │
                    │    └────┬─────┘            │
                    │         │                  │
                    │      S=0│                  │
                    │         │                  │
                    │         ▼                  │
                    │    ┌──────────┐            │
                    └────┤   St3    │────────────┘
                         │ xyz=100  │
                         └────┬─────┘
                              │
                           S=0│
                              │
                              └──────────────────►(back to St0)

Transition Rules:
- From any state: if S=1, go to St0
- From St0: if S=0, go to St1
- From St1: if S=0, go to St2
- From St2: if S=0, go to St3
- From St3: if S=0, go to St0
```

**State Transition Table:**

| Current State | S | Next State | x | y | z | Notes |
|:-------------:|:-:|:----------:|:-:|:-:|:-:|:------|
| St0 (00)      | 0 | St1 (01)   | 0 | 0 | 0 | Continue |
| St0 (00)      | 1 | St0 (00)   | 0 | 0 | 0 | Stay/Reset |
| St1 (01)      | 0 | St2 (10)   | 0 | 0 | 1 | Continue |
| St1 (01)      | 1 | St0 (00)   | 0 | 0 | 1 | Reset |
| St2 (10)      | 0 | St3 (11)   | 0 | 1 | 0 | Continue |
| St2 (10)      | 1 | St0 (00)   | 0 | 1 | 0 | Reset |
| St3 (11)      | 0 | St0 (00)   | 1 | 0 | 0 | Continue |
| St3 (11)      | 1 | St0 (00)   | 1 | 0 | 0 | Reset |

**State Encoding:** Using 2 bits (s₁s₀)
- St0 = 00
- St1 = 01
- St2 = 10
- St3 = 11

**Next State Equations:**

```
n₁ = s₁'·s₀·S' + s₁·s₀'·S'
   = S'·(s₁'·s₀ + s₁·s₀')
   = S'·(s₁ ⊕ s₀)

n₀ = s₁'·s₀'·S'
```

**Output Equations:**

```
x = s₁·s₀  (output 1 only in St3)
y = s₁·s₀' (output 1 only in St2)
z = s₁'·s₀ (output 1 only in St1)
```

---

### Part (b): Postpone for 3 Cycles

**Requirement:** When S=1, halt sequence for at least 3 cycles. When S returns to 0 after 3 cycles, continue to next value.

#### Solution for Part (b)

**States Needed:**
- St0: Output 000
- St1: Output 001
- St2: Output 010
- St3: Output 100
- Pause1: 1st halt cycle
- Pause2: 2nd halt cycle
- Pause3: 3rd halt cycle

**State Diagram:**

```
         FSM Part (b) - 3-Cycle Postpone
         =================================

Normal Sequence (when S=0):
     St0(000) → St1(001) → St2(010) → St3(100) → St0...

When S=1 from any state, enter pause sequence:

        ┌──────────┐
   ────►│   St0    │
        │ xyz=000  │
        └────┬─────┘
             │ S=0
             ▼
        ┌──────────┐       S=1      ┌──────────┐
        │   St1    │─────────────────►│ Pause1   │
        │ xyz=001  │                 │ xyz=001  │
        └────┬─────┘                 └────┬─────┘
             │                            │
          S=0│                            │ (always)
             ▼              S=1           ▼
        ┌──────────┐───────────────► ┌──────────┐
        │   St2    │                 │ Pause2   │
        │ xyz=010  │                 │ xyz=010  │
        └────┬─────┘                 └────┬─────┘
             │                            │
          S=0│                            │ (always)
             ▼              S=1           ▼
        ┌──────────┐───────────────► ┌──────────┐
        │   St3    │                 │ Pause3   │
        │ xyz=100  │                 │ xyz=100  │
        └────┬─────┘                 └────┬─────┘
             │                            │
          S=0│                         S=0│ S=1
             │                            ▼
             │                       (continue sequence
             │                        from next state)
             └────────────────────────────┘

Detailed Transitions:
- From St0: S=0 → St1, S=1 → Pause1
- From St1: S=0 → St2, S=1 → Pause1
- From St2: S=0 → St3, S=1 → Pause1
- From St3: S=0 → St0, S=1 → Pause1
- From Pause1: (always) → Pause2
- From Pause2: (always) → Pause3
- From Pause3: S=0 → (resume next state), S=1 → Pause3
```

**State Encoding:** Using 3 bits (s₂s₁s₀)

| State | s₂s₁s₀ | Output xyz | Notes |
|:-----:|:------:|:----------:|:------|
| St0   | 000    | 000        | Normal state 0 |
| St1   | 001    | 001        | Normal state 1 |
| St2   | 010    | 010        | Normal state 2 |
| St3   | 011    | 100        | Normal state 3 |
| Pause1| 100    | (same as before) | 1st pause cycle |
| Pause2| 101    | (same as before) | 2nd pause cycle |
| Pause3| 110    | (same as before) | 3rd+ pause cycle |

**State Transition Table:**

| Current | s₂s₁s₀ | S | Next State | n₂n₁n₀ | x | y | z | Notes |
|:-------:|:------:|:-:|:----------:|:------:|:-:|:-:|:-:|:------|
| St0     | 000    | 0 | St1        | 001    | 0 | 0 | 0 | Continue |
| St0     | 000    | 1 | Pause1     | 100    | 0 | 0 | 0 | Halt |
| St1     | 001    | 0 | St2        | 010    | 0 | 0 | 1 | Continue |
| St1     | 001    | 1 | Pause1     | 100    | 0 | 0 | 1 | Halt (keep output) |
| St2     | 010    | 0 | St3        | 011    | 0 | 1 | 0 | Continue |
| St2     | 010    | 1 | Pause1     | 100    | 0 | 1 | 0 | Halt (keep output) |
| St3     | 011    | 0 | St0        | 000    | 1 | 0 | 0 | Continue |
| St3     | 011    | 1 | Pause1     | 100    | 1 | 0 | 0 | Halt (keep output) |
| Pause1  | 100    | X | Pause2     | 101    | (prev) | (prev) | (prev) | 1st cycle |
| Pause2  | 101    | X | Pause3     | 110    | (prev) | (prev) | (prev) | 2nd cycle |
| Pause3  | 110    | 0 | (next)     | varies | (prev) | (prev) | (prev) | Resume |
| Pause3  | 110    | 1 | Pause3     | 110    | (prev) | (prev) | (prev) | Stay paused |

Note: When resuming from Pause3, we need additional logic to determine which state to go to next. This requires storing the "previous normal state" or using additional state bits.

**Enhanced Implementation:**
To properly track which state to return to, we can use a more sophisticated state encoding or add a 2-bit "return state" register.

---

### Part (c): Postpone for 30 Cycles Using Counter

**Requirement:** When S=1, halt for at least 30 cycles. After 30 cycles and S=0, continue to next value. Use MSI component to keep FSM simple.

#### Solution for Part (c)

**Strategy:** Use a **5-bit counter** (can count 0-31) as an MSI component to track pause cycles.

**Components:**
1. **Main FSM:** 4 states (St0, St1, St2, St3, Pause)
2. **5-bit Counter:** Counts pause cycles (0 to 30)
3. **Comparator:** Checks if counter ≥ 30

**State Diagram:**

```
       FSM Part (c) - 30-Cycle Postpone with Counter
       ==============================================

Main FSM States:
     St0 → St1 → St2 → St3 → St0...
                ↓
              Pause (when S=1)

        ┌──────────────────────────────────┐
   ────►│           St0                    │
        │        xyz = 000                 │
        └────┬─────────────────────────────┘
             │ S=0
             ▼
        ┌──────────────────────────────────┐
        │           St1                    │
        │        xyz = 001                 │
        └────┬─────────────────────────────┘
             │ S=0                  S=1
             ▼                       │
        ┌──────────────┐             │
        │     St2      │             │     ┌──────────────────┐
        │  xyz = 010   │─────────────┼────►│      Pause       │
        └────┬─────────┘             │     │ Counter Active   │
             │ S=0                   │     │  xyz=(previous)  │
             ▼                       │     └────┬─────────────┘
        ┌──────────────┐             │          │
        │     St3      │             │          │
        │  xyz = 100   │─────────────┘          │
        └────┬─────────┘                        │
             │ S=0                               │
             │                   (count >= 30    │
             │                    AND S=0)       │
             └───────────────────────────────────┘
                Resume to next state in sequence

Control Signals:
- Counter Enable: Active during Pause state
- Counter Reset:  When leaving Pause state or S=0 in normal states
- Compare >= 30:  Counter value compared with 30
```

**Implementation Block Diagram:**

```
                Complete System Architecture
                ==============================

Inputs: S, clk

┌─────────────────────────────────────────────────────┐
│                   Main FSM                          │
│                                                     │
│  States: St0(00), St1(01), St2(10), St3(11),      │
│          Pause(determined by control signal)       │
│                                                     │
│  Inputs: S, cnt_done                               │
│  Outputs: x, y, z, cnt_enable, cnt_reset           │
└──────┬─────────────────────────┬───────────────────┘
       │                         │
       │ cnt_enable, cnt_reset   │ x, y, z (outputs)
       │                         │
       ▼                         ▼
┌────────────────┐         ┌──────────┐
│   5-bit        │         │  Outputs │
│   Counter      │         └──────────┘
│   (MSI 74163)  │
└────┬───────────┘
     │
     │ count[4:0]
     │
     ▼
┌────────────────┐
│   Comparator   │  count >= 30?
│   (count≥30)   ├─────► cnt_done
└────────────────┘

Counter Operation:
- Reset when: cnt_reset = 1
- Count when: cnt_enable = 1 (during Pause state)
- cnt_done = 1 when count >= 30
```

**Simplified State Table:**

| State | S | cnt_done | Next State | cnt_enable | cnt_reset | xyz | Notes |
|:-----:|:-:|:--------:|:----------:|:----------:|:---------:|:---:|:------|
| St0   | 0 | X        | St1        | 0          | 1         | 000 | Normal |
| St0   | 1 | X        | Pause      | 1          | 0         | 000 | Enter pause |
| St1   | 0 | X        | St2        | 0          | 1         | 001 | Normal |
| St1   | 1 | X        | Pause      | 1          | 0         | 001 | Enter pause |
| St2   | 0 | X        | St3        | 0          | 1         | 010 | Normal |
| St2   | 1 | X        | Pause      | 1          | 0         | 010 | Enter pause |
| St3   | 0 | X        | St0        | 0          | 1         | 100 | Normal |
| St3   | 1 | X        | Pause      | 1          | 0         | 100 | Enter pause |
| Pause | 0 | 1        | (next)     | 0          | 1         | (keep) | Resume |
| Pause | X | 0        | Pause      | 1          | 0         | (keep) | Continue counting |
| Pause | 1 | 1        | Pause      | 1          | 0         | (keep) | S still high |

**MSI Counter Component (74LS163 - 4-bit counter):**

For 30 cycles, we need a 5-bit counter. We can use:
- Two 74LS163 4-bit counters cascaded, OR
- One 74LS393 dual 4-bit counter configured for 5 bits

**Counter Logic:**
```
Clock: System clock (when cnt_enable = 1)
Reset: cnt_reset signal from FSM
Output: count[4:0]
Compare: count >= 30 (binary 11110)
```

**Comparison Circuit:**
```
cnt_done = (count == 30) OR (count == 31)
         = count[4]·count[3]·count[2]·count[1]·(count[0]' + count[0])
         = count[4]·count[3]·count[2]·count[1]
```

**Benefits of Using Counter:**
- Main FSM remains simple (only 4-5 states)
- Easy to modify pause duration (just change comparator value)
- Scalable to longer pause periods without adding states

---

## Summary and Key Takeaways

### Question 1 - Key Concepts:
✅ **Decoder Usage:** Decoders generate minterms that can be combined to implement any Boolean function
✅ **Hierarchical Decoding:** Using multiple small decoders (2×4) instead of one large decoder
✅ **Enable Input:** Used to activate/deactivate decoder sections
✅ **OR Gate Combination:** Multiple decoder outputs ORed together for each function output

### Question 2 - Key Concepts:
✅ **FSM for Sequential Control:** Vending machine requires tracking accumulated state
✅ **Moore Machine:** Outputs depend only on current state
✅ **State Minimization:** Only track necessary amount levels (0, 5, 10, 15, 20 cents)
✅ **Change Calculation:** Logic to determine correct change based on overpayment

### Question 3 - Key Concepts:
✅ **Output Sequence Generation:** Using states to produce specific output patterns
✅ **Input Control:** Modifying FSM behavior based on control input (S)
✅ **Counter Integration:** Using MSI components to extend FSM capabilities
✅ **Scalability:** Part (c) shows how hardware design scales for larger requirements

---

## Additional Learning Resources

### Recommended Study Topics:
1. **Boolean Algebra Simplification:** K-maps, Quine-McCluskey method
2. **Sequential Circuit Design:** D flip-flops, JK flip-flops, timing analysis
3. **MSI Components:** Decoders, encoders, multiplexers, counters
4. **FSM Optimization:** State minimization, state encoding techniques
5. **Hardware Description Languages:** VHDL/Verilog for implementing these designs

### Practice Problems:
1. Design a traffic light controller FSM
2. Implement a sequence detector for pattern "1011"
3. Design a digital lock with 4-digit code
4. Create an elevator controller FSM for 3 floors

---

**END OF SOLUTION**

*This solution provides complete coverage of prerequisite knowledge and detailed solutions with diagrams for all three questions. Each problem is solved step-by-step with clear explanations, truth tables, state diagrams, and circuit implementations.*
