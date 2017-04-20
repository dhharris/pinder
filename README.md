# Pinder
### About
Pinder is a desktop application for Tinder written in Python. The goal of this project is to provide every feature
that Tinder offers *for free* with *no conditions*, right on your computer. In other words, you get the premium
version of Tinder with no ads or distractions.

### Features
* Like, dislike and super like people around you
* Change your location without paying for premium access
* Undo the last swipe you made
* (planned) View multiple photos and the bio of your potential match
* (planned) Messaging system
* (planned) Cross platform support for app wrappers

### Images
![screenshot](https://raw.githubusercontent.com/dhharris/pinder/master/pinder_screencap.png)

### Requirements
* The latest version of Python 3, which can be found [here](https://www.python.org)
* The following python libraries (can be installed using pip)
	* bs4
	* lxml
	* py2app (if you plan on building the application)
	* pynder
	* requests
	* robobrowser
	* wxPython
* The software can be run using the python interpreter, but if you want to test the *application distribution*,
only MacOS is supported (for now)

### Licensing
This will always be *"Free and Open Source Software"*. That means that anyone can do anything they want with it,
including for commercial purposes. Formally, it is licsensed under the "MIT License", which you can find in LICENSE.TXT 


## Contributing

### Documentation (INCOMPLETE)
Make sure you have the requirements installed. Run the app using the python interpreter

```bash
python3 pinder.py
```

In addition, if you are running MacOS, you can build the distribution file as follows

```bash
./build.sh
```

This will create two folders, `build` and `dist`. The latter contains the `pinder.app` file, which can be run on MacOS.
See the [py2app documentation](https://py2app.readthedocs.io/en/latest/) for more information.

### Todo list
* Unit testing
* Refactoring and cleaning up viewer.py
* Better error handling for popup windows
* Messaging system
* Store facebook tokens more securely
* Better build scripts, with options for development or deployment builds