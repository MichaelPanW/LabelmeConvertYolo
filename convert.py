from os import path
from glob import glob
from json import load


def getValue(point, all_size):
    return str(round(point/all_size, 6))


labels = []
labels_file_name = input("label file(labels.txt):") or 'labels.txt'
label_folder = input("label folder(label):") or 'label'
output_folder = input("output folder(output):") or 'output'
with open(labels_file_name) as f:
    labels = f.read().splitlines()
for filename in glob(path.join(label_folder, '*.json')):
    raw_name = filename.split('\\')[-1]
    with open(filename, 'r') as f:  # open in readonly mode
        with open(output_folder+'/'+raw_name.replace('.json', '.txt'), 'w') as w:  # open in readonly mode
            data = load(f)
            for shape in data['shapes']:
                if (shape['label'] in labels):
                    try:
                        w.write(str(labels.index(shape['label'])+1)+" ")
                        w.write(getValue(shape['points']
                                [0][0], data['imageWidth']))
                        w.write(getValue(shape['points']
                                [0][1], data['imageHeight']))
                        w.write(getValue(shape['points']
                                [1][0], data['imageWidth']))
                        w.write(getValue(shape['points']
                                [1][1], data['imageHeight']))
                        w.write("\n")
                    except:
                        pass
