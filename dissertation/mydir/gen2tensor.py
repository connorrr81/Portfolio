import numpy as np

from collections import OrderedDict

def gen2tensor(gen, gen_ids='-ACGT'):
    output_dict = OrderedDict()

    num_ids = len(gen_ids)
    
    one_hot_encoder = {}
    for (i, gen_id) in enumerate(gen_ids):
        value = [0 for _ in range(num_ids)]
        value[i] = 1
        one_hot_encoder[gen_id] = value

    for key, value in gen.items():
        one_hot_list = list()
        
        for gen_id in value:
            one_hot_list.append(one_hot_encoder[gen_id])
        
        output_dict[key] = np.array(one_hot_list)

    return output_dict
