import traceback
from xml.dom import minidom
import xml.etree.ElementTree as ET
from program.errorLogClass import ErrorLogObj


class X3dObject():
    def __init__(self, filePath, decryptFile):
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.decryptFile = decryptFile
        self.xmlFile = None
        self.root = None
        self.elementList = []
        self.meshElementList = []
        self.error = ""

    def makeX3d(self):
        try:
            self.elementList = []
            self.meshElementList = []
            self.xmlFile = ET.Element("X3D", attrib={
                "version":"3.0",
                "profile":"Immersive",
                "xmlns:xsd":"http://www.w3.org/2001/XMLSchema-instance",
                "xsd:noNamespaceSchemaLocation":"http://www.web3d.org/specifications/x3d-3.0.xsd"
            })
            self.root = ET.SubElement(self.xmlFile, "Scene")
            self.makeTransform()
            self.makeMeshAndMtrl()

            doc = minidom.parseString(ET.tostring(self.xmlFile, "utf-8"))
            with open(self.filePath, "w", encoding="utf-8") as f:
                doc.writexml(f, encoding="utf-8", newl='\n', indent='', addindent='  ')
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        self.errObj.write(self.error)

    def makeTransform(self):
        for trans in self.decryptFile.frameList:
            addElem = None
            if trans["parentFrameNo"] == -1:
                addElem = ET.SubElement(self.root, "Transform")
            else:
                parentFrameNo = trans["parentFrameNo"]
                addElem = ET.SubElement(self.elementList[parentFrameNo], "Transform")
            addElem.attrib["DEF"] = trans["name"]
            addElem.attrib["translation"] = self.decryptFile.matrixToPos(trans["matrix"])
            addElem.attrib["scale"] = "1.0 1.0 1.0"
            addElem.attrib["rotation"] = self.decryptFile.matrixToRot(trans["matrix"])
            if trans["meshNo"] != -1:
                meshElem = ET.SubElement(addElem, "Group")
                meshElem.attrib["DEF"] = "Mesh_No.{0}".format(trans["meshNo"])
                self.meshElementList.append(meshElem)
            self.elementList.append(addElem)

    def chunks(self, list, num):
        for i in range(0, len(list), num):
            yield list[i:i+num]

    def makeMeshAndMtrl(self):
        for midx, mesh in enumerate(self.decryptFile.meshList):
            for mtrl in mesh["mtrlList"]:
                shapeElem = ET.SubElement(self.meshElementList[midx], "Shape")

                appearanceElem = ET.SubElement(shapeElem, "Appearance")
                meterialElem = ET.SubElement(appearanceElem, "Material")
                if "texc" in mtrl or "texl" in mtrl:
                    imageTextureElem = ET.SubElement(appearanceElem, "ImageTexture")
                    if "texc" in mtrl:
                        imageTextureElem.attrib["url"] = mtrl["texc"]
                    else:
                        imageTextureElem.attrib["url"] = mtrl["texl"]

                if "diff" in mtrl:
                    meterialElem.attrib["diffuseColor"] = "{0} {1} {2}".format(mtrl["diff"][0], mtrl["diff"][1], mtrl["diff"][2])
                if "emis" in mtrl:
                    meterialElem.attrib["emissiveColor"] = "{0} {1} {2}".format(mtrl["emis"][0], mtrl["emis"][1], mtrl["emis"][2])
                if "spec" in mtrl:
                    meterialElem.attrib["specularColor"] = "{0} {1} {2}".format(mtrl["spec"][0], mtrl["spec"][1], mtrl["spec"][2])

                indexedFaceSetElem = ET.SubElement(shapeElem, "IndexedFaceSet")
                indexedFaceSetElem.attrib["solid"] = "false"
                polyStartIndex = mtrl["polyIndexStart"] * 3
                polyEndIndex = polyStartIndex + mtrl["polyCount"] * 3
                splitCoordIndexList = mesh["coordIndexList"][polyStartIndex:polyEndIndex]
                chunkCoordIndexList = list(self.chunks(splitCoordIndexList, 3))
                coordIndexValue = ""
                for chunkCoordIndexInfo in chunkCoordIndexList:
                    for coordIndex in reversed(chunkCoordIndexInfo):
                        coordIndexValue += "{0} ".format(coordIndex - mtrl["coordIndexStart"])
                    coordIndexValue += "-1 "
                indexedFaceSetElem.attrib["coordIndex"] = coordIndexValue

                coordinateElem = ET.SubElement(indexedFaceSetElem, "Coordinate")
                coordStartIndex = mtrl["coordIndexStart"]
                coordEndIndex = coordStartIndex + mtrl["coordCount"]
                splitCoordList = mesh["coordList"][coordStartIndex:coordEndIndex]
                coordValue = ""
                for coord in splitCoordList:
                    coordValue += "{0} {1} {2} ".format(-coord[0], coord[1], coord[2])
                coordinateElem.attrib["point"] = coordValue

                colorRGBAElem = ET.SubElement(indexedFaceSetElem, "ColorRGBA")
                colorRGBAStartIndex = mtrl["coordIndexStart"]
                colorRGBAEndIndex = colorRGBAStartIndex + mtrl["coordCount"]
                splitColorInfoList = mesh["colorInfoList"][colorRGBAStartIndex:colorRGBAEndIndex]
                colorValue = ""
                for colorInfo in splitColorInfoList:
                    colorValue += "{0} ".format(colorInfo[2] / 255.0)
                    colorValue += "{0} ".format(colorInfo[1] / 255.0)
                    colorValue += "{0} ".format(colorInfo[0] / 255.0)
                    colorValue += "{0} ".format(colorInfo[3] / 255.0)
                colorRGBAElem.attrib["color"] = colorValue

                textureCoordinateElem = ET.SubElement(indexedFaceSetElem, "TextureCoordinate")
                texCoordStartIndex = mtrl["coordIndexStart"]
                texCoordEndIndex = texCoordStartIndex + mtrl["coordCount"]
                splitTexCoordList = mesh["uvList"][texCoordStartIndex:texCoordEndIndex]
                texCoordValue = ""
                for uv in splitTexCoordList:
                    texCoordValue += "{0} {1} ".format(uv[0], -uv[1])
                textureCoordinateElem.attrib["point"] = texCoordValue
