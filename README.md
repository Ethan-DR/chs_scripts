# chs_scripts

Setting up
Move the script into the folder where you put the xml docs you are currently working on.
Open the script file (I suggest using textedit) and on line 12 add in the path to that folder
E.g. I work on the path:
“/users/intern4/desktop/perseus_files_to_be_added/”
If your folder is on your desktop, your path will probably be (replace caps with correct information):
“/users/INTERN#/desktop/FOLDER_NAME/”
Note that the quotes ARE needed for this to work
So long as you keep all your editing in that folder you won’t have to do this again.
If terms spits out an error saying something about the EOF that means there’s a problem with the second quotation mark in the file path (line 12). To fix this just copy the quotation mark from the beginning of the path and paste it on to the end of the path. Replacing the final quotation mark should fix this problem. This problem arises because we you may have opened the script as a rich text file.

Running the greek script
Navigate to the folder in your terminal (you can do this in a second terminal window, one where you don’t do git stuff)
In terminal write: python ./greek.py FILENAME
E.g. I was testing on 070 so my run command looked like:
python ./greek.py tlg0007.tlg073.perseus-grc1.xml
The converted fill can be found in the same folder with the proper name (the program assumes that the greek file’s name just requires a change from grc1 to grc2).

After running the greek script:
Copy and paste purple
 <?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="http://www.stoa.org/epidoc/schema/latest/tei-epidoc.rng"
schematypens="http://relaxng.org/ns/structure/1.0"?>
Change the <title> to greek and add in a lang tag 
Comment out/delete the <title type="sub">
Check that the date at the end of <imprint> is not in Roman numerals
Add url to ref element at the end of <biblStruct> 
In the first refsDecl comment out the state elements
Comment out the entire second <refsDecl>
 Reformat the changes recorded in <respStmt> 
Can often just change this information to: <change who="RS" when="2010-05">tagged and parsed</change>
Move the first <milestone> inside of the <p> tag (and check if the other <milestone> tags are within <p> tags too)
Search for and convert any errant single or double quotes
Check for punctuation with extra spaces
The fastest way to do this is to search for “ ([.!?;:,])” (note that you don’t use the quotes and that there must be a space before the parentheses) and replace with “\1” (again no quotes). You have to have the “Regular Expression” box checked when you do this.
Check notes for titles
Tag titles with <title rend=”italic”>
Add any languages used to the <langUsage> section
