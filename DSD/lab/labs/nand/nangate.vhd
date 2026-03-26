library ieee;
use ieee.std_logic_1164.all;


entity nangate is 
port 
	(
		a : in std_logic;
		b : in std_logic;
		c : out std_logic
	);
end nangate;
	
architecture bhv of nangate is 
begin 
	c <= not (a and b);
end bhv;