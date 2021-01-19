# BSP03-Web-Scraper-4.0

In this repository you will find the source code of the tool.

To edit the websites that the tool will look at, just edit the file "websites_config_file.txt". Only valid URLs should be put in this text file, and each line should only contain URLs and nothing else. After each URL go to the next line.

To edit the parameters that the tool will look for, just edit the file "parameters_config_file.txt". Only valid JavaScript methods should be put in this text file, and each line should only contain one method and nothing else. After each method go to the next line.

The tool has to be run through "webpage_cloner_4.0.py"

The downloaded files will be stored in the "WebPageDownloads" folder that will be created after execution in the "Source" folder. The results of will be stored in the "parameters_counted.csv" file that will be created after execution in the "Source" folder.

!!!CAUTION!!! At the start of each execution the tool will wipe out the previous "WebPageDownloads" folder and the previous "parameters_counted.csv" file.