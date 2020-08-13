assign INA_int[31:0] =(CE_DFF)?(1<<<row_addr[4:0]):32'b0;
assign INB_int[31:0] =(CE_DFF)?(1<<<row_addr[9:5]):32'b0;
