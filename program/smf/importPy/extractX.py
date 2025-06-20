import traceback
from program.errorLogClass import ErrorLogObj


class XObject():
    def __init__(self, filePath, decryptFile):
        self.errObj = ErrorLogObj()
        self.filePath = filePath
        self.decryptFile = decryptFile
        self.header = "xof 0303txt 0032\n\n"
        self.w = None
        self.xFileObj = {}
        self.error = ""

    def makeXFile(self):
        try:
            self.xFileObj = {}
            self.makeStructure()
            self.w = open(self.filePath, "w", encoding="utf-8")
            self.w.write(self.header + "\n\n")
            self.writeFrameAndMesh(self.xFileObj)
            self.w.close()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        self.errObj.write(self.error)

    def makeStructure(self):
        frameObjList = []
        for trans in self.decryptFile.frameList:
            frameObj = {"name": trans["name"], "matrix": trans["matrix"], "mesh":{}, "child":[]}

            if trans["parentFrameNo"] != -1:
                frameObjList[trans["parentFrameNo"]]["child"].append(frameObj)
            else:
                self.xFileObj = frameObj

            if trans["meshNo"] != -1:
                frameObj["mesh"] = self.decryptFile.meshList[trans["meshNo"]]
            frameObjList.append(frameObj)

    def writeFrameAndMesh(self, frameObj, indent=""):
        self.w.write(indent)
        self.w.write("Frame {0} {{\n".format(frameObj["name"]))

        self.w.write((indent + " FrameTransformMatrix {\n"))
        self.w.write((indent + "  "))
        self.w.write(indent)
        self.w.write(",".join(map(str, frameObj["matrix"][0])) + ",")
        self.w.write(",".join(map(str, frameObj["matrix"][1])) + ",")
        self.w.write(",".join(map(str, frameObj["matrix"][2])) + ",")
        self.w.write(",".join(map(str, frameObj["matrix"][3])) + ";;\n")
        self.w.write((indent + " }\n\n"))

        if len(frameObj["mesh"]) > 0:
            meshObj = frameObj["mesh"]
            # Mesh Start
            self.w.write((indent + " Mesh {0} {{\n".format(meshObj["name"].replace(" ", "_"))))
            self.w.write((indent + "  {0};\n".format(len(meshObj["coordList"]))))
            coordCheckList = []
            originCoordList = []
            originCoordCnt = 0
            for idx, coord in enumerate(meshObj["coordList"]):
                self.w.write((indent + "  {0};{1};{2};".format(coord[0], coord[1], coord[2])))
                if idx == len(meshObj["coordList"]) - 1:
                    self.w.write(";\n")
                else:
                    self.w.write(",\n")
                if coord not in coordCheckList:
                    coordCheckList.append(coord)
                    originCoordList.append(idx)
                    originCoordCnt += 1
                else:
                    originCoordList.append(coordCheckList.index(coord))

            self.w.write((indent + "  {0};\n".format(len(meshObj["coordIndexList"] ) // 3)))
            for idx, coordIdx in enumerate(meshObj["coordIndexList"]):
                if idx % 3 == 0:
                    self.w.write((indent + "  3;"))
                self.w.write("{0}".format(coordIdx))

                if idx % 3 == 2:
                    if idx == len(meshObj["coordIndexList"]) - 1:
                        self.w.write(";;\n\n")
                    else:
                        self.w.write(";,\n")
                else:
                    self.w.write(",")

            # normalList Start
            self.w.write((indent + "  MeshNormals {\n"))
            self.w.write((indent + "   {0};\n".format(len(meshObj["normalList"]))))
            for idx, normal in enumerate(meshObj["normalList"]):
                self.w.write((indent + "   {0};{1};{2};".format(normal[0], normal[1], normal[2])))
                if idx == len(meshObj["normalList"]) - 1:
                    self.w.write(";\n")
                else:
                    self.w.write(",\n")

            self.w.write((indent + "   {0};\n".format(len(meshObj["coordIndexList"] ) // 3)))
            for idx, coordIdx in enumerate(meshObj["coordIndexList"]):
                if idx % 3 == 0:
                    self.w.write((indent + "   3;"))
                self.w.write("{0}".format(coordIdx))

                if idx % 3 == 2:
                    if idx == len(meshObj["coordIndexList"]) - 1:
                        self.w.write(";;\n\n")
                    else:
                        self.w.write(";,\n")
                else:
                    self.w.write(",")
            self.w.write((indent + "  }\n\n"))
            # normalList End

            # colorInfoList Start
            self.w.write((indent + "  MeshVertexColors {\n"))
            self.w.write((indent + "   {0};\n".format(len(meshObj["colorInfoList"]))))
            for idx, colorInfo in enumerate(meshObj["colorInfoList"]):
                self.w.write((indent + "   {0};".format(idx)))
                self.w.write("{0};".format(colorInfo[2] / 255.0))
                self.w.write("{0};".format(colorInfo[1] / 255.0))
                self.w.write("{0};".format(colorInfo[0] / 255.0))
                self.w.write("{0};".format(colorInfo[3] / 255.0))
                if idx == len(meshObj["coordList"]) - 1:
                    self.w.write(";\n")
                else:
                    self.w.write(",\n")
            self.w.write((indent + "  }\n\n"))
            # colorInfoList End

            # uvList Start
            self.w.write((indent + "  MeshTextureCoords {\n"))
            self.w.write((indent + "   {0};\n".format(len(meshObj["uvList"]))))
            for idx, uv in enumerate(meshObj["uvList"]):
                self.w.write((indent + "   {0};{1};".format(uv[0], uv[1])))
                if idx == len(meshObj["coordList"]) - 1:
                    self.w.write(";\n")
                else:
                    self.w.write(",\n")
            self.w.write((indent + "  }\n\n"))
            # uvList End

            # mtrl Start
            self.w.write((indent + "  MeshMaterialList {\n"))
            self.w.write((indent + "   {0};\n".format(len(meshObj["mtrlList"]))))
            allPolyCount = 0
            for mtrl in meshObj["mtrlList"]:
                allPolyCount += mtrl["polyCount"]
            self.w.write((indent + "   {0};\n".format(allPolyCount)))

            for midx, mtrl in enumerate(meshObj["mtrlList"]):
                for i in range(mtrl["polyCount"]):
                    self.w.write((indent + "   {0}".format(midx)))
                    if midx == len(meshObj["mtrlList"]) - 1 and i == mtrl["polyCount"] - 1:
                        self.w.write(";\n\n")
                    else:
                        self.w.write(",\n")
            
            for mtrl in meshObj["mtrlList"]:
                # Material Start
                self.w.write((indent + "   Material {\n"))
                diff = [0.0, 0.0, 0.0, 0.0]
                if "diff" in mtrl:
                    diff = mtrl["diff"]
                self.w.write((indent + "    {0};{1};{2};{3};;\n".format(diff[0], diff[1], diff[2], diff[3])))
                self.w.write((indent + "    51.200001;\n"))
                spec = [0.0, 0.0, 0.0]
                if "spec" in mtrl:
                    spec = mtrl["spec"]
                self.w.write((indent + "    {0};{1};{2};;\n".format(spec[0], spec[1], spec[2])))
                emis = [0.0, 0.0, 0.0]
                if "emis" in mtrl:
                    emis = mtrl["emis"]
                self.w.write((indent + "    {0};{1};{2};;\n".format(emis[0], emis[1], emis[2])))
                if "texc" in mtrl:
                    self.w.write((indent + "    TextureFilename {\n"))
                    self.w.write((indent + "     \"{0}\";\n".format(mtrl["texc"])))
                    self.w.write((indent + "    }\n"))
                self.w.write((indent + "   }\n"))
                # Material End
            self.w.write((indent + "  }\n"))
            # mtrl End

            if len(meshObj["boneList"]) > 0:
                self.writeBone(meshObj["boneList"], meshObj["boneWeightList"], indent)

            self.w.write((indent + " }\n\n"))
            # Mesh End

            

        if len(frameObj["child"]) > 0:
            for child in frameObj["child"]:
                self.writeFrameAndMesh(child, indent + " ")

        self.w.write((indent + "}\n"))

    def writeBone(self, boneList, boneWeightList, indent):
        skinWeightsList = []
        for boneInfo in boneList:
            skinWeightsInfo = {}
            frameIdx = boneInfo["frameNo"]
            frameName = self.decryptFile.frameList[frameIdx]["name"]
            skinWeightsInfo["name"] = frameName
            skinWeightsInfo["coordIndexList"] = []
            skinWeightsInfo["coordWeightList"] = []
            skinWeightsInfo["matrixOffset"] = boneInfo["matrixOffset"]
            skinWeightsList.append(skinWeightsInfo)
        
        for coordIndex, boneWeightInfo in enumerate(boneWeightList):
            weight = boneWeightInfo[0]
            boneIdxList = boneWeightInfo[1]
            skinWeightsList[boneIdxList[0]]["coordIndexList"].append(coordIndex)
            skinWeightsList[boneIdxList[0]]["coordWeightList"].append(weight)
            skinWeightsList[boneIdxList[1]]["coordIndexList"].append(coordIndex)
            skinWeightsList[boneIdxList[1]]["coordWeightList"].append(1.0 - weight)
            skinWeightsList[boneIdxList[2]]["coordIndexList"].append(coordIndex)
            skinWeightsList[boneIdxList[2]]["coordWeightList"].append(0)
            skinWeightsList[boneIdxList[3]]["coordIndexList"].append(coordIndex)
            skinWeightsList[boneIdxList[3]]["coordWeightList"].append(0)

        self.w.write((indent + "  XSkinMeshHeader {\n"))
        self.w.write((indent + "   4;\n"))
        self.w.write((indent + "   4;\n"))
        self.w.write((indent + "   {0};\n".format(len(boneList))))
        self.w.write((indent + "  }\n"))

        for i in range(len(skinWeightsList)):
            self.w.write((indent + "  SkinWeights {\n"))
            self.w.write((indent + "   \"{0}\";\n".format(skinWeightsList[i]["name"])))
            count = len(skinWeightsList[i]["coordIndexList"])
            self.w.write((indent + "   {0};\n".format(count)))
            for coordIndex in skinWeightsList[i]["coordIndexList"]:
                self.w.write((indent + "   {0}".format(coordIndex)))
                if coordIndex == count - 1:
                    self.w.write(";\n")
                else:
                    self.w.write(",\n")
            for coordIndex in skinWeightsList[i]["coordWeightList"]:
                self.w.write((indent + "   {0}".format(coordIndex)))
                if coordIndex == count - 1:
                    self.w.write(";\n")
                else:
                    self.w.write(",\n")
            self.w.write((indent + "   "))
            self.w.write(",".join(map(str, skinWeightsList[i]["matrixOffset"][0])) + ",")
            self.w.write(",".join(map(str, skinWeightsList[i]["matrixOffset"][1])) + ",")
            self.w.write(",".join(map(str, skinWeightsList[i]["matrixOffset"][2])) + ",")
            self.w.write(",".join(map(str, skinWeightsList[i]["matrixOffset"][3])) + ";;\n")

            self.w.write((indent + "  }\n"))