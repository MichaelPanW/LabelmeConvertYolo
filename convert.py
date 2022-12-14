from os import path
from glob import glob
from json import load
import pathlib
import shutil


def writeFile(name, image_folder=''):
    # Opens the file using 'w' method. See below for list of methods.
    with open(name+'.txt', "w") as fil:
        for file in glob(path.join('labels/'+name+'/', '*.txt')):
            raw_name = file.split('\\')[-1]
            # Writes to the file used .write() method
            fil.write(image_folder+name+'/' +
                      raw_name.replace('.txt', '.jpg')+'\n')
        fil.close()  # Closes file


def getValue(point, all_size):
    return str(round(point/all_size, 6))


labels = []
labels_file_name = input("label file(labels.txt):") or 'labels.txt'
label_folder = input("label folder(data):") or 'data'
images_folder = './images/'
output_folder = 'all_label'
pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
with open(labels_file_name) as f:
    labels = f.read().splitlines()
for filename in glob(path.join(label_folder, '*.json')):
    raw_name = filename.split('\\')[-1]
    with open(filename, 'r') as f:  # open in readonly mode

        data = load(f)
        with open(output_folder+'/'+raw_name.replace('.json', '.txt'), 'w') as w:
            for shape in data['shapes']:
                if (shape['label'] in labels):
                    try:
                        # open in readonly mode
                        w.write(str(labels.index(shape['label']))+" ")
                        w.write(getValue((shape['points']
                                [1][0]+shape['points']
                                [0][0])/2, data['imageWidth']))
                        w.write(" ")
                        w.write(getValue((shape['points']
                                [1][1]+shape['points']
                                [0][1])/2, data['imageHeight']))
                        w.write(" ")
                        w.write(getValue(shape['points']
                                [1][0]-shape['points']
                                [0][0], data['imageWidth']))
                        w.write(" ")
                        w.write(getValue(shape['points']
                                [1][1]-shape['points']
                                [0][1], data['imageHeight']))
                        w.write("\n")
                    except:
                        pass
pathlib.Path('labels/train').mkdir(parents=True, exist_ok=True)
pathlib.Path('labels/test').mkdir(parents=True, exist_ok=True)
pathlib.Path('labels/val').mkdir(parents=True, exist_ok=True)
pathlib.Path('images/train').mkdir(parents=True, exist_ok=True)
pathlib.Path('images/test').mkdir(parents=True, exist_ok=True)
pathlib.Path('images/val').mkdir(parents=True, exist_ok=True)
file_list = glob(path.join(output_folder, '*.txt'))
limit = len(file_list)/10
for index in range(len(file_list)):
    raw_name = file_list[index].split('\\')[-1]
    if (index < limit):
        shutil.copyfile(file_list[index], 'labels/test/'+raw_name)
        shutil.copyfile(file_list[index].replace('.txt', '.jpg').replace('all_label', 'data'), images_folder +
                        'test/'+raw_name.replace('.txt', '.jpg'))
    elif index < limit*2:
        shutil.copyfile(file_list[index], 'labels/val/'+raw_name)
        shutil.copyfile(file_list[index].replace('.txt', '.jpg').replace('all_label', 'data'), images_folder +
                        'val/'+raw_name.replace('.txt', '.jpg'))
    else:
        shutil.copyfile(file_list[index], 'labels/train/'+raw_name)
        shutil.copyfile(file_list[index].replace('.txt', '.jpg').replace('all_label', 'data'), images_folder +
                        'train/'+raw_name.replace('.txt', '.jpg'))

file_list = glob(path.join(output_folder, '*.txt'))
writeFile('test', images_folder)
writeFile('val', images_folder)
writeFile('train', images_folder)
