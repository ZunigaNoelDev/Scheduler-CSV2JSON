# Scheduler-CSV2JSON
Converts a schedule of class offerings from a CSV file to a JSON file that can be pushed to a database via a POST request.


## Why this exists
The company I work for uses a Google Sheet to plan a schedule of classes it will offer throughout the summer. From this Google Sheet, we had to manually enter the date, time, course, location, and price into our website. While the task wasn't difficult, it was monotonous and time consuming having to enter upwards of 200 course offerings across 4 different locations. With expansion in mind, this practice of manually entering data was not sustainable.

This script accepts the CSV version of the Google Sheet and parses it to post each offering to the company's website within minutes, limited primarily by the speed at which the server can handle the requests. 

## Application Specific Requirements
Because this script was made for a very specific purpose it asks for a few pieces of information right off the bat.

* The script requires the oID for each class offered as well as the oID of the location it will be offered in; these IDs are pulled from our database, but dummy files are included here for testing.
* The script also requires the ID of the person posting and the api endpoint that will be handling the requests; these have been omitted from the script for security reasons.
* After the initial setup, a CSV schedule is loaded into the script and it will ask for the rows and columns of specific information if it cannot be automatically parsed.

Once the file has been read, the script will either output a single payload including all courses or a series of individual entries to be posted separately.

## Screenshots

![Alt text](/Files/Screenshots/example_schedule.png "Example schedule")
![Alt text](/Files/Screenshots/gui.png "GUI")

## TODO 
* Remove dependency on Requests
* Add login feature to remove manual entry of user uID
* Automate search of required files in script's root directory
* Generalize CSV to JSON schedule parsing 
