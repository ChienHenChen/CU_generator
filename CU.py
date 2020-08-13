import math
import fileinput
import os
import subprocess as sp

# User inputs

##Extra control signal for R/W assisted features (top level)
input_pins_dict= {}
output_pins_dict = {}

#Get the SRAM macro configurations info.#
while True:
	#Get the SRAM Capacity value#
	while True:
		while True:	
			try:
				Capacity=int(input("Please enter the total SRAM capacity (bits) :"))
				Capacity_base2=math.log(Capacity,2)
				Capacity_base2_round=math.floor(Capacity_base2)
				break
			except:
				print("Please re-enter the correct total SRAM capacity")
		if Capacity_base2 - Capacity_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct SRAM bank capacity")

	#Get the SRAM Wordsize value#
	while True:
		while True:	
			try:
				Wordsize=int(input("Please enter the wordsize of this SRAM macro (bits) :"))
				Wordsize_base2=math.log(Wordsize,2)
				Wordsize_base2_round=math.floor(Wordsize_base2)
				break
			except:
				print("Please re-enter the wordsize value of this SRAM macro")
		if Wordsize_base2 - Wordsize_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct wordsize value")
	#Get the SRAM # of Banks value#
	while True:
		while True:	
			try:
				Banks=int(input("Please enter the number of Banks in this SRAM macro:"))
				Banks_base2=math.log(Banks,2)
				Banks_base2_round=math.floor(Banks_base2)
				break
			except:
				print("Please re-enter the number of Banks in this SRAM macro")
		if Banks_base2 - Banks_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct number of Banks value")
	#Get the SRAM # of Rows value#
	while True:
		while True:	
			try:
				Rows=int(input("Please enter the number of Rows in the local bank:"))
				Rows_base2=math.log(Rows,2)
				Rows_base2_round=math.floor(Rows_base2)
				break
			except:
				print("Please re-enter the number of Rows in in the local bank")
		if Rows_base2 - Rows_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct number of Rows value")

	#Get the SRAM # of Columns value#
	while True:
		while True:	
			try:
				Columns=int(input("Please enter the number of Columns the local bank:"))
				Columns_base2=math.log(Columns,2)
				Columns_base2_round=math.floor(Columns_base2)
				break
			except:
				print("Please re-enter the number of Columns in the local bank")
		if Columns_base2 - Columns_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct number of Columns value")
	
	NumberofWord=int(Capacity/Wordsize)
	NumberofWordPerBank=int((Capacity/Banks)/Wordsize)		
	CMUX_C=int(Columns/Wordsize)
	CMUX_R=int(NumberofWordPerBank/Rows)
	if CMUX_C == CMUX_R:
		CMUX=CMUX_C
		break
	else:
		print("The information of SRAM macro configuration is something wrong. Please double check and re-enter")

print("The configuration of this SRAM cdl file is as following")
print("Capacity:"+str(Capacity))
print("Wordsize:"+str(Wordsize))
print("NumberofWord:"+str(NumberofWord))
print("NumberofBank:"+str(Banks))
print("NumberofWordPerBank:"+str(NumberofWordPerBank))
print("Rows:"+str(Rows))
print("Columns:"+str(Columns))
print("CMUX:"+str(CMUX))

#Running the HSPICE simulation to get the delay timing value
f_hspice = open("sim/SRAM_crit_path_base.sp","r")
filedata = f_hspice.read()
f_hspice.close()

filedata = filedata.replace(".param Wordsize=",".param Wordsize="+str(Wordsize))
filedata = filedata.replace(".param Rows=",".param Rows="+str(Rows))
filedata = filedata.replace(".param Columns=",".param Columns="+str(Columns))

f_hspice = open("sim/SRAM_crit_path.sp","w")
f_hspice.write(filedata)
f_hspice.close()

maindir=os.getcwd() # pwd function
simdir=maindir+"/sim"
os.chdir(simdir) # need this os.chdir to help python compiler to change directory
tp=sp.Popen(['hspice', '-i', 'SRAM_crit_path.sp', '-o', 'SRAM_crit_path.lis']) #execute a new process
tp.wait()

