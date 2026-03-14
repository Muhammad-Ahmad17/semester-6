# 4-Bit Serial-to-Parallel Shift Register - Quick Reference & Tips

## Quick Summary

### What It Does
Converts 4 bits of serial data (one bit at a time) into a 4-bit parallel output.

### Key Equation
```
S_reg <= Serial_In & S_reg(3 downto 1);
```
- **&** = Concatenation operator (combines signals)
- Shifts existing data right, new bit enters from left
- Happens on every **rising_edge(CLK)** when **Shift = '1'**

---

## Implementation Checklist

- [ ] Entity has ports: CLK, RESET, Shift, Serial_In, S(3:0)
- [ ] Declared internal signal: signal S_reg : STD_LOGIC_VECTOR(3 downto 0);
- [ ] Process sensitivity: process(CLK, RESET)
- [ ] Asynchronous reset: if RESET='1' then S_reg <= (others => '0');
- [ ] Synchronous shift: elsif rising_edge(CLK) then
- [ ] Shift control: if Shift='1' then
- [ ] Shift operation: S_reg <= Serial_In & S_reg(3 downto 1);
- [ ] Output assignment: S <= S_reg;

---

## Common Mistakes to Avoid

### ❌ MISTAKE 1: Using S_reg(2 downto 0) instead of S_reg(3 downto 1)
```vhdl
-- WRONG:
S_reg <= Serial_In & S_reg(2 downto 0);  -- Only 3 bits! Result is 4 bits, but wrong data
```
**Why it's wrong:** S_reg(2 downto 0) is only 3 bits. Concatenating with 1-bit Serial_In gives 4 bits, but you lose S[3] data.

```vhdl
-- CORRECT:
S_reg <= Serial_In & S_reg(3 downto 1);  -- 1 bit + 3 bits = 4 bits correct
```

---

### ❌ MISTAKE 2: Forgetting the Shift Control Signal
```vhdl
-- WRONG: Shifts every clock cycle
elsif rising_edge(CLK) then
    S_reg <= Serial_In & S_reg(3 downto 1);
```

```vhdl
-- CORRECT: Only shifts when Shift='1'
elsif rising_edge(CLK) then
    if Shift = '1' then
        S_reg <= Serial_In & S_reg(3 downto 1);
    end if;
end process;
```

---

### ❌ MISTAKE 3: Using <= instead of := in process
```vhdl
-- WRONG: (inside process, this might cause issues in simulation)
if Shift = '1' then
    S_reg := Serial_In & S_reg(3 downto 1);  -- Assignment operator (:=)
end if;
```

```vhdl
-- CORRECT: Use <= inside process for signals
if Shift = '1' then
    S_reg <= Serial_In & S_reg(3 downto 1);  -- Signal assignment (<= )
end if;
```

---

### ❌ MISTAKE 4: Synchronous Reset (Should be Asynchronous)
```vhdl
-- WRONG: Reset only happens on clock edge (delayed)
elsif rising_edge(CLK) then
    if RESET = '1' then
        S_reg <= (others => '0');
    elsif Shift = '1' then
        S_reg <= Serial_In & S_reg(3 downto 1);
    end if;
```

```vhdl
-- CORRECT: Reset happens immediately, independent of clock
if RESET = '1' then
    S_reg <= (others => '0');
elsif rising_edge(CLK) then
    if Shift = '1' then
        S_reg <= Serial_In & S_reg(3 downto 1);
    end if;
end if;
```

---

### ❌ MISTAKE 5: Not Connecting Internal Signal to Output
```vhdl
-- WRONG: Output never updates
architecture Behavioral of serial_to_parallel is
    signal S_reg : STD_LOGIC_VECTOR(3 downto 0);
begin
    process(CLK, RESET) ...
    -- Missing: S <= S_reg;
end Behavioral;
```

```vhdl
-- CORRECT: Connect interno signal to output port
architecture Behavioral of serial_to_parallel is
    signal S_reg : STD_LOGIC_VECTOR(3 downto 0);
begin
    process(CLK, RESET) ...
    S <= S_reg;  -- Provides output
end Behavioral;
```

---

## Why the Shift Direction?

### Data Path Visualization

The register stores data with indices 3, 2, 1, 0:

```
Position:  [3] [2] [1] [0]
           MSB           LSB
```

**When shifting right with `Serial_In & S_reg(3 downto 1)`:**

```
Before:    [S3] [S2] [S1] [S0]
                  ↓   ↓   ↓
After:     [In] [S3] [S2] [S1]
           ← New data enters from left
           → Old data exits from right
```

**Example: Shifting in 0101 serially (one bit per clock):**

| Clock | Serial_In | S[3] | S[2] | S[1] | S[0] |
|-------|-----------|------|------|------|------|
| 1     | 0         | 0    | 0    | 0    | 0    |
| 2     | 1         | 0    | 0    | 0    | 1    |
| 3     | 0         | 0    | 0    | 1    | 0    |
| 4     | 1         | 0    | 1    | 0    | 1    |

Result: S = "0101" (pattern loaded successfully)

---

## Testing Your Implementation

### Test Case 1: Reset
```
RESET = 1 → S should immediately become "0000"
RESET = 0 → S can start changing
```

### Test Case 2: Shift Enable
```
Shift = 0 → S stays constant (no change)
Shift = 1 → S shifts on every CLK rising edge
```

### Test Case 3: Data Loading
```
Load 4 bits serially → After 4 clock cycles, 
all bits should appear in S[3:0]
```

---

## Synthesis Considerations

| Feature | Notes |
|---------|-------|
| **Asynchronous Reset** | Preferred for reliable initialization |
| **Clocked Behavior** | Proper timing with reset and shift signals |
| **Area** | Minimal: 4 flip-flops + modest logic |
| **Timing** | Single combinational delay for shift operation |

---

## Common Debug Tips

**Problem:** Output not changing even with Shift = '1'
- **Check:** Is CLK correct? Are you looking at rising edges?
- **Check:** Is RESET asserted? Reset dominates all logic.

**Problem:** Only 3 bits loading instead of 4
- **Check:** Are you using S_reg(3 downto 1) or (2 downto 0)?

**Problem:** Data appears in wrong order
- **Check:** Remember: Serial_In enters left, exits right
- Data reverses from serial input order

**Problem:** Design not synthesizing
- **Check:** All signals properly declared?
- **Check:** Using correct VHDL syntax (IEEE 1164)?

---

## Alternative Implementation (For Reference)

If you prefer explicit bit assignments:

```vhdl
elsif rising_edge(CLK) then
    if Shift = '1' then
        -- Explicit shift (same result as concatenation)
        S_reg(3) <= Serial_In;
        S_reg(2) <= S_reg(3);
        S_reg(1) <= S_reg(2);
        S_reg(0) <= S_reg(1);
    end if;
end if;
```

**However**, concatenation version is cleaner:
```vhdl
S_reg <= Serial_In & S_reg(3 downto 1);
```

---

## Hands-On Exercise

**Write this without looking at the reference:**

1. Entity with proper ports
2. Internal 4-bit signal
3. Process with CLK and RESET
4. Asynchronous reset logic
5. Synchronous shift logic with enable
6. Output assignment

**Expected time:** 5-10 minutes
