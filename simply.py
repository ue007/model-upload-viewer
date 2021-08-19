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
        raise Exception("Failed to load ./in/ReductionOutput.obj.")
    sgScene = sgSceneImporter.GetScene()

    # Create the reduction processor.
    sgReductionProcessor = sg.CreateReductionProcessor()

    sgReductionProcessor.SetScene(sgScene)

    sgReductionSettings = sgReductionProcessor.GetReductionSettings()

    # Set reduction target to triangle ratio with a ratio of 50%.
    sgReductionSettings.SetReductionTargets(
        Simplygon.EStopCondition_All, True, False, False, False
    )
    sgReductionSettings.SetReductionTargetTriangleRatio(0.5)

    # Start the reduction process.
    sgReductionProcessor.RunProcessing()

    sgSceneExporter = sg.CreateSceneExporter()
    sgSceneExporter.SetScene(sgScene)
    # 打印转换后的三角面片数
    print(sgScene.GetTriangleCount())
    sgScene.CreateAABB(False)
    print(sgScene.GetRadius())
    sgSceneExporter.SetExportFilePath("./out/simply/ReductionOutput.gltf")
    if not sgSceneExporter.RunExport():
        raise Exception("Failed to save ReductionOutput.gltf.")


if __name__ == "__main__":
    sg = simplygon_loader.init_simplygon()
    if sg is None:
        exit(Simplygon.GetLastInitializationError())

    RunReduction(sg)

    sg = None
    gc.collect()
