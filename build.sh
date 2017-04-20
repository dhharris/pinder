#!/bin/sh
py2applet --make-setup src/pinder.py src/*.jpg
rm -rf build/ dist/
python3 setup.py py2app -A
