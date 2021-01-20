import os,sys,subprocess
import pymongo
import cv2
import datetime
import base64
import shutil

client = pymongo.MongoClient()
db = client['nbaImages']
imageRepo = db['imageRepo']

path = os.path.dirname(__file__)

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def createFolder(folderName):
    fName = os.path.join(path, folderName)

    if (not os.path.isdir(fName)):
        os.mkdir(fName)

    return fName


def deleteFolder(folderName):
    fName = os.path.join(path, folderName)

    if (os.path.isdir(fName)):
        shutil.rmtree(fName)





def add(teamName, folderName):
    print('Are these images going to be \'public\' or \'private\'?')
    print('Private - These images will only be visible to this team')
    print('Public - These images will be visible to everyone')
    print()

    isPublic = None
    invalid = True
    while (invalid):
        command = str(
            input("Will your images be \'public\' or \'private\': ")).strip().lower()
        print()

        invalid = False

        if (command == 'public'):
            isPublic = True
        elif (command == 'private'):
            isPublic = False
        else:
            valid = False
            print('\'' + command + '\'',
                  'is not a valid input, please enter  \'public\' or \'private\'')
            print()

    fName = createFolder(folderName)

    print('A folder has been created at the location', fName)
    print('Please copy all of the images  that you would like to add into this repository and paste them into the input folder.')
    print('It is very important that you COPY your files instead of moving them as this folder is temportary will be deleted.')
    print('When you are finished inserting your images into the folder, please enter \'done\' to continue or \'cancel\' to cancel this action.')
    print()

    open_file(fName)

    continuing = None
    invalid = True
    while (invalid):
        continueInput = input(
            'Enter  \'done\' or \'cancel\': ').strip().lower()
        print()

        invalid = False

        if (continueInput == 'done'):
            continuing = True
        elif (continueInput == 'cancel'):
            continuing = False
        else:
            print('\'' + continueInput + '\'',
                  'is not a valid input, please enter either \'done\' or \'cancel\'')
            print()

    if (continuing):
        date = datetime.date.today().strftime("%d/%m/%Y")

        # Get all images from folder
        imagesToAdd = []
        for filename in os.listdir(fName):
            path = os.path.join(fName, filename)
            if cv2.imread(path) is not None:
                with open(path, 'rb') as imageFile:
                    imagesToAdd.append({
                        'data': base64.b64encode(imageFile.read()),
                        'name': filename,
                        'author': teamName,
                        'type': filename.split('.')[1].upper(),
                        'public': isPublic,
                        'date': date
                    })

        imageRepo.insert_many(imagesToAdd)

        print('You have inserted', len(imagesToAdd),
              'image(s) into the repository.')

    else:
        print('This action has been terimated.')
       

    deleteFolder(folderName)


def show(teamName, folderName):
    myimages = imageRepo.find(
        {'$or': [{'public': {'$eq': True}}, {'author': teamName}]})

    print('Your images are being loaded')
    print()

    fName = createFolder(folderName)

    for image in myimages:
        cnt = 0
        filename = image.get('name')
        while (os.path.exists(os.path.join(folderName, filename))):
            cnt += 1
            filename = image.get('name').split(
                '.')[0] + " (" + str(cnt) + ")." + image.get('name').split('.')[1]

        with open(os.path.join(folderName, filename), 'wb') as imageFile:
            imageFile.write(base64.b64decode(image['data']))

    print('A folder has been created at the location', fName)
    print('This folder contains all of the images in the repository that are either public or owned by your team.')

    open_file(fName)

    input('Press \'enter\' to continue: ')
    print()

    deleteFolder(folderName)


def delete(teamName, folderName):
    images = imageRepo.find({'author': teamName})

    print('Your images are being loaded to a folder')
    print()

    fName = createFolder(folderName)

    filenameToMongoId = {}
    for image in images:
        cnt = 0
        filename = image.get('name')
        while (os.path.exists(os.path.join(folderName, filename))):
            cnt += 1
            filename = image.get('name').split(
                '.')[0] + " (" + str(cnt) + ")." + image.get('name').split('.')[1]

        filenameToMongoId[filename] = image.get('_id')
        with open(os.path.join(folderName, filename), 'wb') as imageFile:
            imageFile.write(base64.b64decode(image.get('data')))

    print('A folder has been created at the location', fName)
    print('This folder contains all of the images in the repository that are for this team.')
    print('To delete an image from the repository, all you have to do is remove it from the folder.')
    print('When you are done deleting your images, please enter \'done\' to continue or \'cancel\' to cancel this action.')
    print()

    open_file(fName)

    continuing = None
    invalid = True
    while (invalid):
        continueInput = input(
            'Enter either \'done\' or \'cancel\': ').strip().lower()
        print()

        invalid = False

        if (continueInput == 'done'):
            continuing = True
        elif (continueInput == 'cancel'):
            continuing = False
        else:
            print('\'' + continueInput + '\'',
                  'is not a valid input, please enter either \'done\' or \'cancel\'')
            print()

    if (continuing):
        for filename in os.listdir(fName):
            filenameToMongoId.pop(filename, None)

        imagesToDelete = [filenameToMongoId[k] for k in filenameToMongoId]

        imageRepo.delete_many({'_id': {'$in': imagesToDelete}})

        print('You have deleted', len(imagesToDelete), 'images from the repo.')
        print()
    else:
        print('This action has been cancelled.')
        print()

    deleteFolder(folderName)
