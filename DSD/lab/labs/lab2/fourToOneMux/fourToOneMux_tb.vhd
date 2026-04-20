library ieee;
use ieee.std_logic_1164.all;

entity fourToOneMux_tb is
end fourToOneMux_tb;

architecture tb of fourToOneMux_tb is
    signal a, b, c, d : std_logic;
    signal s : std_logic_vector(1 downto 0);
    signal f : std_logic;
begin
    -- Instantiate the design
    uut: entity work.fourToOneMux
        port map (
            a => a, b => b, c => c, d => d,
            s => s, f => f
        );
    
    -- Test process
    process
    begin
        -- Test all combinations
        -- Case 1: s="00" -> f = a
        a <= '1'; b <= '0'; c <= '0'; d <= '0'; s <= "00";
        wait for 10 ns;
        assert f = '1' report "Error: s=00, f should be 1" severity error;
        
        -- Case 2: s="01" -> f = b
        a <= '0'; b <= '1'; c <= '0'; d <= '0'; s <= "01";
        wait for 10 ns;
        assert f = '1' report "Error: s=01, f should be 1" severity error;
        
        -- Case 3: s="10" -> f = c
        a <= '0'; b <= '0'; c <= '1'; d <= '0'; s <= "10";
        wait for 10 ns;
        assert f = '1' report "Error: s=10, f should be 1" severity error;
        
        -- Case 4: s="11" -> f = d
        a <= '0'; b <= '0'; c <= '0'; d <= '1'; s <= "11";
        wait for 10 ns;
        assert f = '1' report "Error: s=11, f should be 1" severity error;
        
        -- Case 5: Test with all zeros
        a <= '0'; b <= '0'; c <= '0'; d <= '0'; s <= "00";
        wait for 10 ns;
        assert f = '0' report "Error: All zeros test failed" severity error;
        
        -- Case 6: Test with all ones
        a <= '1'; b <= '1'; c <= '1'; d <= '1'; s <= "01";
        wait for 10 ns;
        assert f = '1' report "Error: All ones test failed" severity error;
        
        report "All tests completed!";
        wait;
    end process;
end tb;