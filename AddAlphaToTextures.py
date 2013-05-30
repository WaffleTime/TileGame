import os, os.path

import sfml as sf


def main():

    os.chdir(os.getcwd() + "/Resources/Textures/")

    lyst = os.listdir(os.getcwd())

    print lyst

    for item in lyst:

        if os.path.isfile(item)     \
           and item[-4:] == ".bmp":

            print "Item converted successfully!"

            oldImg = sf.Image.load_from_file(item)

            newImg = sf.Image.load_from_pixels(oldImg.width, oldImg.height, oldImg.get_pixels())

            newImg.create_mask_from_color(sf.Color(255,0,255), 0)

            newImg.save_to_file(item[0:-4]+".png")


main()
