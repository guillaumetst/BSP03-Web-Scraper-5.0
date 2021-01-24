# BSP03-Web-Scraper-5.0

In this repository you will find the source code of the tool.

To edit the websites that the tool will look at, just edit the file "websites_config_file.txt". Only valid URLs should be put in this text file, and each line should only contain URLs and nothing else. After each URL go to the next line. 

To edit the parameters that the tool will look for, just edit the file "parameters_config_file.txt". Only valid JavaScript methods should be put in this text file, and each line should only contain one method and nothing else. After each method go to the next line.

The tool has to be run through "webpage_cloner_5.0.py". If the tool is run Through an IDE then the current folder must be "Sources" and not "BSP03-Web-Scraper-5.0".

The downloaded files will be stored in the "WebPageDownloads" folder that will be created after execution in the "Source" folder. The results of will be stored in the "parameters_counted.csv" file that will be created after execution in the "Source" folder.

!!!CAUTION!!! At the start of each execution the tool will wipe out the previous "WebPageDownloads" folder and the previous "parameters_counted.csv" file.

# Before running the program make sure that the correct value is inserted in the setup() function at line 193. 
setup(0) means that the program will use the website_config_file.txt file edited by the user, using custom URLs.\n
setup(n) for any n !=0 means that the program will use the top n websites of the Alexa Top 1M list.
