# xkcd Treasure Chest

This is a collection of my favorite xkcd comics, updated on a strict interesting-xkcd-discovered schedule. All comics can be found in the `images` folder.

Accompanying is also a Python file that takes can scrapes an xkcd comic given its number and updates the images folder and the README file.

### Dependencies

You will need the following packages installed for Python 2.7:
* `urllib`
* `json`

### Use

1. `python xkcd.py add [<comic_number_1>, <comic_number_2>, ...]`

   Fetches and adds the comic numbers to the `images` folder and updates the README file.

2. `python xkcd.py remove [<comic_number_1>, <comic_number_2>, ...]`

   Removes the comic numbers from the `images` folder and updates the README file.

3. `python xkcd.py update`

   Updates the README file based based on changes in the skeleton without adding/removing any comics.

4. `python xkcd.py reset`

   Clears the image folder and updates the README file.

### Favorite Comics
