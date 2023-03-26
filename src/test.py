import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

@cocotb.test()
async def test_cfg0_isdff(dut):
    dut.rst.value = 1
    dut.io_in.value = 2;
    dut.cfg_mux.value = 0;

    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0

    dut._log.info("dff test")
    for i in range(10):
        dut._log.info("pushing {}".format(i % 4))

        dut.io_in.value = (i % 4);
        await ClockCycles(dut.clk, 1)
        dut._log.info("clock out {}".format(dut.segments.value))

        await ClockCycles(dut.clk, 1)
        dut._log.info("clock out {}".format(dut.segments.value))

        await ClockCycles(dut.clk, 1)
        dut._log.info("clock out {}".format(dut.segments.value))

# TODO(emilian): Make this work.
@cocotb.test()
async def test_cfg02_bigloop_mux(dut):
    dut.rst.value = 1
    dut.io_in.value = 2;
    dut.cfg_mux.value = 0;

    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0

    dut._log.info("dff test")
    for i in range(10):
        dut._log.info("pushing {}".format(i % 4))

        dut.io_in.value = (i % 4);
        await ClockCycles(dut.clk, 1)
        dut._log.info("clock out {}".format(dut.segments.value))

        await ClockCycles(dut.clk, 1)
        dut._log.info("clock out {}".format(dut.segments.value))

        await ClockCycles(dut.clk, 1)
        dut._log.info("clock out {}".format(dut.segments.value))
