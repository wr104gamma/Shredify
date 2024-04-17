# Shredify 1.0
Shredify 1.0 is a GUI interface that piggybacks on the shred shell command.
The user chooses how many passes to write over a given file(s) before it
finally fills the data with zeroes. The user can cut and paste batch files
from their desktop interface, add entire directories, or one file at a time.

Three files are included; shredify, shredbody.py, and drivescan.py.
shredify is the bootloader which will grab administrator access and then
send the command to gather a list of unused, large files, and recycle bin
materials and store it in your Documents folder. drivescan_results.txt is
the name of the created file. After creating the list of junk files the
main application is opened, shredbody.py.

Shredbody.py is the main program and will handle securely deleting selected
file(s). From this window you can import the junk file list, !!BE CAREFUL!!
you may see stored drive snapshots and other large files required by your
system. WE ARE NOT RESPONSIBLE FOR LOST DATA. USE AT YOUR OWN RISK

INSTALL NOTES:
1. Download all three files or the Zip; Shredify, shredbody.py, and scandrive.py. 
2 Open a terminal window to your download directory with the three files or zip
3. Unzip if you chose to download the archive
4. The following will take care of the placing the files in your /bin/ system folder:
sudo mv shredify /bin/ && sudo mv shredbody.py /bin/ && sudo mv scandrive.py /bin/
5. The following will make your program files executable and accessible by your group
sudo chmod u=rwx,g=r,o= /bin/shredbody.py  && sudo chmod u=rwx,g=r,o= /bin/shredify  && sudo chmod u=rwx,g=r,o= /bin/scandrive.py
6. Create a Desktop link. Open a terminal window and type: 
cd Desktop && ln -s /bin/shredify
7. Change the icon style by right-clicking and going to properties.


Let me know if you have any trouble! 
wr104gamma@gmail.com
