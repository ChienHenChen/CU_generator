assign INA_int[15:0] =(CE_DFF & ~row_addr[8])?(1<<<row_addr[3:0]):16'b0;
assign INB_int[15:0] =(CE_DFF & ~row_addr[8])?(1<<<row_addr[7:4]):16'b0;
assign INA_int[31:16] =(CE_DFF & row_addr[8])?(1<<<row_addr[3:0]):16'b0;
assign INB_int[31:16] =(CE_DFF & row_addr[8])?(1<<<row_addr[7:4]):16'b0;
