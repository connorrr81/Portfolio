def get_line_stats(path):
    with open(path) as file:
        line_len_counts = {}
        line_gen_counts = {}

        for line in file:
            if not line.startswith('>'):
                line = line.rstrip('\n')

                line_len = len(line)
                line_gen = ''.join(sorted(set(line)))

                if line_len in line_len_counts:
                    line_len_counts[line_len] += 1
                else:
                    line_len_counts[line_len] = 1
               
                if line_gen in line_gen_counts:
                    line_gen_counts[line_gen] += 1
                else:
                    line_gen_counts[line_gen] = 1

        return line_len_counts, line_gen_counts
