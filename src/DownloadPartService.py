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
        database.execute("""DELETE FROM Part""")  