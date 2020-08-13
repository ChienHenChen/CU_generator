//This control_unit generator is designed for Beta version MemGen
//Version: V2 for Aug2020 tapeout
//Date: Aug 2020
//Author: Chien-Hen Chen


//-------------------------------
// Parameter definition
//-------------------------------
`define ADDR_BIT_COUNT 9
`define ROWS 128
`define ROWS_BIT_COUNT 7
`define CMUX 4
`define COLS_BIT_COUNT 2
`define IN_NUMBER 16		
//-------------------------------
// Input and output definition
//-------------------------------
module CU (
	//Input port
	input CLK,
	input CE,
	input WE,
	input [`ADDR_BIT_COUNT-1:0] ADDR,
	//Extra input pins
	//Extra output pins
	//Output port
	//Output for INA
	output [`IN_NUMBER-1:0] INA,
	//Output for INB
	output [`IN_NUMBER-1:0] INB,
	//Output for CSEL
	output [`CMUX-1:0] CSEL,
	output CK,
	output PRCH,
	output WEN,
	output SAE

);

//-------------------------------
// Register and wire Definition
//-------------------------------
//register for input pins
reg [`ADDR_BIT_COUNT-1:0] ADDR_DFF;
reg CE_DFF;
reg WE_DFF;
//wire for delay signal
wire SAE_dly;
//wire for row/column decoder
wire [`ADDR_BIT_COUNT-`COLS_BIT_COUNT-1:0] row_addr;
wire [`COLS_BIT_COUNT-1:0] col_addr;
//wire for INA, INB & WLE
wire [`IN_NUMBER-1:0] INA_int;
wire [`IN_NUMBER-1:0] INB_int;
wire WLE;
//-------------------------------
// Register for input pins
//-------------------------------
always @(posedge CLK) begin
	ADDR_DFF<=ADDR;
	CE_DFF<=CE;
	WE_DFF<=WE;
end
//-------------------------------
// Combinations block for SAE,WE,PRCH & WLE
//-------------------------------
assign CK=CLK & CE_DFF;
assign PRCH = (CE_DFF & ~WE_DFF)?(~CLK):1'b1;
assign WLE=~CLK & CE_DFF;
assign WEN= CLK  & WE_DFF & CE_DFF;
//assign SAE=~CLK & ~WE_DFF & CE_DFF; 
//assign WLE=WLE_dly & ~CLK & CE_DFF;
assign SAE=SAE_dly & ~CLK & ~WE_DFF & CE_DFF;
//-------------------------------
// Assign for Address bits
//-------------------------------
assign row_addr=ADDR_DFF[`ADDR_BIT_COUNT-1:`COLS_BIT_COUNT];
assign col_addr=ADDR_DFF[`COLS_BIT_COUNT-1:0];
//-------------------------------
// XDEC
//-------------------------------
//Write the rowdec template
assign INA_int[7:0] =(CE_DFF & ~row_addr[6])?(1<<<row_addr[2:0]):8'b0;
assign INB_int[7:0] =(CE_DFF & ~row_addr[6])?(1<<<row_addr[5:3]):8'b0;
assign INA_int[15:8] =(CE_DFF & row_addr[6])?(1<<<row_addr[2:0]):8'b0;
assign INB_int[15:8] =(CE_DFF & row_addr[6])?(1<<<row_addr[5:3]):8'b0;
//assign the output INA and INB
assign INA=(WLE)?INA_int:16'b0;
assign INB=(WLE)?INB_int:16'b0;
//-------------------------------
// YDEC
//-------------------------------
assign CSEL=(CE_DFF)?(1<<<col_addr):4'b0;

//Output signal w inserting delay elements
DLY_MODULE DLY_MODULE (.in(~CK),.SAE(SAE_dly));
endmodule
