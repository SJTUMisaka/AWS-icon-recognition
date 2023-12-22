import os
import shutil

folder_source = '../../data/awsIcons/'
folder_target = '../../data/awsIcons_processed/'
os.makedirs(folder_target, exist_ok=True)
# go through source folder
for root, dirs, files in os.walk(folder_source):
    for file in files:
        if file.endswith('.png'):
            src_file = os.path.join(root, file)
            dest_file = os.path.join(folder_target, file)
            
            # check existence
            if os.path.exists(dest_file):
                base, ext = os.path.splitext(file)
                dest_file = os.path.join(folder_target, f"{base}_duplicate{ext}")
            
            # copy png file to target folder
            shutil.copy(src_file, dest_file)
            print(f"Copied: {src_file} to {dest_file}")