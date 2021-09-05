import sys
import argparse

def train_test_split(train_percentage):
    annotations = open(r"keras-yolo3/pre_split_train.txt","r")
    test_file = open(r"keras-yolo3/test.txt","w")
    train_file = open(r"keras-yolo3/train.txt","w")
    class_count = {}
    for annot in annotations.readlines():
        img_data = annot.strip().split(' ')
        img_path = img_data[0]
        boxes = img_data[1:]
        for box in boxes:
            class_no = box.strip()[-1]
            if class_no not in class_count:
                class_count[class_no] = 1
            else:
                class_count[class_no] += 1
    annotations.seek(0)
    
    class_train = {}
    class_test = {}
    for class_no in class_count:
        class_train[class_no] = round((train_percentage/100.0) * class_count[class_no])
        class_test = class_count[class_no] - class_train[class_no]
    
    # init
    train_count = {}
    for class_no in class_count:
        train_count[class_no] = 0
        
    for annot in annotations.readlines():
        if len(annot.strip()) != 0:
            # class_no = annot.strip()[-1]
            img_data = annot.strip().split(' ')
            img_path = img_data[0]
            boxes = img_data[1:]
            
            train_boxes = []
            test_boxes = []
            for box in boxes:
                class_no = box[-1]
                if train_count[class_no] < class_train[class_no]:
                    train_boxes.append(box)
                    if class_no not in train_count:
                        train_count[class_no] = 1
                    else:
                        train_count[class_no] += 1
                else:
                    test_boxes.append(box)
            
            train_line = img_path
            test_line = img_path
            for box in train_boxes:
                train_line+= ' ' + box
            for box in test_boxes:
                test_line+= ' ' + box   
                
            if (train_line != img_path):
                train_file.write(train_line + '\n')
            
            if (test_line != img_path):
                test_file.write(test_line + '\n')
                   
    annotations.close()
    test_file.close()
    train_file.close()
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument(
        '--n_folds', type=str,
        help='path to vott csv file'
    )
    
    args = parser.parse_args()
    obj = vars(args)
    
    if 'n_folds' not in obj:
        print(
        '''
        Error: Argument --n_folds must be specified
        
        '''
        )
    train_test_split(int(obj['n_folds']))
    