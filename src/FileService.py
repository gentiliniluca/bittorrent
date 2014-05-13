import File
import PartService
#import sys

class FileService:
        
    @staticmethod
    def insertNewFile(database, sessionid, randomid, lenfile, lenpart, filename):
        file = File.File(randomid, lenfile, lenpart, filename)            
        file.insert(database) 
        
        npart = lenfile // lenpart + 1
        
        i = 0
        while i < npart:
            partid = i
            PartService.PartService.insertNewPart(sessionid, randomid, partid)
    
    @staticmethod
    def getFile(database, randomid):
        database.execute("""SELECT randomid, lenfile, lenpart, filename
                            FROM File
                            WHERE randomid = %s""",
                            randomid)
        
        randomid, lenfile, lenpart, filename = database.fetchone()
        
        file = File.File(randomid, lenfile, lenpart, filename)
        
        return file  
    
#    @staticmethod
#    def getFiles(database, searchString):
#        searchString = "%" + searchString + "%"
#        database.execute("""SELECT filename, filemd5, sessionid, ipp2p, pp2p
#                            FROM file, peer, peer_has_file
#                            WHERE file_filemd5 = filemd5 AND
#                                 peer_sessionid = sessionid AND
#                                  filename LIKE %s
#                            ORDER BY filemd5, sessionid""",
#                            searchString)
#        
#        #print database._last_executed
#        try:
#            i = -1
#            files = []
#            #peers = []
#            previous_filemd5 = ""
#           while True:
#            
#                filename, filemd5, sessionid, ipp2p, pp2p = database.fetchone()
#                #print filename, filemd5, sessionid, ipp2p, pp2p
#                
#                if filemd5 != previous_filemd5:
#                    files.append(File.File(filemd5, filename))
#                    #print files[i].filemd5
#                    #j = 0
#                    #files[i].setPeers([])
#                    previous_filemd5 = filemd5
#                    i = i + 1
#                
#                #print len(files[i].peers)
#                files[i].peers.append(Peer.Peer(sessionid, ipp2p, pp2p))
#                #print len(files[i].peers)
#                #print files[i].peers[j].sessionid
#                #j = j + 1
#        
#        except:
#            pass
#            #print sys.exc_info()
#            
#        return files