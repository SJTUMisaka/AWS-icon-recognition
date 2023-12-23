import os
import shutil
import random

folder_source = '../../data/awsIcons/'
folder_target = '../../data/awsIcons_processed/'
folder_train = '../../data/train/'
folder_test = '../../data/test/'
train_ratio = 0.8

def get_png_files(folder_source, folder_target):
    os.makedirs(folder_target, exist_ok=True)
    # go through source folder
    for root, dirs, files in os.walk(folder_source):
        for file in files:
            if file.endswith('.png'):
                src_file = os.path.join(root, file)
                label = file[:file.rfind('_')]
                dest_dir = os.path.join(folder_target, label)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, file)
                
                # check existence
                if os.path.exists(dest_file):
                    base, ext = os.path.splitext(file)
                    dest_file = os.path.join(dest_dir, f"{base}_duplicate{ext}")
                
                # copy png file to target folder
                shutil.copy(src_file, dest_file)
                print(f"Copied: {src_file} to {dest_file}")

def train_test_split(source_root, train_root, test_root, train_ratio=0.8):
    """
    Split the dataset into a training set and a test set.
    """
    if not os.path.exists(train_root):
        os.makedirs(train_root)
    if not os.path.exists(test_root):
        os.makedirs(test_root)

    for class_name in os.listdir(source_root):
        class_path = os.path.join(source_root, class_name)
        if os.path.isdir(class_path):
            # Create corresponding directories in train and test
            train_class_path = os.path.join(train_root, class_name)
            test_class_path = os.path.join(test_root, class_name)
            if not os.path.exists(train_class_path):
                os.makedirs(train_class_path)
            if not os.path.exists(test_class_path):
                os.makedirs(test_class_path)

            images = os.listdir(class_path)
            random.shuffle(images)  # Randomize the list of images

            num_train = max(1, int(len(images) * train_ratio))  # At least one image in training
            num_test = max(1, int(len(images) * (1 - train_ratio)))  # At least one image in testing

            # Split and copy images
            for i, img in enumerate(images):
                src_img_path = os.path.join(class_path, img)
                if i < num_train:
                    dst_img_path = os.path.join(train_class_path, img)
                    shutil.copy(src_img_path, dst_img_path)
                if len(images) - i <= num_test:
                    dst_img_path = os.path.join(test_class_path, img)
                    shutil.copy(src_img_path, dst_img_path)

get_png_files(folder_source, folder_target)
train_test_split(folder_target, folder_train, folder_test, train_ratio)