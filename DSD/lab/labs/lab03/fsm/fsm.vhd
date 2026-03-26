library ieee;
use ieee.std_logic_1164.all;

entity fsm is
	port (
		reset : out
		X, clk : out
		Z : out
	);
end fsm;

architecture myfsm of fsm is
-- state encoding
	 type state_type is (S0,S1,S2,S3,S4,S5,S6);
	 -- initially S0 is the statea when the fpga loads
-- signals
	signal state , nextState , stateType ;

begin




-- state register
process (reset , clk)
begin
	if reset = '1'
		state <= S0 ;
	elsif riding_edge (clk) then
		state <= nextState;
	end;
end process ;

-- next state logic

process (state ,	X)
begin
	case state is

		-- s0
		when S0 =>
			if  X = '0' then
				nextState <= S1 ;
				Z <= '1';
			else
				nextState <= S0 ;
				Z <= '0';
			end if;

		-- s1
		when S1 =>
			if  X = '0' then
				nextState <= S3 ;
				Z <= '1';
			else
				nextState <= S4 ;
				Z <= '0';
			end if;
		--s2
		when S2 =>
			if  X = '0' then
				nextState <= S4 ;
				Z <= '0';
			else
				nextState <= S4 ;
				Z <= '1';
			end if;

		when S0 =>
			if  X = '0' then
				nextState <= S1 ;
				Z <= '1';
			else
				nextState <= S0 ;
				Z <= '0';
			end if;when S0 =>
			if  X = '0' then
				nextState <= S1 ;
				Z <= '1';
			else
				nextState <= S0 ;
				Z <= '0';
			end if;when S0 =>
			if  X = '0' then
				nextState <= S1 ;
				Z <= '1';
			else
				nextState <= S0 ;
				Z <= '0';
			end if;


end process ;











end myfsm
