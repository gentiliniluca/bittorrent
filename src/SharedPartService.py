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
                            randomid, partid)
        
        partid, data, SharedFile_randomid = database.fetchone()
        
        sharedPart = SharedPart.SharedPart(partid, data, SharedFile_randomid)
        
        return sharedPart