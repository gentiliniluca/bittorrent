import DownloadPeer

class DownloadPeerService:
    
    @staticmethod
    def insertNewDownloadPeer(database, ipp2p, pp2p):
        downloadPeer = DownloadPeer.DownloadPeer(None, ipp2p, pp2p)
        downloadPeer.insert(database)
        return downloadPeer
    
    @staticmethod
    def getPeer(database, downloadpeerid):
        database.execute("""SELECT downloadpeerid, ipp2p, pp2p
                            FROM DownloadPeer
                            WHERE downloadpeerid = %s""",
                            downloadpeerid)
        downloadpeerid, ipp2p, pp2p = database.fetchone()
        downloadPeer = DownalodPeer.DownloadPeer(dowanladpeerid, ipp2p, pp2p)
        return downloadPeer
     
    @staticmethod
    def deleteDownloadPeer(self, database):        
        database.execute("""DELETE FROM DownloadPeer""")