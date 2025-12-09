import os
import vtk
import qt
import ctk
import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
import numpy as np
from pathlib import Path

#
# MeshComparisonTool
#

class MeshComparisonTool(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Mesh Comparison Tool"
        self.parent.categories = ["Surface Models"]
        self.parent.dependencies = []
        self.parent.contributors = ["Your Name"]
        self.parent.helpText = """
This module performs batch comparison of PLY (reference) and STL (comparison) mesh files.
It computes multiple distance metrics suitable for scientific publications including:
- Hausdorff Distance
- RMS Distance
- Mean Absolute Distance
- Median Distance
- 95th Percentile Distance

The workflow includes:
1. Manual 3-point landmark-based initial alignment
2. ICP fine registration
3. Visual verification before calculation
4. Automatic generation of distance heatmaps
5. Excel export of all metrics
"""
        self.parent.acknowledgementText = """
Developed for scientific mesh comparison analysis.
"""

#
# MeshComparisonToolWidget
#

class MeshComparisonToolWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)
        self.logic = None
        self._parameterNode = None
        self._updatingGUIFromParameterNode = False
        
        # State variables
        self.currentPairIndex = 0
        self.filePairs = []
        self.referenceLandmarks = None
        self.comparisonLandmarks = None
        self.results = []

    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        uiWidget = slicer.util.loadUI(self.resourcePath('UI/MeshComparisonTool.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class.
        self.logic = MeshComparisonToolLogic()

        # Connections
        self.ui.inputDirectoryButton.directoryChanged.connect(self.onInputDirectoryChanged)
        self.ui.outputDirectoryButton.directoryChanged.connect(self.onOutputDirectoryChanged)
        self.ui.scanFilesButton.clicked.connect(self.onScanFiles)
        self.ui.loadNextPairButton.clicked.connect(self.onLoadNextPair)
        self.ui.setReferenceLandmarksButton.clicked.connect(self.onSetReferenceLandmarks)
        self.ui.setComparisonLandmarksButton.clicked.connect(self.onSetComparisonLandmarks)
        self.ui.clearLandmarksButton.clicked.connect(self.onClearLandmarks)
        self.ui.performAlignmentButton.clicked.connect(self.onPerformAlignment)
        self.ui.acceptAndCalculateButton.clicked.connect(self.onAcceptAndCalculate)
        self.ui.skipPairButton.clicked.connect(self.onSkipPair)
        self.ui.abortBatchButton.clicked.connect(self.onAbortBatch)
        self.ui.exportResultsButton.clicked.connect(self.onExportResults)

        # Initial state
        self.updateGUIState()

    def cleanup(self):
        """
        Called when the application closes and the module widget is destroyed.
        """
        self.removeObservers()

    def updateGUIState(self):
        """Update GUI elements based on current state"""
        hasPairs = len(self.filePairs) > 0
        hasCurrentPair = self.currentPairIndex < len(self.filePairs)
        hasLandmarks = self.referenceLandmarks is not None and self.comparisonLandmarks is not None
        
        self.ui.loadNextPairButton.enabled = hasPairs and hasCurrentPair
        self.ui.setReferenceLandmarksButton.enabled = hasCurrentPair
        self.ui.setComparisonLandmarksButton.enabled = hasCurrentPair
        self.ui.performAlignmentButton.enabled = hasLandmarks
        self.ui.acceptAndCalculateButton.enabled = hasLandmarks
        self.ui.skipPairButton.enabled = hasCurrentPair
        self.ui.abortBatchButton.enabled = hasPairs
        self.ui.exportResultsButton.enabled = len(self.results) > 0
        
        # Update progress
        if hasPairs:
            self.ui.progressLabel.text = f"Pair {self.currentPairIndex + 1} of {len(self.filePairs)}"
        else:
            self.ui.progressLabel.text = "No file pairs loaded"

    def onInputDirectoryChanged(self, path):
        """Called when input directory is changed"""
        self.ui.statusLabel.text = f"Input directory: {path}"

    def onOutputDirectoryChanged(self, path):
        """Called when output directory is changed"""
        self.ui.statusLabel.text = f"Output directory: {path}"

    def onScanFiles(self):
        """Scan input directory for matching PLY/STL file pairs"""
        inputDir = self.ui.inputDirectoryButton.directory
        if not inputDir or not os.path.exists(inputDir):
            slicer.util.errorDisplay("Please select a valid input directory")
            return
        
        self.filePairs = self.logic.findFilePairs(inputDir)
        
        if not self.filePairs:
            slicer.util.errorDisplay("No matching PLY/STL file pairs found in the directory")
            return
        
        self.currentPairIndex = 0
        self.results = []
        self.ui.statusLabel.text = f"Found {len(self.filePairs)} file pairs"
        self.ui.filePairsList.clear()
        
        for ply, stl in self.filePairs:
            self.ui.filePairsList.addItem(f"{os.path.basename(ply)} <-> {os.path.basename(stl)}")
        
        self.updateGUIState()

    def onLoadNextPair(self):
        """Load the next file pair"""
        if self.currentPairIndex >= len(self.filePairs):
            slicer.util.infoDisplay("All pairs processed!")
            return
        
        plyPath, stlPath = self.filePairs[self.currentPairIndex]
        
        # Clear scene
        slicer.mrmlScene.Clear(0)
        
        # Reset landmarks
        self.referenceLandmarks = None
        self.comparisonLandmarks = None
        
        # Load meshes
        try:
            referenceNode = self.logic.loadMesh(plyPath, "Reference_PLY")
            comparisonNode = self.logic.loadMesh(stlPath, "Comparison_STL")
            
            # Set different colors
            referenceNode.GetDisplayNode().SetColor(0.0, 0.8, 0.0)  # Green
            comparisonNode.GetDisplayNode().SetColor(0.8, 0.0, 0.0)  # Red
            comparisonNode.GetDisplayNode().SetOpacity(0.5)
            
            # Center view
            slicer.app.layoutManager().threeDWidget(0).threeDView().resetFocalPoint()
            
            self.ui.statusLabel.text = f"Loaded: {os.path.basename(plyPath)} and {os.path.basename(stlPath)}"
            
            # Create landmark nodes
            self.referenceLandmarks = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "Reference_Landmarks")
            self.comparisonLandmarks = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "Comparison_Landmarks")
            
            self.referenceLandmarks.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)
            self.comparisonLandmarks.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)
            
        except Exception as e:
            slicer.util.errorDisplay(f"Error loading files: {str(e)}")
            return
        
        self.updateGUIState()

    def onSetReferenceLandmarks(self):
        """Activate placement of reference landmarks"""
        if self.referenceLandmarks:
            slicer.modules.markups.logic().SetActiveListID(self.referenceLandmarks)
            interactionNode = slicer.app.applicationLogic().GetInteractionNode()
            selectionNode = slicer.app.applicationLogic().GetSelectionNode()
            selectionNode.SetReferenceActivePlaceNodeClassName("vtkMRMLMarkupsFiducialNode")
            selectionNode.SetActivePlaceNodeID(self.referenceLandmarks.GetID())
            interactionNode.SetCurrentInteractionMode(interactionNode.Place)
            self.ui.statusLabel.text = "Place 3 landmarks on the GREEN reference mesh"

    def onSetComparisonLandmarks(self):
        """Activate placement of comparison landmarks"""
        if self.comparisonLandmarks:
            slicer.modules.markups.logic().SetActiveListID(self.comparisonLandmarks)
            interactionNode = slicer.app.applicationLogic().GetInteractionNode()
            selectionNode = slicer.app.applicationLogic().GetSelectionNode()
            selectionNode.SetReferenceActivePlaceNodeClassName("vtkMRMLMarkupsFiducialNode")
            selectionNode.SetActivePlaceNodeID(self.comparisonLandmarks.GetID())
            interactionNode.SetCurrentInteractionMode(interactionNode.Place)
            self.ui.statusLabel.text = "Place 3 corresponding landmarks on the RED comparison mesh"

    def onClearLandmarks(self):
        """Clear all placed landmarks and start fresh"""
        if self.referenceLandmarks:
            self.referenceLandmarks.RemoveAllControlPoints()
            self.ui.statusLabel.text = "Reference landmarks cleared"
        
        if self.comparisonLandmarks:
            self.comparisonLandmarks.RemoveAllControlPoints()
            self.ui.statusLabel.text = "All landmarks cleared - ready to start fresh"
        
        self.updateGUIState()

    def onPerformAlignment(self):
        """Perform initial landmark-based alignment followed by ICP"""
        if not self.referenceLandmarks or not self.comparisonLandmarks:
            slicer.util.errorDisplay("Please set landmarks first")
            return
        
        if self.referenceLandmarks.GetNumberOfControlPoints() != 3:
            slicer.util.errorDisplay("Please place exactly 3 landmarks on the reference mesh")
            return
        
        if self.comparisonLandmarks.GetNumberOfControlPoints() != 3:
            slicer.util.errorDisplay("Please place exactly 3 landmarks on the comparison mesh")
            return
        
        try:
            # Get mesh nodes
            referenceNode = slicer.util.getNode("Reference_PLY")
            comparisonNode = slicer.util.getNode("Comparison_STL")
            
            # Perform alignment
            transformNode = self.logic.performAlignment(
                referenceNode, 
                comparisonNode,
                self.referenceLandmarks,
                self.comparisonLandmarks
            )
            
            self.ui.statusLabel.text = "Alignment complete. Please verify visually before calculation."
            self.updateGUIState()
            
        except Exception as e:
            slicer.util.errorDisplay(f"Error during alignment: {str(e)}")

    def onAcceptAndCalculate(self):
        """Accept alignment and calculate distances"""
        try:
            # Get mesh nodes
            referenceNode = slicer.util.getNode("Reference_PLY")
            comparisonNode = slicer.util.getNode("Comparison_STL")
            
            # Calculate distances
            plyPath, stlPath = self.filePairs[self.currentPairIndex]
            outputDir = self.ui.outputDirectoryButton.directory
            
            if not outputDir:
                slicer.util.errorDisplay("Please select an output directory")
                return
            
            result = self.logic.calculateDistances(
                referenceNode,
                comparisonNode,
                os.path.basename(plyPath),
                outputDir
            )
            
            self.results.append(result)
            
            self.ui.statusLabel.text = f"Calculation complete. Hausdorff: {result['hausdorff_distance']:.4f}"
            
            # Move to next pair
            self.currentPairIndex += 1
            
            if self.currentPairIndex < len(self.filePairs):
                self.onLoadNextPair()
            else:
                slicer.util.infoDisplay("All pairs processed! Click 'Export Results' to save to Excel.")
                self.updateGUIState()
            
        except Exception as e:
            slicer.util.errorDisplay(f"Error calculating distances: {str(e)}")

    def onSkipPair(self):
        """Skip current pair"""
        self.currentPairIndex += 1
        if self.currentPairIndex < len(self.filePairs):
            self.onLoadNextPair()
        else:
            slicer.util.infoDisplay("All pairs processed!")
            self.updateGUIState()

    def onAbortBatch(self):
        """Abort batch processing"""
        reply = qt.QMessageBox.question(
            slicer.util.mainWindow(),
            "Abort Batch",
            "Do you want to abort batch processing? Already calculated results will be kept.",
            qt.QMessageBox.Yes | qt.QMessageBox.No
        )
        
        if reply == qt.QMessageBox.Yes:
            self.currentPairIndex = len(self.filePairs)  # Set to end
            self.updateGUIState()
            self.ui.statusLabel.text = "Batch processing aborted"

    def onExportResults(self):
        """Export results to Excel"""
        outputDir = self.ui.outputDirectoryButton.directory
        if not outputDir:
            slicer.util.errorDisplay("Please select an output directory")
            return
        
        if not self.results:
            slicer.util.errorDisplay("No results to export")
            return
        
        try:
            excelPath = self.logic.exportToExcel(self.results, outputDir)
            slicer.util.infoDisplay(f"Results exported to:\n{excelPath}")
        except Exception as e:
            slicer.util.errorDisplay(f"Error exporting results: {str(e)}")

