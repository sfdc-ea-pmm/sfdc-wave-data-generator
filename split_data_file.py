import sys, os
import boto3
import codecs
import csv
import io

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(10 * megabytes)      # default: 10 MB
fileSuffix = '-dataPart-'
fromdir = '' 


def split(fromdir, fromfile, todir, suffix='part', chunksize=chunksize, deleteSource=False): 
    delete_later = ''
    fname, fext = fromfile.split('.')

    if os.environ.get('READ_MODE') == 'S3':
        client = boto3.client('s3')
        s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
        source_file_object = client.get_object(Bucket=s3_bucket_name, Key=fromdir+fromfile)
        source_file_body = source_file_object['Body']
        text_stream = codecs.getreader("utf-8")(source_file_body)
        partnum = 0
        while 1:                                       # eof=empty string from read
            chunk = text_stream.read(chunksize)        # get next part <= chunksize
            if not chunk: break
            partnum  = partnum+1
            filename = os.path.join(todir, ((fname+suffix+'%d'+'.'+fext) % partnum))
            chunk2 = io.BytesIO(bytes(chunk, 'utf-8'))
            client.upload_fileobj(chunk2, s3_bucket_name, filename)
            client.put_object_acl(ACL='public-read', Bucket=s3_bucket_name, Key=filename)
        text_stream.close(  )

        if deleteSource:
            client.delete_object(Bucket=s3_bucket_name, Key=fromdir+fromfile)

    else: 
        if not os.path.exists(todir):                  # caller handles errors
            os.mkdir(todir)                            # make dir, read/write parts
        else:
            for fn in os.listdir(todir):               # delete any existing splitted files
                if fromfile == fn:
                    if deleteSource: delete_later = os.path.join(todir, fn)
                else:
                    if fname+suffix in fn:
                        os.remove(os.path.join(todir, fn))
        
        partnum = 0
        input = open(fromdir+fromfile, 'rb')           # use binary mode on Windows
        while 1:                                       # eof=empty string from read
            chunk = input.read(chunksize)              # get next part <= chunksize
            if not chunk: break
            partnum  = partnum+1
            filename = os.path.join(todir, ((fname+suffix+'%d'+'.'+fext) % partnum))
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
    if os.environ.get('READ_MODE') != 'S3':
        fsize = os.path.getsize(absfrom)
    else:
        client = boto3.client('s3')
        s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
        source_file_object = client.get_object(Bucket=s3_bucket_name, Key=fromdir+fromfile)
        fsize = source_file_object['ContentLength']

    if fsize > chunksize:
        print ('Splitting', absfrom, 'to', absto, 'by', chunksize)
        r = split(fromdir, fromfile, todir, suffix, chunksize, deleteSource)
    else:
        r = 0 
    return r


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: split_data_file.py [from-dir file-to-split target-dir [chunksize-in-bytes] [deleteSource=True/False]]')
    else:
        ## this section is used when calling as a script
        if len(sys.argv) == 1:
            fromdir = ''
            fromfile = 'test.csv'
            todir = 'testoutput'
        elif len(sys.argv) < 5:
            fromfile, todir = sys.argv[1:3]           # args in cmdline
            if len(sys.argv) == 4: chunksize = int(sys.argv[3])
        ##
        _, absto = map(os.path.abspath, [fromfile, todir])

        try:
            parts = split_if_needed(fromdir, fromfile, todir, fileSuffix, chunksize, deleteSource=True)
        except:
            print ('Error during split:')
            print (sys.stderr)
        else:
            if parts == 0:
                print('File not splitted')
            else: 
                print ('Split finished:', parts, 'parts are in', absto)
