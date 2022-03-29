import re

from collections import OrderedDict

def get_line_ids(path, line_len, gen_ids='-ACGT'):
    with open(path) as file:

        line_ids = OrderedDict()
        key_before = False

        for line in file:
            if line.startswith('>'):
                if key_before:
                    raise ValueError
                else:
                    key = re.search(r"(?:\|)(.*)", line).group(1)

                key_before = True
            else:
                if key_before:
                    line = line.rstrip('\n')

                    if (len(line) == line_len) and (set(''.join(sorted(set(line)))).issubset(set(gen_ids))):
                        line_ids[key] = line
                else:
                    raise ValueError

                key_before = False

        return line_ids
