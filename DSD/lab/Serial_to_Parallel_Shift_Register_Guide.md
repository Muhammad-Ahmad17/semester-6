# 4-Bit Serial-to-Parallel Shift Register (S2P)

## Part 1: General Logic & Concepts

### What is a Serial-to-Parallel Shift Register?

A **Serial-to-Parallel (S2P) Shift Register** is a sequential digital circuit that:

- **Accepts data serially** (one bit at a time) through a single input line
- **Outputs data in parallel** (all bits simultaneously) on multiple output lines
- **Shifts data** through internal registers on each clock pulse
- Is used to convert slow serial communication to fast parallel processing

### 4-Bit S2P Shift Register Operation

#### Block Diagram Concept:

```
Serial_In → [D₀ | D₁ | D₂ | D₃] → Parallel Output (S[3:0])
                ↑     ↑     ↑
         Shifts right on CLK (with Shift='1')
```

#### How It Works:

**Example: Shifting in data "1011" serially**

| Clock | Serial_In | Shift | S[3] | S[2] | S[1] | S[0] | Comment                          |
| ----- | --------- | ----- | ---- | ---- | ---- | ---- | -------------------------------- |
| 0     | X         | 0     | 0    | 0    | 0    | 0    | Initial state                    |
| ↑1   | 1         | 1     | 1    | 0    | 0    | 0    | First bit (1) enters             |
| ↑2   | 0         | 1     | 0    | 1    | 0    | 0    | Second bit (0) enters            |
| ↑3   | 1         | 1     | 1    | 0    | 1    | 0    | Third bit (1) enters             |
| ↑4   | 1         | 1     | 1    | 1    | 0    | 1    | Fourth bit (1) enters - Complete |

**After 4 clock cycles:** Parallel output = **S[3:0] = "1101"** (1011 reversed due to shifting)

---

### Key Components:

1. **Serial_In**: Single input wire carrying one bit per clock cycle
2. **S[3:0]**: 4-bit register storing the shifted data
   - S[3] = Leftmost position (oldest data)
   - S[0] = Rightmost position (newest data entering)
3. **CLK**: Clock signal (rising edge triggered)
4. **Shift**: Control signal
   - Shift = '1' → Data moves
   - Shift = '0' → Data holds (no movement)

---

### Shift Operation Logic:

**When Shift = '1' on rising clock edge:**

```
S[3] ← S[2]       (S[2] moves to S[3])
S[2] ← S[1]       (S[1] moves to S[2])
S[1] ← S[0]       (S[0] moves to S[1])
S[0] ← Serial_In  (New serial data enters at S[0])
```

**When Shift = '0':**

```
S[3:0] ← S[3:0]  (No change, data held)
```

---

## Part 2: VHDL Implementation

### Architecture & Structure:

```vhdl
Entity: serial_to_parallel
  Inputs:  CLK, RESET, Shift, Serial_In
  Outputs: S(3 downto 0)
```

### Full VHDL Code:

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.all;

-- Entity Definition
entity serial_to_parallel is
    port (
        CLK         : in  STD_LOGIC;           -- Clock input (rising edge)
        RESET       : in  STD_LOGIC;           -- Asynchronous reset (active high)
        Shift       : in  STD_LOGIC;           -- Shift enable control signal
        Serial_In   : in  STD_LOGIC;           -- Serial data input (1 bit)
        S           : out STD_LOGIC_VECTOR(3 downto 0)  -- 4-bit parallel output
    );
end serial_to_parallel;

-- Architecture Definition
architecture Behavioral of serial_to_parallel is
  
    -- Internal signal to store the 4-bit register
    signal S_reg : STD_LOGIC_VECTOR(3 downto 0);
  
begin
  
    -- Main Process: Triggered on rising edge of CLK or RESET
    process(CLK, RESET)
    begin
        if RESET = '1' then
            -- Asynchronous reset: Clear all 4 bits to '0'
            S_reg <= '0000';
  
        elsif rising_edge(CLK) then
            -- On rising clock edge
            if Shift = '1' then
                -- Perform shift operation
                -- New data enters at S[0], old data exits from S[3]
                S_reg <= Serial_In & S_reg(3 downto 1);
  
                -- Breaking down the above line:
                -- S_reg(3 downto 1) = S_reg(2 downto 0) [shifted right]
                -- Serial_In & S_reg(3 downto 1) = concatenation
                -- Result: {Serial_In, S[2], S[1], S[0]}
  
            end if;
            -- If Shift = '0', S_reg maintains its current value (implicit hold)
        end if;
    end process;
  
    -- Continuous assignment: Connect internal register to output
    S <= S_reg;
  
