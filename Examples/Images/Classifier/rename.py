import os

def replace(fpath, old_str, new_str):
    for path, subdirs, files in os.walk(fpath):
        for name in files:
            if(old_str.lower() in name.lower()):
                os.rename(os.path.join(path,name), os.path.join(path,
                                            name.lower().replace(old_str,new_str)))
rename('/Users/fernanfederici/Dropbox/000_hardware/DIY_equip_2016/FluoPi/Examples/Images/Classifier/BeRFP_data', '*.jpg', 'image_(%s).jpg')



