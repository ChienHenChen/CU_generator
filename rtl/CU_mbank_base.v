//This control_unit generator is designed for Beta version MemGen
//Version: V2 for Aug2020 tapeout
//Date: Aug 2020
//Author: Chien-Hen Chen

//-------------------------------
// Parameter definition
//-------------------------------
`define ADDR_BIT_COUNT 11
`define BANKS 4
`define BANKS_BIT_COUNT 2
`define ROWS 128
`define ROWS_BIT_COUNT 7
`define CMUX 4
`define COLS_BIT_COUNT 2
`define IN_NUMBER 16
`define WORD_SIZE 32 
//-------------------------------
// Input and output definition
//-------------------------------
module CU (
	//Input port
	input CLK,
	input CE,
	input WE,
	input [`ADDR_BIT_COUNT-1:0] ADDR,
	//DOUT come into MUX
	//Extra input pins
	//Extra output pins
	//Output port
	//Output for INA
	//Output for INB
	//Output for CSEL
	output [`BANKS-1:0] CK,
	output [`BANKS-1:0] PRCH,
	output [`BANKS-1:0] WEN,
	output [`BANKS-1:0] SAE,
	output [`WORD_SIZE-1:0] DOUT
);
//-------------------------------
// Register and wire Definition
//-------------------------------
//register for input pins
reg [`ADDR_BIT_COUNT-1:0] ADDR_DFF;
reg CE_DFF;
reg WE_DFF;
//wire for delay signal
//wire for row/column decoder
wire [`BANKS_BIT_COUNT-1:0] bank_addr;
wire [`ROWS_BIT_COUNT-1:0] row_addr;
wire [`COLS_BIT_COUNT-1:0] col_addr;
//wire for global control signal
wire CK_int;
wire PRCH_int;
wire WEN_int;
wire WLE_int;
wire SAE_int;
//wire for DATA_REQ
//wire [`BANKS-1:0] DATA_REQ;
//wire for global INA, INB, CSEL, BS & WLE
wire [`IN_NUMBER-1:0] INA_int;
wire [`IN_NUMBER-1:0] INB_int;
wire [`CMUX-1:0] CSEL;
wire [`BANKS-1:0] BS;
wire [`BANKS-1:0] WLE;
//register for DO MUX
reg [`WORD_SIZE-1:0] DO;
//-------------------------------
// Register for input pins
//-------------------------------
always @(posedge CLK) begin
	ADDR_DFF<=ADDR;
	CE_DFF<=CE;
	WE_DFF<=WE;
end
//-------------------------------
// Combinations block for global CK,PRCH,WEN,WLE & SAE
//-------------------------------
assign CK_int=CLK & CE_DFF;
assign PRCH_int = (CE_DFF & ~WE_DFF)?(~CLK):1'b1;
assign WLE_int=~CLK & CE_DFF & ~WLEB_dly;
assign WEN_int= CLK & WE_DFF & CE_DFF;
assign SAE_int=~CLK & ~WE_DFF & CE_DFF; 
//assign WLE_int=WLE_dly & ~CLK & CE_DFF & ~WLEB_dly;
//assign SAE_int=SAE_dly & ~CLK & ~WE_DFF & CE_DFF;
//-------------------------------
// Combinations block for local CK,PRCH,WEN,WLE & SAE
//-------------------------------
//for local CK
//for local PRCH
//for local WLE
//for local WEN
//for local SAE
//-------------------------------
// Assign for Address bits
//-------------------------------
assign bank_addr=ADDR_DFF[`ADDR_BIT_COUNT-1:`ADDR_BIT_COUNT-`BANKS_BIT_COUNT];
assign row_addr=ADDR_DFF[`ADDR_BIT_COUNT-`BANKS_BIT_COUNT-1:`COLS_BIT_COUNT];
assign col_addr=ADDR_DFF[`COLS_BIT_COUNT-1:0];
//-------------------------------
// DATA_REQ assign
//-------------------------------
//for local DATA_REQ
//-------------------------------
// BDEC
//-------------------------------
assign BS=(CE_DFF)?(1<<<bank_addr):4'b0;
//-------------------------------
// XDEC
//-------------------------------
//Write the rowdec template
//for local INA
//for local INB
//-------------------------------
// YDEC
//-------------------------------
assign CSEL=(CE_DFF)?(1<<<col_addr):4'b0;
//for local CSEL
//-------------------------------
// Mux for Output selection
//-------------------------------
//wire assign for DOUT from each bank
always@* begin
	case (bank_addr)
		//MUX CASE
		default:DO=32'b0;
	endcase
end
assign DOUT=DO;
//Output signal w inserting delay elements
endmodule
