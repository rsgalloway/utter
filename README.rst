
Utter is a text-to-speech (tts) Python library that also supports multiple language
translation (requires Google Translate API key).

You can try the Heroku web app here (sorry, Chrome only):

http://utter.herokuapp.com

Note: I've capped the language translation at 2M characters per day. Once that's
reached, it won't work any more that day.

Usage
-----

Basic usage ::

    $ utter <file.txt> | "some text" [-s <source lang>] [-t <target lang>]

Language specification must be in the form of a two letter code, e.g. for English 
use the code "en", for Spannish use the code "es", etc. It also requires first
specifying a Google API key value, either in the source or in the environment. ::

    $ export GOOGLE_API_KEY="<your api key>"

Installation
------------

Using easy install ::

    $ easy_install utter

Or from source ::

    $ git clone https://github.com/rsgalloway/utter.git
    $ cd utter
    $ python setup.py install

Web App
-------

Utter comes with a basic flask web app that uses the chrome webkit speech input
to record a user's voice, which is converted to text before being passed to utter
to translate and play back in a selected language.

Running the app using Flask ::

    $ git checkout web
    $ python main.py

will run the app at http://localhost:5000.

To deploy on heroku ::

    $ heroku create
    $ git push heroku web:master

