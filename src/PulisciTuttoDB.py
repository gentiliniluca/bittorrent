import Connessione
import SharedPartService
import SharedFileService
import SearchResultService
import FileService
import DownloadPeerService
import DownloadPartService
import SharedPartService
import PeerService
import PartService


conn_db=Connessione.Connessione()
try:
    
    
    PartService.PartService.delete(conn_db.crea_cursore())
    DownloadPartService.DownloadPartService.deleteParts(conn_db.crea_cursore())
    SearchResultService.SearchResultService.delete(conn_db.crea_cursore())
    SharedPartService.SharedPartService.delete(conn_db.crea_cursore())
    SharedFileService.SharedFileService.delete(conn_db.crea_cursore())
    PeerService.PeerService.delete(conn_db.crea_cursore())
    FileService.FileService.delete(conn_db.crea_cursore())
    DownloadPeerService.DownloadPeerService.deleteDownloadPeer(conn_db.crea_cursore())
    
    
    
finally:
    conn_db.esegui_commit()
    conn_db.chiudi_connessione
