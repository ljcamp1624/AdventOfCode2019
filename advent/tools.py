from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent._str.replace('\\', '/')

def ReadTxt(file_name, root_dir=ROOT_DIR):
    out = []
    v = []
    for x in open(r''+root_dir + '/' + file_name, 'r').readlines():
        n = x.split('\n')[0]
        if len(n) == 0:
            out.append(v)
            v = []
        else:
            v.append(n)
    out.append(v)
    return out