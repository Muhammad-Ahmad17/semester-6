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

-- VENDOR "Altera"
-- PROGRAM "Quartus Prime"
-- VERSION "Version 25.1std.0 Build 1129 10/21/2025 SC Lite Edition"

-- DATE "03/26/2026 21:52:49"

-- 
-- Device: Altera EP4CE115F29C7 Package FBGA780
-- 

-- 
-- This VHDL file should be used for Questa Altera FPGA (VHDL) only
-- 

LIBRARY CYCLONEIVE;
LIBRARY IEEE;
USE CYCLONEIVE.CYCLONEIVE_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	warningAlaram IS
    PORT (
	ignition : IN std_logic;
	door : IN std_logic;
	sbelt : IN std_logic;
	warning : OUT std_logic
	);
END warningAlaram;

ARCHITECTURE structure OF warningAlaram IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL devoe : std_logic := '1';
SIGNAL devclrn : std_logic := '1';
SIGNAL devpor : std_logic := '1';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_ignition : std_logic;
SIGNAL ww_door : std_logic;
SIGNAL ww_sbelt : std_logic;
SIGNAL ww_warning : std_logic;
SIGNAL \warning~output_o\ : std_logic;
SIGNAL \ignition~input_o\ : std_logic;
SIGNAL \door~input_o\ : std_logic;
SIGNAL \sbelt~input_o\ : std_logic;
SIGNAL \U2|x~0_combout\ : std_logic;

BEGIN

ww_ignition <= ignition;
ww_door <= door;
ww_sbelt <= sbelt;
warning <= ww_warning;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

\warning~output\ : cycloneive_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \U2|x~0_combout\,
	devoe => ww_devoe,
	o => \warning~output_o\);

\ignition~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_ignition,
	o => \ignition~input_o\);

\door~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_door,
	o => \door~input_o\);

\sbelt~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_sbelt,
	o => \sbelt~input_o\);

\U2|x~0\ : cycloneive_lcell_comb
-- Equation(s):
-- \U2|x~0_combout\ = (\ignition~input_o\ & ((\door~input_o\) # (!\sbelt~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1000100010101010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \ignition~input_o\,
	datab => \door~input_o\,
	datad => \sbelt~input_o\,
	combout => \U2|x~0_combout\);

ww_warning <= \warning~output_o\;
END structure;


