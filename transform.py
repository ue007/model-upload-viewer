import math
import os
import sys
import glob
import gc
import threading

from pathlib import Path
from simplygon import simplygon_loader
from simplygon import Simplygon

filePathIn = sys.argv[1]
filePathOut = sys.argv[2]


def transformUnit(sg: Simplygon.ISimplygon):
    sgSceneImporter = sg.CreateSceneImporter()
    sgSceneImporter.SetImportFilePath(filePathIn)
    if not sgSceneImporter.RunImport():
        raise Exception("Failed to load " + filePathIn)
    sgScene = sgSceneImporter.GetScene()

    # 转换单位开始
    transform = sg.CreateTransform3()
    transform.AddScaling(1000, 1000, 1000)
    matrix = transform.GetMatrix()
    geom = sgScene.NewCombinedGeometry()
    geom.Transform(matrix)

    mmScene = sg.CreateScene()
    mmSceneMesh = sg.CreateSceneMesh()
    mmSceneMesh.SetGeometry(geom)
    mmScene.GetMaterialTable().Copy(sgScene.GetMaterialTable())
    mmScene.GetTextureTable().Copy(sgScene.GetTextureTable())
    mmScene.GetBoneTable().Copy(sgScene.GetBoneTable())
    mmScene.GetSelectionSetTable().Copy(sgScene.GetSelectionSetTable())
    mmScene.GetRootNode().AddChild(mmSceneMesh)
    # 转换单位结束

    mmScene.CreateAABB(False)

    sgSceneExporter = sg.CreateSceneExporter()
    sgSceneExporter.SetScene(mmScene)
    sgSceneExporter.SetEmbedReferences(True)
    sgSceneExporter.SetExportCascadedScenes(True)
    sgSceneExporter.SetExportFilePath(filePathOut)

    if not sgSceneExporter.RunExport():
        raise Exception("Failed to save " + filePathOut + ".")


if __name__ == "__main__":
    sg = simplygon_loader.init_simplygon()
    if sg is None:
        exit(Simplygon.GetLastInitializationError())

    transformUnit(sg)

    sg = None
    gc.collect()
