from inc_noesis import *


MAGIC_FOURCC = 1297239878
CHUNK_FOURCC_HEAD = 1212498244
CHUNK_FOURCC_VRTX = 1448236120
CHUNK_FOURCC_POLY = 1347374169
CHUNK_FOURCC_TXPG = 1415073863
UV_TOFLOAT_CONST = 0.000244140625;


def registerNoesisTypes():
    handle = noesis.register( "Mercedes Benz Truck Racing (2000) OIF format", ".oif")

    noesis.setHandlerTypeCheck(handle, MBTRModelCheckType)
    noesis.setHandlerLoadModel(handle, MBTRModelLoadModel)
    
    return 1 

        
    
class Vector4F:
    def __init__(self, w = 0, x = 0, y = 0, z = 0):    
        self.x = x
        self.y = y
        self.z = z
        self.z = w
        
    def read(self, reader):
        self.w, self.x, self.y, self.z = noeUnpack('>4f', reader.readBytes(16))  
        
    def getXYZStorage(self):
        return (self.x, self.y, self.z) 
        
    def toBytes(self):
        data = self.getStorage()
        result = bytearray(noePack('4f', *data))
        
        return result            
    
    
class MBTRPolyVertex:
    def __init__(self):
        self.index = 0
        self.u = 0
        self.v = 0       
        
    def read(self, reader):
        self.index, self.u, self.v = noeUnpack('>3H', reader.readBytes(6)) 
        self.u *= UV_TOFLOAT_CONST
        self.v *= UV_TOFLOAT_CONST
 
    def geUVStorage(self):
        return (self.u, self.v)    
        

class MBTRPolygon:
    def __init__(self):
        self.texIndex = 0 
        self.vertexes = 0
        self.pVertexes = []
        
    def readHeader(self, reader):    
        reader.seek(2, NOESEEK_REL)
        self.vertCount = reader.readUShort()        
        reader.seek(2, NOESEEK_REL)    
        self.texIndex = reader.readUShort()
        reader.seek(4, NOESEEK_REL)    
        reader.seek(4, NOESEEK_REL)
        
    def readVertexes(self, reader):    
        for i in range(self.vertCount):
            pVertex = MBTRPolyVertex()
            pVertex.read(reader)
            self.pVertexes.append(pVertex)         
       
        reader.seek(72 - self.vertCount*6, NOESEEK_REL)       
       
    def read(self, reader):
        self.readHeader(reader)         
        self.readVertexes(reader)
        

class MBTRObject:       
    def __init__(self, reader):
        self.reader = reader
        self.size = 0
        self.vertCount = 0
        self.polyCount = 0
        self.texCount = 0
        self.vertexes = []
        self.polygons = []
        self.textures = []
        
    def readHeadChunk(self, reader):
        reader.seek(2, NOESEEK_REL)
        self.vertCount = reader.readUShort()
        self.polyCount = reader.readUShort()
        self.texCount = reader.readUShort()
        
    def readPolygons(self, reader):
        for i in range(self.polyCount):
            polygon = MBTRPolygon()
            polygon.read(reader)
        
            self.polygons.append(polygon)              
        
    def readVertexes(self, reader):
        for i in range(self.vertCount):    
            vertex = Vector4F()
            vertex.read(reader)
        
            self.vertexes.append(vertex)
        
    def readTexures(self, reader):
        for i in range(self.texCount):
            name = noeAsciiFromBytes(reader.readBytes(32))
        
            self.textures.append(name) 
        
    def readDataChunks(self, reader):          
        while (True):
            fourcc = reader.readUInt()
            size = reader.readUInt()
            
            if fourcc == CHUNK_FOURCC_HEAD:
                self.readHeadChunk(reader)   
            if fourcc == CHUNK_FOURCC_POLY:
                self.readPolygons(reader)
            if fourcc == CHUNK_FOURCC_VRTX:
                self.readVertexes(reader)   
            if fourcc == CHUNK_FOURCC_TXPG:
                self.readTexures(reader)
                
            if reader.tell() >= self.size + 8:
                break
            
    def readHeader(self, reader):   
        self.magic = reader.readUInt() 
        if self.magic != MAGIC_FOURCC: 
            return 0
               
        reader.setEndian(NOE_LITTLEENDIAN)
        self.size = reader.readUInt()
        reader.setEndian(NOE_BIGENDIAN)
        
        reader.seek(4, NOESEEK_REL)
        
        return 1        
         
    def read(self):
        if self.readHeader(self.reader):
            self.readDataChunks(self.reader)
    
    
def MBTRModelCheckType(data):     
            
    return 1                 
    
    
def MBTRModelLoadModel(data, mdlList):
    noesis.logPopup()
    noesis.logFlush()
    
    obj = MBTRObject(NoeBitStream(data))
    obj.read() 
    
    ctx = rapi.rpgCreateContext() 

    textures = []
    materials = []
    
    for texture in obj.textures:
        tex = rapi.loadExternalTex(texture + ".tga")
        if tex == None:
            tex = NoeTexture(texture, 0, 0, bytearray())
        textures.append(tex)            
        material = NoeMaterial(texture, texture)
    material.setFlags(noesis.NMATFLAG_TWOSIDED, 1)
    materials.append(material)   

    for poly in obj.polygons:
        rapi.rpgSetMaterial(obj.textures[poly.texIndex]) 
        vrtxs = []
        uvs = [] 
        for vert in poly.pVertexes:
            vrtxs.append(obj.vertexes[vert.index].getXYZStorage())
            uvs.append(vert.geUVStorage())
        
        rapi.immBegin(noesis.RPGEO_TRIANGLE)

        # TODO:triangulation, some polys for example are 11 verts in number
        for i in range(3): 
            rapi.immUV2(uvs[i])          
            rapi.immVertex3(vrtxs[i])
 
        if len(vrtxs) == 4:       
            rapi.immUV2(uvs[0])         
            rapi.immVertex3(vrtxs[0])
            rapi.immUV2(uvs[2])             
            rapi.immVertex3(vrtxs[2])
            rapi.immUV2(uvs[3])             
            rapi.immVertex3(vrtxs[3])             
 
        rapi.immEnd()    
            
 
    mdl = rapi.rpgConstructModelSlim()
    mdl.setModelMaterials(NoeModelMaterials(textures, materials))     
    mdlList.append(mdl)
 
    return 1     