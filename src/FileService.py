import File
import PartService
#import sys

class FileService:
        
    @staticmethod
    def insertNewFile(database, sessionid, randomid, lenfile, lenpart, filename):
        file = File.File(randomid, lenfile, lenpart, filename)            
        file.insert(database) 
        
        npart = lenfile // lenpart
        if lenfile % lenpart != 0:
            npart = npart + 1
        
        i = 0
        while i < npart:
            partid = i + 1
            PartService.PartService.insertNewPart(database, sessionid, randomid, partid)
            i=i+1
    
    @staticmethod
    def getFile(database, randomid):
        database.execute("""SELECT randomid, lenfile, lenpart, filename
                            FROM File
                            WHERE randomid = %s""",
                            randomid)
        
        randomid, lenfile, lenpart, filename = database.fetchone()
        
        file = File.File(randomid, lenfile, lenpart, filename)
        
        return file  
    
    @staticmethod
    def getFiles(database, searchString):
        searchString = "%" + searchString + "%"
        database.execute("""SELECT randomid, lenfile, lenpart, filename
                            FROM File
                            WHERE filename LIKE %s
                            ORDER BY randomid""",
                            searchString)        
        
        try:            
            files = []         
            
            while True:            
                randomid, lenfile, lenpart, filename = database.fetchone()       
                files.append(File.File(randomid, lenfile, lenpart, filename))     
                                
        except:
            pass            
            
        return files
    
    @staticmethod
    def delete(database):
        database.execute("""DELETE FROM File""")