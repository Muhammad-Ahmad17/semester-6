-- Copyright (C) 2025  Altera Corporation. All rights reserved.
-- Your use of Altera Corporation's design tools, logic functions 
-- and other software and tools, and any partner logic 
-- functions, and any output files from any of the foregoing 
-- (including device programming or simulation files), and any 
-- associated documentation or information are expressly subject 
-- to the terms and conditions of the Altera Program License 
-- Subscription Agreement, the Altera Quartus Prime License Agreement,
-- the Altera IP License Agreement, or other applicable license
-- agreement, including, without limitation, that your use is for
-- the sole purpose of programming logic devices manufactured by
-- Altera and sold by Altera or its authorized distributors.  Please
-- refer to the Altera Software License Subscription Agreements 
-- on the Quartus Prime software download page.

-- *****************************************************************************
-- This file contains a Vhdl test bench with test vectors .The test vectors     
-- are exported from a vector file in the Quartus Waveform Editor and apply to  
-- the top level entity of the current Quartus project .The user can use this   
-- testbench to simulate his design using a third-party simulation tool .       
-- *****************************************************************************
-- Generated on "03/26/2026 21:52:47"
                                                             
-- Vhdl Test Bench(with test vectors) for design  :          warningAlaram
-- 
-- Simulation tool : 3rd Party
-- 

LIBRARY ieee;                                               
USE ieee.std_logic_1164.all;                                

ENTITY warningAlaram_vhd_vec_tst IS
END warningAlaram_vhd_vec_tst;
ARCHITECTURE warningAlaram_arch OF warningAlaram_vhd_vec_tst IS
-- constants                                                 
-- signals                                                   
SIGNAL door : STD_LOGIC;
SIGNAL ignition : STD_LOGIC;
SIGNAL sbelt : STD_LOGIC;
SIGNAL warning : STD_LOGIC;
COMPONENT warningAlaram
	PORT (
	door : IN STD_LOGIC;
	ignition : IN STD_LOGIC;
	sbelt : IN STD_LOGIC;
	warning : OUT STD_LOGIC
	);
END COMPONENT;
BEGIN
	i1 : warningAlaram
	PORT MAP (
-- list connections between master ports and signals
	door => door,
	ignition => ignition,
	sbelt => sbelt,
	warning => warning
	);

-- door
t_prcs_door: PROCESS
BEGIN
	door <= '0';
WAIT;
END PROCESS t_prcs_door;

-- ignition
t_prcs_ignition: PROCESS
BEGIN
	ignition <= '0';
WAIT;
END PROCESS t_prcs_ignition;

-- sbelt
t_prcs_sbelt: PROCESS
BEGIN
	sbelt <= '0';
WAIT;
END PROCESS t_prcs_sbelt;
END warningAlaram_arch;
