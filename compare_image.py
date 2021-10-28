'''
This python script will check for duplicates in two folders.
One directory contain all of the original photos called ref_directory
and another directory containing possible dup photos called check_directory
once this script is run, every photo from the ref_directory will be checked against every single image of the check_directory
including sub-folders.

the check_directory will then contain two folders, dup_folder and no_dup_folder and a text log with details

************************
Text Log
************************
details will then include:
When the script was run
how long it was run for
number of files that went through the script
number of images found
number of non-images found
number of duplicates and non-duplicates
list of duplicates including their file name and where the other set is located

************************
Checking in one folder
************************
In the event both ref and check directory are the same,
the script will then check for duplicates within the one directory and provide the text log only.
This is because if the images are shifted, it may screw up any form of organisation the user has

************************
Checking in two folder
************************
ref_directory  : Where the folders are used as a ref to check
check_directory: Everything here is checked to see if they are duplicates with the Ref folder

User is asked where the Ref Folder and the Check Folder are.

Once this script is run, it will first check whether is there any duplicates within the ref directory itself

Yes? Go to Checking in two folder - Dup Exist in Ref Directory
No? Go to Checking in two folder - No Dup in Ref Directory

************************************************
Checking in two folder - No Dup in Ref Directory
************************************************

Every photo from the ref_directory will be checked against every single image of the
check_directory including sub-folders.

the check_directory will then contain two folders, dup_folder and no_dup_folder and a text log with details

************************************************
Checking in two folder - Dup Exists in Ref Directory
************************************************


'''
import datetime, time, shutil
import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_absolute_error

start_time = time.time()

ref_path = Path.cwd()  # currently the path is fixed to the script working directory
check_path = Path('C:\\Users\\Randy\\GitHub\\Compare images check')
new_folder_path = ref_path #placeholder

print(type(ref_path))

acceptable_formats = ['.png', '.jpeg', '.jpg']

# --------------------------------------------------- working ---------------------------------------
#
# all_files = path.glob('*')
#
# images = []
# images_dict = {}
#
# #Testing Reading only files with acceptable formats
# for file in all_files:
#     for format in acceptable_formats:
#         if file.name.endswith(format):
#             print('Read file with file name {}'.format(file.name))
#             image_path = Path.joinpath(path, file.name)
#             image = plt.imread(image_path)
#             #storing them in image
#             images.append([image_path,np.array(image).ravel()])
#             images_dict[image_path] = [np.array(image).ravel()]
#
# #for key, contents in images_dict.items():
#
# ref_image = images[2][1]
# mae_list = []
# dup_list = []
# #
# for index in range(len(images)):
#     print(ref_image)
#     print(images[index][1])
#     mae_list.append(mean_absolute_error(ref_image,images[index][1]))
#
# print(list(mae_list))
#
# dup_list_indices = []
#
# #possible to use .loc accessor
# for index , mae in enumerate(mae_list):
#     if mae == 0:
#         dup_list_indices.append(index)
#
# dup_list.append(index for index,mae in enumerate(mae_list) if mae == 0)
#
# print(list(dup_list_indices))
# ---------------------------------------------------end of  working ---------------------------------------

# def return_dups(images, indices, ref_index):
#     return_list = []
#     for index in indices:
#         if index != ref_index:
#             #returns file name if it is not the reference index
#             return_list.append(images[index][0])
#     return return_list
#
# dup_list = return_dups(images, dup_list_indices, 2)
#
# print(dup_list)

# --------------------------------------------------- working ---------------------------------------

mae_list = []
all_files = []
image_files = []
non_image_files = []
dup_files_index = []
non_dup_files_index = []
dup_files_details = []
non_dup_files_details = []

# TODO retrieving images for both sides, check and ref directory

# TODO check images against both sides

def search_for_images(path):
    '''search for images in a directory including (nested) subfolders and return two lists.
    image_files contains all of the images
    non_image_files contains all of the non_images'''

    global image_files, non_image_files

    for root, dirs, files in os.walk(path):  # path is currently held static
        print(root)
        print(dirs)
        print(files)
        for file in files:
            print('reading ', file)
            print('file located in ', Path(root).joinpath(file))
            if str(file).endswith(tuple(acceptable_formats)):  # if they are of acceptable format, the file will be
                print(file, " contains acceptable format")
                image_path = Path(root).joinpath(file)
                image_read = plt.imread(image_path)
                image = image_read.ravel()
                image_files.append([image_path, image])
            else:
                print(file, " does not contain acceptable format")
                non_image_files.append(Path(root).joinpath(file))

    print('image file details:\n',
          'image file length is {} \n'.format(len(image_files)),
          'image files:\n',
          [x for x in image_files], sep='')

    print('non image file details:\n',
          'non image file length is {} \n'.format(len(non_image_files)),
          'non image files:\n',
          [x for x in non_image_files], sep='')


