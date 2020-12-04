from collections import Counter


if __name__ == '__main__':
    dict_map = ['a1', 'a2', 'a3', 'a2', 'a3', 'a2', 'a3', 'a2', 'a3', 'a2', 'a3',
        'a1', 'a2', 'a3', 'a1', 'a2', 'a3', 'a1', 'a2', 'a3', 'a1', 'a2', 'a3',
        'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2',
        'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2',
        'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a2', 'a1', 'a3',  'a1', 'a3',  'a1', 'a3',  'a1', 'a3',  'a1', 'a3',  'a1', 'a3',  'a1', 'a3',  'a1', 'a3',  'a1', 'a3',  'a1', 'a3',  'a1', 'a3',
        'a3','a3','a3','a3','a3','a3','a3','a3','a3','a3','a3']

    key_val = Counter(dict_map)
    print (key_val)
    for key in key_val:
        print (key, key_val[key])
