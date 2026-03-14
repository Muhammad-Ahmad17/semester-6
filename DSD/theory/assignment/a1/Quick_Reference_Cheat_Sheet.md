# Quick Reference Cheat Sheet
## Digital System Design Assignment 1

---

## 🎯 Question 1: Fuel Sensor - Key Points

### Input/Output Summary
```
INPUT:  G[3:0] = 4-bit fuel level (0-12 decimal)
OUTPUT: F8, F4, F2, F1 (indicators), R (reserve)
```

### Fuel Level Ranges
| Decimal | Condition | F8 | F4 | F2 | F1 | R | Display Pattern |
|---------|-----------|----|----|----|----|---|-----------------|
| 12      | > 11      | 1  | 1  | 1  | 1  | 0 | ████ Full       |
| 10-11   | ≤ 11, >9  | 0  | 1  | 1  | 1  | 0 | ███░ 75%        |
| 7-9     | ≤ 9, >6   | 0  | 0  | 1  | 1  | 0 | ██░░ 50%        |
| 4-6     | ≤ 6, >3   | 0  | 0  | 0  | 1  | 0 | █░░░ 25%        |
| 2-3     | ≤ 3       | 0  | 0  | 0  | 0  | 0 | ░░░░ Empty      |
| 0-1     | < 2       | 0  | 0  | 0  | 0  | 1 | 🚨 RESERVE      |

### Simplified Boolean Equations
```
F8 = G₃·G₂·G₁'·G₀'                    (only minterm 12)
F4 = G₃·G₁ + G₃·G₂·G₁'·G₀'           (minterms 10,11,12)
F2 = G₃·G₂' + G₂·G₁·G₀                (minterms 7-12)
F1 = G₂ + G₃                          (minterms 4-12)
R  = G₃'·G₂'·G₁'                      (minterms 0,1)
```

### Decoder Implementation Strategy
```
5 Decoders total:
- 1 Master decoder (G₃G₂) → 4 enables for sub-decoders
- 4 Sub-decoders (G₁G₀) → Generate 16 minterms (m₀-m₁₅)
- Combine with OR gates to create outputs
```

---

## 🎯 Question 2: Photo Booth FSM - Key Points

### State Summary
| State | Amount | Next on N | Next on D | Next on Q | Change Logic |
|-------|--------|-----------|-----------|-----------|--------------|
| S0    | 0¢     | S5        | S10       | S0 (P=1)  | Exact        |
| S5    | 5¢     | S10       | S15       | S0 (P,RN) | Return 5¢    |
| S10   | 10¢    | S15       | S20       | S0 (P,RD) | Return 10¢   |
| S15   | 15¢    | S20       | S0 (P)    | S0 (P,RN,RD) | Return 15¢|
| S20   | 20¢    | S0 (P)    | S0 (P,RN) | S0 (P,RT) | Return 20¢   |

### Quick Decision Tree
```
If total = 25¢ → Print, no change
If total = 30¢ → Print, return 1 nickel
If total = 35¢ → Print, return 1 dime
If total = 40¢ → Print, return 1 nickel + 1 dime
If total = 45¢ → Print, return 2 dimes (RT=1)
```

### State Encoding
```
S0  = 000  (0 cents)
S5  = 001  (5 cents)
S10 = 010  (10 cents)
S15 = 011  (15 cents)
S20 = 100  (20 cents)

Need 3 flip-flops (2³ = 8 states, using 5)
```

---

## 🎯 Question 3: Sequence Controller - Key Points

### Base Sequence (All Parts)
```
State   Output (xyz)
────────────────────
St0  →  000
St1  →  001
St2  →  010
St3  →  100
St0  →  000 (repeat)
```

### Part (a): Stop/Reset
```
Behavior: S=1 → Reset to 000
         S=0 → Continue sequence

Example:
000 → 001 → [S=1] → 000 → 000 → [S=0] → 001 → 010...
          RESET!              START!
```

### Part (b): 3-Cycle Postpone
```
Behavior: S=1 → Pause for minimum 3 cycles
         S=0 after 3+ cycles → Continue

States needed: St0, St1, St2, St3, Pause1, Pause2, Pause3
Total: 7 states → 3 flip-flops

Example:
000 → 001 → [S=1] → 001 → 001 → 001 → [S=0] → 010 → 100...
          PAUSE (frozen)    3 cycles    RESUME!
```

### Part (c): 30-Cycle Postpone with Counter
```
Components:
- Main FSM: 4 states (St0-St3) + Pause
- 5-bit counter: Counts 0-31
- Comparator: Checks count ≥ 30

Logic:
When S=1 → Enter Pause, enable counter
Counter counts each clock cycle
When count=30 AND S=0 → Resume sequence
Output stays frozen during pause
```

---

## 📐 Essential Formulas