end Behavioral;
```

---

### Line-by-Line VHDL Explanation:

#### 1. **Library & Use Clause**

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.all;
```

- Imports standard logic library for STD_LOGIC data type

#### 2. **Entity Port Declarations**

```vhdl
CLK: rising_edge(CLK) → Triggers shift operation
RESET: When RESET='1' → All bits → '0' (cleared)
Shift: When '1' → Perform shift; When '0' → Hold data
Serial_In: Single bit entering at S[0]
S: 4-bit output bus
```

#### 3. **Signal Declaration**

```vhdl
signal S_reg : STD_LOGIC_VECTOR(3 downto 0);
```

- Internal 4-bit register for storing state
- Index 3 = MSB (leftmost), Index 0 = LSB (rightmost)

#### 4. **Process Sensitivity List**

```vhdl
process(CLK, RESET)
```

- Process triggers when CLK or RESET changes

#### 5. **Reset Condition (Asynchronous)**

```vhdl
if RESET = '1' then
    S_reg <= (others => '0');
```

- When RESET active: immediately clears all bits (no clock needed)
- `(others => '0')` = Fill entire vector with zeros

#### 6. **Shift Operation (Synchronous)**

```vhdl
elsif rising_edge(CLK) then
    if Shift = '1' then
        S_reg <= Serial_In & S_reg(3 downto 1);
```

- **Only executes** on rising edge of CLK
- **Concatenation operator `&`**: Combines signals
  - `Serial_In & S_reg(3 downto 1)` = [Serial_In, S[3], S[2], S[1]]
  - This is assigned to S_reg[3:0]

**Data Flow Visualization:**

```
Before: S_reg = [S3, S2, S1, S0]
After:  S_reg = [Serial_In, S3, S2, S1]
        (S0 is discarded, new bit enters at left)
```

#### 7. **Output Assignment**

```vhdl
S <= S_reg;
```

- Continuously outputs internal register to port S

---

## Part 3: Simulation Example

### Test Scenario: Loading "1011" serially

```
Time | CLK | RESET | Shift | Serial_In | S_reg[3:0] | Notes
0ns  | ↑   | 0     | 1     | 1         | 0001       | Bit 1 enters
20ns | ↑   | 0     | 1     | 0         | 0100       | Bit 0 enters (1011 reversed)
40ns | ↑   | 0     | 1     | 1         | 1010       | Bit 1 enters
60ns | ↑   | 0     | 1     | 1         | 1101       | Bit 1 enters (Complete!)
80ns | ↑   | 0     | 0     | X         | 1101       | Shift disabled (hold)
```

---

## Part 4: VHDL Implementation Advantages

| Feature                         | Benefit                                     |
| ------------------------------- | ------------------------------------------- |
| **Asynchronous RESET**    | Reliable initialization regardless of clock |
| **Synchronous Shift**     | Predictable timing, no glitches             |
| **Shift Enable**          | Controls when shifting occurs               |
| **Concurrent Assignment** | Output always reflects current register     |

---

## Part 5: Practical Applications

1. **Serial Communication** (RS-232, SPI): Converting serial data to parallel for microcontroller
2. **Data Acquisition**: Collecting sensor bits into a byte
3. **UART Receivers**: Building receive data registers
4. **Protocol Converters**: Serial ↔ Parallel conversions

---

## Summary

**General Logic:**

- 4 flip-flops arranged in series
- Data enters from left (Serial_In), shifts right on CLK
- After 4 cycles, complete 4-bit word appears on output

**VHDL Implementation:**

- Uses a single signal `S_reg` to represent the 4-bit register
- Concatenation operator (`&`) performs the shift: `Serial_In & S_reg(3 downto 1)`
- Control signal `Shift` enables/disables shifting
- Asynchronous reset initializes to zero
