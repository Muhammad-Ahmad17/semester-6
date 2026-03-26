library ieee;
use ieee.std_logic_1164.all;

entity orGate is 
	port (
		a : in std_logic;
		b : in std_logic;
		x : out std_logic
	);
end orGate;

architecture str of orGate is 
begin 
	x <= a or b ;
end str;