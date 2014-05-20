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
        downloadPeer = DownloadPeer.DownloadPeer(dowanladpeerid, ipp2p, pp2p)
        return downloadPeer
    
    @staticmethod
    def getPeerfromIp(database, ipp2p,pp2p):
        database.execute("""SELECT downloadpeerid, ipp2p, pp2p
                            FROM DownloadPeer
                            WHERE ipp2p = %s AND pp2p = %s""",
                            (ipp2p,pp2p))
        downloadpeerid, ipp2p, pp2p = database.fetchone()
        downloadPeer = DownloadPeer.DownloadPeer(downloadpeerid, ipp2p, pp2p)
        #print("* "+str(downloadPeer.downloadpeerid))
        return downloadPeer
    
    @staticmethod
    def getDownloadPeer(database, downloadpartid):
        database.execute("""SELECT downloadpeerid, ipp2p, pp2p
                            FROM DownloadPeer, DownloadPart
                            WHERE downloadpeerid = DownloadPeer_downloadpeerid AND
                                  downloadpartid = %s
                            ORDER BY RAND()
                            LIMIT 1""",
                            downloadpartid)
        
        downloadpeerid, ipp2p, pp2p = database.fetchone()
        downloadPeer = DownloadPeer.DownloadPeer(downloadpeerid, ipp2p, pp2p)
        
        return downloadPeer
     
    @staticmethod
    def deleteDownloadPeer(database):        
        database.execute("""DELETE FROM DownloadPeer""")