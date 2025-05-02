import os
import shutil
import math
import codecs
import traceback
from PIL import Image
from fbx import FbxManager
from fbx import FbxScene
from fbx import FbxExporter
from fbx import FbxSkeleton
from fbx import FbxMesh
from fbx import FbxLayerElementVertexColor
from fbx import FbxColor
from fbx import FbxLayerElementNormal
from fbx import FbxSkin
from fbx import FbxCluster
from fbx import FbxAMatrix
from fbx import FbxSurfacePhong
from fbx import FbxFileTexture
from fbx import FbxTexture
from fbx import FbxNode
from fbx import FbxNull
from fbx import FbxQuaternion
from fbx import FbxDouble3
from fbx import FbxVector2
from fbx import FbxVector4
from fbx import FbxLayerElement

class FbxObject():
    def __init__(self, filePath, decryptFile):
        self.filePath = filePath
        self.fileName = os.path.splitext(os.path.basename(filePath))[0]
        self.decryptFile = decryptFile
        self.frameObj = None
        self.manager = None
        self.scene = None
        self.rootNode = None
        self.skeletonNodeList = []
        self.meshNodeList = []
        self.currentMaterialCount = 0
        self.imageFileList = []
        self.exporter = None

    def makeFbxFile(self):
        try:
            self.manager = FbxManager.Create()
            self.scene = FbxScene.Create(self.manager, "MyScene")
            self.rootNode = self.scene.GetRootNode()

            self.makeStructure()
            self.makeNode(self.frameObj, self.rootNode)
            self.makeBone()
            self.exportFbx()
            self.manager.Destroy()
            return True
        except Exception:
            self.error = traceback.format_exc()
            return False

    def printError(self):
        w = codecs.open("error.log", "w", "utf-8", "strict")
        w.write(self.error)
        w.close()

    def makeStructure(self):
        frameObjList = []
        for trans in self.decryptFile.frameList:
            frameObj = {"name": trans["name"], 
                        "matrix": trans["matrix"], 
                        "parentFrameNo": trans["parentFrameNo"], 
                        "bone": False, 
                        "rootBone": False, 
                        "mesh": {}, 
                        "meshNo": trans["meshNo"],
                        "child": []}

            if trans["parentFrameNo"] != -1:
                frameObjList[trans["parentFrameNo"]]["child"].append(frameObj)
            else:
                self.frameObj = frameObj

            if trans["meshNo"] != -1:
                frameObj["mesh"] = self.decryptFile.meshList[trans["meshNo"]]
            frameObjList.append(frameObj)
        
        for mesh in self.decryptFile.meshList:
            if len(mesh["boneList"]) > 0:
                for bidx, bone in enumerate(mesh["boneList"]):
                    frameNo = bone["frameNo"]
                    frameObjList[frameNo]["bone"] = True
                    if bidx == 0:
                        frameObjList[frameNo]["rootBone"] = True

    def makeNode(self, frameObj, parentNode):
        newNode = FbxNode.Create(self.manager, frameObj["name"])
        if frameObj["bone"]:
            newNodeAttr = FbxSkeleton.Create(self.manager, frameObj["name"])
            if frameObj["rootBone"]:
                self.skeletonRootNode = newNode
                newNodeAttr.SetSkeletonType(FbxSkeleton.EType.eRoot)
            else:
                newNodeAttr.SetSkeletonType(FbxSkeleton.EType.eLimbNode)
            self.skeletonNodeList.append(newNode)
        elif len(frameObj["mesh"]) > 0:
            newNodeAttr = self.makeMesh(newNode, frameObj["meshNo"], frameObj["mesh"])
            self.meshNodeList.append(newNode)
        else:
            newNodeAttr = FbxNull.Create(self.manager, frameObj["name"])
        newNode.SetNodeAttribute(newNodeAttr)

        translation = self.decryptFile.matrixToPos(frameObj["matrix"]).split()
        newNode.LclTranslation.Set(FbxDouble3(float(translation[0]), float(translation[1]), float(translation[2])))
        q = self.decryptFile.matrixToRot(frameObj["matrix"]).split()
        quaternion = FbxQuaternion(float(q[0]), float(q[1]), float(q[2]), float(q[3]))
        euler = quaternion.DecomposeSphericalXYZ()
        newNode.LclRotation.Set(FbxDouble3(math.degrees(euler[0]), math.degrees(euler[1]), math.degrees(euler[2])))
        parentNode.AddChild(newNode)

        if len(frameObj["child"]) > 0:
            for child in frameObj["child"]:
                self.makeNode(child, newNode)

    def makeMesh(self, meshNode, meshNo, meshObj):
        mesh = FbxMesh.Create(self.manager, "mesh_{0}".format(meshNo))
        # 頂点を設定（鏡反転対応）
        mesh.InitControlPoints(len(meshObj["coordList"]))
        for i, coord in enumerate(meshObj["coordList"]):
            mesh.SetControlPointAt(FbxVector4(-coord[0], coord[1], coord[2]), i)

        # 鏡反転対応
        polygonInfoList = []
        polygonInfo = []
        for i, coordIndex in enumerate(meshObj["coordIndexList"]):
            polygonInfo.append(coordIndex)
            if i % 3 == 2:
                polygonInfoList.append(polygonInfo)
                polygonInfo = []

        # 三角形ポリゴンを定義
        for polygonInfo in polygonInfoList:
            for i, coordIndex in enumerate(reversed(polygonInfo)):
                if i % 3 == 0:
                    mesh.BeginPolygon()
                mesh.AddPolygon(coordIndex)
                if i % 3 == 2:
                    mesh.EndPolygon()

        layer = mesh.GetLayer(0)
        if not layer:
            mesh.CreateLayer()
            layer = mesh.GetLayer(0)

        # 頂点カラー
        colorElement = FbxLayerElementVertexColor.Create(mesh, "")
        colorElement.SetMappingMode(FbxLayerElement.EMappingMode.eByControlPoint)
        colorElement.SetReferenceMode(FbxLayerElement.EReferenceMode.eDirect)
        colorArray = colorElement.GetDirectArray()
        for colorInfo in meshObj["colorInfoList"]:
            colorArray.Add(FbxColor(colorInfo[2] / 255.0, colorInfo[1] / 255.0, colorInfo[0] / 255.0, colorInfo[3] / 255.0))
        layer.SetVertexColors(colorElement)

        # 法線（鏡反転対応）
        normalElement = FbxLayerElementNormal.Create(mesh, "{0}_normals".format(self.fileName))
        normalElement.SetMappingMode(FbxLayerElement.EMappingMode.eByControlPoint)
        normalElement.SetReferenceMode(FbxLayerElement.EReferenceMode.eDirect)
        normalArray = normalElement.GetDirectArray()
        for normal in meshObj["normalList"]:
            normalArray.Add(FbxVector4(-normal[0], normal[1], normal[2]))
        layer.SetNormals(normalElement)

        # UV
        uvElement = mesh.CreateElementUV("mesh_{0}".format(meshNo))
        uvElement.SetMappingMode(FbxLayerElement.EMappingMode.eByControlPoint)
        uvElement.SetReferenceMode(FbxLayerElement.EReferenceMode.eDirect)
        uvArray = uvElement.GetDirectArray()
        for uv in meshObj["uvList"]:
            uvArray.Add(FbxVector2(uv[0], 1.0 - uv[1]))

        # マテリアル
        materialElement = mesh.CreateElementMaterial()
        materialElement.SetMappingMode(FbxLayerElement.EMappingMode.eByPolygon)
        materialElement.SetReferenceMode(FbxLayerElement.EReferenceMode.eIndex)

        materialIndexList = []
        for mIdx, mtrl in enumerate(meshObj["mtrlList"]):
            material = FbxSurfacePhong.Create(self.manager, "{0}_material_mesh_{1}_{2}".format(self.fileName, meshNo, mIdx))
            if "diff" in mtrl:
                material.DiffuseFactor.Set(1)
                material.Diffuse.Set(FbxDouble3(mtrl["diff"][0], mtrl["diff"][1], mtrl["diff"][2]))
            if "emis" in mtrl:
                material.SpecularFactor.Set(1)
                material.Emissive.Set(FbxDouble3(mtrl["emis"][0], mtrl["emis"][1], mtrl["emis"][2]))
            if "spec" in mtrl:
                material.SpecularFactor.Set(1)
                material.Specular.Set(FbxDouble3(mtrl["spec"][0], mtrl["spec"][1], mtrl["spec"][2]))
            material.TransparencyFactor.Set(0.0)

            # 画像のテクスチャ
            if "texc" in mtrl:
                file = mtrl["texc"]
                # tgaの場合、pngに変換
                if os.path.splitext(file)[1].lower() == ".tga":
                    file = os.path.splitext(file)[0] + ".png"
                dirname = os.path.dirname(self.filePath)
                self.imageFileList.append(os.path.join(dirname, file))
                texture = FbxFileTexture.Create(self.manager, "")
                texture.SetFileName(file)
                texture.SetTextureUse(FbxTexture.ETextureUse.eStandard)
                texture.SetMappingType(FbxTexture.EMappingType.eUV)
                material.Diffuse.ConnectSrcObject(texture)
            meshNode.AddMaterial(material)
            for i in range(mtrl["polyCount"]):
                materialIndexList.append(self.currentMaterialCount + mIdx)
        self.currentMaterialCount += len(meshObj["mtrlList"])

        mtrlIndexArray = materialElement.GetIndexArray()
        for materialIndex in materialIndexList:
            mtrlIndexArray.Add(materialIndex)

        return mesh

    def makeBone(self):
        for meshIdx in range(len(self.decryptFile.meshList)):
            meshObj = self.decryptFile.meshList[meshIdx]
            if len(meshObj["boneList"]) > 0:
                meshNode = self.meshNodeList[meshIdx]
                mesh = meshNode.GetNodeAttribute()

                skin = FbxSkin.Create(self.manager, "")
                mesh.AddDeformer(skin)

                clusterList = []
                for boneIdx in range(len(meshObj["boneList"])):
                    cluster = FbxCluster.Create(self.manager, "")
                    cluster.SetLink(self.skeletonNodeList[boneIdx])
                    cluster.SetLinkMode(FbxCluster.ELinkMode.eTotalOne)
                    transformMatrix = FbxAMatrix()
                    cluster.SetTransformMatrix(transformMatrix)
                    cluster.SetTransformLinkMatrix(self.skeletonNodeList[boneIdx].EvaluateGlobalTransform())
                    skin.AddCluster(cluster)
                    clusterList.append(cluster)

                for vertexIndex, boneWeightInfo in enumerate(meshObj["boneWeightList"]):
                    for idx in boneWeightInfo[1]:
                        cluster = clusterList[idx]
                        cluster.AddControlPointIndex(vertexIndex, boneWeightInfo[0])

    def exportFbx(self):
        dirname = os.path.splitext(self.filePath)[0]
        filename = os.path.basename(self.filePath)
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        self.exporter = FbxExporter.Create(self.manager, "")
        self.exporter.Initialize(os.path.join(dirname, filename), -1, self.manager.GetIOSettings())
        self.exporter.Export(self.scene)
        self.exporter.Destroy()

        for imageFile in self.imageFileList:
            if os.path.exists(imageFile):
                newPath = os.path.join(dirname, os.path.basename(imageFile))
                shutil.copy(imageFile, newPath)
            else:
                if os.path.splitext(imageFile)[1].lower() == ".png":
                    # pngの場合、tgaから変換
                    tgaFile = os.path.splitext(imageFile)[0] + ".tga"
                    tgaPath = os.path.join(os.path.dirname(self.filePath), os.path.basename(tgaFile))
                    if os.path.exists(tgaPath):
                        newPath = os.path.join(dirname, os.path.basename(imageFile))
                        image = Image.open(tgaPath)
                        image.save(newPath, "png")