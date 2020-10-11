import tqdm
import os
import util

def verify(src_folder, dst_folder, check_hash):
    '''
    :param src_folder:
    :param dst_folder:
    :param check_hash:
    :return:
    '''
    error = False
    err_msg = None
    file_num = 0
    for (root, folders, files) in os.walk(src_folder):
        file_num += len(files)
    progress = 0
    for (root, folders, files) in os.walk(src_folder):
        for f in files:
            src_path = os.path.join(root, f)
            dst_name = util.get_video_new_name(src_path)
            dst_path = util.get_verify_dst_name(dst_name, src_folder, dst_folder)
            if not os.path.exists(dst_path):
                error = True
                err_msg = 'file:{} not found in {}'.format(f, dst_folder)
                break
            if check_hash:
                src_digest = util.get_file_digest(src_path)
                dst_digest = util.get_file_digest(dst_path)
                if src_digest != dst_digest:
                    error = True
                    err_msg = 'file:{} hash digest is different'.format(f)
                    break
            progress += 1
            print('checking: {}/{}, file:{}'.format(progress, file_num, dst_path))
    return error, err_msg