os.chdir(maindir)
f_rlist = open("sim/SRAM_crit_path.lis","r")
for line in f_rlist:
	line=line.strip() #Using rstrip to remove the new line
	if line.startswith('t_wddiff_w1='):
		t_wddiff_w1_list=line.split("=")
		t_wddiff_w1=float(t_wddiff_w1_list[1])
	elif line.startswith('t_wddiff_w0='):
		t_wddiff_w0_list=line.split("=")
		t_wddiff_w0=float(t_wddiff_w0_list[1])
	elif line.startswith('t_bldiff_r1='):
		t_bldiff_r1_list=line.split("=")
		t_bldiff_r1=float(t_bldiff_r1_list[1])
	elif line.startswith('t_bldiff_r0='):
		t_bldiff_r0_list=line.split("=")
		t_bldiff_r0=float(t_bldiff_r0_list[1])
t_wddiff=max(t_wddiff_w1,t_wddiff_w0)*1e9
t_bldlff=max(t_bldiff_r1,t_bldiff_r0)*1e9
print(t_wddiff)
print(t_bldlff)
f_rlist.close()

'''
##scrub the delay valye from lib file
fhand_r=open("/app3/lib/ARM/TSMC-CLN65LP-20161013/arm/tsmc/cln65lp/sc9_base_hvt/r0p0/lib/sc9_cln65lp_base_hvt_tt_typical_max_1p20v_25c.lib","r")
fhand_w=open("lib_scrub/delay_value.txt","w")
cell_pointer=False
value_pointer=False
for line in fhand_r:
	line=line.rstrip()
	if line.startswith("  cell(DLY"):
		cell_pointer=True
		line_list=line.split()
		cell_name_list_1=line_list[0].split("(")
		cell_name_list_2=cell_name_list_1[1].split(")")
		fhand_w.write(cell_name_list_2[0]+"\t")
	elif line.startswith("        cell_rise"):
		if cell_pointer==True:
			value_pointer=True
	elif line.startswith("          values("):
		if cell_pointer ==True and value_pointer==True:
			line_list=line.split()
			value_list_1=line_list[0].split('"')
			value_list_2=value_list_1[1].split(",")
			fhand_w.write(value_list_2[0]+"\n")
			cell_pointer=False
			value_pointer=False 
fhand_r.close()
fhand_w.close()
'''

fhand_dly_value=open("lib_scrub/delay_value.txt","r")
for line in fhand_dly_value:
	line=line.rstrip()
	if line.startswith('DLY2'):
		dly_value_list=line.split()
		dly_cell_name=str(dly_value_list[0])
		dly_value_per_stage=float(dly_value_list[1])
		print(dly_value_per_stage)
	break;

WLE_enable_stage=math.floor(t_wddiff/dly_value_per_stage)
SAE_enable_stage=round(t_bldlff/dly_value_per_stage*2)

print(dly_cell_name)
#print(WLE_enable_stage)
print(SAE_enable_stage)


##Output pins with delay elements
#output_pins_w_dly_dict= {"WLE":WLE_enable_stage,"SAE":SAE_enable_stage}
output_pins_w_dly_dict= {"SAE":SAE_enable_stage}
#output_pins_w_dly_dict= {}
max_stage=0
num_output_pin=0
for pin_name in output_pins_w_dly_dict:
	num_output_pin=num_output_pin+1
	if max_stage is None:
		max_stage=output_pins_w_dly_dict[pin_name]
	elif output_pins_w_dly_dict[pin_name] > max_stage:
		max_stage=output_pins_w_dly_dict[pin_name]

# Build strings
input_pins_string = ""
output_pins_string = ""
output_pins_w_dly_string=""
wire_for_dly_string=""
#for multi-bank 
DOUT_pins_string=""
DOUT_MUX_string=""
##output_RSEL_string=""
output_INA_string=""
output_INB_string=""
output_CSEL_string=""
assign_CK_string=""
assign_PRCH_string=""
assign_WEN_string=""
assign_WLE_string=""
assign_SAE_string=""
assign_DREQ_string=""
assign_INA_string=""
assign_INB_string=""
assign_CSEL_string=""

