import urllib2
import sys
import os
import re

def if_exist_then_increment(param_path, param_file_name):
    full_path = param_path + "/" + param_file_name
    print("check if exist : " + full_path.encode('utf-8'))
    ##check if a file exist with full path
    if os.path.isfile(full_path):
        print("file already exist!!")
        ##if the file exists, check it's numbering
        ##before check numbering, we need to extract file name
        filenameonly, fileextension = os.path.splitext(param_file_name)
        print("file name only : " + filenameonly.encode('utf-8'))
        print("file extension : " + fileextension.encode('utf-8'))
        ##check if it ends with "-number", which means it has already been modified by this process or others
        if re.search('-\d+$', filenameonly):
            print("end with -number!!")
            numbers = re.search('\d+$', filenameonly)
            if numbers:
                number = numbers.group(0)
                print("last number :" + number)
                num = int(number) + 1
                newfilenameonly = re.sub(r'\d+$', str(num), filenameonly)
                incremnted_filename = newfilenameonly + fileextension
                print("incremented file name : " + incremnted_filename.encode('utf-8'))
                return if_exist_then_increment(param_path, incremnted_filename)
            else:
                # normaly it should never get here
                print("something's wrong")
                return ""
        else:
            ##if the file name does not end with "-number", just add "-1" to fixedfilename
            modifiedfilename = filenameonly + "-1" + fileextension
            print("-1 added file name : " + modifiedfilename.encode('utf-8'))
            ##one more thing.. we need to check if "-1" added file name exists
            return if_exist_then_increment(param_path, modifiedfilename)
    else:
        print("file does not exist : " + full_path.encode('utf-8'))
        ##finally manage to get out of this function with proper value
        return full_path


print(sys.argv[1])
fullpath = sys.argv[1]
print("full path : " + fullpath)
filename = os.path.basename(fullpath)
path = os.path.dirname(os.path.abspath(fullpath))
print("path : " + path)
print("file name : " + filename)
## unquote filename
fixedfilename = urllib2.unquote(filename).decode('utf8')
print ("fixed file name : " + fixedfilename.encode('utf-8'))
fixedfullpath = path + "/" + fixedfilename
print("fixed full path : " + fixedfullpath.encode('utf-8'))

checkedfilenamepath = if_exist_then_increment(path, fixedfilename)
print("final filename : " + checkedfilenamepath.encode('utf-8'))
# checkedfilename = os.path.basename(checkedfilenamepath)
print("change from : " + fullpath.encode('utf-8'))
print("change to : " + checkedfilenamepath.encode('utf-8'))
if checkedfilenamepath != "":
    os.rename(fullpath, checkedfilenamepath)
