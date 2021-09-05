def parse_csv_line(line):
    if(len(line.split(',')) > 6):
        print(line)
        return;
    img_name, xmin, ymin, xmax, ymax, species_name = line.split(',')
    return img_name[1:-1], int(float(xmin)), int(float(ymin)), int(float(xmax)), int(float(ymax)), species_name.strip()[1:-1]

def generate_annotations_from_VOTT(imgs_path, csv_path, class_no):
    row_box_annotations = open(r"train.txt","a")
    csv = open(csv_path,'r')
    csv.readline() # first line contains meta data
    for line in csv.readlines():
        img_name, xmin, ymin, xmax, ymax, species_name = parse_csv_line(line)
        img_path = imgs_path+'/'+img_name
        # row_box_annotations.write(f"{img_path} {xmin},{ymin},{xmax},{ymax},{class_no}\n")
        row_box_annotations.write(f"{img_path} {xmin},{ymin},{xmax},{ymax},0\n") # used for detection (1 fish class only)
    csv.close()
    row_box_annotations.close()
    
def generate_annotations_from_VOTT_fixed(imgs_path, csv_path, class_no):
    row_box_annotations = open(r"train.txt","a")
    csv = open(csv_path,'r')
    csv.readline() # first line contains meta data
    entries = {}
    for line in csv.readlines():
        img_name, xmin, ymin, xmax, ymax, species_name = parse_csv_line(line)
        img_path = imgs_path+'/'+img_name
        if img_path not in entries:
            entries[img_path] = f"{xmin},{ymin},{xmax},{ymax},{class_no}"
        else:
            entries[img_path] += f" {xmin},{ymin},{xmax},{ymax},{class_no}"
        # row_box_annotations.write(f"{img_path} {xmin},{ymin},{xmax},{ymax},{class_no}\n")
        # row_box_annotations.write(f"{img_path} {xmin},{ymin},{xmax},{ymax},0\n") # used for detection (1 fish class only)
    
    for key in entries:
        row_box_annotations.write(key+ " " + entries[key] + "\n")
    csv.close()
    row_box_annotations.close()
    
    
# directory : csv file
species = [
    ('annotations/Thalassoma-lunare', 'annotations/Thalassoma-lunare/fishes-export.csv', 0),
    ('annotations/Chaetodon-auriga', 'annotations/Chaetodon-auriga/Chaetodon-auriga-export.csv', 1),
    ('annotations/Amphiprion-bicinctus', 'annotations/Amphiprion-bicinctus/clownfish-export.csv', 2),
    ('annotations/Acanthurus-mata', 'annotations/Acanthurus-mata/Surgeonfish-export.csv', 3),
    ('annotations/Pterois-volitans', 'annotations/Pterois-volitans/Lionfish-export.csv', 4),
    ('drive-download\images\Acanthurus-mata', 'drive-download\images\Acanthurus-mata\Acanthurus-mata-export.csv', 3),
    ('drive-download\images\Chaetodon-auriga', 'drive-download\images\Chaetodon-auriga\Chaetodon-auriga-export.csv', 1),
    ('drive-download\images\Pterois-volitans', 'drive-download\images\Pterois-volitans\Pterois-volitans-export.csv', 4),
    ('drive-download\images\Thalassoma-lunare', 'drive-download\images\Thalassoma-lunare\Thalassoma-lunare-export.csv', 0),
    ('drive-download\images\clownfish', 'drive-download\images\clownfish\clownfish-export.csv', 2),

    ]

classes = open(r"dataset/fish_classes.txt","w")
for i in range(len(species)):
    imgs_path, csv_path, class_no = species[i]
    generate_annotations_from_VOTT_fixed(imgs_path,csv_path,class_no)
    
    classes.write(imgs_path.split('/')[-1] + '\n')
classes.close()
