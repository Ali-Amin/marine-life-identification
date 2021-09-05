import sys

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        species = sys.argv[1:]
        
        train_file = open(r'keras-yolo3/train.txt','w+')
        fish_classes = open(r'keras-yolo3/dataset/fish_classes.txt','w')
        for line in train_file.readlines():
        
            
        train_file.close()
        fish_classes.close()