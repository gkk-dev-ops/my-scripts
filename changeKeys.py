#!/usr/bin/python3

import os
import sys
import shutil
import json
import subprocess
import argparse

HOME = os.getenv('HOME')
PRIV_KEY = "id_rsa"
PUB_KEY = "id_rsa.pub"
BLACKLISTED_FILES = 'blacklist.json'

def usage():
    print("""
    changeKeys.py [keys directory name]

    
    """)

def blacklisted_files() -> list[str]:
    with open(BLACKLISTED_FILES, 'r') as f:
        data = json.load(f)
    return data['blacklist']

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
        if file in blacklisted_files():
            continue
        print(f"{file}")

    dir = input("What key's do you want to copy? ")
    return dir


def generate_keys_catalog(key_catalog):
    os.mkdir(key_catalog)
    ssh_gen_cmd = ['ssh-keygen', '-b', '2048', '-t', 'rsa', '-f',
                os.path.join(HOME,'.ssh', key_catalog, PRIV_KEY),
                '-q',  '-N', '""']
    subprocess.run(ssh_gen_cmd)


def guide_user_change_keys():
    key_catalog = userPrompt()
    if key_catalog not in os.listdir(os.getcwd()):
        print("Specified catalog does not exist.")
        sys.exit(3)
    change_keys(key_catalog)

def change_keys(key_catalog):
    delete_keys()
    copy_keys(key_catalog)

def main():
    parser = argparse.ArgumentParser(
            description="""
    To change ssh keys in your .ssh directory you can just run the script and
    follow steps listed in prompt or run it with name of subdirectory where
    target keys are stored.
            """)
    parser.add_argument('-ck', '--change-keys', dest='keys_to_be_changed', help='keys catalog to change')
    parser.add_argument('-ac', '--add-catalog', dest='add_catalog', help='add new catalog for storing ssh keys')
    args = parser.parse_args()
    if args.keys_to_be_changed:
        change_keys(args.keys_to_be_changed)
    if args.add_catalog:
        generate_keys_catalog(args.add_catalog)

if __name__ == "__main__":
    os.chdir(os.path.join(HOME,'.ssh'))
    
    if len(sys.argv) > 1:
        main()
    else:
        guide_user_change_keys()
