import Connessione
import SharedFileService
import SharedPartService
import os

file_path = "/home/davide/Immagini/DeathNote3.jpg"
file_path2 = "/home/davide/Immagini/DeathNote30.jpg"

partid = 0

conn_db = Connessione.Connessione()

openedFile = open(file_path, "rb")
data = openedFile.read(1024*1024*1024)
length = os.stat(file_path).st_size

sharedFile = SharedFileService.SharedFileService.insertNewSharedFile(conn_db.crea_cursore(), "AVVOLTOIO.JPG", length, 256)
SharedPartService.SharedPartService.insertNewSharedPart(conn_db.crea_cursore(), partid, data, sharedFile.randomid)

openedFile.close()

conn_db.esegui_commit()
conn_db.chiudi_connessione()

conn_db = Connessione.Connessione()

openedFile = open(file_path2, "wb")
sharedPart = SharedPartService.SharedPartService.getSharedPart(conn_db.crea_cursore(), sharedFile.randomid, partid)

openedFile.write(sharedPart.data)
openedFile.close()

conn_db.esegui_commit()
conn_db.chiudi_connessione()