### Number of Flip-Flops
```
For N states: need ⌈log₂(N)⌉ flip-flops

2-4 states   → 2 FF
5-8 states   → 3 FF
9-16 states  → 4 FF
17-32 states → 5 FF
```

### Decoder Outputs
```
2×4 Decoder with Enable E, inputs A₁A₀:
D₀ = E·A₁'·A₀'
D₁ = E·A₁'·A₀
D₂ = E·A₁·A₀'
D₃ = E·A₁·A₀
```

### Binary to Decimal
```
0000 = 0    0100 = 4    1000 = 8     1100 = 12
0001 = 1    0101 = 5    1001 = 9     1101 = 13
0010 = 2    0110 = 6    1010 = 10    1110 = 14
0011 = 3    0111 = 7    1011 = 11    1111 = 15
```

---

## ✅ Common Solution Patterns

### Truth Table Format
```
┌────────┬────────┬────────┐
│ Inputs │ States │ Outputs│
├────────┼────────┼────────┤
│   00   │   S0   │  xyz   │
│   01   │   S1   │  xyz   │
└────────┴────────┴────────┘
```

### State Diagram Elements
```
┌─────────┐
│  State  │  ← Circle for state
│ outputs │  ← Outputs inside or adjacent
└────┬────┘
     │
  input    ← Transition label
     │
     ▼
┌─────────┐
│  Next   │
│  State  │
└─────────┘
```

### FSM Implementation Block
```
┌─────────────────┐
│  Combinational  │
│     Logic       │
│                 │
│ Inputs: s, x    │
│ Outputs: n, y   │
└────┬────────┬───┘
     │        │
   n │        │ y
     ▼        ▼
┌────────┐
│  State │
│Register│
│(D-FF)  │
└────────┘
     │
   s │ (feedback)
     └──────►
```

---

## 🎓 Quick Study Checklist

Before writing your solution, make sure you can:

### For Question 1:
- [ ] Convert decimal to 4-bit binary
- [ ] Understand 2×4 decoder truth table
- [ ] Identify which decoder outputs are active for any input
- [ ] Combine multiple minterms with OR gates
- [ ] Draw decoder symbol and connections

### For Question 2:
- [ ] Identify all necessary states
- [ ] Draw complete state diagram with all transitions
- [ ] Create state transition table
- [ ] Determine correct change for any input combination
- [ ] Encode states with minimum flip-flops

### For Question 3:
- [ ] Draw basic sequence generator FSM
- [ ] Add control input (S) to modify behavior
- [ ] Understand difference between reset and pause
- [ ] Calculate required pause cycles
- [ ] Use counter for long delays

---

## 💡 Test Your Understanding

### Self-Check Questions:

**Q1:** What decoder outputs are active when G=9 (1001)?
<details>
<summary>Answer</summary>
Master decoder D1₂ (G₃=1,G₂=0), then D4₁ (G₁=0,G₀=1) → m₉
</details>

**Q2:** In photo booth, what happens if user inserts D, D, D?
<details>
<summary>Answer</summary>
S0 → S10 → S20 → S0 (print, return 5¢ nickel)
Total: 30¢, change: 5¢
</details>

**Q3:** How many states needed for 3-cycle postpone?
<details>
<summary>Answer</summary>
7 states: St0, St1, St2, St3, Pause1, Pause2, Pause3
Requires 3 flip-flops
</details>

**Q4:** Why use counter in part (c)?
<details>
<summary>Answer</summary>
Counting to 30 requires 30 states without counter.
With 5-bit counter, FSM stays simple (5 states only).
Counter handles the delay, FSM handles sequence.
</details>

---

## 🚀 Quick Tips for Each Question

### Question 1 Tips:
1. Create truth table FIRST (all 13 valid inputs)
2. Group outputs by ranges (>11, ≤11, ≤75%, etc.)
3. Draw ONE decoder fully, then replicate
4. Trace one example through entire circuit

### Question 2 Tips:
1. List states = possible amounts (0,5,10,15,20)
2. For each state, check ALL 3 coin inputs
3. Calculate total, determine if ≥25¢
4. If yes, print and calculate change
5. Draw diagram BEFORE writing table

### Question 3 Tips:
1. (a) is simplest - just add reset path
2. (b) needs 3 extra pause states
3. (c) use counter, NOT extra states
4. Show counter separately from main FSM
5. Timing diagram helps visualize behavior

---

## 📝 Solution Writing Template

### Question Format:
```
1. Problem Understanding
   - Restate requirements
   - Identify inputs/outputs

2. Approach
   - High-level strategy
   - Components needed

3. Detailed Solution
   - Truth tables
   - State diagrams
   - Boolean equations
   - Circuit diagrams

4. Verification
   - Test cases
   - Example trace-through

5. Final Answer
   - Clearly labeled circuit
```

---

**Use this cheat sheet for quick reference while solving!** 📖

Good luck! 🎓
