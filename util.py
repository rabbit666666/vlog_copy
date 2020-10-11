import os
import datetime
import hashlib
import sys

BLOCK_1M = 1024 * 1024

def convert_timestamp_to_date(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    date = '{:04}_{:02}_{:02}_{:02}_{:02}_{:02}'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return date

def convert_timestamp_to_date2(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    date = '{:04}_{:02}_{:02}'.format(dt.year, dt.month, dt.day)
    return date

def get_raw_name(path):
    dir, base_name = os.path.split(path)
    tokens = base_name.split('@')
    raw_name = None
    if len(tokens) == 1:
        raw_name = tokens[0]
    elif len(tokens) == 2:
        raw_name = tokens[1]
    raw_path = os.path.join(dir, raw_name)
    return raw_path

def get_video_new_name(full_path):
    if full_path.find('@') != -1:
        return full_path
    modify_time = os.path.getmtime(full_path)
    date = convert_timestamp_to_date(modify_time)
    dir, base_name = os.path.split(full_path)
    name, ext = os.path.splitext(base_name)
    new_path = os.path.join(dir, '{}@{}{}'.format(date, name, ext))
    return new_path

def get_file_digest(path):
    with open(path, 'rb') as fd:
        file_hash = hashlib.sha256()
        while True:
            chunk = fd.read(BLOCK_1M)
            if not chunk:
                break
            file_hash.update(chunk)
        digest = file_hash.hexdigest()
    return digest

def is_renamed(full_path):
    return full_path.find('@') != -1

def get_copy_dst_name(src_folder, dst_folder):
    if src_folder.find('@') != -1:
        base_name = os.path.basename(src_folder)
        new_dst_dir = os.path.join(dst_folder, base_name)
    else:
        min_mt = sys.maxsize
        max_mt = 0
        for (root, folders, files) in os.walk(src_folder):
            for f in files:
                path = os.path.join(root, f)
                mt = os.path.getmtime(path)
                min_mt = min(min_mt, mt)
                max_mt = max(max_mt, mt)
        min_date = convert_timestamp_to_date2(min_mt)
        max_date = convert_timestamp_to_date2(max_mt)
        date_range = '{}-{}'.format(min_date, max_date)
        dir_name = '{}@{}'.format(date_range, src_folder.split(os.sep)[-1])
        new_dst_dir = os.path.join(dst_folder, dir_name)
    return new_dst_dir

def get_verify_dst_name(src_path, src_folder, dst_folder):
    new_dst_path = src_path.replace(src_folder, dst_folder)
    return new_dst_path