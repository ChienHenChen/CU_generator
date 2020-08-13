//This delay chians element is designed for Beta version MemGen
//Version: V0
//Date: Jun 2020
//Author: Chien-Hen Chen

//-------------------------------
// Parameter definition
//-------------------------------

//-------------------------------
// Input and output definition
//-------------------------------
module DLY_MODULE (
	//Input port
	input in,
	//Output port
	output SAE
);

//Wire Definition
wire in0;
wire in1;
wire in2;
wire in3;
wire in4;
wire in5;
wire in6;
wire in7;
wire in8;
wire in9;
assign in0=in;

//Delay cells instantiation
DLY2_X0P5M_A9TH U0 (.A(in0),.Y(in1));
DLY2_X0P5M_A9TH U1 (.A(in1),.Y(in2));
DLY2_X0P5M_A9TH U2 (.A(in2),.Y(in3));
DLY2_X0P5M_A9TH U3 (.A(in3),.Y(in4));
DLY2_X0P5M_A9TH U4 (.A(in4),.Y(in5));
DLY2_X0P5M_A9TH U5 (.A(in5),.Y(in6));
DLY2_X0P5M_A9TH U6 (.A(in6),.Y(in7));
DLY2_X0P5M_A9TH U7 (.A(in7),.Y(in8));
DLY2_X0P5M_A9TH U8 (.A(in8),.Y(in9));
DLY2_X0P5M_A9TH U9 (.A(in9),.Y(in10));

//Output assign
assign SAE= in10;
endmodule
