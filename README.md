# DuplicateImageCheck
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
