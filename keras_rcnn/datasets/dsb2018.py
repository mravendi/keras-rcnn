def md5sum(pathname, blocksize=65536):
    checksum = hashlib.md5()

    with open(pathname, "rb") as stream:
        for block in iter(lambda: stream.read(blocksize), b""):
            checksum.update(block)

    return checksum.hexdigest()


def load_data(path2data,data_group):
    # checking if it locally exists
    path2json=path2data+"{}.json".format(data_group)
    if os.path.exists(path2json):
        print('loading from local')
        with open(path2json) as f:
            dictionaries = json.load(f)
        return dictionaries    
    
    listOfDirs=os.listdir(path2data+data_group)
    print('len of dataset: %s' %len(listOfDirs))
    
    dictionaries=[]
    for i,dirnm in enumerate(listOfDirs):
        print('processing %s %s' %(i,dirnm)) 

        # path to image and masks
        path2dir=os.path.join(path2data,data_group,dirnm)
        path2imgs=os.path.join(path2dir,'images','*.png')
        path2masks=os.path.join(path2dir,'masks','*.png')
        path2imgs=glob.glob(path2imgs)
        path2masks=glob.glob(path2masks)

        img = imread(path2imgs[0])[:,:,:IMG_CHANNELS]
        # create image dict
        imgobj_dict={
            "image":{
                'pathname':path2imgs[0],
                'checksum': md5sum(path2imgs[0]),
                'shape':{
                    'r':img.shape[0],
                    'c':img.shape[1],
                    'channels':img.shape[2]
                }
            },
            "objects": []
        }

        # create objects list
        for path2obj in path2masks:
            mask = imread(path2obj)
            label_mask = label(mask, connectivity=mask.ndim)
            props = regionprops(label_mask)
            obj_dict={
                "bounding_box":{
                        "minimum":{
                            "r":props[0].bbox[0],
                            "c":props[0].bbox[1]
                        },
                        "maximum":{
                            "r":props[0].bbox[2],
                            "c":props[0].bbox[3],
                        },
                },
                "category": "nuclei",        
            }

            imgobj_dict['objects'].append(obj_dict)
        dictionaries.append(imgobj_dict)
    
    # store as a json for future use
    with open(path2json, "w") as stream:
        json.dump(dictionaries, stream)
        
    return dictionaries


##########################################################
##########################################################
## sample use
dicts_train=load_data(path2dsb2018,"stage1_train")
dicts_test=load_data(path2dsb2018,"stage1_test")



