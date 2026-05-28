import json
from tqdm import tqdm

# Read file
def read_json_datas(path):
    '''Read JSON given dictionary in every line'''
    datas = []
    with open(path, "r", encoding="utf-8") as fp:
        for i in fp.readlines():
            datas.append(json.loads(i))
    return datas

# Read JSON Array
def read_json_array(path):
    '''Read JSON given array of dictionaries'''
    with open(path, "r", encoding="utf-8") as fp:
        datas = json.loads(fp.read())
    return datas

# save data
def save_datas(obj, path):
    datas = []
    for line in obj:
        data = {}
        for k, v in line:
            data[k] = v
        datas.append(data)
    with open(path, "w", encoding="utf-8") as fp:
        with tqdm(range(len(datas))) as pbar:
            for i in pbar:
                pbar.set_description("The %s document is saved" % (i + 1))
                fp.write(json.dumps(datas[i])+"\n")

# Read words from file
def read_text(path):
    '''Read words file as list'''
    words = []
    with open(path, 'r', encoding='utf-8') as fp:
        for word in fp.readlines():
            word = word.strip()
            words.append(word)
    return words

# string escape
def string_escape(string):
    string = string.replace("\\", "\\\\")
    string = string.replace("(", "\(")
    string = string.replace(")", "\)")
    string = string.replace("{", "\{")
    string = string.replace("}", "\}")
    string = string.replace("[", "\[")
    string = string.replace("]", "\]")
    string = string.replace("-", "\-")
    string = string.replace(".", "\.")
    string = string.replace("+", "\+")
    string = string.replace("=", "\=")
    string = string.replace("*", "\*")
    string = string.replace("?", "\?")
    string = string.replace("^", "\^")
    string = string.replace("$", "\$")
    return string

def save_json(obj, path):
    with open(path, "w") as outfile:
        json.dump(obj, outfile)
    return True
