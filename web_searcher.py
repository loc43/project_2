import random
import requests
from globals import poem_marker, ref_list

def find_poem(url):
    response = requests.get(url)
    decoded = response.text
    tmp = decoded
    while poem_marker in tmp:
        idx = tmp.index(poem_marker)
        a = ''
        for elem in tmp[idx + len(poem_marker) + 1 : ]:
            if elem == '"':
                break
            a += elem
        ref_list.append(a)
        tmp = tmp[idx + 10 : ]
    return random.choice(ref_list)


def find_end(str):
    cnt = 0
    sum = 0
    tmp = str
    while cnt < 4:
        idx = tmp.index('>')
        tmp = tmp[idx + 1 : ]
        cnt += 1
        sum += idx + 1
    return sum

def find_text(url):
    response = requests.get(url)
    decoded = response.text
    start_marker = '<div class="entry-content poem-text" itemscope itemtype="http://schema.org/CreativeWork">'
    idx_1 = decoded[ : 50000].index(start_marker)
    tmp = decoded[idx_1 + len(start_marker) + 6: idx_1 + 500]
    try:
        idx_2 = tmp.index('<p>')
    except:
        idx_2 = find_end(tmp)
    return(decipher(tmp[ : idx_2]))


def decipher(list):
    while '<' in list:
        list = list[ : list.index('<')] + list[list.index('>') + 1 : ]
    while '&#8212;' in list:
        list = list[ : list.index('&#8212;')] + '--' + list[list.index('&#8212;') + 7:] 
    while '&#8230;' in list:
        list = list[ : list.index('&#8230;')] + '!' + list[list.index('&#8230;') + 7:] 
    while '&#171;' in list:
        list = list[ : list.index('&#171;')] + '"' + list[list.index('&#171;') + 6:] 
    while '&#187;' in list:
        list = list[ : list.index('&#187;')] + '"' + list[list.index('&#187;') + 6:] 
    return list
