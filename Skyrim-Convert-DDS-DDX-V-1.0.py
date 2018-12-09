############################################################################################
###^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^Made by Death_Dealer^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^###
###-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^DDS-DDX Conversion^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-###
###^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-SKYRIM-EDITION-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^###
############################################################################################
import struct, zlib, binascii, sys, tkinter, array, os
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
############################################################################################
infile =  filedialog.askopenfilename(title = "Select a .dds to extract..",
    filetypes = (("Direct Draw Surface Files","*.dds"),
    ("all files","*.*")))
Imagelevel = input('Enter a ImageLevel (1-3) = ')
############################################################################################ 
with open(infile, 'rb') as infile_:
    infile_read = infile_.read(128)
    header_hex = binascii.hexlify(infile_read)
############################################################################################
head=(b'\x4F\x5A\x50\x33')
length=int.from_bytes((infile_read[(11):(15)]), byteorder='big')
a=128
keyint=(1)

while a != length:
    keyint+=(1)
    b=((a)*(2))
    a=b
    
print('keyint1 = '+str(keyint))

hex_keyint = (keyint).to_bytes(1, byteorder='big')
hex_keyint = (b'\x05\x00\x00'+hex_keyint)

head_part_1 = infile_read[:25]

head_part_2 = infile_read[29:]

keyint2=(1)
a=1
while a != length:
    keyint2+=(1)
    b=a*2
    a=b
print('keyint2 = '+str(keyint2))

hex_keyint2 = (keyint2).to_bytes(4, byteorder='big')

header = (head+hex_keyint+head_part_1+hex_keyint2+head_part_2)

nvtt_tag = (b'\x4E\x56\x54\x54\x04\x00\x02\x00')
header_1 = header[:76]
header_2 = header[84:]
header = header_1+nvtt_tag+header_2

mip_map_count_int = input('Amount of MipMapping to attach? (small-10/medium-11/large-12) ')
mip_map_count = int(mip_map_count_int).to_bytes(1, byteorder='big')
mip_map_count_int = int(mip_map_count_int)-2
header_1 = header[:36]
header_2 = header[37:]
header = header_1+mip_map_count+header_2

############################################################################################
DXT = header[92:96].decode("utf-8").lower()

if DXT == ('dxt1'):
    DXT = ('dxt1a')
    
os.system(('nvdxt -')+(DXT)+(' -nmips 3 -file ')+str(os.path.basename(infile))+(' -outfile ')+(os.path.basename(infile)))
os.system(('detach ')+(str(os.path.basename(infile))[:-4]))

if int(Imagelevel) == int(1):
    os.system(('nvdxt -')+(DXT)+(' -nmips ')+str(mip_map_count_int)+(' -file ')+str(os.path.basename(infile)[:-4])+('_00.dds')+(' -outfile ')+(os.path.basename(infile)[:-4])+('_00.dds'))

if int(Imagelevel) == int(2):
    os.system(('nvdxt -')+(DXT)+(' -nmips ')+str(mip_map_count_int)+(' -file ')+str(os.path.basename(infile)[:-4])+('_01.dds')+(' -outfile ')+(os.path.basename(infile)[:-4])+('_01.dds'))
    
if int(Imagelevel) == int(3):
    os.system(('nvdxt -')+(DXT)+(' -nmips ')+str(mip_map_count_int)+(' -file ')+str(os.path.basename(infile)[:-4])+('_02.dds')+(' -outfile ')+(os.path.basename(infile)[:-4])+('_02.dds'))

print('DXT = '+str(DXT))

y = array.array('L', header)
y.byteswap()
header_prep_ = (binascii.hexlify(y))
ddx_header = (binascii.unhexlify(header_prep_))

############################################################################################

com_1 = open((os.path.basename(infile)[:-4])+str('.dds'), 'rb').read()

com_1_c = zlib.compress(com_1[128:],6)
    
com_size_1=(len(com_1_c).to_bytes(4, byteorder='big'))

############################################################################################

com_2 = open((os.path.basename(infile)[:-4])+str('_01.dds'), 'rb').read()
  
com_2_c = zlib.compress(com_2[128:],6)

com_size_2=(len(com_2_c).to_bytes(4, byteorder='big'))

############################################################################################

com_3 = open((os.path.basename(infile)[:-4])+str('_02.dds'), 'rb').read()

com_3_c = zlib.compress(com_3[128:],6)

com_size_3=(len(com_3_c).to_bytes(4, byteorder='big'))

############################################################################################
null = (b'\x00\x00\x00\x00')

if Imagelevel == str('3'):
    ddx = (ddx_header+com_size_3+com_size_2+com_size_1+com_3_c+com_2_c+com_1_c)
 
if Imagelevel == str('2'):
    ddx = (ddx_header+com_size_2+com_size_1+null+com_2_c+com_1_c)

if Imagelevel == str('1'):
    ddx = (ddx_header+com_size_1+null+null+com_1_c)
    
with open(((str(infile)[:-4])+str('.ddx')),'wb')as out:
    out_write = out.write(ddx)

os.remove((os.path.basename(infile)[:-4])+str('_00.dds'))
os.remove((os.path.basename(infile)[:-4])+str('_01.dds'))
os.remove((os.path.basename(infile)[:-4])+str('_02.dds'))
############################################################################################
