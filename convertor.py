#!/usr/bin/python3


# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import math
import os
import sys
import glob
import gc
import threading

from pathlib import Path
from simplygon import simplygon_loader
from simplygon import Simplygon


def RunReduction(sg: Simplygon.ISimplygon):
    sgSceneImporter = sg.CreateSceneImporter()
    sgSceneImporter.SetImportFilePath("./in/ReductionOutput.fbx")
    if not sgSceneImporter.RunImport():
        raise Exception("Failed to load ./in/ReductionOutput.fbx.")
    sgScene = sgSceneImporter.GetScene()
    # Create the reduction processor.
    # sgReductionProcessor = sg.CreateReductionProcessor()

    # sgReductionProcessor.SetScene(sgScene)

    # sgReductionSettings = sgReductionProcessor.GetReductionSettings()

    # Set reduction target to triangle ratio with a ratio of 50%.
    # sgReductionSettings.SetReductionTargets(
    #     Simplygon.EStopCondition_All, True, False, False, False
    # )
    # sgReductionSettings.SetReductionTargetTriangleRatio(1.0)

    # Start the reduction process.
    # sgReductionProcessor.RunProcessing()

    # 转换单位开始 
    transform = sg.CreateTransform3()
    transform.AddScaling(1000, 1000, 1000)
    matrix = transform.GetMatrix()
    geom = sgScene.NewCombinedGeometry()
    geom.Transform(matrix)
    print(geom.GetTriangleCount())

    sgScene2 = sg.CreateScene()
    sgSceneMesh2 = sg.CreateSceneMesh()
    sgSceneMesh2.SetGeometry(geom)

    sgScene2.GetRootNode().AddChild(sgSceneMesh2)
    # 转换单位结束

    # 打印转换后的三角面片数
    print(sgScene2.GetTriangleCount())
    sgScene2.CreateAABB(False)
    # 打印整个场景包围球的半径
    # print(sgScene2.GetRadius())
    print(sgScene2.GetInf())
    min = sgScene2.GetInf()
    print(sgScene2.GetSup())
    max = sgScene2.GetSup()
    # 打印模型尺寸：长宽高
    print(max[0] - min[0], max[1] - min[1], max[2] - min[2])

    sgSceneExporter = sg.CreateSceneExporter()
    sgSceneExporter.SetScene(sgScene2)
    sgSceneExporter.SetExportFilePath("./out/convertor/ReductionOutput.gltf")
    if not sgSceneExporter.RunExport():
        raise Exception("Failed to save ReductionOutput.gltf.")


if __name__ == "__main__":
    sg = simplygon_loader.init_simplygon()
    if sg is None:
        exit(Simplygon.GetLastInitializationError())

    RunReduction(sg)

    sg = None
    gc.collect()
