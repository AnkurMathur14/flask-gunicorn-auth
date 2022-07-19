import os
import fcntl
import json
import contextlib

READ = 1
WRITE = 2

@contextlib.contextmanager
def config_dir(cfg_dir, mode):
    if not os.path.isdir(cfg_dir):
        os.makedirs(cfg_dir, 0o700)
        os.system(cmd)

    lock_file = os.path.join(cfg_dir, 'cfg.lock')
    with open(lock_file, 'wb') as lock_fd:
        pass
    if mode == READ:
        lock_fd = open(lock_file, 'rb')
        fcntl.lockf(lock_fd, fcntl.LOCK_SH)
    else:
        lock_fd = open(lock_file, 'wb')
        fcntl.lockf(lock_fd, fcntl.LOCK_EX)
    try:
        yield
    finally:
        lock_fd.close()

def write(obj, cfg_dir, bname):
    cfg_file = os.path.join(cfg_dir, bname)
    with open(cfg_file, 'w') as cfg_stream:
        json.dump(obj, cfg_stream, indent=2)

def read(cfg_dir, bname):
    cfg_file = os.path.join(cfg_dir, bname)
    if os.path.exists(cfg_file):
        with open(cfg_file, 'r') as cfg_stream:
            return json.load(cfg_stream)
    else:
        return []
        
# Functions for saving and loading the user information
def save_users(users):
    cfg_dir = "/root/myproject"
    with config_dir(cfg_dir, WRITE):
        write(users, cfg_dir, 'users.json')
    return True
    
def get_users():
    users = []
    cfg_dir = "/root/myproject"
    with config_dir(cfg_dir, READ):
        users = read(cfg_dir, 'users.json')
    return users

# Functions for saving and loading the filesystems information
def save_filesystems(filesystems):
    cfg_dir = "/root/myproject"
    with config_dir(cfg_dir, WRITE):
        write(filesystems, cfg_dir, 'filesystems.json')
    return True
    
def get_filesystems():
    filesystems = []
    cfg_dir = "/root/myproject"
    with config_dir(cfg_dir, READ):
        filesystems = read(cfg_dir, 'filesystems.json')
    return filesystems