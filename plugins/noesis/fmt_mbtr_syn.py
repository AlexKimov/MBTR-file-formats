#


from inc_noesis import *


STR_DEFAULT_LEN = 24


def registerNoesisTypes():
    handle = noesis.register("Mercedes Benz Truck Racing resource archive", ".syn")
    noesis.setHandlerExtractArc(handle, resExtractSYNFile)
    
    return 1
    
    
class synFileData:
    def __init__(self, entry = None):
        self.entry = entry
        self.fileData = None
     
    def getUnpackedData(self):
        unpackedBuffer = None
    
        if self.fileData: # intput buffer
            cycle = 0
            currentPos = 0
            flag = 0
        
            # unpacked data - output buffer
            unpackedBuffer = bytearray(self.entry.unpackedSize)
            unpackedBufferPos = 0
        
            while True:
                if not cycle:
                    flag = self.fileData[currentPos]
                    currentPos += 1
                    cycle = 128

                if cycle & flag: # copy raw data
                    unpackedBuffer[unpackedBufferPos] = self.fileData[currentPos]
                    unpackedBufferPos += 1
                    currentPos += 1
                else:                                   
                    controlBytes = self.fileData[currentPos: currentPos + 2]
                    length = (controlBytes[0] & 0xF) + 3
                    distance = controlBytes[1] | (16 * (controlBytes[0] & 0xF0))
                    
                    currentPos += 2                    
                    pos = unpackedBufferPos - distance
                    tmp = unpackedBuffer[pos: pos + length]                    
                    unpackedBuffer[unpackedBufferPos: unpackedBufferPos + length] =  tmp
                    unpackedBufferPos += length
                    
 
                    
                if unpackedBufferPos >= self.entry.unpackedSize or \
                    currentPos >= self.entry.size:             
                    break
                    
                cycle >>= 1
           
        return unpackedBuffer
    
    def read(self, reader):
        if self.entry:
            self.entry.unpackedSize = reader.readUInt()
            self.fileData = reader.readBytes(self.entry.size - 4)
        
        
class synFileEntry():
    def __init__(self):
        self.filename = '' 
        self.offset = 0        
        self.size = 0
        self.unpackedSize = 0
        
    def read(self, filereader):        
        self.filename = noeAsciiFromBytes(filereader.readBytes(24).split(b"\0", 1)[0])

        self.offset = filereader.readUInt() 
        self.size = filereader.readUInt() 
  
  
class synFile():  
    def __init__(self, filereader):
        self.reader = filereader
        self.fileCount = 0
        self.fileEntries = []
    
    def readHeader(self):
        self.reader.seek(4, NOESEEK_ABS)
        self.fileCount = self.reader.readUInt()
        self.reader.seek(8, NOESEEK_REL)    

    def readEntries(self):
        for i in range(self.fileCount):
            entry = synFileEntry()
            entry.read(self.reader)
            
            self.fileEntries.append(entry)             
    
    def read(self):
        self.readHeader()
        self.readEntries()
                    
    def getFiles(self):
        for entry in self.fileEntries: 
            self.reader.seek(entry.offset, NOESEEK_ABS) 
           
            file = synFileData(entry)
            file.read(self.reader)
            
            yield file   
        
    
def resExtractSYNFile(fileName, fileLen, justChecking):
    with open(fileName, "rb") as f:
        if justChecking: #it's valid
            return 1       

        syn = synFile(NoeBitStream(f.read()))
        syn.read()
        
        for f in syn.getFiles():            
            rapi.exportArchiveFile(f.entry.filename, f.getUnpackedData())
            
              
    return 1