library verilog;
use verilog.vl_types.all;
entity fourToOneMux_vlg_sample_tst is
    port(
        a               : in     vl_logic;
        b               : in     vl_logic;
        c               : in     vl_logic;
        d               : in     vl_logic;
        s               : in     vl_logic_vector(1 downto 0);
        sampler_tx      : out    vl_logic
    );
end fourToOneMux_vlg_sample_tst;
