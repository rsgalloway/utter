#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
# Copyright (c) 2012-2013, Ryan Galloway (ryan@rsgalloway.com)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  - Neither the name of the software nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ---------------------------------------------------------------------------------------------
# docs and latest version available for download at
#   http://github.com/rsgalloway/utter
# ---------------------------------------------------------------------------------------------

import os
import sys
import urllib2
from urllib import urlencode, quote
import tempfile
from collections import OrderedDict
import simplejson as json

__doc__ = """
utter is a simple Python utility that converts text to speech, and
optionally language translation using the Google Translate API.

The Google Translate API requires a developer key. You can get one of
these by visiting

https://code.google.com/apis/console
"""

# Puncuation characters, used to split word groups
_PUNCUATION_ = [',', ':', ';', '.', '?', '!']

# Put your Google API key here
global _KEY_
_KEY_ = os.environ.get('GOOGLE_API_KEY', None)

# Google Translate API URLs
_SPEECH_URL_ = 'https://www.google.com/speech-api/v1/recognize'
_LANG_URL_ = 'https://www.googleapis.com/language/translate/v2'
_TTS_URL_ = 'http://translate.google.com/translate_tts'

# Maximum chars per word group
_MAX_CHAR_COUNT_ = 100

def set_api_key(key):
    """
    Sets the global Google API Key value.

    :param key: Google API Key value
    """
    global _KEY_
    _KEY_ = key

def parse_text(text, max_chars=_MAX_CHAR_COUNT_):
    """
    Splits given text string into discrete sentences, based on 
    puncutation and/or char limits.

    :param text: Text string
    :param max_chars: Maximum chars in a sentence (default 100)
    """
    if os.path.isfile(text):
        text = open(text, 'r').read().strip().replace('\n', ' ')
    sentences = []
    words = text.split()
    sentence = ''
    for w in words:
        if w[len(w)-1] in _PUNCUATION_:
            if (len(sentence) + len(w) + 1 < max_chars):
                sentence += ' ' + w
                sentences.append(sentence.strip())
            else:
                sentences.append(sentence.strip())
                sentences.append(w.strip())
            sentence = ''
        else:
            if (len(sentence) + len(w) + 1 < max_chars):   
                sentence += ' ' + w 
            else:
                sentences.append(sentence.strip())
                sentence = w
    if len(sentence) > 0:
        sentences.append(sentence.strip().encode("utf-8"))
    return sentences

def stt(wave):
    """
    Converts speech to text from an input wave file.

    :param wave: Path to .wav file.
    """
    f = open(wave, 'rb')
    data = f.read()
    f.close()
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'),
                                        ('Content-type', 'audio/x-flac; rate=16000'),
                                        ]
    query_string = urlencode(OrderedDict(xjerr=1, client="chromium", lang="en-US"))
    url = "?".join([_SPEECH_URL_, query_string])
    response = opener.open(url, data=data)
    data = json.load(response).get("data")

def trans(text, source="en", target="en"):
    """
    Translates input text.

    :param source: source language abbreviation, e.g. "en"
    :param target: target language abbreviation
    """
    if _KEY_ is None:
        raise Exception("Google API key not set")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]
    query_string = urlencode(OrderedDict(key=_KEY_, q=text, source=source, target=target))
    url = "?".join([_LANG_URL_, query_string])
    response = opener.open(url)
    data = json.load(response).get("data")
    # e.g. {'data': {'translations': [{'translatedText': 'Hallo'}]}}
    return data.get("translations")[0]["translatedText"]

def tts(text, source, target):
    """
    Converts ascii text into spoken mp3 files.

    :param text: text file or string
    :param source: source language abbreviation, e.g. "en"
    :param target: target language abbreviation
    """
    outdir = tempfile.mkdtemp()
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]
    sentences = parse_text(text)

    # translate
    if source != target:
        sentences = parse_text(trans(text, source, target))

    # text to speech
    for i, sentence in enumerate(sentences):
        query_string = urlencode(OrderedDict(q=sentence, tl=target))
        url = "?".join([_TTS_URL_, query_string])
        response = opener.open(url)
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        f = open(os.path.join(outdir, 'tts_%04d.mp3' % i), 'wb')
        f.write(response.read())
        f.close()

    return outdir
