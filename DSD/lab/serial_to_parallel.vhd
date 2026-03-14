library IEEE;
use IEEE.STD_LOGIC_1164.all;

-- ============================================================================
-- Entity: serial_to_parallel
-- Description: 4-Bit Serial-to-Parallel Shift Register
-- ============================================================================
entity serial_to_parallel is
    port (
        CLK         : in  STD_LOGIC;                      -- Clock input (rising edge)
        RESET       : in  STD_LOGIC;                      -- Asynchronous reset (active high)
        Shift       : in  STD_LOGIC;                      -- Shift enable control signal
        Serial_In   : in  STD_LOGIC;                      -- Serial data input (1 bit at a time)
        S           : out STD_LOGIC_VECTOR(3 downto 0)   -- 4-bit parallel output register
    );
end serial_to_parallel;

-- ============================================================================
-- Architecture: Behavioral
-- ============================================================================
architecture Behavioral of serial_to_parallel is
    
    -- Internal signal: 4-bit register to store shifted data
    -- S[3] = Oldest data (leftmost)
    -- S[0] = Newest data (rightmost)
    signal S_reg : STD_LOGIC_VECTOR(3 downto 0);
    
begin
    
    -- ========================================================================
    -- Main Sequential Process
    -- Triggered on: Rising edge of CLK OR change in RESET
    -- ========================================================================
    process(CLK, RESET)
    begin
        -- First: Check for RESET (asynchronous, highest priority)
        if RESET = '1' then
            -- Clear all 4 bits when reset is asserted
            S_reg <= (others => '0');   -- S_reg = "0000"
            
        -- Then: Check for rising clock edge (synchronous operation)
        elsif rising_edge(CLK) then
            
            -- Shift control: Only shift if Shift signal is '1'
            if Shift = '1' then
                
                -- ============================================================
                -- SHIFT OPERATION
                -- ============================================================
                -- Concatenate new serial input with shifted register bits
                -- 
                -- Visual representation:
                --   Before: S_reg = [S[3], S[2], S[1], S[0]]
                --   After:  S_reg = [Serial_In, S[3], S[2], S[1]]
                --           └─────┬──────────────────────────────┘
                --                 └─ New value assigned
                --
                -- The & operator concatenates:
                --   Serial_In            = leftmost bit
                --   S_reg(3 downto 1)    = remaining 3 bits shifted right
                -- ============================================================
                S_reg <= Serial_In & S_reg(3 downto 1);
                
            end if;
            -- When Shift = '0': S_reg retains its value (implicit hold)
            
        end if;
    end process;
    
    -- ========================================================================
    -- Continuous Assignment
    -- Output the internal register to the port
    -- ========================================================================
    S <= S_reg;
    
end Behavioral;