for pin_name in input_pins_dict:
	if input_pins_dict[pin_name] == 1:
		input_pins_string = input_pins_string + "\tinput "+ pin_name + ",\n"
	elif input_pins_dict[pin_name] > 1:
		input_pins_string = input_pins_string + "\tinput "+"[" + str(input_pins_dict[pin_name]-1) + ":0] " + pin_name + ",\n"

for pin_name in output_pins_dict:
	if output_pins_dict[pin_name] == 1:
		output_pins_string = output_pins_string + "\toutput "+ pin_name + ",\n"
	elif output_pins_dict[pin_name] > 1:
		output_pins_string = output_pins_string + "\toutput "+"[" + str(output_pins_dict[pin_name]-1) + ":0] " + pin_name + ",\n"

for i in range(Banks):
	DOUT_pins_string=DOUT_pins_string+"\tinput [`WORD_SIZE-1:0] DOUT"+str(i)+",\n"
	DOUT_MUX_string=DOUT_MUX_string+"\t\t"+str(i)+":DO=DOUT"+str(i)+";\n"

##Address bit count calculation#
ADDR_BIT_COUNT=int(math.log(NumberofWord,2))
BANKS_BIT_COUNT=int(math.log(Banks,2))
ROWS_BIT_COUNT=int(math.log(Rows,2))
COLS_BIT_COUNT=int(math.log(CMUX,2))

#information of INA and INB
sqrt_rows=math.sqrt(Rows)
sqrt_rows_log2=math.log(sqrt_rows,2)
IN_POWER=math.ceil(sqrt_rows_log2)
IN_NUMBER=int(2**IN_POWER)

#information of INA and INB
if Rows > 8:
	sqrt_rows=math.sqrt(Rows)
	sqrt_rows_log2=math.log(sqrt_rows,2)
	IN_POWER=math.ceil(sqrt_rows_log2)
	IN_NUMBER=int(2**IN_POWER)
elif Rows <=8:
	IN_NUMBER=Rows


##Read a base Verilog file for CU_gen##
os.chdir(maindir)
if Banks==1:
	f = open("rtl/CU_sbank_base.v","r")
	filedata = f.read()	
	f.close()

elif Banks>=2:
	f = open("rtl/CU_mbank_base.v","r")
	filedata = f.read()	
	f.close()

# Update Verilog with new user inputs
if Banks==1:
	filedata = filedata.replace("`define ADDR_BIT_COUNT 9",   "`define ADDR_BIT_COUNT " + str(ADDR_BIT_COUNT))
elif Banks>=2:
	filedata = filedata.replace("`define ADDR_BIT_COUNT 11",   "`define ADDR_BIT_COUNT " + str(ADDR_BIT_COUNT))
	filedata = filedata.replace("`define WORD_SIZE 32",   "`define WORD_SIZE " + str(Wordsize))

filedata = filedata.replace("\t//Extra input pins\n","\t//Extra input pins\n"+input_pins_string)
filedata = filedata.replace("\t//Extra output pins\n","\t//Extra output pins\n"+output_pins_string)
filedata = filedata.replace("`define ROWS 128","`define ROWS " + str(Rows))
filedata = filedata.replace("`define ROWS_BIT_COUNT 7","`define ROWS_BIT_COUNT " + str(ROWS_BIT_COUNT))
filedata = filedata.replace("`define CMUX 4","`define CMUX " + str(CMUX))
filedata = filedata.replace("`define COLS_BIT_COUNT 2","`define COLS_BIT_COUNT " + str(COLS_BIT_COUNT))
filedata = filedata.replace("`define IN_NUMBER 16", "`define IN_NUMBER " + str(IN_NUMBER))
filedata = filedata.replace("col_addr):4'b0;","col_addr):"+str(CMUX)+"'b0;")
filedata = filedata.replace("CSEL:4'b0;","CSEL:"+str(CMUX)+"'b0;")

#writing the rowdec template into the verilog file
rowdec_string=""
rowdec_name=str(int(math.log(Rows,2)))+"_to_"+str(Rows)+".v"
f_rowdec = open("rowdec_template/"+rowdec_name,"r")
for line in f_rowdec:
	rowdec_string=rowdec_string+line
