library verilog;
use verilog.vl_types.all;
entity warningAlaram is
    port(
        ignition        : in     vl_logic;
        door            : in     vl_logic;
        sbelt           : in     vl_logic;
        warning         : out    vl_logic
    );
end warningAlaram;
