import SharedPart

class SharedPartService:
        
    @staticmethod
    def insertNewSharedPart(database, partid, data, SharedFile_randomid):       
        try:
            sharedPart = SharedPart.SharedPart(partid, data, SharedFile_randomid)            
            sharedPart.insert(database)
        except:
            pass
    
    @staticmethod
    def getSharedPart(database, randomid, partid):
        database.execute("""SELECT partid, data, SharedFile_randomid 
                            FROM SharedPart
                            WHERE SharedFile_randomid = %s AND partid = %s""",
                            (randomid, partid))
        
        partid, data, SharedFile_randomid = database.fetchone()
        
        sharedPart = SharedPart.SharedPart(partid, data, SharedFile_randomid)
        
        return sharedPart
    
    @staticmethod
    def getSharedParts(database, randomid):
        database.execute("""SELECT partid, data, SharedFile_randomid
                            FROM SharedPart
                            WHERE SharedFile_randomid = %s
                            ORDER BY partid""",
                            randomid)        
        
        sharedParts = []
        try:
            while True:            
                partid, data, randomid = database.fetchone()       
                sharedParts.append(SharedPart.SharedPart(partid, data, randomid))     
                                
        except:
            pass            
            
        return sharedParts
    
    @staticmethod
    def delete(database):
        database.execute("""DELETE FROM SharedPart""")
