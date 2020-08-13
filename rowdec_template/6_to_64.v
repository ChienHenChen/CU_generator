assign INA_int[7:0] =(CE_DFF)?(1<<<row_addr[2:0]):8'b0;
assign INB_int[7:0] =(CE_DFF)?(1<<<row_addr[5:3]):8'b0;
