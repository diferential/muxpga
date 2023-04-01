import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

CMD_SHIFT_CFG = 0;
CMD_RUN = 1;
ROWS = 5;
COLS = 3;

async def do_input_cycle(dut, rst, io_in, cmd):
    await Timer(1, units='us')

    dut.rst.value = rst;
    dut.io_in.value = io_in;
    dut.cmd.value = cmd;

    dut._log.info("sending rst={} in={} cmd={}".format(rst, io_in, cmd));
    await Timer(1, units='us');
    
    dut.rst.value = 1;
    await ClockCycles(dut.clk, 10);

    val = dut.segments.value;
    dut._log.info("clock out {}".format(val));
    return val;

async def do_reset(dut):
    for i in range(10):
        # write some random cmd values, they should be ignored.
        assert(do_input_cycle(dut, 1, 3, CMD_RUN) == 0);

@cocotb.test()
async def test_cfg0_isdff(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")
    await do_reset(dut);

    cells = (ROWS-1)*COLS;

    cmd = 0;
    dut._log.info("dff test")
    for i in range(cells):
        do_input_cycle(0, i%4, cmd);

# TODO(emilian): Make this work.
@cocotb.test()
async def test_cfg02_bigloop_mux(dut):
    dut.rst.value = 1
    dut.io_in.value = 2;
    dut.cmd.value = 0;

    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")
    await Timer(1, units='us')
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    await Timer(1, units='us')
    dut.rst.value = 0
    await Timer(1, units='us')

    await Timer(1, units='us')
    dut._log.info("pushing {}".format(7))
    dut.io_in.value = 7;
    await Timer(1, units='us')
    await ClockCycles(dut.clk, 1)
    val = dut.segments.value;
    dut._log.info("clock out {}".format(val));
    assert int(val) == 0;

    for r in range(ROWS - 1):
        for c in range(COLS):
            # 6 routes both inputs from left, 0 from below
            val = 6 if c == COLS - 1  else 0;
            dut._log.info("pushing {}".format(val))
            await Timer(1, units='us')
            dut.io_in.value = val;
            await Timer(1, units='us')

            await ClockCycles(dut.clk, 1)
            val = dut.segments.value;
            dut._log.info("clock out {}".format(val));
            assert int(val) == 0;

            val = 0;  # cfg
            dut._log.info("pushing {}".format(val))
            await Timer(1, units='us')
            dut.io_in.value = val;
            await Timer(1, units='us')

            await ClockCycles(dut.clk, 1)
            val = dut.segments.value;
            dut._log.info("clock out {} at {} {}".format(val, r, c));
            if (r == ROWS - 2 and c == COLS - 1):
                assert int(val) == 7 << 4;
            else:
                assert int(val) == 0;

    # await ClockCycles(dut.clk, 1)
    # val = dut.segments.value;
    # dut._log.info("clock out {}".format(val));
    # assert int(val) == 8;

    # switch to execution
    dut.cmd.value = 1;
        
    dut._log.info("dff test")
    for i in range(40):
        dut._log.info("pushing {}".format(i % 8))

        await Timer(1, units='us')
        dut.io_in.value = (i % 8);
        await Timer(1, units='us')

        await ClockCycles(dut.clk, 1)
        dut._log.info("clock out {}".format(dut.segments.value))

        # await ClockCycles(dut.clk, 1)
        # dut._log.info("clock out {}".format(dut.segments.value))

        # await ClockCycles(dut.clk, 1)
        # dut._log.info("clock out {}".format(dut.segments.value))
