library ieee;
use ieee.std_logic_1164.all;

entity serialToParallel is 
	port (
		clk , reset : in std_logic;
		sr_in : in std_logic;
		pr_out : out std_logic_vector (3 downto 0)
	);
end serialToParallel;

architecture str of serialToParallel is 
	signal s_s : std_logic_vector(3 downto 0);
begin
	process (clk,reset)
	begin 
		if reset = '1' then 
			s_s <= "0000"; -- reset to 0000
		elsif rising_edge (clk) then
			s_s <= sr_in & s_s (3 downto 1);
		end if;
	end process;
	pr_out <= s_s;
end str;