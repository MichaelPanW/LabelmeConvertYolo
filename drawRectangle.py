from os import path
from glob import glob
import cv2
import pathlib

label_folder = 'all_label'
output_folder = 'draw'
pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

for filename in glob(path.join(label_folder, '*.txt')):
    print(filename)
    with open(filename, 'r') as f:  # open in readonly mode
        path = (filename.replace('all_label', 'data').replace(
            '.txt', '.jpg').replace('\\', '/'))
        image = cv2.imread(path)
        lines = f.read().splitlines()
        height, width, channels = image.shape
        print(width, height)
        raw_name = path.split('/')[-1]
        for line in lines:
            data = line.split(' ')
            print((
                ((float(data[1])-(float(data[3])/2))),
                ((float(data[2])-(float(data[4])/2))),
                ((float(data[1])+(float(data[3])/2))),

                ((float(data[2])+(float(data[4])/2)))))
            print(
                int((float(data[1])-(float(data[3])/2))*width),
                int((float(data[2])-(float(data[4])/2))*height),
                int((float(data[1])+(float(data[3])/2))*width),
                int((float(data[2])+(float(data[4])/2))*height))
            image = cv2.rectangle(
                image, (
                    int((float(data[1])-(float(data[3])/2))*width),
                    int((float(data[2])-(float(data[4])/2))*height),
                    int(((float(data[3])))*width),
                    int((float(data[4]))*height)), (255, 255, 255), 2)
        cv2.imwrite(output_folder+'/'+raw_name, image)
