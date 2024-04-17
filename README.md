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
