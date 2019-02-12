import sys

print('Hello, World!')

print('The sum of 2 and 3 is 5.')

sum = int(sys.argv[1]) + int(sys.argv[2])


print('The sum of {0} and {1} is {2}.'.format(sys.argv[1], sys.argv[2], sum))



import boto3
import botocore
import hashlib
import os



BUCKET_NAME = 'ncar-archives-pre' # replace with your bucket name
KEY = 'collectionKey.xml' # replace with your object key
CHKSUMTMP = 'chksumtmp/'

def delete_local_file (location):

    import os
    if os.path.exists(location):
      os.remove(location)
    else:
      print("The file does not exist")
      
      
def checksum (file_path):
    import os
    if not os.path.exists(file_path):
        sys.exit("ERROR: Files %s was not found!" % file_path)
    
    with open(file_path, 'rb') as f:
    	contents = f.read()
    	print("SHA1: %s" % hashlib.sha1(contents).hexdigest())
    	print("SHA256: %s" % hashlib.sha256(contents).hexdigest())
    	#md5 accepts only chunks of 128*N bytes
    	md5 = hashlib.md5()
    	for i in range(0, len(contents), 8192):
    		md5.update(contents[i:i+8192])
    	print("MD5: %s" % md5.hexdigest())
    	print()
    	return



# Create an S3 client
s3c = boto3.client('s3')

#create an s3 resource
s3r = boto3.resource('s3')

# Call S3 to list current buckets
response = s3c.list_buckets()

def getfilefroms3(bucket_name, object_name, down_load_dir):

    s3r = boto3.resource('s3')
    
    import ntpath
    base_name = ntpath.basename(object_name)

    try:
        s3r.Bucket(bucket_name).download_file(object_name, down_load_dir + base_name)
#        print("The bucket has been downloaded.")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    else:
        print ("The file has downloaded succesfully")
    return base_name   

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list
print("Bucket List: %s" % buckets)



# Connet to a specific bucket
bucket = s3r.Bucket(BUCKET_NAME)

# Get subdirectory info
prefix = 'Unprocessed digital collections'
# prefix = 'Test1/'
# prefix = ''



#for obj in bucket.objects.filter(Prefix=prefix):
#  print (obj.key)
  
  
print("Listing Subdirectories/n/n/n")
print()
print()
  

# prefix = ''
downloaddir = '/home/ec2-user/environment/chksumtmp/'

  




def getfilesfroms3folder(bucket, prefix, downloaddir):
    
    filenames = []

    FilesNotFound = True
    i = 0
    for obj in bucket.objects.filter(Prefix=prefix):
#        print('{0}:{1}'.format(bucket.name, obj.key))
        if not obj.key.endswith(os.sep):
            filenames.append(obj.key)
            FilesNotFound = False
            i = i + 1
    
        else:
            print("Object Key {0} ends with a slash".format(obj.key))
            print()
        
    if FilesNotFound:
         print("ALERT", "No file in {0}/{1}".format(bucket, prefix)) 
         
    print('Total objects in bucket {0}, prefix = {1} = {2}' .format(bucket, prefix, i))
    return filenames
     
     
# file_names = getfilesfroms3folder(bucket, prefix, downloaddir)
keys = getfilesfroms3folder(bucket, prefix, downloaddir)

for key in keys:
    base_name = getfilefroms3(bucket.name, key, downloaddir)

    checksum(downloaddir + base_name)
         
    delete_local_file(downloaddir + base_name)
              
bucketname = BUCKET_NAME
filename = KEY


#getfilefroms3(bucketname, filename, downloaddir)

