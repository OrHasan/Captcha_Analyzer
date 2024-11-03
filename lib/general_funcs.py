import re
from os import listdir
from os.path import isfile, join


def get_file_index(history_dir):
    history_files = [f for f in listdir(history_dir) if isfile(join(history_dir, f))]
    current_index = 0
    for file_name in history_files:
        current_index = max(current_index, int(re.search(r'#(\d+)', file_name).group(1)))
    current_index += 1

    return current_index


def my_progress(curr, N, width=10, bars=u'▉▊▋▌▍▎▏ '[::-1], full='█', empty=' '):
    p = curr / N
    nfull = int(p * width)
    return "{:>3.0%} |{}{}{}| {:>2}/{}"\
        .format(p, full * nfull,
                bars[int(len(bars) * ((p * width) % 1))],
                empty * (width - nfull - 1),
                curr, N)
