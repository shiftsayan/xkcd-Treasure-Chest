#!/usr/bin/python3

#########################
######## Imports ########
#########################

import sys
import os
import shutil
import urllib
import json

#########################
### Global Variables ####
#########################

commands = ['add', 'reset', 'update', 'remove']

#########################
### Helper Functions ####
#########################

def repopulate(new_xkcd):
    # Open README.md
    readme = open('README.md', 'w')
    skeleton = open("skeleton.md", 'r')
    tbuf = skeleton.read()

    # Add (sorted) comics to README.md
    for key in sorted(map(int, new_xkcd.keys())):
        cur = new_xkcd[str(key)]
        # Markdown Formatted Entry
        md_bullet = "* [" + str(key) + "](" + cur['url'] + "): " + cur['title'] + " ([explained](" + cur['explain'] + "))\n"
        tbuf += md_bullet

    # Update README.md
    readme.write(tbuf)
    readme.close()
    skeleton.close()

#########################
### Command Functions ###
#########################

def add(number):
    # Open favorites.json
    favorites = open("favorites.json", 'r')
    all_xkcd = json.loads(favorites.read())

    # Check for Duplicates
    if number in all_xkcd.keys():
        return

    # Clear favorites.json
    favorites.close()
    favorites = open("favorites.json", 'w')

    cur_xkcd = dict()

    if int(number) != 404:
        # Fetch Data
        text = urllib.urlopen("https://xkcd.com/" + str(number) + "/info.0.json").read()
        data = json.loads(text)
        # Update Current
        cur_xkcd['url']     = "https://xkcd.com/" + str(number)
        cur_xkcd['explain'] = "http://www.explainxkcd.com/wiki/index.php/" + str(number)
        cur_xkcd['title']   = str(data['title'])
        # Save Image
        image = str(data['img'])
        urllib.urlretrieve(image, "images/" + str(number) + "." + image.split('.')[-1])
    else:
        # Handle xkcd 404
        cur_xkcd['number']  = number
        cur_xkcd['url']     = "https://xkcd.com/" + str(number)
        cur_xkcd['explain'] = "http://www.explainxkcd.com/wiki/index.php/" + str(number)
        cur_xkcd['title']   = "404: Not Found"

    # Update favorites.json
    all_xkcd[str(number)] = cur_xkcd
    favorites.write(json.dumps(all_xkcd))
    favorites.close()

    # Update README.md
    repopulate(all_xkcd)

def reset():
    # New Favorites
    all_xkcd = dict()

    # Clear Favorites
    favorites = open("favorites.json", 'w')
    favorites.write(json.dumps(all_xkcd)) # Empty JSON
    favorites.close()

    # Clear Images
    shutil.rmtree('images/')
    if not os.path.exists('images/'):
        os.makedirs('images/')

    # Update README.md
    repopulate(all_xkcd)

def update():
    # Open favorites.json
    favorites = open("favorites.json", 'r')
    all_xkcd = json.loads(favorites.read())
    favorites.close()

    # Update README.md
    repopulate(all_xkcd)

def remove(number):
    # Open favorites.json
    favorites = open("favorites.json", 'r')
    all_xkcd = json.loads(favorites.read())

    # Check for Existence
    if str(number) not in all_xkcd.keys():
        return

    # Clear favorites.json
    favorites.close()
    favorites = open("favorites.json", 'w')

    # Remove Comic from JSON
    deleted = all_xkcd.pop(str(number))

    # Remove Comic from images/
    for f in os.listdir("images/"):
        if f.split('.')[0] == str(number):
            os.remove("images/" + f)

    # Update favorites.json
    favorites.write(json.dumps(all_xkcd))
    favorites.close()

    # Update README.md
    repopulate(all_xkcd)

#########################
##### Main Function #####
#########################

def main():
    # Get Command from Command Line
    if (len(sys.argv) < 2) or (sys.argv[1] not in commands):
        print("Invalid Argument")
        return
    else:
        command = sys.argv[1]

    # Execute Command
    if command == 'add':
        # Add Multiple Comics
        for number in sys.argv[2:]:
            add(int(number))
    elif command == 'reset':
        reset()
    elif command == 'update':
        update()
    elif command == 'remove':
        # Remove Multiple Comics
        for number in sys.argv[2:]:
            remove(int(number))

if __name__ == '__main__':
    main()
