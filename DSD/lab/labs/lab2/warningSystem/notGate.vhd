library ieee;
use ieee.std_logic_1164.all;

entity notGate is 
	port (
		a : in std_logic;
		x : out std_logic
	);
end notGate;

architecture str of notGate is 
begin 
	x <= not a ;
end str;