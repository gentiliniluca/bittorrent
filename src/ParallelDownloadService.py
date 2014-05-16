import ParallelDownload

class ParallelDownloadService:
    
    @staticmethod
    def insertNewParallelDownload(database, ipp2p, pp2p):
        parallelDownload = ParallelDownload.ParallelDownload(0, 0)
        
        try:
            parallelDownload.insert(database)
        except:
            parallelDownload.update(database)
        
        return parallelDownload
    
    @staticmethod
    def getParallelDownload(database):
        database.execute("""SELECT paralleldownloadid, number
                            FROM ParallelDownload
                            WHERE paralleldownloadid = 0""")
        paralleldownloadid, number = database.fetchone()
        parallelDownload = ParallelDownload.ParallelDownload(paralleldownloadid, number)
        return parallelDownload
     
    @staticmethod
    def increase(database):        
        parallelDownload = ParallelDownloadService.getParallelDownload(database)
        parallelDownload.number = int(parallelDownload.number) + 1
        parallelDownload.update(database)
    
    @staticmethod
    def decrease(database):        
        parallelDownload = ParallelDownloadService.getParallelDownload(database)
        parallelDownload.number = int(parallelDownload.number) - 1
        parallelDownload.update(database)
        
    @staticmethod
    def delete(database):
        database.execute("""DELETE FROM ParallelDownload""")