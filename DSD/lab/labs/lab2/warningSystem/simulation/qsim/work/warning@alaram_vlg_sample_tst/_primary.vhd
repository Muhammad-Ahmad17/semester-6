library verilog;
use verilog.vl_types.all;
entity warningAlaram_vlg_sample_tst is
    port(
        door            : in     vl_logic;
        ignition        : in     vl_logic;
        sbelt           : in     vl_logic;
        sampler_tx      : out    vl_logic
    );
end warningAlaram_vlg_sample_tst;
