#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# This code is PEP8-compliant. See http://www.python.org/dev/peps/pep-0008.

from __future__ import unicode_literals

import autopath

from alex.components.slu.base import SLUPreprocessing
from alex.components.asr.utterance import Utterance
from alex.utils.czech_stemmer import cz_stem


class PTICSSLUPreprocessing(SLUPreprocessing):
    """
    Extends SLUPreprocessing for some transformations specific for Czech:
        - devocalisation of prepositions
        - stemming.

    """
    def __init__(self, *args, **kwargs):
        super(PTICSSLUPreprocessing, self).__init__(*args, **kwargs)
        # XXX This is not very nice.  The parent class cares mainly about
        # normalising English, not Czech.
        # not really, the implicit mapping is just an example.
        # In fact, it could be moved into a default config.

        self.text_normalization_mapping += [
            (['ve'], ['v']),
            (['ke'], ['k']),
            (['ku'], ['k']),
            (['ze'], ['z']),
            (['se'], ['s']),
            (['barandov'], ['barrandov']),
        ]

    def normalise_utterance(self, utterance):
        utterance = super(PTICSSLUPreprocessing,self).normalise_utterance(utterance)
        utt = Utterance(" ".join(map(cz_stem, utterance)))
        return utt
