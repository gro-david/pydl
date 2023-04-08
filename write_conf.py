import os

def main(conf):
    to_write = []
    to_write.append('[Flags]\n')
    to_write.append(f'playlist = {conf["playlist"]}\n')
    to_write.append(f'tag = {conf["tag"]}\n')
    to_write.append(f'experimental = {conf["experimental"]}\n')
    to_write.append(f'manual-tag = {conf["manual-tag"]}\n')
    
    to_write.append('[General]\n')
    to_write.append(f'dl-limit = {conf["dl-limit"]}\n')

    # directory of the running file
    dirname = os.path.dirname(__file__)

    # full path to the config file. works because the config file is in the same directory as the running file
    full_path = os.path.join(dirname, 'pydl.conf')
    
    # open the config file and prepare for translation
    conf_file = open(full_path, 'w')

    conf_file.writelines(to_write)
    conf_file.close()

