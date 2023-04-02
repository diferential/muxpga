
TESTS := tests/*

.PHONY: $(TESTS)
.PHONY: all

all: $(TESTS) results.xml

EMILIAN_LOCAL_DEV ?= no

ifeq ($(EMILIAN_LOCAL_DEV),yes)

# Regenerate plain Verilog from SystemVerilog on local development
# Will submit this to github as we may not have sv2v upstream.
fpga.v: fpga.sv
	sv2v fpga.sv > fpga.v

else ifeq ($(EMILIAN_LOCAL_DEV),gds)

# My local setup complains about combinatorial loops when running GDS
# add some bufs. Github actions do not error out on that.
fpga.v: fpga.sv
	sv2v -DEMILIAN_ADD_BUFS=y fpga.sv > fpga.v

endif


$(TESTS): fpga.v
	@cd $@ && $(MAKE)

results.xml: $(TESTS)
	cat tests/*/results.xml > results.xml

.PHONY: clean
clean:
	$(foreach TEST, $(TESTS), $(MAKE) -C $(TEST) clean;)

regression:
	$(foreach TEST, $(TESTS), $(MAKE) -C $(TEST) regression;
