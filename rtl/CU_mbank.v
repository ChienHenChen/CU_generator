//This control_unit generator is designed for Beta version MemGen
//Version: V2 for Aug2020 tapeout
//Date: Aug 2020
//Author: Chien-Hen Chen

//-------------------------------
// Parameter definition
//-------------------------------
`define ADDR_BIT_COUNT 9
`define BANKS 2
`define BANKS_BIT_COUNT 1
`define ROWS 64
`define ROWS_BIT_COUNT 6
`define CMUX 4
`define COLS_BIT_COUNT 2
`define IN_NUMBER 8
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
	input [`WORD_SIZE-1:0] DOUT0,
	input [`WORD_SIZE-1:0] DOUT1,
	//Extra input pins
	//Extra output pins
	//Output port
	//Output for INA
	output [`IN_NUMBER-1:0] INA0,
	output [`IN_NUMBER-1:0] INA1,
	//Output for INB
	output [`IN_NUMBER-1:0] INB0,
	output [`IN_NUMBER-1:0] INB1,
	//Output for CSEL
	output [`CMUX-1:0] CSEL0,
	output [`CMUX-1:0] CSEL1,
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
wire SAE_dly;
//wire for row/column decoder
wire bank_addr;
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
assign WLE_int=~CLK & CE_DFF;
assign WEN_int= CLK & WE_DFF & CE_DFF;
//assign SAE_int=~CLK & ~WE_DFF & CE_DFF; 
//assign WLE_int=WLE_dly & ~CLK & CE_DFF;
assign SAE_int=SAE_dly & ~CLK & ~WE_DFF & CE_DFF;
//-------------------------------
// Combinations block for local CK,PRCH,WEN,WLE & SAE
//-------------------------------
//for local CK
assign CK[0]=(BS[0])?CK_int:1'b0;
assign CK[1]=(BS[1])?CK_int:1'b0;
//for local PRCH
assign PRCH[0]=(BS[0])?PRCH_int:1'b1;
assign PRCH[1]=(BS[1])?PRCH_int:1'b1;
//for local WLE
assign WLE[0]=(BS[0])?WLE_int:1'b0;
assign WLE[1]=(BS[1])?WLE_int:1'b0;
//for local WEN
assign WEN[0]=(BS[0])?WEN_int:1'b0;
assign WEN[1]=(BS[1])?WEN_int:1'b0;
//for local SAE
assign SAE[0]=(BS[0])?SAE_int:1'b0;
assign SAE[1]=(BS[1])?SAE_int:1'b0;
//-------------------------------
// Assign for Address bits
//-------------------------------
assign bank_addr=ADDR_DFF[`ADDR_BIT_COUNT-1];
assign row_addr=ADDR_DFF[`ADDR_BIT_COUNT-`BANKS_BIT_COUNT-1:`COLS_BIT_COUNT];
assign col_addr=ADDR_DFF[`COLS_BIT_COUNT-1:0];
//-------------------------------
// DATA_REQ assign
//-------------------------------
//for local DATA_REQ
//-------------------------------
// BDEC
//-------------------------------
assign BS=(CE_DFF)?(1<<<bank_addr):2'b0;
//-------------------------------
// XDEC
//-------------------------------
//Write the rowdec template
assign INA_int[7:0] =(CE_DFF)?(1<<<row_addr[2:0]):8'b0;
assign INB_int[7:0] =(CE_DFF)?(1<<<row_addr[5:3]):8'b0;
//for local INA
assign INA0=(WLE[0])?INA_int:8'b0;
assign INA1=(WLE[1])?INA_int:8'b0;
//for local INB
assign INB0=(WLE[0])?INB_int:8'b0;
assign INB1=(WLE[1])?INB_int:8'b0;
//-------------------------------
// YDEC
//-------------------------------
assign CSEL=(CE_DFF)?(1<<<col_addr):4'b0;
//for local CSEL
assign CSEL0=(BS[0])?CSEL:4'b0;
assign CSEL1=(BS[1])?CSEL:4'b0;
//-------------------------------
// Mux for Output selection
//-------------------------------
//wire assign for DOUT from each bank
always@* begin
	case (bank_addr)
		//MUX CASE
		0:DO=DOUT0;
		1:DO=DOUT1;
		default:DO=32'b0;
	endcase
end
assign DOUT=DO;
//Output signal w inserting delay elements
DLY_MODULE DLY_MODULE (.in(~CK_int),.SAE(SAE_dly));
endmodule
