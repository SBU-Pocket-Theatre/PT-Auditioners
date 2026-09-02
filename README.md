# PT-Auditioners

This code determines which characters a person on a production team who auditioned can see during callbacks.

You can download the latest release [here](https://github.com/SBU-Pocket-Theatre/PT-Auditioners/releases).

## Documentation
### Creating A Show
You can create a show with the "Create New Show" button. You will be prompted to name your show, and you must also provide a list of comma-separated roles for the show. After you do this, clicking continue save the show and automatically load it into the editor. 

### Loading A Show
If you have previously created a show, you can click the "Load Show" button. You will be provided with a dropdown menu containing all of your created shows. Once you select the show, clicking "Load" will load the show into the editor.

### Entering Data
After loading a show, you'll want to add people to it. You can do this using the "Add Person" button - a window will pop up prompting you to enter the person's name. You can add the roles people are called back for using the "Add Role To Person" - a window will pop up with two dropdowns, one to select the person and one to select the role. Once you are done entering the data, you can press the "Run" button to launch the conflict interface.

### Saving and Loading Data
If you would like to save your progress as you enter data, you can press the "Save Data" button. You can save the data as a .csv file which can later be loaded by the "Load Data" button. If you want to make edits to the data you've entered, currently the only way to do this is to save the data as a .csv, edit it, and then load it into the editor again. Please be sure to keep the original formatting of the file so that the editor is still able to read it!  

If you find the data entry process too slow, you can also click the "Save Template" button. This will create a .csv file in the correct format that you can edit with Excel, Google Sheets, etc. Again, be sure to maintain the formatting, otherwise the editor won't be able to read the file.

### Conflict Interface (the CLI)
When you press the "Run" button, the editor will close, and the conflict interface will appear. You can enter a person's name to see the lists of roles they can and cannot see in the audition room. The interface will then ask if you want to see the reasoning for why people cannot see certain roles. Once this is complete, it will ask if you want to generate a graph (visual representation) of the data. If you say yes, a .png file will be generated named with the person's name in whatever folder you're running the .exe file from. You will then be prompted to give a different person's name, or you can type "exit" to end the process.