#
# MeshComparisonToolLogic
#

class MeshComparisonToolLogic(ScriptedLoadableModuleLogic):
    """This class implements all the actual computation logic.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self):
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)

    def findFilePairs(self, directory):
        """
        Find all matching PLY/STL file pairs in directory
        Returns list of tuples: [(ply_path, stl_path), ...]
        """
        plyFiles = {}
        stlFiles = {}
        
        # Scan directory
        for file in os.listdir(directory):
            fullPath = os.path.join(directory, file)
            if not os.path.isfile(fullPath):
                continue
            
            name, ext = os.path.splitext(file)
            ext = ext.lower()
            
            if ext == '.ply':
                plyFiles[name] = fullPath
            elif ext == '.stl':
                stlFiles[name] = fullPath
        
        # Find matching pairs
        pairs = []
        for name in plyFiles:
            if name in stlFiles:
                pairs.append((plyFiles[name], stlFiles[name]))
        
        return sorted(pairs)

    def loadMesh(self, filePath, nodeName):
        """Load a mesh file (PLY or STL)"""
        ext = os.path.splitext(filePath)[1].lower()
        
        if ext == '.ply':
            reader = vtk.vtkPLYReader()
        elif ext == '.stl':
            reader = vtk.vtkSTLReader()
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        reader.SetFileName(filePath)
        reader.Update()
        
        # Create model node
        modelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", nodeName)
        modelNode.SetAndObservePolyData(reader.GetOutput())
        modelNode.CreateDefaultDisplayNodes()
        
        return modelNode

    def performAlignment(self, referenceNode, comparisonNode, referenceLandmarks, comparisonLandmarks):
        """
        Perform alignment:
        1. Initial landmark-based alignment
        2. ICP fine registration
        """
        # Get landmark points
        refPoints = vtk.vtkPoints()
        compPoints = vtk.vtkPoints()
        
        for i in range(3):
            pos = [0, 0, 0]
            referenceLandmarks.GetNthControlPointPosition(i, pos)
            refPoints.InsertNextPoint(pos)
            
            comparisonLandmarks.GetNthControlPointPosition(i, pos)
            compPoints.InsertNextPoint(pos)
        
        # Landmark-based transformation
        landmarkTransform = vtk.vtkLandmarkTransform()
        landmarkTransform.SetSourceLandmarks(compPoints)
        landmarkTransform.SetTargetLandmarks(refPoints)
        landmarkTransform.SetModeToRigidBody()
        landmarkTransform.Update()
        
        # Apply landmark transformation to comparison mesh
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetInputData(comparisonNode.GetPolyData())
        transformFilter.SetTransform(landmarkTransform)
        transformFilter.Update()
        
        transformedPolyData = transformFilter.GetOutput()
        
        # ICP fine registration with improved parameters
        icp = vtk.vtkIterativeClosestPointTransform()
        icp.SetSource(transformedPolyData)
        icp.SetTarget(referenceNode.GetPolyData())
        icp.GetLandmarkTransform().SetModeToRigidBody()
        icp.SetMaximumNumberOfIterations(500)  # Increased from 100
        icp.SetMaximumMeanDistance(0.0001)  # Tighter convergence from 0.001
        icp.SetMaximumNumberOfLandmarks(5000)  # Increased from 1000
        icp.SetCheckMeanDistance(1)
        icp.StartByMatchingCentroidsOn()
        icp.Modified()
        icp.Update()
        
        # Log ICP results for user feedback
        print(f"ICP completed with {icp.GetNumberOfIterations()} iterations")
        print(f"Mean distance: {icp.GetMeanDistance():.6f}")
        
        # Apply ICP transformation
        finalTransformFilter = vtk.vtkTransformPolyDataFilter()
        finalTransformFilter.SetInputData(transformedPolyData)
        finalTransformFilter.SetTransform(icp)
        finalTransformFilter.Update()
        
        # Update comparison node
        comparisonNode.SetAndObservePolyData(finalTransformFilter.GetOutput())
        
        # Create and return transform node for documentation
        transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode", "Alignment_Transform")
        
        # Combine transforms
        combinedTransform = vtk.vtkGeneralTransform()
        combinedTransform.Concatenate(icp)
        combinedTransform.Concatenate(landmarkTransform)
        
        transformNode.SetAndObserveTransformToParent(combinedTransform)
        
        return transformNode

    def calculateDistances(self, referenceNode, comparisonNode, filename, outputDir):
        """
        Calculate all distance metrics and generate heatmap
        """
        import time
        
        referencePoly = referenceNode.GetPolyData()
        comparisonPoly = comparisonNode.GetPolyData()
        
        # Build locator for reference mesh
        cellLocator = vtk.vtkCellLocator()
        cellLocator.SetDataSet(referencePoly)
        cellLocator.BuildLocator()
        
        # Calculate distances from comparison to reference
        distances = []
        numPoints = comparisonPoly.GetNumberOfPoints()
        
        for i in range(numPoints):
            point = comparisonPoly.GetPoint(i)
            closestPoint = [0, 0, 0]
            cellId = vtk.reference(0)
            subId = vtk.reference(0)
            dist2 = vtk.reference(0.0)
            
            cellLocator.FindClosestPoint(point, closestPoint, cellId, subId, dist2)
            distances.append(np.sqrt(float(dist2)))
        
        distances = np.array(distances)
        
        # Calculate metrics
        hausdorff = float(np.max(distances))
        rms = float(np.sqrt(np.mean(distances**2)))
        mean_dist = float(np.mean(distances))
        median_dist = float(np.median(distances))
        percentile_95 = float(np.percentile(distances, 95))
        
        # Get transform matrix
        transformNode = slicer.util.getNode("Alignment_Transform")
        transformMatrix = vtk.vtkMatrix4x4()
        transformNode.GetMatrixTransformToParent(transformMatrix)
        
        # Store distances as scalars for visualization
        distanceArray = vtk.vtkFloatArray()
        distanceArray.SetName("Distance")
        distanceArray.SetNumberOfTuples(numPoints)
        for i in range(numPoints):
            distanceArray.SetValue(i, distances[i])
        
        comparisonPoly.GetPointData().SetScalars(distanceArray)
        comparisonNode.Modified()
        
        # Generate and save heatmap
        self.saveHeatmap(comparisonNode, filename, outputDir)
        
        # Prepare result dictionary
        result = {
            'filename': filename,
            'hausdorff_distance': hausdorff,
            'rms_distance': rms,
            'mean_distance': mean_dist,
            'median_distance': median_dist,
            'percentile_95': percentile_95,
            'num_points_reference': referencePoly.GetNumberOfPoints(),
            'num_points_comparison': comparisonPoly.GetNumberOfPoints(),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'transform_matrix': self.matrixToString(transformMatrix)
        }
        
        return result

    def matrixToString(self, matrix):
        """Convert VTK matrix to string for Excel export"""
        matrixStr = ""
        for i in range(4):
            row = []
            for j in range(4):
                row.append(f"{matrix.GetElement(i, j):.6f}")
            matrixStr += " ".join(row)
            if i < 3:
                matrixStr += "; "
        return matrixStr

    def saveHeatmap(self, modelNode, filename, outputDir):
        """Save heatmap visualization as PNG"""
        # Create heatmap subfolder
        heatmapDir = os.path.join(outputDir, "heatmaps")
        os.makedirs(heatmapDir, exist_ok=True)
        
        # Setup display for heatmap
        displayNode = modelNode.GetDisplayNode()
        displayNode.SetScalarVisibility(True)
        displayNode.SetActiveScalarName("Distance")
        displayNode.SetAndObserveColorNodeID("vtkMRMLColorTableNodeFileColdToHotRainbow.txt")
        displayNode.SetScalarRangeFlag(displayNode.UseDataScalarRange)
        displayNode.SetOpacity(1.0)
        
        # Take screenshot
        threeDView = slicer.app.layoutManager().threeDWidget(0).threeDView()
        threeDView.resetFocalPoint()
        
        # Wait for render
        slicer.app.processEvents()
        
        # Capture image
        renderWindow = threeDView.renderWindow()
        windowToImage = vtk.vtkWindowToImageFilter()
        windowToImage.SetInput(renderWindow)
        windowToImage.Update()
        
        # Save as PNG
        baseName = os.path.splitext(filename)[0]
        outputPath = os.path.join(heatmapDir, f"{baseName}_heatmap.png")
        
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(outputPath)
        writer.SetInputConnection(windowToImage.GetOutputPort())
        writer.Write()

    def exportToExcel(self, results, outputDir):
        """Export results to Excel file"""
        try:
            import pandas as pd
        except ImportError:
            # Install pandas if not available
            slicer.util.pip_install("pandas openpyxl")
            import pandas as pd
        
        # Convert results to DataFrame
        df = pd.DataFrame(results)
        
        # Reorder columns
        columns = [
            'filename',
            'hausdorff_distance',
            'rms_distance',
            'mean_distance',
            'median_distance',
            'percentile_95',
            'num_points_reference',
            'num_points_comparison',
            'transform_matrix',
            'timestamp'
        ]
        df = df[columns]
        
        # Rename columns for clarity
        df.columns = [
            'Filename',
            'Hausdorff Distance (max)',
            'RMS Distance',
            'Mean Distance',
            'Median Distance',
            '95th Percentile Distance',
            'Number of Points (Reference)',
            'Number of Points (Comparison)',
            'Transform Matrix',
            'Timestamp'
        ]
        
        # Export to Excel
        excelPath = os.path.join(outputDir, 'mesh_comparison_results.xlsx')
        df.to_excel(excelPath, index=False, sheet_name='Results')
        
        return excelPath

#
# MeshComparisonToolTest
#

class MeshComparisonToolTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_MeshComparisonTool1()

    def test_MeshComparisonTool1(self):
        """ Basic test
        """
        self.delayDisplay("Starting the test")
        
        logic = MeshComparisonToolLogic()
        
        self.delayDisplay('Test passed')
