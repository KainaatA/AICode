import re
import PyPDF2
import numpy as np
from copy import deepcopy
from __params import CREDENTIALS
from nltk.tokenize import word_tokenize
from nltk.lm import WittenBellInterpolated
from nltk.util import pad_sequence, everygrams


class PlagiarismScoring:
    
    @staticmethod
    def _textify(fpaths, only_clean=False):
        text = ''
        for fpath in fpaths:
            with open(file=fpath, mode='rb') as file:
                reader = PyPDF2.PdfFileReader(file)

                for page_number in range(reader.numPages):        
                    page = reader.getPage(page_number)
                    text += page.extractText()+'\n\n'
        
        if not only_clean:
            text = re.sub(r'\[.*\]|\{.*\}', '', text)
        
        text = re.sub(r'[^\w\s]', '', text)
   
        return text

    def _tokenize(self, text, ngrams):
        
        return list(pad_sequence(word_tokenize(text), ngrams, pad_left=True, left_pad_symbol="<s>"))

    def resolve_score(self, fpaths):
       
        resolved_scores = {}
        for fpath in fpaths:

            tmp_fpaths = deepcopy(fpaths)
            tmp_fpaths.remove(fpath)

            text_ = PlagiarismScoring._textify(fpaths=tmp_fpaths)

            # set ngram number
            n = 4

            # pad the text and tokenize
            data_ = self._tokenize(text=text_, ngrams=n)

            # generate ngrams
            ngrams = list(everygrams(data_, max_len=n))
            # build ngram language models
            model = WittenBellInterpolated(n)
            model.fit([ngrams], vocabulary_text=data_)


            # Tokenize and pad the text
            _text = PlagiarismScoring._textify(fpaths=[fpath], only_clean=True)
            _data = self._tokenize(text=_text, ngrams=n)

            # assign scores
            scores = []
            for i, item in enumerate(_data[n-1:]):
                s = model.score(item, _data[i:i+n-1])
                scores.append(s)

            resolved_scores.update({fpath : sum(scores)/len(scores)})
        print('INFO: Plagiarism scores have been resolved.')
        return resolved_scores
