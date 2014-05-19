import SearchResult
import File
import Peer
import sys
import os

class SearchResultService:
    
    @staticmethod
    def insertNewSearchResult(database, randomid, filename, lenfile, lenpart):
        
        try:
            sr = SearchResultService.getSearchResult(database, randomid, filename, lenfile, lenpart)
        
        except:
            sr = SearchResult.SearchResult(None, randomid, filename, lenfile, lenpart, 'F')
            sr.insert(database)
        
        return sr
    
    @staticmethod
    def getSearchResult(database, randomid, filename, lenfile, lenpart):
        
        database.execute("""SELECT idsearchresult, randomid, filename, lenfile, lenpart, choose
                            FROM SearchResult
                            WHERE randomid = %s AND filename = %s AND lenfile = %s AND lenpart = %s""",
                            (randomid, filename, lenfile, lenpart))
        
        idsearchresult, randomid, filename, lenfile, lenpart, choose = database.fetchone()
        
        searchResult = SearchResult.SearchResult(idsearchresult, randomid, filename, lenfile, lenpart, choose)
        
        return searchResult
    
    @staticmethod
    def getSearchResults(database):
        database.execute("""SELECT idsearchresult, randomid, filename, lenfile, lenpart, choose
                            FROM SearchResult""")        
        
        try:            
            searchResults = []         
            
            while True:            
                idsearchresult, randomid, filename, lenfile, lenpart, choose = database.fetchone()       
                searchResults.append(SearchResult.SearchResult(idsearchresult, randomid, filename, lenfile, lenpart, choose))     
                                
        except:
            pass            
            
        return searchResults
      
    @staticmethod
    def delete(database):
        database.execute("""DELETE FROM SearchResult""")
        
    
    @staticmethod
    def getSearchResultTrue(database):
        database.execute("""SELECT idsearchresult, randomid, filename, lenfile, lenpart, choose
                            FROM SearchResult
                            WHERE choose= %s""", "T")
        
        idsearchresult, randomid, filename, lenfile, lenpart, choose = database.fetchone()
        
        searchResult = SearchResult.SearchResult(idsearchresult, randomid, filename, lenfile, lenpart, choose)
        
        return searchResult
    
    @staticmethod
    def unsetDownloadSearchResult(database):
        database.execute("""UPDATE SearchResult
                            SET choose = 'F'
                            WHERE choose = 'T'""")