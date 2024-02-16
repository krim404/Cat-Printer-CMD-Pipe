# Cat-Printer-CMD-Pipe
Uses https://github.com/NaitLee/Cat-Printer print.py to act as an command line tool to directly print your favorite text onto your thermo printer  
Also uses https://github.com/FriedOrange/MatrixSans as a great printable font. Matrix-Sans is supplied in this repostory

![Demo](/demo.png?raw=true "Demo Picture")

## How to use
Step 1: Install https://github.com/NaitLee/Cat-Printer and copy the files from this repository in the folder.  
Step 2: Pipe the text you want to print to the text.py, for example `ls -lh | python3 ~/Cat-Printer/text.py`  
Step 3: Profit

Optional: add a shortcut to your .rc file like: `alias catprint="python3 ~/Cat-Printer/text.py"`, so you can use it all the time by simply piping to `catprint`

## Variables
You can set some enviroment variables:
* "cat_font" - set the used TTF font, default: MatrixSans-Regular.ttf
* "cat_font_size" - the font size used (as it will always be resized just increases the quality) default:  20)
* "cat_font_spacing" - the spacing between lines, default:  -2)
* "cat_length" - the maximum amount of characters till linebreak, default:  60)
* "cat_search" - the timeout to search for a compatible printer, default:  6)
* "cat_max-retries" - how many times printer.py should be called before giving up, default: 5)

