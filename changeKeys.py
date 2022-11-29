#!/usr/bin/python3

import os
import shutil

HOME = os.getenv('HOME')
PRIV_KEY = "id_rsa"
PUB_KEY = "id_rsa.pub"


def delete_keys():
    """Deletes keys from current directory"""
    for key in [PRIV_KEY, PUB_KEY]:
        if os.path.exists(key):
            os.remove(key)
            print(f"Removed {key}")
        else:
            print(f"{key} is not in current directory")


def copy_keys(dir):
    """Copies keys to current directory"""
    src_dir = os.path.join(os.getcwd(), dir)
    for key in [PRIV_KEY, PUB_KEY]:
        print(f"     Copying {key} From {src_dir}")
        if os.path.exists(os.path.join(src_dir,key)):
            shutil.copy2(os.path.join(src_dir, key),
                         os.path.join(os.getcwd(), key))
        else:
            print("Those key's don't exist")


def userPrompt():
    """Returns files to be copied and prompts user"""
    print("You may want to use:")
    for file in os.listdir(os.getcwd()):
        if file in [".git", "known_hosts", "changeKeys.py", "config", "166907050426000", "known_hosts.old", "id_rsa", "id_rsa.pub", '.DS_Store']:
            continue
        print(f"{file}")

    dir = input("What key's do you want to copy? ")
    return dir


def main():
    dir = userPrompt()
    if dir == "":
        return "No keys specified"
    delete_keys()
    copy_keys(dir)


if __name__ == "__main__":
    os.chdir(os.path.join(HOME,'.ssh'))
    main()
