import ctypes
import os
import shutil

import argcomplete
from gooey import Gooey, GooeyParser

import util
from verify import verify

def copy_files(src_folder, dst_folder):
    total = 0
    for (root, folders, files) in os.walk(src_folder):
        total += len(files)
    progress = 0
    for (root, folders, files) in os.walk(src_folder):
        for f in files:
            src_path = os.path.join(root, f)
            dst_path = util.get_video_new_name(src_path)
            dst_path = dst_path.replace(src_folder, dst_folder)
            if os.path.exists(dst_path):
                progress += 1
                print('progress: {}/{}, file:{}'.format(progress, total, dst_path))
                continue
            dst_dir, _ = os.path.split(dst_path)
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(src_path, dst_path)
            progress += 1
            print('progress: {}/{}, file:{}'.format(progress, total, dst_path))
    print('copy complete.')

def rename_files(folder):
    for (root, folders, files) in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            if util.is_renamed(path):
                continue
            new_path = util.get_video_new_name(path)
            if os.path.exists(new_path):
                continue
            os.rename(path, new_path)
    print('rename_complete')

def check_copy(src, dst):
    # check all file is copied and copy is correct.
    error, err_msg = verify(src, dst, check_hash=True)
    if error:
        print(err_msg)
        return error
    print('checking complete, everything is ok.')

@Gooey(
    default_size=(1500, 1000),
    required_cols=1,
    optional_cols=1,
    program_name='OsmoCopy[OsmoPocket拷贝工具]',
)
def main():
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    parser = GooeyParser(description='')
    parser.add_argument('--src', metavar='源目录', widget='DirChooser', help='源目录, 如大疆SD的目录就是: X:\\DCIM')
    parser.add_argument('--dst', metavar='输出目录', widget='DirChooser',
                        help='目的目标, 如D:\\Target，则会将DCIM内的文件拷贝到D:\\Target\\DCIM')
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if not args.src or not args.dst:
        parser.print_usage()
        exit(1)

    if not os.path.exists(args.src):
        print('source path:{} does not exist.'.format(args.src))
        exit(1)
    if not os.path.exists(args.src):
        print('source path:{} does not exist.'.format(args.dst))
        exit(1)

    # if args.copy is None:
    #     print('please set action, copy or check?')
    #     parser.print_usage()
    #     exit(1)

    print('{} -> {}'.format(args.src, args.dst))
    args.dst = util.get_copy_dst_name(args.src, args.dst)
    copy_files(args.src, args.dst)
    error = check_copy(args.src, args.dst)
    if error:
        exit(1)
    exit(0)

if __name__ == '__main__':
    main()
