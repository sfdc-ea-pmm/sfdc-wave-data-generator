from data_generator import DataGenerator


import sys, os
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(10 * megabytes)                   # default: roughly a floppy

def split(fromfile, todir, chunksize=chunksize): 
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fname in os.listdir(todir):            # delete any existing files
            os.remove(os.path.join(todir, fname)) 
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(todir, ('part%04d' % partnum))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum
            
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: split.py [file-to-split target-dir [chunksize]]')
    else:
        if len(sys.argv) < 3:
            interactive = 1
            fromfile = raw_input('File to be split? ')       # input if clicked 
            todir    = raw_input('Directory to store part files? ')
        else:
            interactive = 0
            fromfile, todir = sys.argv[1:3]                  # args in cmdline
            if len(sys.argv) == 4: chunksize = int(sys.argv[3])
        absfrom, absto = map(os.path.abspath, [fromfile, todir])
        print ('Splitting', absfrom, 'to', absto, 'by', chunksize)

        try:
            parts = split(fromfile, todir, chunksize)
        except:
            print ('Error during split:')
            print (sys.exc_type, sys.exc_value)
        else:
            print ('Split finished:', parts, 'parts are in', absto)
        if interactive: raw_input('Press Enter key') # pause if clicked



# import logging.handlers
# log = logging.getLogger()
# fh = logging.handlers.RotatingFileHandler("test.csv", maxBytes=1*10**7, backupCount=100) 
# # 100 MB each, up to a maximum of 100 files
# log.addHandler(fh)
# log.setLevel(logging.INFO)
# f = open("test.csv")
# while True:
#     log.info(f.readline().strip())




# import os
# import time

# #---
# file = "test.csv" 
# out_dir = "/slices"
# size_ofslices = 10 # in mb
# identifying_string = "\n"
# #---

# line_number = -1
# records = [0]

# # analyzing file -------------------------------------------

# print("analyzing file...\n")
# # size in mb
# print("checking file size...")
# size = int(os.stat(file).st_size/1000000)
# print("file size:", size, "mb")
# # number of sections
# print("calculating number of slices...")
# sections = int(size/size_ofslices)
# print(sections, "slices of", size_ofslices, "mb")
# # misc. data
# print("checking number of lines...")
# with open(file) as src:
#     for line in src:
#         line_number = line_number+1
#         if identifying_string in line:
#             records.append(line_number)
# # last index (number of lines -1)
# ns_oflines = line_number
# print("number of lines:", ns_oflines)
# # number of records
# print("checking number of records...")
# ns_records = len(records)-1
# print("number of records:", ns_records)
# # records per section
# print("calculating number records per section ...")
# ns_recpersection = int(ns_records/sections)
# print("records per section:", ns_recpersection)

# # preparing data -------------------------------------------

# rec_markers = [i for i in range(ns_records) if i% ns_recpersection == 0]+[ns_records]   # dividing records (indexes of) in slices
# line_markers = [records[i] for i in rec_markers]                                        # dividing lines (indexes of) in slices
# line_markers[-1] = ns_oflines; line_markers.pop(-2)                                     # setting lias linesection until last line

# # creating sections ----------------------------------------

# sl = 1
# line_number = 0

# curr_marker = line_markers[sl]
# outfile = out_dir+"/"+"slice_"+str(sl)+".txt"

# def writeline(outfile, line):
#     with open(outfile, "a") as out:
#         out.write(line)

# with open(file) as src:
#     print("creating slice", sl)
#     for line in src:
#         if line_number <= curr_marker:
#             writeline(outfile, line)
#         else:
#             sl = sl+1
#             curr_marker = line_markers[sl]
#             outfile = out_dir+"/"+"slice_"+str(sl)+".txt"
#             print("creating slice", sl)
#             writeline(outfile, line)       
#         line_number = line_number+1






# def run(source_file_name, output_file_name):
#     data_gen = DataGenerator()

#     # load source file
#     data_gen.load_source_file(source_file_name)

#     # write to new path
#     data_gen.write(output_file_name)


