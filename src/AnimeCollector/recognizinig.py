# recognizing.py - Recognizing engine 
# Copyright (c) 2009 Andre 'Necrotex' Peiffer
# See COPYING for details

# Standardlib
import re
import cPickle
import difflib
from os import path

# AnimeCollector 
from globs import ac_data_path

class engine:
    """
    Regogniziging engine
        
    When creating a instance of this class, the filename musst
    be overhanded.
    E.g. engine = regognizing.engine("filename.avi")
    
    Filename processing:
    This methodes filter the provided filename.
    Protected methods:
        __filter: removes hashtags, subgroup and codecs
            Returns: the filterd anime name
        
    Private methods:
        _getName: removes all but the anime name.
            Returns: anime name
        
        _getEpisode: removes all but the current watched 
                        episode
            Returns: current watched episode
        
        Not implemented yet:
        _getSeason: checks if there a more then one season
            Returns: current series season
    
    Regogniziging engine:
    These methodes provides functions to recognize the
    current watched series and change the episode in the
    local database.
    
    Private methodes:
        __matching: Evaluates a ratio of probable equally
                    of the current watched series and the
                    entries in the local database, writes
                    it into a dict and sort it.
            returns: a sorted dictonary with {animename : ratio}
    
        __update: updates the local database
            returns: true on success and false on failure
    
    Public methods:    
        match: main method
            returns: # TODO: Find a good return
    """
    
    def __init__(self, filename):
        
        self.filename = filename

        # Read database, if it can't be read return false
        if path.exists(ac_data_path):
            dbhandle = open(ac_data_path, "rb")
            self.db  = cPickle.load(dbhandle)
            dbhandle.close()
        else:
            return False
          
    def __del__(self):
        """ Maybe needed to close a opened file/DB"""
        #TODO: Find a OS undependend way for checking if a
        # file is open.
        pass
        
    #####################
    # Filename Processing
    #####################
        
    def __filter(self):
        """Get rid of hashtags, subgroup, codec and such"""
         
        # Second version of the RegEx. 
        # matches all charactes between "[" and "]"
        reg = re.compile("([[a-zA-Z0-9\-]*])")
        anime_raw = reg.sub("", self.filename)
         
        # get rid of underscores
        anime_raw = anime_raw.replace("_"," ")
         
        # get rid of the file extension, currently just .mkv, .mp4 and .avi
        anime_raw = re.sub("((.mkv)|(.mp4)|(.avi))$","",anime_raw)
          
        return anime_raw.strip()
    
    def _getName(self):
        """getting and returning anime name"""

        # get rid of the Episode 
        animeName = re.sub("[0-9\s]{1,}", "", __filter())

        # get rid of scores
        animeName = animeName.replace("-","")

        return animeName.strip()
    
    def _getEpisode(self):
        """getting and returning anime episode"""
        animeEpisode = re.sub("[a-zA-Z\-~\s]{1,}", "", \
            __filter())
            
        # TODO: Add a RegEx for matching out the Season Number
        
        return animeEpisode.strip()
   
    def _getSeason(self):
          """
          Check if there are more than one and return
          the season of the current watched. Future feature. ^^
          """
          pass

    ##########
    # Matching
    ##########

    def __matching(self):
        """ 
        Evaluates a ratio of probable equally and returns the most likely Anime
        """
        currentDB = dict()
        matching = dict()

        # Fill a dict with the 
        for anime in self.db[key]:
            currentDB[anime].append(0)
        
        # The essence machting algorithm
        for anime in currentDB[key]:
            ratio = difflib.SequenceMatcher(None, anime, \
                self._getName())
            matching[anime] = ratio
        
        # Sorting self.matching and retrun it...
        # Well, this is a bit of a hack since you can't really sort dicts
        # TODO: Should be tested :D
        rLst = matching.items()
        rSort = [ [v[1],v[0]] for v in rLst]
        rSort.sort()
        matching = [rSort[i][1] for i in range(0,len(rSort))]
        
        # check if there is a ratio over 0.8
        if matching[0] < 0.8:
            # if not return false
            return False
        
        # return the most likely animename
        return matching[0]

    def __update(self):
        
        if not __matching():
            return False
        
        dictMatch = __matching()
        
        # Update self.db
        for k in self.db:
            if k == dictMatch[0]:
                self.db[k]['my_watched_episodes'] = \
                    self._getEpisode()
        
        # Write changes to locale db
        dbhandle = open(ac_data_path, "rb")
        cPickle.dump(self.db, dbhandle)
        dbhandle.close()
        return True
    
    def match(self):
        pass
