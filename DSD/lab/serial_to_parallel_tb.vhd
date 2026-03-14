library IEEE;
use IEEE.STD_LOGIC_1164.all;

-- ============================================================================
-- Testbench: serial_to_parallel_tb
-- Description: Tests 4-bit Serial-to-Parallel Shift Register functionality
-- ============================================================================
entity serial_to_parallel_tb is
end serial_to_parallel_tb;

-- ============================================================================
-- Testbench Architecture
-- ============================================================================
architecture TB_Behavior of serial_to_parallel_tb is
    
    -- ========================================================================
    -- Component Declaration
    -- ========================================================================
    component serial_to_parallel is
        port (
            CLK       : in  STD_LOGIC;
            RESET     : in  STD_LOGIC;
            Shift     : in  STD_LOGIC;
            Serial_In : in  STD_LOGIC;
            S         : out STD_LOGIC_VECTOR(3 downto 0)
        );
    end component;
    
    -- ========================================================================
    -- Testbench Signals (Stimuli and Responses)
    -- ========================================================================
    signal CLK_tb       : STD_LOGIC := '0';
    signal RESET_tb     : STD_LOGIC := '1';
    signal Shift_tb     : STD_LOGIC := '0';
    signal Serial_In_tb : STD_LOGIC := '0';
    signal S_tb         : STD_LOGIC_VECTOR(3 downto 0);
    
    -- Clock period constant
    constant CLK_PERIOD : time := 20 ns;  -- 50 MHz clock
    
begin
    
    -- ========================================================================
    -- DUT: Device Under Test (Instantiate the shift register)
    -- ========================================================================
    DUT : serial_to_parallel
        port map (
            CLK       => CLK_tb,
            RESET     => RESET_tb,
            Shift     => Shift_tb,
            Serial_In => Serial_In_tb,
            S         => S_tb
        );
    
    -- ========================================================================
    -- Clock Generation Process
    -- Creates a continuous clock with 50% duty cycle
    -- ========================================================================
    process
    begin
        CLK_tb <= '0';
        wait for CLK_PERIOD / 2;
        CLK_tb <= '1';
        wait for CLK_PERIOD / 2;
    end process;
    
    -- ========================================================================
    -- Main Stimulus Process
    -- ========================================================================
    process
    begin
        
        -- ====================================================================
        -- TEST 1: Reset Operation
        -- ====================================================================
        report "========================================";
        report "TEST 1: RESET OPERATION";
        report "========================================";
        
        RESET_tb  <= '1';           -- Assert reset
        Shift_tb  <= '0';
        Serial_In_tb <= '0';
        wait for 2 * CLK_PERIOD;    -- Wait for 2 clock cycles
        
        RESET_tb  <= '0';           -- De-assert reset
        wait for CLK_PERIOD;
        
        -- ====================================================================
        -- TEST 2: Shift in Data "1011" (MSB first)
        -- ====================================================================
        report "========================================";
        report "TEST 2: SHIFT IN DATA '1011'";
        report "========================================";
        
        -- Cycle 1: Shift in bit 1
        Shift_tb  <= '1';
        Serial_In_tb <= '1';
        wait for CLK_PERIOD;
        report "Cycle 1: Input 1, Output: " & to_string(S_tb);
        
        -- Cycle 2: Shift in bit 0
        Serial_In_tb <= '0';
        wait for CLK_PERIOD;
        report "Cycle 2: Input 0, Output: " & to_string(S_tb);
        
        -- Cycle 3: Shift in bit 1
        Serial_In_tb <= '1';
        wait for CLK_PERIOD;
        report "Cycle 3: Input 1, Output: " & to_string(S_tb);
        
        -- Cycle 4: Shift in bit 1
        Serial_In_tb <= '1';
        wait for CLK_PERIOD;
        report "Cycle 4: Input 1, Output: " & to_string(S_tb);
        report "Final Data Loaded: 1011 (shown as 1101 due to shift direction)";
        
        -- ====================================================================
        -- TEST 3: Hold Data (Shift Disabled)
        -- ====================================================================
        report "========================================";
        report "TEST 3: HOLD DATA (SHIFT DISABLED)";
        report "========================================";
        
        Shift_tb  <= '0';           -- Disable shifting
        Serial_In_tb <= '1';        -- Try to input new data
        
        wait for CLK_PERIOD;
        report "Cycle 1 (No Shift): Input 1, Output: " & to_string(S_tb);
        
        wait for CLK_PERIOD;
        report "Cycle 2 (No Shift): Input 1, Output: " & to_string(S_tb);
        report "Data held constant (no change)";
        
        -- ====================================================================
        -- TEST 4: Shift in Different Pattern "0101"
        -- ====================================================================
        report "========================================";
        report "TEST 4: SHIFT IN PATTERN '0101'";
        report "========================================";
        
        Shift_tb  <= '1';           -- Enable shifting
        
        -- Cycle 1: Shift in bit 0
        Serial_In_tb <= '0';
        wait for CLK_PERIOD;
        report "Cycle 1: Input 0, Output: " & to_string(S_tb);
        
        -- Cycle 2: Shift in bit 1
        Serial_In_tb <= '1';
        wait for CLK_PERIOD;
        report "Cycle 2: Input 1, Output: " & to_string(S_tb);
        
        -- Cycle 3: Shift in bit 0
        Serial_In_tb <= '0';
        wait for CLK_PERIOD;
        report "Cycle 3: Input 0, Output: " & to_string(S_tb);
        
        -- Cycle 4: Shift in bit 1
        Serial_In_tb <= '1';
        wait for CLK_PERIOD;
        report "Cycle 4: Input 1, Output: " & to_string(S_tb);
        report "New Pattern Loaded: 0101 (shown as 1010 due to shift direction)";
        
        -- ====================================================================
        -- TEST 5: Reset During Operation
        -- ====================================================================
        report "========================================";
        report "TEST 5: RESET DURING OPERATION";
        report "========================================";
        
        wait for CLK_PERIOD;
        report "Before Reset: " & to_string(S_tb);
        
        RESET_tb  <= '1';           -- Assert reset
        wait for CLK_PERIOD / 4;
        report "Reset asserted (asynchronous): " & to_string(S_tb);
        
        RESET_tb  <= '0';           -- De-assert reset
        wait for CLK_PERIOD;
        report "After Reset: " & to_string(S_tb);
        
        -- ====================================================================
        -- Simulation End
        -- ====================================================================
        report "========================================";
        report "END OF SIMULATION";
        report "========================================";
        wait;
        
    end process;
    
end TB_Behavior;

-- ============================================================================
-- NOTE: To run this testbench in ModelSim/Questa:
-- ============================================================================
-- 1. Compile both files:
--    vcom serial_to_parallel.vhd
--    vcom serial_to_parallel_tb.vhd
--
-- 2. Simulate:
--    vsim TB_Behavior
--
-- 3. Run waveform:
--    run 500 ns
--
-- 4. View signals in waveform window
-- ============================================================================
