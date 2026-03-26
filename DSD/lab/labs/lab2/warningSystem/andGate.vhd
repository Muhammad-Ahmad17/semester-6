library ieee;
use ieee.std_logic_1164.all;

entity andGate is 
	port (
		a : in std_logic;
		b : in std_logic;
		x : out std_logic
	);
end andGate;

architecture str of andGate is 
begin 
	x <= a and b ;
end str;