# Function to resize both images and return the mean absolute error (mae)
def resize_return_mae(ref_image, check_image):
    if ref_image.shape != check_image.shape:
        check_image.reshape(ref_image.shape)
    else:
        return mean_absolute_error(ref_image, check_image)


def check_dup():
    # WHEN REF AND CHECK FOLDERS ARE THE SAME
    # Checking of duplicates in all of the files in the image folder and have two folders
    # non_dups containing non-dups
    # dups containing the dups
    # Hold one as reference and checks against the rest of the images. Puts dup into dup list

    global dup_files_index, non_dup_files_index, dup_files_details, non_dup_files_details, image_files

    for index in range(len(image_files)):
        ref_index = 0
        while ref_index < len(image_files):
            print('index is ', index)
            print('ref index is ', ref_index)
            print('ref image ', image_files[ref_index][1])
            print('check image ', image_files[index][1])
            # should not check against itself
            ref_image = image_files[ref_index][1]
            if (ref_index == index) | (ref_index in dup_files_index):
                ref_index += 1
                continue
            else:
                check_image = image_files[index][1]
                print(ref_image.shape)
                print(check_image.shape)
                # if the shape does not match means that the image size is different.
                # chances are if the size is different, the image will be different as well.
                if ref_image.shape == check_image.shape:
                    mae = mean_absolute_error(ref_image, check_image)
                    print('mae is ', mae)
                    ref_index += 1
                    if mae == 0:
                        dup_files_index.append(index)
                    else:
                        non_dup_files_index.append(index)
                else:
                    non_dup_files_index.append(index)
                    ref_index += 1
                # mae_list.append([index,mean_absolute_error(ref_image, check_image)])

    dup_files_index = set(dup_files_index)
    non_dup_files_index = set(non_dup_files_index) - dup_files_index

    dup_files_details = pd.DataFrame(image_files).iloc[list(dup_files_index)]
    non_dup_files_details = pd.DataFrame(image_files).iloc[list(non_dup_files_index)]

    print(dup_files_details[0])
    print(non_dup_files_details[0])


# ---------------------------------------------------end of  working ---------------------------------------

# TODO: enable user to put directory manually in input


def move_images_into_folder():
    #moves the files from the dup and the non_dup set into the folders

    dup_path = Path(new_folder_path).joinpath('Dup_folder')
    no_dup_path = Path(new_folder_path).joinpath('No_Dup_folder')

    for dup_file_path in dup_files_details[0]:
        shutil.move(str(dup_file_path), str(dup_path))

    for no_dup_file_path in non_dup_files_details[0]:
        shutil.move(str(no_dup_file_path),str(no_dup_path))

def create_dup_folders_output_file(path):
    # Outputs log file details with dup and non dup details
    # creates the folder and changes the current directory to the new folder path

    global start_time, dup_files_details, non_dup_files_details ,new_folder_path # use global variables

    dup_folder_name = str('duplicate_results_') + str(time.strftime('%Y_%m_%d_%H_%M_%S'))
#    if not os.path.exists(Path(path).joinpath(dup_folder_name)):
    os.mkdir(Path(path).joinpath(dup_folder_name))
    new_folder_path = Path(path).joinpath(dup_folder_name)
#    else:
#        os.mkdir(Path(path).joinpath(alternate_dup_folder_name))
#        new_folder_path = Path(path).joinpath(alternate_dup_folder_name)

    os.mkdir(Path(new_folder_path).joinpath('Dup_folder'))
    os.mkdir(Path(new_folder_path).joinpath('No_Dup_folder'))
    run_time = time.time() - start_time

    os.chdir(new_folder_path)  # changes the current directory to the new folder path

    # Outputs the log file
    with open('log_file.txt', 'w') as log_file:
        log_file.write('Log file for duplicate application\n')
        log_file.write('Start Time ' + str(datetime.datetime.now()) + '\n')
        log_file.write('Total Runtime ' + str(round(float(run_time), 2)) + 'secs \n')

        log_file.write('*' * 25)
        log_file.write('\n')
        log_file.write('Duplicated Files\n')
        log_file.write('*' * 25)

        log_file.write('\nFile location\n')
        for item in dup_files_details[0]:
            log_file.write("%s\n" % item)

        log_file.write('\n')
        log_file.write('*' * 25)
        log_file.write('\n')
        log_file.write('Non Duplicated Files\n')
        log_file.write('*' * 25)

        log_file.write('\nFile location\n')
        for item in non_dup_files_details[0]:
            log_file.write("%s\n" % item)
        log_file.write('\n')


search_for_images(ref_path)
check_dup()
create_dup_folders_output_file(ref_path)

# TODO use a sample check path and see if the checks work

# Checks if the ref and the check path is the same
# if str(ref_path) == str(check_path):
#     pass
# else:
#     move_images_into_folder()
