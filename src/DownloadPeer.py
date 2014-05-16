class DownloadPeer:
    def __init__(self, downloadpeerid, ipp2p, pp2p):
        self.downloadpeerid = downloadpeerid
        self.ipp2p = ipp2p
        self.pp2p = pp2p
    
    def insert(self, database):            
            
            database.execute("""INSERT INTO DownloadPeer
                                (ipp2p, pp2p)
                                VALUES
                                (%s, %s)""",
                                (self.ipp2p, self.pp2p))