filedata = filedata.replace("//Write the rowdec template\n","//Write the rowdec template\n"+rowdec_string)
filedata = filedata.replace("INA_int:16'b0;","INA_int:"+str(IN_NUMBER)+"'b0;")
filedata = filedata.replace("INB_int:16'b0;","INB_int:"+str(IN_NUMBER)+"'b0;")

# For Multi-bank (Define Banks, Define BANKS_BIT_COUNT, bank_addr, DOUTM_UX)
if Banks>=2:
	filedata = filedata.replace("`define BANKS 4","`define BANKS " + str(Banks))
	filedata = filedata.replace("`define BANKS_BIT_COUNT 2","`define BANKS_BIT_COUNT " + str(BANKS_BIT_COUNT))
	filedata = filedata.replace("bank_addr):4'b0;","bank_addr):"+str(Banks)+"'b0;")
	filedata = filedata.replace("\t//DOUT come into MUX\n","\t//DOUT come into MUX\n"+DOUT_pins_string)
	filedata = filedata.replace("\t\t//MUX CASE\n","\t\t//MUX CASE\n"+DOUT_MUX_string)

## For BANKS_BIT_COUNT==1
if Banks==2:
	filedata = filedata.replace("wire [`BANKS_BIT_COUNT-1:0] bank_addr;","wire bank_addr;")
	filedata = filedata.replace("assign bank_addr=ADDR_DFF[`ADDR_BIT_COUNT-1:`ADDR_BIT_COUNT-`BANKS_BIT_COUNT];","assign bank_addr=ADDR_DFF[`ADDR_BIT_COUNT-1];")

# for CMUX=2 and CMUX=1
##CMUX=1
if COLS_BIT_COUNT == 0:
	filedata = filedata.replace("output [`CMUX-1:0] CSEL","output CSEL")
	filedata = filedata.replace("wire [`COLS_BIT_COUNT-1:0] col_addr;", " ")
	filedata = filedata.replace("wire [`CMUX-1:0] CSEL;", "wire CSEL;")
	filedata = filedata.replace("assign col_addr=ADDR_DFF[`COLS_BIT_COUNT-1:0];"," ")
	filedata = filedata.replace("assign CSEL=(CE_DFF)?(1<<<col_addr):1'b0;","assign CSEL=CE_DFF;")
##CMUX=2
elif COLS_BIT_COUNT == 1: 
	filedata = filedata.replace("wire [`COLS_BIT_COUNT-1:0] col_addr;","wire col_addr;")
	filedata = filedata.replace("assign col_addr=ADDR_DFF[`COLS_BIT_COUNT-1:0];","assign col_addr=ADDR_DFF[0];")

#Delay Module instantiation
if max_stage !=0:
	if Banks == 1:
		output_pins_w_dly_string="DLY_MODULE DLY_MODULE (.in(~CK)"
	elif Banks >=2:
		output_pins_w_dly_string="DLY_MODULE DLY_MODULE (.in(~CK_int)"
for pin_name in output_pins_w_dly_dict:
	output_pins_w_dly_string=output_pins_w_dly_string+",."+pin_name+"("+pin_name+"_dly)"
	wire_for_dly_string=wire_for_dly_string+"wire "+pin_name+"_dly;\n"
	if Banks==1:
		filedata = filedata.replace("assign "+pin_name,"//assign "+pin_name)
		filedata = filedata.replace("////assign "+pin_name+"="+pin_name+"_dly","assign "+pin_name+"="+pin_name+"_dly")	
	elif Banks >=2:
		filedata = filedata.replace("assign "+pin_name+"_int","//assign "+pin_name+"_int")
		filedata = filedata.replace("////assign "+pin_name+"_int="+pin_name+"_dly","assign "+pin_name+"_int="+pin_name+"_dly")
if max_stage !=0:
	output_pins_w_dly_string = output_pins_w_dly_string +");\n"

filedata = filedata.replace("//Output signal w inserting delay elements\n","//Output signal w inserting delay elements\n"+output_pins_w_dly_string)
filedata = filedata.replace("//wire for delay signal\n","//wire for delay signal\n"+wire_for_dly_string)

