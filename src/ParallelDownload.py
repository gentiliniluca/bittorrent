class PrallelDownload:
    
    def __init__(self, paralleldownloadid, number):
        self.paralleldownloadid = paralleldownloadid
        self.number = number    
    
    def insert(self, database):        
            database.execute("""INSERT INTO ParallelDownload
                                (paralleldownloadid, number)
                                VALUES (%s, %s)""",
                                (self.paralleldownloadid, self.number))
    
    def update(self, database):
        database.execute("""UPDATE ParallelDownload
                            SET number = %s
                            WHERE paralleldownloadid = %s""",
                            (self.number, self.paralleldownloadid))