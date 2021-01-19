# REQUIRED LIBRARIES
import os, shutil, time, sys
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re, csv
import get_websites



# GLOBAL VARIABLE
CURR_DIR = os.path.dirname(os.path.realpath(__file__))+'/'



# SETUP FUNCTION EXECUTING AT LAUNCH
def setup(n):

    # Open parameters configuration file to store parameters in a list
    parameters_config_file = open(CURR_DIR + "parameters_config_file.txt", "r")
    global parameters_array
    parameters_array = []
    parameters_lines = parameters_config_file.readlines() 
    for line in parameters_lines:
        parameters_array.append(line.strip('\n'))


    # Depending on the function parameter execute different operations
    if n == 0:
        # If n == 0 then use the user created version of 
        # the "websites_config_file.txt" file
        websites_config_file = open(CURR_DIR + "websites_config_file.txt", "r")
    else:
        # If n != 0 then use the top nth websites of Alexa List
        get_websites.get_top_websites()
        get_websites.create_website_config(n)
        websites_config_file = open(CURR_DIR + "AlexaTopSites/top-1m.csv", "r")


    # Save the websites in a list while adding "http://" to the URL
    global websites_array
    websites_array = []
    websites_lines = websites_config_file.readlines() 
    for line in websites_lines:
        if line.__contains__('https://') == False:
            websites_array.append('http://' + line.strip('\n'))    
        else:
            websites_array.append(line.strip('\n'))


    return parameters_array,websites_array



# CLEANUP FUNCTION TO DELETE PREVIOUSLY DOWNLOADED FILES
def folder_cleanup(path, folder):
    dir_name = path + folder
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        if not os.listdir(dir_name):
            print("Directory is empty, cleanup is not needed.\n")
        else:    
            print("Directory is not empty, cleaning up...\n")
            shutil.rmtree(dir_name, ignore_errors=False, onerror=None)
            os.mkdir(dir_name)
            print('Cleanup done!\n')
    else:
        print("Given Directory doesn't exist. Creating...\n")
        os.mkdir(dir_name)
        print('Folder '+ folder +' has been created successfully!\n')



# SAVEPAGE FUNCTION THAT DOWNLOADS JAVASCRIPT FILES OF A GIVEN WEBPAGE
def savePage(url, pagefilename='page'):
    # Local function for downloading desired files from a webpage
    def soupfindnSave(pagefolder, tag2find='script', inner='src'):
        if not os.path.exists(pagefolder):
            os.mkdir(pagefolder)
            print(pagefolder)

        # Look for the specified file types in the "soup"
        for res in soup.findAll(tag2find):
            try:         
                if not res.has_attr(inner): # check if inner tag (file object) exists
                    continue # may or may not exist
                filename = os.path.basename(res[inner]) # clean special chars
                fileurl = urljoin(url, res.get(inner)) # get url of specific file
                filepath = os.path.join(pagefolder, filename) # get path of specific file
                res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                if not os.path.isfile(filepath): # was not downloaded
                    with open(filepath, 'wb') as file:
                        filebin = session.get(fileurl)
                        file.write(filebin.content)
            except Exception as exc:
                print(exc, file=sys.stderr)
        return soup
    
    # Create session
    session = requests.Session()

    # Create HTTP request to the desired URL
    response = session.get(url)

    # Create soup based on the webpage we juste requested
    soup = BeautifulSoup(response.text, features="lxml")

    # Name of the folder
    pagefolder = pagefilename+'_files'

    # Save all of the desired files in the previously created folder
    soup = soupfindnSave(pagefolder, 'script', 'src')

    return soup



# FILTER FUNCTION THAT CORRECTLY ORGANIZES AND
# FILTERS FILES FOR LATER USE
def js_filter(path, domain_name):
    print('Filtering: ', path)
    old_path = path + domain_name + '_files/'
    new_path = path + 'WebPageDownloads/' + domain_name + '_files/'
    if not os.path.exists(new_path): # create only once
            os.mkdir(new_path)
    
    for root, _, files in os.walk(old_path):
        for file_ in files:
            file_path = os.path.join(root, file_)
            file_name = os.path.basename(file_path)   
            if file_path.__contains__(".js") == True:
                dest_path = new_path + file_name
                print("MOVING: ", file_name, " from ",file_path, " to ", dest_path, "\n")
                shutil.move(file_path,dest_path)
    print("DELETING: ", old_path, "\n")
    shutil.rmtree(old_path)



# PARSER FUNCTION THAT CHECKS THE PRESENCE OF A STRING IN A FILE
def js_parser(path, method_name):
    print('Parsing: '+ path)
    summary_path = path + '/summary.txt'

    appearance_counter = 0 # Variable to count appearance of string
    appeared_in = [] # Array to hold files in which string appears

    for root, _, files in os.walk(path): # Go through all files
        for file_ in files:
            file_path = os.path.join(root, file_) # Create file path
            file_name = os.path.basename(file_path) # Create file name
            print('Current File:' + file_name)

            # Open file in order to look for string
            with open(file_path, encoding="ISO-8859-1") as f: 
                if method_name in f.read():
                    if file_name == 'summary.txt':
                        break

                    # If string appears then add 1 to counter and add file name to array
                    appearance_counter += 1
                    print(file_path + ' contains ' + method_name)
                    appeared_in.append('Appears in file: ' + file_name)

    # Lines 163-183 are used to write into a summary file
    if appearance_counter == 0:
        print("The method " + method_name +
        " did not appear in the files of the webpage.\n")

        with open(summary_path, "a") as summary_file:
            summary_file.write("The method " + method_name +
            " did not appear in the files of the webpage.\n")

        return 0

    else:
        print("The method " + method_name + " appeared a total of "
        + str(appearance_counter) + " times in the following files:\n")

        with open(summary_path, "a") as summary_file:
            summary_file.write("The method " + method_name +
            " appeared a total of " + str(appearance_counter) +
            " times in the following files:\n")

            for string in appeared_in:
                summary_file.write(string + "\n")
            summary_file.write("\n")
        
        return appearance_counter



# MAIN EXECUTION OF THE TOOL
setup(10)
folder_cleanup(CURR_DIR, 'WebPageDownloads')
website_counter = 0
filename = "parameters_counted.csv"
file_header = ['url']

for parameter in parameters_array:
    file_header.append(parameter)

row_array = []

for website in websites_array:
    
    print("\n CHECKING WEBSITE: ", website, "\n")
    url = website
    download_location = CURR_DIR
    domain_name = url.replace("http://","")
    domain_name = domain_name.replace("https://","")
    domain_name = domain_name.replace("www.", "")
    domain_name = domain_name.replace("/", "")
    parameters_ocurrences = {'url': url}

    try:
        savePage(url, domain_name)

        js_filter(download_location , domain_name)

        for parameter in parameters_array:
            print("\n CHECKING PARAMETER: ", parameter, "\n")        
            parameters_ocurrences[parameter] = js_parser(download_location + "WebPageDownloads/" + domain_name + '_files', parameter)

        row_array.append(parameters_ocurrences)    
    
    except:
        pass
    
    website_counter += 1

with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = file_header, lineterminator = '\n')
    writer.writeheader()
    writer.writerows(row_array)