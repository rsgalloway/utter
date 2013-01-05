
Utter is a text-to-speech (tts) Python library that also supports multiple language
translation (requires Google Translate API key).

Usage
-----

Basic usage ::

    > utter <file.txt> | "some text" [-s <source lang>] [-t <target lang>]

Language specification must be in the form of a two letter code, e.g. for English 
use the code "en", for Spannish use the code "es", etc. 

Installation
------------

Using easy install ::

    > easy_install utter

Or from source ::

    > git clone https://github.com/rsgalloway/utter.git
    > cd utter
    > python setup.py install

