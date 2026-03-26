library ieee;
use ieee.std_logic_1164.all;
use work.myCompo.all;

entity warningAlaram is 
	port (
		ignition , door , sbelt : in std_logic ;
		warning : out std_logic
	);
end warningAlaram;

architecture str of warningAlaram is 
signal s_sbelt , s_sbeltDoor : std_logic;
begin 
	U0 : notGate port map (a=>sbelt , x=>s_sbelt);
	U1 : orGate port map (a=>s_sbelt , b=>door , x=>s_sbeltDoor);
	U2 : andGate port map (a=>ignition , b=>s_sbeltDoor , x=>warning);
	
end str;

