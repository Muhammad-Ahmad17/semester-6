library ieee;
use ieee.std_logic_1164.all;
package myCompo is 	
	--
	component orGate is 
	port (
		a : in std_logic;
		b : in std_logic;
		x : out std_logic
	);
	end component;
	--
	component andGate is 
	port (
		a : in std_logic;
		b : in std_logic;
		x : out std_logic
	);
	end component;
	--
	component notGate is 
	port (
		a : in std_logic;
		x : out std_logic
	);
	end component;
	--
end myCompo;