##check pulse width control for WLEB & SAEB
if output_pins_w_dly_dict.get('WLEB') is None:
	filedata = filedata.replace(" & ~WLEB_dly;", ";")
if output_pins_w_dly_dict.get('SAEB') is None:
	filedata = filedata.replace(" & ~SAEB_dly;", ";")


##Multi-bank output signals
if Banks>=2:	
	for i in range(Banks):
		output_INA_string = output_INA_string + "\toutput [`IN_NUMBER-1:0] INA"+str(i)+",\n"
		output_INB_string = output_INB_string + "\toutput [`IN_NUMBER-1:0] INB"+str(i)+",\n"
		assign_CK_string = assign_CK_string + "assign CK["+str(i)+"]=(BS["+str(i)+"])?CK_int:1'b0;\n" 
		assign_PRCH_string = assign_PRCH_string + "assign PRCH["+str(i)+"]=(BS["+str(i)+"])?PRCH_int:1'b1;\n"
		assign_WEN_string = assign_WEN_string + "assign WEN["+str(i)+"]=(BS["+str(i)+"])?WEN_int:1'b0;\n"
		assign_WLE_string = assign_WLE_string + "assign WLE["+str(i)+"]=(BS["+str(i)+"])?WLE_int:1'b0;\n"
		assign_SAE_string = assign_SAE_string + "assign SAE["+str(i)+"]=(BS["+str(i)+"])?SAE_int:1'b0;\n"
		##assign_DREQ_string = assign_DREQ_string + "assign DATA_REQ["+str(i)+"]=BS["+str(i)+"] & ~CLK;\n" 
		assign_INA_string = assign_INA_string + "assign INA"+str(i)+"=(WLE["+str(i)+"])?INA_int:"+str(IN_NUMBER)+"'b0;\n"
		assign_INB_string = assign_INB_string + "assign INB"+str(i)+"=(WLE["+str(i)+"])?INB_int:"+str(IN_NUMBER)+"'b0;\n"
		assign_CSEL_string = assign_CSEL_string + "assign CSEL"+str(i)+"=(BS["+str(i)+"])?CSEL:"+str(CMUX)+"'b0;\n"
		if CMUX ==1:
			output_CSEL_string = output_CSEL_string + "\toutput CSEL"+str(i)+",\n"
		elif CMUX >1:
			output_CSEL_string = output_CSEL_string + "\toutput [`CMUX-1:0] CSEL"+str(i)+",\n"
			


	filedata = filedata.replace("\t//Output for INA\n","\t//Output for INA\n"+output_INA_string)
	filedata = filedata.replace("\t//Output for INB\n","\t//Output for INB\n"+output_INB_string)
	filedata = filedata.replace("\t//Output for CSEL\n","\t//Output for CSEL\n"+output_CSEL_string)
	filedata = filedata.replace("for local CK\n","for local CK\n"+assign_CK_string)
	filedata = filedata.replace("for local PRCH\n","for local PRCH\n"+assign_PRCH_string)
	filedata = filedata.replace("for local WEN\n","for local WEN\n"+assign_WEN_string)
	filedata = filedata.replace("for local WLE\n","for local WLE\n"+assign_WLE_string)
	filedata = filedata.replace("for local SAE\n","for local SAE\n"+assign_SAE_string)
	##filedata = filedata.replace("for local DATA_REQ\n","for local DATA_REQ\n"+assign_DREQ_string)
	filedata = filedata.replace("for local INA\n","for local INA\n"+assign_INA_string)
	filedata = filedata.replace("for local INB\n","for local INB\n"+assign_INB_string)
	filedata = filedata.replace("for local CSEL\n","for local CSEL\n"+assign_CSEL_string)

#Write out new CU_gen Verilog
if Banks==1:
	f = open("rtl/CU_sbank.v","w")
	f.write(filedata)
	f.close()

elif Banks>=2:
	f = open("rtl/CU_mbank.v","w")
	f.write(filedata)
	f.close()

