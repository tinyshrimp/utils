'''
Created on Jan 4, 2011

@author: xiwang
'''
import os

STDOUT_MSGS='/tmp/stdout_msgs'
STDERR_MSGS='/tmp/stderr_msgs'
        
def copyfile(source, dest):
    if not hasattr(source, 'read'):
        src_file = open(source, 'rb')
    if not hasattr(dest, 'write'):
        dest_file = open(dest, 'wb')
    while True:
        buffer = src_file.read(1024*1024)
        if buffer:
            dest_file.write(buffer)
        else:
            break
    dest_file.close()
    src_file.close()
    
def executeCommand(cmd):    
    import subprocess
    
    stdout_msgs = open(STDOUT_MSGS, 'w')
    stderr_msgs = open(STDERR_MSGS, 'w')
    
    sp = subprocess.Popen(cmd, shell=True, stdout=stdout_msgs, stderr=stderr_msgs)
    ret = sp.wait()
    
    stdout_msgs.close()
    stderr_msgs.close()

    stdout_msgs = open(STDOUT_MSGS, 'r')
    outs = stdout_msgs.readlines()
    stdout_msgs.close()
    os.remove(STDOUT_MSGS)
    
    stderr_msgs = open(STDERR_MSGS, 'r')
    errs = stderr_msgs.readlines()
    stderr_msgs.close()
    os.remove(STDERR_MSGS)
    
    return (ret, outs, errs)
