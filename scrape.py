import sys
import urllib
import json

def main():
    try:
        number = sys.argv[1]
    except:
        number = raw_input("Enter comic number: ")

    cur_xkcd = dict()

    if int(number) == 404:
        # Update Current
        cur_xkcd['url']     = "https://xkcd.com/" + str(number)
        cur_xkcd['explain'] = "http://www.explainxkcd.com/wiki/index.php/" + str(number)
        cur_xkcd['title']   = "404: Not Found"
    else:
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

    # Open favorites.json
    favorites = open("favorites.json", 'r')
    all_xkcd = json.loads(favorites.read())
    # Clear favorites.json
    favorites.close()
    favorites = open("favorites.json", 'w')
    # Update favorites.json
    all_xkcd[str(number)] = cur_xkcd
    favorites.write(json.dumps(all_xkcd))
    favorites.close()

    # Open README.md
    readme = open('README.md', 'w')
    skeleton = open("skeleton.md", 'r')
    tbuf = skeleton.read()

    # Add (sorted) comics to README.md
    for key in sorted(all_xkcd.keys()):
        cur = all_xkcd[key]
        # Markdown Formatted Entry
        md_bullet = "* [xkcd " + key + "](" + cur['url'] + "): " + cur['title'] + " ([explained](" + cur['explain'] + "))\n"
        tbuf += md_bullet

    # Update README.md
    readme.write(tbuf)
    readme.close()
    skeleton.close()

if __name__ == '__main__':
    main()
