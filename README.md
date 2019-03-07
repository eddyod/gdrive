This script is based on an issue from: 
https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url

I modified it to check for an existing file. If it finds the file, it
will continue from that point instead of downloading the whole file
again. Similar to what 'wget -c' does. My router was bombing out with
large downloads. Thanks At&t!
