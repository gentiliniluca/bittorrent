class DownloadPart:
    def __init__(self, downloadpartid, downloadpeerid):
        self.downloadpartid = downloadpartid
        self.downloadpeerid = downloadpeerid    
    
    def insert(self, database):        
            database.execute("""INSERT INTO DownloadPart
                                (downloadpartid, DownloadPeer_downloadpeerid)
                                VALUES (%s, %s)""",
                                (self.downloadpartid, self.downloadpeerid))