library ieee;
use ieee.std_logic_1164.all;

entity fourToOneMux is 
	port (
		a,b,c,d : in std_logic;
		s : in std_logic_vector(1 downto 0);
		f : out std_logic
	);
end fourToOneMux;

architecture bhv of fourToOneMux is 
begin 

	process (s)
	begin
		case s is
			when "00" => 
				f <= a;
			when "01" => 
				f <= b;
			when "10" => 
				f <= c;
			when others => 
				f <= d;
		end case;
	end process;
	
end bhv;