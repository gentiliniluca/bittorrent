import DownloadPart

class DownloadPartService:
        
    @staticmethod
    def insertNewDownloadPart(database, downloadpartid, downloadpeerid):     
        downloadPart = DownloadPart.DownloadPart(downloadpartid, downloadpeerid)            
        downloadPart.insert(database) 
        return downloadPart
    
    @staticmethod
    def getPartCount(database):
        database.execute("""SELECT downloadpartid, count(*) as counter
                            FROM DownloadPart
                            GROUP BY downloadpartid
                            ORDER BY counter""")
        
        counts = []       
        previousCounter = -1       
        try:            
            
            while True:        
                downloadpartid, counter = database.fetchone()
                if previousCounter != counter:
                    if previousCounter != -1:
                        counts.append(parts)
                    parts = []                    
                    previousCounter = counter                
                
                parts.append(downloadpartid)                 
                
        except:
            counts.append(parts)            
        
        return counts
     
    @staticmethod
    def deleteParts(database):
        database.execute("""DELETE FROM DownloadPart""")
        
    @staticmethod
    def getRandomPart(database, randomid):  
        database.execute("""SELECT downloadpartid, count(*) as counter
                            FROM DownloadPart
                            WHERE downloadpartid NOT IN (SELECT downloadpartid 
                                                         FROM SharedPart
                                                         WHERE SharedFile_randomid = %s)
                            GROUP BY downloadpartid
                            ORDER BY counter""", randomid)
        
        partid, = database.fetchone()
        
        return partid