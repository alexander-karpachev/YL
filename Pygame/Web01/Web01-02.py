import os


def human_read_format(size):
    d = {
        0: 'Б',
        1: 'КБ',
        2: 'МБ',
        3: 'ГБ'
    }
    n = min(3, (len(str(size)) - 1) // 3)
    divisor = (1024 ** n)
    if size == 0:
        divisor = 1
    elif size < divisor:
        n -= 1
        divisor = (1024 ** n)
    r = round(size / divisor)
    return str(r) + d.get(n)


def get_files_sizes(dir):
    os.chdir(dir)
    r = list()
    for f in os.listdir():
        if os.path.isfile(f):
            full_name = dir+'\\'+f
            size = os.stat(full_name).st_size
            r.append([full_name, human_read_format(size)])
    return r

