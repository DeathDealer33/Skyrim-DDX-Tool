############################################################################################
###^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^Made by Death_Dealer^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^###
###-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^DDX-DDS Conversion^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-###
###^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-SKYRIM-EDITION-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^###
############################################################################################
import struct, zlib, binascii, sys, tkinter, array, os
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
############################################################################################
root = Tk()
root.withdraw()
infile =  filedialog.askopenfilename(title = "Select a .ddx to extract..",
    filetypes = (("Direct Draw X Files","*.ddx"),
    ("all files","*.*"))) 
############################################################################################ 
with open(infile, 'rb') as infile_:
    infile_read = infile_.read(148)
    header_hex = binascii.hexlify(infile_read)
############################################################################################   

x = (infile_read)
y = array.array('l', x)
y.byteswap()
header_prep_ = (binascii.hexlify(y))
null= (b'00')
header_prep1 = header_prep_[16:16+60]
header_prep2 = header_prep_[62:16+194]
header_prep = (header_prep1+null+header_prep2)

############################################################################################
data_len_1 = int.from_bytes((infile_read[(136):(140)]), byteorder='big')
data_len_2 = int.from_bytes((infile_read[(140):(144)]), byteorder='big')
data_len_3 = int.from_bytes((infile_read[(144):(148)]), byteorder='big')
############################################################################################

large_length = int((header_hex[40:48]), 16)
large_width = int((header_hex[48:56]), 16)

if data_len_3 !=(0):
    medium_length = int(large_length / 2)
    medium_width = int(large_width / 2)
else:
    medium_length = int(large_length)
    medium_width = int(large_width)
    
if data_len_2 !=(0):    
    small_length = int(medium_length / 2)
    small_width = int(medium_width / 2)
else:
    small_length = int(medium_length)
    small_width = int(medium_width)

header_part_1 = binascii.hexlify(y[2:5])
header_part_2 = binascii.hexlify(y[7:34])

small_len_hex = binascii.hexlify(struct.pack('i', small_length))
small_wid_hex = binascii.hexlify(struct.pack('i', small_width))
medium_len_hex = binascii.hexlify(struct.pack('i', medium_length))
medium_wid_hex = binascii.hexlify(struct.pack('i', medium_width))
large_len_hex = binascii.hexlify(struct.pack('i', large_length))
large_wid_hex = binascii.hexlify(struct.pack('i', large_width))

small_header = binascii.unhexlify((header_part_1 + small_len_hex + small_wid_hex + header_part_2))

medium_header = binascii.unhexlify((header_part_1 + medium_len_hex + medium_wid_hex + header_part_2))

large_header = binascii.unhexlify((header_part_1 + large_len_hex + large_wid_hex + header_part_2))

############################################################################################
filename = (os.path.splitext(os.path.basename(infile)))
with open(infile, 'rb') as infile:
    infile_read = infile.read()
if data_len_1 != (0):
    small_data_com = infile_read[148:148+data_len_1]
    small_decom =  zlib.decompress(small_data_com)
    small = filename[0] + ("-small") + (".dds")
    with open(small, 'wb') as small_:
        small_write = small_.write(small_header)
        small_write = small_.write(small_decom)
        print(str(filename[0] + ("-small") + (".dds")+(' -')+str(small_length)+('x')+str(small_width)))
        
if data_len_2 != (0):
    medium_data_com = infile_read[148+data_len_1:148+data_len_1+data_len_2]
    medium_decom =  zlib.decompress(medium_data_com)
    medium = filename[0] + ("-medium") + (".dds")
    with open(medium, 'wb') as medium_:
        medium_write = medium_.write(medium_header)
        medium_write = medium_.write(medium_decom)
        print(str(filename[0] + ("-medium") + (".dds")+(' -')+str(medium_length)+('x')+str(medium_width)))
        
if data_len_3 != (0):
    large_data_com = infile_read[148+data_len_1+data_len_2:148+data_len_1+data_len_2+data_len_3]
    large_decom =  zlib.decompress(large_data_com)
    large = filename[0] + ("-large") + (".dds")
    with open(large, 'wb') as large_:
        large_write = large_.write(large_header)
        large_write = large_.write(large_decom)
        print(str(filename[0] + ("-large") + (".dds")+(' -')+str(large_length)+('x')+str(large_width)))
############################################################################################