#Write the delay module verilog file
f = open("rtl/DLY_MODULE_base.v","r") 
filedata = f.read()
f.close()

#output ports declaration
output_ports_string=""
output_ports_pointer=0
for pin_name in output_pins_w_dly_dict:
	output_ports_string=output_ports_string+"\toutput " + pin_name
	if output_ports_pointer < num_output_pin-1:
		output_ports_string=output_ports_string+",\n"
	elif output_ports_pointer == num_output_pin-1:
		output_ports_string=output_ports_string+"\n"
	output_ports_pointer = output_ports_pointer+1

## wire and delay elements declarations	
wires_string=""
delay_cells_string=""
for i in range(max_stage):
	wires_string = wires_string + "wire in" + str(i)+";\n"
	delay_cells_string = delay_cells_string + dly_cell_name + " U" +str(i)+" (.A(in"+str(i)+"),.Y(in" +str(i+1)+"));\n"

##Assign output based on the number of stage
output_assign_string=""
for pin_name in output_pins_w_dly_dict:
	#output_assign_string = output_assign_string + "assign in"+str(output_pins_w_dly_dict[pin_name])+"="+pin_name+";\n"
	output_assign_string = output_assign_string + "assign "+pin_name+"= in"+str(output_pins_w_dly_dict[pin_name])+";\n"

# Update Verilog code
filedata = filedata.replace("\t//Output port\n","\t//Output port\n"+output_ports_string)
filedata = filedata.replace("//Wire Definition\n","//Wire Definition\n"+wires_string)	
filedata = filedata.replace("//Delay cells instantiation\n","//Delay cells instantiation\n"+delay_cells_string)
filedata = filedata.replace("//Output assign\n","//Output assign\n"+output_assign_string)	
f = open("rtl/DLY_MODULE.v","w")
f.write(filedata)
f.close()

##Copy the output .v file to CU.v file
rtldir=maindir+"/rtl"
os.chdir(rtldir)
if Banks==1:
	tp=sp.Popen(['cp', 'CU_sbank.v', 'CU.v']) #execute a copy process
	tp.wait()
elif Banks>=2:
	tp=sp.Popen(['cp', 'CU_mbank.v', 'CU.v']) #execute a copy process
	tp.wait()


syndir=maindir+"/syn"
os.chdir(syndir)
tp=sp.Popen(['python3', 'syn.py']) #execute the synthesis process 
tp.wait()


aprdir=maindir+"/apr"
os.chdir(aprdir)
tp=sp.Popen(['python3', 'apr.py']) #execute the APR process 
tp.wait()


tp=sp.Popen(['rm', '-rf', 'CU.io']) #remove the IO file 
tp.wait()


##change the module name and then and inout pins VDD/VSS
apr_out_dir=maindir+"/apr/run_0/outputs"
os.chdir(apr_out_dir)
CU_module_name="CU_"+str(NumberofWordPerBank)+"X"+str(Wordsize)+"XCM"+str(CMUX)+"XBANK"+str(Banks)
CU_module_verilog_name=CU_module_name+".v"

f_lvs_v_r = open("CU_lvs.v","r")
f_lvs_v_w = open(CU_module_verilog_name,"w")

replace_pointer=False
for line in f_lvs_v_r:
	if replace_pointer==False:
		if line.startswith("module CU (\n"):
			line = line.replace("module CU (\n", "module "+CU_module_name+" (\n")
			f_lvs_v_w.write(line)
			replace_pointer=True
		else:
			f_lvs_v_w.write(line)
	else:			
		if Banks==1:
			line = line.replace("SAE);\n","SAE,\n\tVDD,\n\tVSS);\n")
			line = line.replace("SAE;\n","SAE;\n   inout VDD;\n   inout VSS;\n")
			f_lvs_v_w.write(line)
		elif Banks>=2:
			line = line.replace("DOUT);\n","DOUT,\n\tVDD,\n\tVSS);\n")
			line = line.replace("DOUT;\n","DOUT;\n   inout VDD;\n   inout VSS;\n")
			f_lvs_v_w.write(line)

replace_pointer=False
f_lvs_v_r.close()
f_lvs_v_w.close()

