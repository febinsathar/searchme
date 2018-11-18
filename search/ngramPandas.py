from tqdm import tqdm
from Levenshtein import distance
from itertools import chain, product


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,  cls).__call__(*args, **kwargs)
        return cls._instances[cls]




class NgramPandas(metaclass = Singleton):
    def __init__(self, data):
        self.searchDF = {}
        self.total_words= data.shape[0]
        self.trigramMap={}
        self.fourgramMap={}
        self.build_bulk_ngram(data)
        self.max_letter_len
    
    def build_bulk_ngram(self,data):
        computeDF=data[~data['word'].isnull()]
        computeDF["len"]=computeDF['word'].str.len()
        computeDF['lookupindex']=computeDF['freq'].rank(method='first')
        computeDF["3gram"]=computeDF['word'].apply(lambda x: self.ngrams(x,3,True,False,"-"))
        computeDF["4gram"]=computeDF['word'].apply(lambda x: self.ngrams(x,4,False,False,"-"))
        self.max_letter_len=int(computeDF["len"].max())
        computeDF.set_index(['lookupindex', 'word','len'], inplace=True)
        self.fourgramMap={}
        self.trigramMap={}
        pbar=tqdm(total = self.total_words)
        for index,rec in computeDF.iterrows():
            pbar.update(1)
            for gram in rec['3gram'].keys():
                if(gram in self.trigramMap):
                    self.trigramMap[gram].append(index[0])
                else:
                    self.trigramMap[gram]=[index[0]]
            for gram in rec['4gram'].keys():
                if(gram in self.fourgramMap):
                    self.fourgramMap[gram].append(index[0])
                else:
                    self.fourgramMap[gram]=[index[0]]
        self.searchDF=computeDF[['freq']].copy(deep=True)           
    @staticmethod
    def check_start(searchLength,search_term,queryString):
        if(queryString[:searchLength]==search_term):
            return True
        else:
            return False
    
    @staticmethod   
    def ngrams(sequence, n, pad_left=False, pad_right=False, pad_symbol=None):
        if pad_left:
            sequence = chain((pad_symbol,) * (n-1), sequence)
        if pad_right:
            sequence = chain(sequence, (pad_symbol,) * (n-1))
        sequence = list(sequence)
        count = max(0, len(sequence) - n + 1)
        ngramset={}
        for i in range(count):
            val="".join(sequence[i:i+n])
            if val in ngramset:
                ngramset[val]=ngramset[val]+1
            else:
                ngramset[val]=1
        return ngramset
    
    def search_me(self,search_term):
        print("searching",search_term)
        searchLength=len(search_term)
        resultListfromNgram=[]
        if(searchLength<15):
            predgramList=self.ngrams(search_term,3,True,False,"-")
            for pred in predgramList.keys():
                resultListfromNgram=resultListfromNgram+self.trigramMap[pred]
        else:
            predgramList=self.ngrams(search_term,4,False,False,"-")
            for pred in predgramList.keys():
                resultListfromNgram=resultListfromNgram+self.fourgramMap[pred]
        res=self.searchDF[(self.searchDF.index.get_level_values('lookupindex').isin(set(resultListfromNgram))) &(self.searchDF.index.get_level_values('len')>=searchLength)].copy(deep=True)
        res['score']=res.index.get_level_values('word').map(lambda x: distance(x,search_term))
        res['has_start']=res.index.get_level_values('word').map(lambda x: self.check_start(searchLength,search_term,x))
        return res.sort_values(['has_start','score','len','freq'],ascending=[False,True,True,False])

    
    def addChild(self, key, data=None):
        #Todo: extension to add to the ngram tree         
        pass
