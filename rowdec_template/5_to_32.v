assign INA_int[3:0] =(CE_DFF & ~row_addr[4])?(1<<<row_addr[1:0]):4'b0;
assign INB_int[3:0] =(CE_DFF & ~row_addr[4])?(1<<<row_addr[3:2]):4'b0;
assign INA_int[7:4] =(CE_DFF & row_addr[4])?(1<<<row_addr[1:0]):4'b0;
assign INB_int[7:4] =(CE_DFF & row_addr[4])?(1<<<row_addr[3:2]):4'b0;
