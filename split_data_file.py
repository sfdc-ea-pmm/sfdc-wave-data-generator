import sys, os

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(10 * megabytes)      # default: 10 MB
fileSuffix = '-dataPart-'


def split(fromdir, fromfile, todir, suffix='part', chunksize=chunksize, deleteSource=False): 
    delete_later = ''
    fname, fext = fromfile.split('.')
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fn in os.listdir(todir):            # delete any existing splitted files
            if fromfile == fn:
                if deleteSource: delete_later = os.path.join(todir, fn)
            else:
                if fname+suffix in fn:
                    os.remove(os.path.join(todir, fn)) 
    
    partnum = 0
    input = open(fromdir+fromfile, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(todir, ((fname+suffix+'%04d'+'.'+fext) % partnum))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    assert partnum <= 9999                         # join sort fails if 5 digits
    if deleteSource and delete_later!='': 
        os.remove(delete_later)
    return partnum
            
def split_if_needed(fromdir, fromfile, todir, suffix='part', chunksize=chunksize, deleteSource=False):
    absfrom = fromdir+fromfile
    absto = todir
    fsize = os.path.getsize(absfrom)
    if fsize > chunksize:
        print ('Splitting', absfrom, 'to', absto, 'by', chunksize)
        r = split(fromdir, fromfile, todir, suffix, chunksize, deleteSource)
    else:
        r = 0 
    return r


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: split_data_file.py [file-to-split target-dir [chunksize-in-bytes]]')
    else:
        ## this section is used when calling as a script
        if len(sys.argv) == 1:
            fromfile = 'test.csv'
            todir = 'testoutput'
        elif len(sys.argv) < 5:
            fromfile, todir = sys.argv[1:3]           # args in cmdline
            if len(sys.argv) == 4: chunksize = int(sys.argv[3])
        ##
        absfrom, absto = map(os.path.abspath, [fromfile, todir])

        try:
            parts = split_if_needed(fromfile, todir, fileSuffix, chunksize)
        except:
            print ('Error during split:')
            print (sys.exc_type, sys.exc_value)
        else:
            if parts == 0:
                print('File not splitted')
            else: 
                print ('Split finished:', parts, 'parts are in', absto)
