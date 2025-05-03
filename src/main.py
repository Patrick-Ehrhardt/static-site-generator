from textnode import *
from leafnode import *
from parentnode import *
from otherfunctions import *
from blocks import *
import os
import shutil
import sys

def update_static_public():
    if os.path.exists("./public"):
        shutil.rmtree("./public/")
    #print(os.listdir("./static"))
    #print("./static/" + os.listdir("./static/")[0])
    #shutil.copy("./static/" + os.listdir("./static/")[0], "./")
    copy_recursive("./static/", "./public/")

def copy_recursive(source, target):
    if not os.path.isdir(target):
        #print(f"making {target} dir")
        os.mkdir(target)
    file_list = os.listdir(source)
    for file in file_list:
        #print(file)
        if os.path.isfile(source + file):
            #print(f"copying {source + file} to {target + file}")
            shutil.copy(source + file, target + file)
        elif os.path.isdir(source + file):
            copy_recursive(source + file + "/", target + file + "/")
    return

def main():
    basepath = "/"
    #print(type(sys.argv))
    #print(len(sys.argv))
    if(len(sys.argv) > 1):
        basepath = sys.argv[1]
        """
    if not os.path.exists(basepath):
        os.makedirs(basepath)
    if not os.path.exists(basepath + "public/"):
        print(f"making {basepath}public/")
        os.makedirs("." + basepath + "public/")
    if not os.path.exists(basepath + "content/"):
        print(f"making {basepath}content/")
        os.makedirs("." + basepath + "content/")
    print(f"basepath = {basepath}") """
    update_static_public()
    generate_page_recursive(f".{basepath}content/", f".{basepath}template.html", f".{basepath}public/", basepath)
    return



    




if __name__ == "__main__":
    main()

