`default_nettype none

module diferential_muxpga (
  input [7:0] io_in,
  output [7:0] io_out
);

   wire        clk = io_in[0];
   wire        reset = io_in[1];
   wire [3:0]  cfg = io_in[6:3];

   localparam  ROWS = 3;
   localparam  COLS = 3;
   localparam  BITS = 3;

   generate
      genvar   row;
      genvar   col;

      wire [BITS-1:0] cell_q[0:COLS-1][0:ROWS-1] ;
      for (row = 0; row < ROWS; row = row + 1'b1) begin
         for (col = 0; col < COLS; col = col + 1'b1) begin
            reg [3:0] cfg_mux;
            assign cfg_mux = cfg;
            
            reg [BITS-1:0] cell_in1;
            reg [BITS-1:0] cell_in2;

            localparam rminus1 = (ROWS + row - 1) % ROWS;
            localparam rplus1 = (ROWS + row - 1) % ROWS;
            localparam cminus1 = (COLS + col - 1) % COLS;
            localparam cplus1 = (COLS + col - 1) % COLS;

            always @(*) begin
               case(cfg_mux[1:0])
                 0:  cell_in1 = cell_q[rminus1][col];
                 1:  cell_in1 = cell_q[rminus1][cminus1];
                 2:  cell_in1 = cell_q[row][cminus1];
                 3:  cell_in1 = cell_q[row][cplus1];
                 default:  cell_in1 = cell_q[row][col];
               endcase
            end

            always @(*) begin
               case(cfg_mux[3:2])
                 0:  cell_in2 = cell_q[rminus1][col];
                 1:  cell_in2 = cell_q[rminus1][cminus1];
                 2:  cell_in2 = cell_q[row][cminus1];
                 3:  cell_in2 = cell_q[row][cplus1];
                 default:  cell_in2 = cell_q[row][col];
               endcase
            end

            diferential_cell c(clk, reset, cell_in1, cell_in2, cfg, cell_q[row][col]);
         end

         assign io_out[row] = cell_q[row][COLS - 1'b1];
      end
   endgenerate

   assign io_out = {cell_q[ROWS - 1][0], cell_q[ROWS - 1][COLS - 1]};

endmodule

module diferential_cell
  #(
    parameter B = 3
   )
  (
    input        clk,
    input        reset,
    input [B-1:0]  in1,
    input [B-1:0]  in2,
    input [3:0]  cfg,
    output [B-1:0] q
    );

   reg [3:0]    dff;
   reg [3:0]    f_out;
   
   always @(*) begin
      case(cfg[1:0])
        0:  f_out = in1 & in2;
        1:  f_out = in1 | in2;
        2:  f_out = in1;
        3:  f_out = in2;
      endcase
   end

   always @(posedge clk) begin
      if (reset) begin
         dff <= 0;
      end else begin
         dff <= f_out;
      end
   end

   // This the fact that we have non-registered outputs potentially could have cycles.
   // I'm curious what the synthesis tools will do here.
   // assign q = cfg[1] ? dff : f_out;
   assign q = dff;
endmodule
