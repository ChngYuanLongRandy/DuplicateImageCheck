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


***
Noticed an issue in reading images
Corrupted or unreadable image.
For example, a file ending with acceptable format but it is unable to be opened as a JPG.

'''
#! Python3

import datetime, time, shutil
import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_absolute_error

start_time = time.time()

os.chdir('H:')

print(Path.cwd())

ref_path = Path.cwd().joinpath('My Personal Media',"Mom's pics")
#ref_path = Path.cwd().joinpath('Compare images')
#check_path = Path.cwd().joinpath('Compare images')
check_path = Path.cwd().joinpath('My Personal Media','Mum stuff Unsorted')
#check_path = Path.cwd().joinpath('Compare images check')
new_folder_path = check_path  # placeholder

print('Ref path is ', ref_path)
print('Check path is ', check_path)
print('Are they the same? ', os.path.samefile(ref_path, check_path), '\n')

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

check_image_files = []
check_non_image_files = []

ref_image_files = []
ref_non_image_files = []

dup_files_index = []
non_dup_files_index = []

dup_files_details = []
non_dup_files_details = []


# TODO retrieving images for both sides, check and ref directory

# TODO check images against both sides

def search_for_images(path, ref_check):
    '''search for images in a directory including (nested) subfolders and returns two lists.
    if ref_check is true, the path is a reference directory, else it will be a checking directory
    image_files contains all of the images
    non_image_files contains all of the non_images'''

    global check_image_files, check_non_image_files, ref_non_image_files, ref_image_files

    print('Current path is', path, '\n')
    print('Is current path a directory? ', ref_check, '\n')

    for root, dirs, files in os.walk(path):  # path is currently held static
        print(root)
        print(dirs)
        print(files)
        for file in files:
            #print('reading \t', file)
            #print('file located in \t', Path(root).joinpath(file))
            if str(file).endswith(tuple(acceptable_formats)):
                # if they are of acceptable format, the file will be put into folder
                #print(file, " contains acceptable format")
                image_path = Path(root).joinpath(file)
                image_read = plt.imread(image_path)
                image = image_read.ravel()
                if ref_check:  # checks if the path is ref or not then puts it in the correct folder
                    ref_image_files.append([image_path, image])
                else:
                    check_image_files.append([image_path, image])
            else:
                #print(file, " does not contain acceptable format")
                if ref_check:  # checks if the path is ref or not then puts it in the correct folder
                    ref_non_image_files.append(Path(root).joinpath(file))
                else:
                    check_non_image_files.append(Path(root).joinpath(file))

    # if path is ref then append into ref list
    if ref_check:
        print('*'*25,'\n')
        print('Appending into ref image list\nimage file details:\n',
              'image file length is {} \n'.format(len(ref_image_files)),
              'image files:\n',
              [x for x in ref_image_files], sep='')

        print('non image file details:\n',
              'non image file length is {} \n'.format(len(ref_non_image_files)),
              'non image files:\n',
              [x for x in ref_non_image_files], sep='')
        print('*'*25,'\n')
    # if path is NOT ref, i.e a check directory, append into check list
    else:
        print('*'*25,'\n')
        print('Appending into check image list\nimage file details:\n',
              'image file length is {} \n'.format(len(check_image_files)),
              'image files:\n',
              [x for x in check_image_files], sep='')

        print('non image file details:\n',
              'non image file length is {} \n'.format(len(check_non_image_files)),
              'non image files:\n',
              [x for x in check_non_image_files], sep='')
        print('*'*25,'\n')


# Function to resize both images and return the mean absolute error (mae)
def resize_return_mae(ref_image, check_image):
    if ref_image.shape != check_image.shape:
        check_image.reshape(ref_image.shape)
    else:
        return mean_absolute_error(ref_image, check_image)


def check_dup(same):
    # Checks duplicates in the ref and the checking directory
    # WHEN REF AND CHECK FOLDERS ARE THE SAME
    # Checking of duplicates in all of the files in the image folder and have two folders
    # non_dups containing non-dups
    # dups containing the dups
    # Hold one as reference and checks against the rest of the images. Puts dup into dup list
    # WHEN REF AND CHECK FOLDERS ARE NOT THE SAME
    # Base code will be similar to when they are both the same
    # however will include and additional index called checking index to keep track of the
    # list in the checking directory.

    global dup_files_index, non_dup_files_index, dup_files_details, non_dup_files_details, check_image_files, \
        ref_image_files

    # if check and ref folder are the same
    if same:
        print('*'*25,'\n')
        print("Entering check dup, ref and check directory is the same")
        print('*'*25,'\n')
        for current_index in range(len(ref_image_files)):
            ref_index = 0
            while ref_index < len(ref_image_files):
                #print('Current index is ', current_index)
                #print('Ref index is ', ref_index)
                #print('Ref image ', ref_image_files[ref_index][1])
                #print('Check image ', ref_image_files[current_index][1])
                # should not check against itself
                ref_image = ref_image_files[ref_index][1]
                if (ref_index == current_index) | (ref_index in dup_files_index):
                    ref_index += 1
                    continue
                else:
                    check_image = ref_image_files[current_index][1]
                    print(ref_image.shape)
                    print(check_image.shape)
                    # if the shape does not match means that the image size is different.
                    # chances are if the size is different, the image will be different as well.
                    if ref_image.shape == check_image.shape:
                        mae = mean_absolute_error(ref_image, check_image)
                        print('mae is ', mae)
                        ref_index += 1
                        if mae == 0:
                            dup_files_index.append(current_index)
                        else:
                            non_dup_files_index.append(current_index)
                    else:
                        non_dup_files_index.append(current_index)
                        ref_index += 1
                    # mae_list.append([index,mean_absolute_error(ref_image, check_image)])

        dup_files_index = set(dup_files_index)
        non_dup_files_index = set(non_dup_files_index) - dup_files_index

        dup_files_details = pd.DataFrame(ref_image_files).iloc[list(dup_files_index)]
        non_dup_files_details = pd.DataFrame(ref_image_files).iloc[list(non_dup_files_index)]

        print(dup_files_details[0])
        print(non_dup_files_details[0])

    # ref and check folders are not the same
    else:
        print('*'*25,'\n')
        print("Entering check dup, ref and check directory are different/nRef directory is {}/nCheck directory is {}"
              .format(ref_path, check_path))
        print('*'*25,'\n')
        for ref_index in range(len(ref_image_files)):
            for check_index in range(len(check_image_files)):
                #ref_index = 0
                #print('Check index is ', check_index)
                #print('Ref index is ', ref_index)
                #print('Ref image ', ref_image_files[ref_index][1])
                #print('Check image ', check_image_files[check_index][1])
                # should not check against itself
                ref_image = ref_image_files[ref_index][1]
                # Check index should not be in the dup files
                if check_index in dup_files_index:
                    continue
                else:
                    check_image = check_image_files[check_index][1]
                    print('Ref image shape', ref_image.shape)
                    print('Check image shape', check_image.shape)
                    # if the shape does not match means that the image size is different.
                    # chances are if the size is different, the image will be different as well.
                    if ref_image.shape == check_image.shape:
                        mae = mean_absolute_error(ref_image, check_image)
                        print('mae is ', mae)
                        # mean absolute error is zero, i.e the files are the same, non dup
                        if mae == 0:
                            dup_files_index.append(check_index)
                        else:
                            # mae != 0 so both images are not equivalent
                            non_dup_files_index.append(check_index)

                    else:
                        # if does not conform, they are different - so not dups
                        non_dup_files_index.append(check_index)
                        # continues checking through the entire checking directory files.

        dup_files_index = set(dup_files_index)
        non_dup_files_index = set(non_dup_files_index) - dup_files_index

        dup_files_details = pd.DataFrame(check_image_files).iloc[list(dup_files_index)]
        non_dup_files_details = pd.DataFrame(check_image_files).iloc[list(non_dup_files_index)]

        print(dup_files_details[0])
        print(non_dup_files_details[0])


# ---------------------------------------------------end of  working ---------------------------------------

# TODO: enable user to put directory manually in input

def move_images_into_folder():
    # moves the files from the dup and the non_dup set into the folders

    dup_path = Path(check_path).joinpath('Dup_folder')
    no_dup_path = Path(check_path).joinpath('No_Dup_folder')

    for dup_file_path in dup_files_details[0]:
        shutil.move(str(dup_file_path), str(dup_path))

    for no_dup_file_path in non_dup_files_details[0]:
        shutil.move(str(no_dup_file_path), str(no_dup_path))


def create_dup_folders_output_file(path):
    # Outputs log file details with dup and non dup details
    # creates the folder and changes the current directory to the new folder path

    global start_time, dup_files_details, non_dup_files_details, new_folder_path  # use global variables

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
        log_file.write('Total Runtime ' + str(round(float(run_time), 2)) + 'secs \n\n')

        log_file.write('Ref Directory ' + str(ref_path) + ' \n')
        log_file.write('Check Directory ' + str(check_path) + ' \n\n')

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


search_for_images(ref_path, True)
search_for_images(check_path, False)

check_dup(os.path.samefile(ref_path, check_path))

create_dup_folders_output_file(check_path)

# TODO use a sample check path and see if the checks work

# Checks if the ref and the check path is the same
# if str(ref_path) == str(check_path):
#     pass
# else:
#     move_images_into_folder()
