import sys
import argparse

# returns the coordinates of the corners of an annotation from the QUT dataset
def get_coord(annotation_path):
    f = open(annotation_path, "r")
    line = f.read()
    
    ### parse lines
    
    # assume fish is facing left
    top_left, top_right, bottom_right, bottom_left = line.split(";")
    temp_top_left_x, temp_top_left_y = top_left.split(':')[1].strip().split("  ")
    temp_top_right_x, temp_top_right_y = top_right.strip().split("  ")
    temp_bottom_right_x, temp_bottom_right_y = bottom_right.strip().split("  ")
    temp_bottom_left_x, temp_bottom_left_y = bottom_left.strip().split(" ")
    
    # prepare return values
    top_left_x = temp_top_left_x;
    top_left_y = temp_top_left_y;
    top_right_x = temp_top_right_x;
    top_right_y = temp_top_right_y;
    bottom_right_x = temp_bottom_right_x;
    bottom_right_y = temp_bottom_right_y;
    bottom_left_x = temp_bottom_left_x;
    bottom_left_y = temp_bottom_left_y;

    
    # if fish is facing right, swap coordinate values
    if float(temp_top_left_x) > float(temp_bottom_right_x): # will only be true if facing right
        top_right_x = temp_top_left_x
        top_right_y = temp_top_left_y
        bottom_right_x = temp_top_right_x
        bottom_right_y = temp_top_right_y
        bottom_left_x = temp_bottom_right_x
        bottom_left_y = temp_bottom_right_y
        top_left_x = temp_bottom_left_x
        top_left_y = temp_bottom_left_y
    
    f.close()
    return (float(top_left_x), float(top_left_y)), (float(top_right_x), float(top_right_y)),(float(bottom_right_x), float(bottom_right_y)), (float(bottom_left_x), float(bottom_left_y))
    
# change corner coordinate format to box format
def get_box(coords):
    top_left, top_right, bottom_right, bottom_left = coords
    min_x = min(top_left[0], bottom_left[0])
    max_x = max(top_right[0], bottom_right[0])
    min_y = min(top_left[1], bottom_left[1])
    max_y = max(top_right[1], bottom_right[1])
    return int(min_x), int(max_x), int(min_y), int(max_y)
    
# parse the species line from the QUT dataset to get species name, image type, and image name
def parse_species(line):
    class_no, species_name, img_type, img_name, idx = line.split("=")
    return species_name, img_type, img_name


def generate_annotations_from_QUT():
    species = open(r"keras-yolo3/dataset/QUT_fish_data/final_all_index.txt ","r")
    row_box_annotations = open(r"keras-yolo3/train.txt","w")
    classes = open(r"keras-yolo3/dataset/fish_classes.txt", "w")
    class_no = -1
    for line in species.readlines():
        species_name, img_type, img_name = parse_species(line)
        if(img_type=='insitu'):
            if species_name not in classes_map:
                classes.write(f"{species_name}\n")
                class_no+=1
                classes_map[species_name] = class_no
            img_path = f"dataset/QUT_fish_data/images/raw_images/{img_name}.jpg"
            annotation_path = f"keras-yolo3/dataset/QUT_fish_data/annotations/{img_name}.pts"
            coords = get_coord(annotation_path)
            min_x,max_x,min_y,max_y = get_box(coords)
            row_box_annotations.write(f"{img_path} {min_x},{min_y},{max_x},{max_y},{class_no}\n")
            
    species.close()
    row_box_annotations.close()
    classes.close()
    
# parse csv line from VOTT output csv file
def parse_csv_line(line):
    img_name, xmin, ymin, xmax, ymax, species_name = line.split(',')
    return img_name[1:-1], int(float(xmin)), int(float(ymin)), int(float(xmax)), int(float(ymax)), species_name.strip()[1:-1]


def generate_annotations_from_VOTT(imgs_path, csv_path, class_no):
    species = open(r"keras-yolo3/dataset/QUT_fish_data/final_all_index.txt ","r")
    row_box_annotations = open(r"keras-yolo3/train.txt","w")
    csv = open(csv_path,'r')
    csv.readline() # first line contains meta data
    for line in csv.readlines():
        img_name, xmin, ymin, xmax, ymax, species_name = parse_csv_line(line)
        img_path = imgs_path+'/'+img_name
        row_box_annotations.write(f"{img_path} {xmin},{ymin},{xmax},{ymax},{class_no}\n")
    csv.close()
    species.close()
    row_box_annotations.close()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument(
        '--vott_csv', type=str,
        help='path to vott csv file'
    )
    
    parser.add_argument(
        '--vott_images', type=str,
        help='path to vott images folder'
    )
    
    parser.add_argument(
        '--class_no', type=str,
        help='class number'
    )
    
    args = parser.parse_args()
    obj = vars(args)
    
    classes_map = {} #key: species name, value: class no

    if 'vott_csv' not in obj or 'vott_images' not in obj or 'class_no' not in obj:
        print(
        '''
        Error: Arguments --vott_csv , --vott_images, --class_no must be specified
        
        please run the file as follows:
        python parse_annotations.py --vott_images <path_to_images_folder> --vott_csv <vott_csv_path>
        '''
        )
    else:
    #    generate_annotations_from_QUT()
        generate_annotations_from_VOTT(obj['vott_images'], obj['vott_csv'], obj['class_no'])