import SharedFile
import string
import random

class SharedFileService:
    
    @staticmethod
    def insertNewSharedFile(database, filename, lenfile, lenpart):
        
        #generazione randomid
        randomid = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        
        #check di unicita' randomid
        database.execute("""SELECT randomid
                            FROM SharedFile
                            WHERE randomid = %s""",
                            (randomid))
        while database.fetchone() != None:
            randomid = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            database.execute("""SELECT randomid
                                FROM SharedFile
                                WHERE randomid = %s""",
                                (randomid))
        
        #inserimento nuovo sharedFile
        sharedFile = SharedFile.SharedFile(randomid, filename, lenfile, lenpart)
        sharedFile.insert(database)
        
        return sharedFile
    
    @staticmethod
    def getSharedFile(database, filename):
        
        database.execute("""SELECT randomid, filename, lenfile, lenpart
                            FROM SharedFile
                            WHERE filename = %s""",
                            (filename))
        
        randomid, filename, lenfile, lenpart = database.fetchone()
        
        sharedFile = SharedFile.SharedFile(randomid, filename, lenfile, lenpart)
        
        return sharedFile
    
    @staticmethod
    def getSharedFileRandomId(database, randomid):
        
        database.execute("""SELECT randomid, filename, lenfile, lenpart
                            FROM SharedFile
                            WHERE randomid = %s""",
                            (randomid))
        
        randomid, filename, lenfile, lenpart = database.fetchone()
        
        sharedFile = SharedFile.SharedFile(randomid, filename, lenfile, lenpart)
        
        return sharedFile
    
#    @staticmethod
#    def getSharedFiles(database, searchString):
#        
#        searchString = "%" + searchString.upper() + "%"
#        
#        database.execute("""SELECT idsharedfile, filemd5, filename
#                            FROM sharedfile
#                            WHERE filename LIKE %s""",
#                            searchString)
#        
#        sharedFiles = []
#        
#        try:
#            while True:
#                idsharedfile, filemd5, filename = database.fetchone()
#                sharedFile = SharedFile.SharedFile(idsharedfile, filemd5, filename)
#                sharedFiles.append(sharedFile)
#        except:
#            pass
#        
#        return sharedFiles
    
    @staticmethod
    def delete(database):
        database.execute("""DELETE FROM SharedFile""")