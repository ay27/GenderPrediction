import arff

from fucking_python_map import fucking_map


def _generate_att_list(count):
    tmp = list(fucking_map(lambda ii: ('attr%d' % ii, 'REAL'), range(count)))
    tmp.append(('label', ['男', '女']))
    return tmp


if __name__ == '__main__':
    # write to arff file
    user_mat = []
    row = [i for i in range(202)]
    user_mat.append(row)
    obj = {}
    obj['relation'] = 'dictionary'
    obj['attributes'] = _generate_att_list(201)
    obj['data'] = user_mat
    print('attr len %d' % len(obj['attributes']))

    arff_file = open('.tmp.arff', 'w', encoding='urf-8')

    arff.dump(obj, arff_file)
