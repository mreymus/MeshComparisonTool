# Mesh Comparison Tool - User Manual

## Overview

The Mesh Comparison Tool is an extension for 3D Slicer that enables the systematic comparison of PLY reference files with STL comparison files. The tool calculates scientifically recognized distance metrics and is excellent for scientific publications.

## Scientific Background

### Distance Metrics

The tool calculates **unsigned distance**, which is suitable for mesh comparisons when:
- Meshes are not perfectly watertight
- Inside/Outside is not clearly defined
- The focus is on surface deviations

### Calculated Metrics

1. **Hausdorff Distance**: Maximum deviation between surfaces
   - Shows the largest local deviation
   - Important for identifying outliers
   - Frequently cited in scientific publications

2. **RMS (Root Mean Square) Distance**:
   - Quadratic mean of all distances
   - Gives an overall measure of accuracy
   - Standard metric in mesh validation studies

3. **Mean Absolute Distance**:
   - Arithmetic mean of all distances
   - Easy to interpret
   - Robust against moderate outliers

4. **Median Distance**:
   - Middle value of the distance distribution
   - Very robust against outliers
   - Shows typical deviation

5. **95th Percentile**:
   - 95% of points have a distance smaller than this value
   - Robust against extreme outliers
   - Clinically relevant metric

## Installation

### System Requirements

- 3D Slicer 5.0 or newer (Download: https://www.slicer.org)
- **No additional Slicer extensions required**
- Mac, Windows, or Linux

### Installation Steps

1. **Download and Install 3D Slicer**:
   - Visit https://www.slicer.org
   - Download the version for your operating system
   - Install 3D Slicer

2. **Install Extension**:

   **Method A: Drag & Drop (Recommended)**
   - Download the file `MeshComparisonTool.py`
   - Drag the file into the Slicer window
   - Select "Add Python scripted modules to the application"
   - Click "Yes"
   - The module is now available under `Modules` → `Surface Models` → `Mesh Comparison Tool`

   **Method B: Via Application Settings**
   - Go to: `Edit` → `Application Settings` → `Modules`
   - Click `>>` next to "Additional module paths"
   - Navigate to the `MeshComparisonTool` folder
   - Confirm with `OK`
   - Restart 3D Slicer

## File Preparation

### File Format and Naming Convention

**Important**: Files must have identical names (except for the extension)!

**Correct Examples**:
```
✓ patient1.ply     and     patient1.stl
✓ tooth_12.ply     and     tooth_12.stl
✓ scan_20241009.ply and    scan_20241009.stl
```

**Incorrect Examples**:
```
✗ patient1.ply     and     patient_1.stl    (Underscore vs. no underscore)
✗ tooth12.ply      and     tooth_12.stl     (Name difference)
✗ scan.ply         and     scan2.stl        (Number missing in .ply)
```

### Folder Structure

```
Your_Project_Folder/
├── Input/                  ← Place your mesh files here
│   ├── model1.ply
│   ├── model1.stl
│   ├── model2.ply
│   ├── model2.stl
│   └── ...
└── Output/                 ← Created by the tool
    ├── heatmaps/          ← Automatically generated heatmaps
    │   ├── model1_heatmap.png
    │   ├── model2_heatmap.png
    │   └── ...
    └── mesh_comparison_results.xlsx  ← Excel results
```

## Step-by-Step Guide

### 1. Open Module

- Start 3D Slicer
- Go to: `Modules` → `Surface Models` → `Mesh Comparison Tool`

### 2. Select Directories

- **Input Directory**: Select the folder with your PLY/STL files
- **Output Directory**: Select the folder for the results
- Click **"Scan for File Pairs"**
- The tool displays all found file pairs

### 3. Start Batch Process

For each file pair:

#### 3.1 Load Files

- Click **"Load Next Pair"**
- **Green Mesh** = Reference (PLY file)
- **Red Mesh** = Comparison (STL file, semi-transparent)

#### 3.2 Set Landmarks

**Important**: Choose anatomical landmarks that are clearly visible on both meshes!

**Examples of Good Landmarks**:
- Cusps on teeth
- Corners or prominent edges
- Distinct anatomical structures
- Bony landmarks

**Bad Landmarks**:
- Smooth, unmarked surfaces
- Areas with strong curvature without distinct features
- Edges or artifacts

**Procedure**:

1. Click **"Set Reference Landmarks (Green)"**
   - Place 3 landmarks on the green mesh
   - Click on the desired positions
   - **Tip**: Distribute landmarks across the entire mesh (triangle formation)

2. Click **"Set Comparison Landmarks (Red)"**
   - Place 3 corresponding landmarks on the red mesh
   - **Important**: Same order as on the green mesh!
   - Example: If you started with the front cusp on the green mesh, start there on the red mesh too

#### 3.3 Perform Alignment

- Click **"Perform Alignment (Landmark + ICP)"**
- The tool performs:
  1. Initial alignment based on landmarks
  2. ICP fine registration for optimal match
- **Visually verify the alignment!**
  - Rotate the 3D view
  - Check from different angles
  - Look for good overlap of main features

#### 3.4 Make Decision

**Option A: Accept Alignment**
- If alignment looks good: **"Accept && Calculate Distances"**
- The tool calculates all metrics
- Heatmap is automatically saved
- Results are saved
- Next file pair loads automatically

**Option B: Adjust Landmarks**
- If alignment is not optimal:
  - Delete landmarks (Right-click on landmark → Delete)
  - Set new landmarks (see Step 3.2)
  - Perform alignment again

**Option C: Skip Pair**
- Click **"Skip This Pair"**
- Next pair loads

### 4. Finish Batch

After all pairs have been processed (or you cancelled):

- Click **"Export Results to Excel"**
- Excel file is saved in Output folder
- Heatmaps are found in subfolder `heatmaps/`

## Interpreting Results

### Excel File

The Excel file `mesh_comparison_results.xlsx` contains:

| Column | Meaning | Interpretation |
|--------|-----------|----------------|
| Filename | Name of PLY file | Sample identification |
| Hausdorff Distance | Maximum deviation | Largest error, important for quality control |
| RMS Distance | Quadratic mean | Overall accuracy |
| Mean Distance | Average distance | Typical deviation |
| Median Distance | Median distance | 50% of points are below this |
| 95th Percentile | 95th percentile | 95% of points are below this |
| Number of Points (Reference) | Point count reference | Mesh resolution |
| Number of Points (Comparison) | Point count comparison | Mesh resolution |
| Transform Matrix | Transform matrix | For reproducibility |
| Timestamp | Timestamp | Documentation |

### Heatmaps

The heatmap images show:
- **Blue**: Low deviation (good)
- **Green/Yellow**: Moderate deviation
- **Red**: High deviation (problematic)

**Usage**:
- Identify problematic areas
- Visual communication of results
- Quality control
- Inclusion in publications

## Tips for Scientific Publications

### Reporting Metrics

Recommended presentation:

```
Accuracy was evaluated using multiple distance metrics:
- Hausdorff Distance: [Value] mm (maximum deviation)
- RMS Distance: [Value] mm (overall accuracy)
- Mean Distance: [Value] mm ± [Standard Deviation] mm
- 95th Percentile: [Value] mm (95% of points)
```

### Statistical Analysis

The Excel file can be imported into software like SPSS, R, or Python for:
- Descriptive statistics
- Comparative analysis
- Correlation studies
- Graphical presentation

### Figures

Integrate:
1. Example heatmap(s)
2. Boxplot of distance distributions
3. Overlay of reference and comparison mesh

## Troubleshooting

### "No matching PLY/STL file pairs found"

**Problem**: Tool finds no file pairs

**Solution**:
- Check filenames (must match exactly)
- Ensure files are directly in Input folder (not in subfolders)
- Check file extensions (.ply and .stl)

### Alignment Fails

**Problem**: Meshes are not aligned correctly

**Solutions**:
1. Check if you placed exactly 3 landmarks on each mesh
2. Ensure landmarks were placed in the same order
3. Choose more distinct anatomical landmarks
4. Distribute landmarks better across the mesh

### High Distance Values

**Problem**: Unexpected high deviations

**Possible Causes**:
- Poor alignment → Reset landmarks
- Actual differences between meshes
- Different units (mm vs cm)
- Different scan qualities

**Verification**:
- Check the heatmap
- Rotate 3D view from different angles
- Compare with known reference values

### Module Does Not Appear

**Problem**: Extension is not shown

**Solutions**:
1. Restart 3D Slicer
2. Check path in `Application Settings` → `Modules`
3. Check Python console for error messages
4. Reinstall the module

## Technical Details

### Algorithms Used

**Landmark-based Registration**:
- VTK's `vtkLandmarkTransform`
- Rigid-Body Transformation (translation and rotation only)
- Calculates optimal alignment from point correspondences

**ICP Registration**:
- VTK's `vtkIterativeClosestPointTransform`
- Parameters:
  - Max Iterations: 100
  - Max Mean Distance: 0.001
  - Max Landmarks: 1000
  - Rigid-Body Mode (no scaling)

**Distance Calculation**:
- Point-to-Surface Distance
- VTK's `vtkCellLocator` for efficient search
- Unsigned distance (always positive)

### Python Dependencies

Automatically installed on first launch:
- `pandas`: Excel export
- `openpyxl`: Excel file creation
- `numpy`: Numerical calculations (usually pre-installed)

### Data Flow

```
PLY + STL Files
    ↓
Load into VTK structures
    ↓
Landmark Placement (manual)
    ↓
Landmark Transform
    ↓
ICP Fine Registration
    ↓
Distance Calculation
    ↓
Heatmap Generation + Excel Export
```

## Best Practices

### Before Scanning

1. **File Organization**:
   - Use consistent naming conventions
   - Create separate folders for different projects
   - Document your naming scheme

2. **Quality Control**:
   - Open meshes in a viewer (e.g., MeshLab)
   - Check for artifacts or holes
   - Ensure consistent orientation

### During Processing

1. **Landmark Consistency**:
   - Create a landmark protocol
   - Document which anatomical points you use
   - Always use the same order

2. **Visual Control**:
   - Take time for verification
   - Rotate view from multiple angles
   - If unsure: Better to repeat than accept bad data

3. **Batch Processing**:
   - Process similar cases in one session
   - Take regular breaks
   - Document problematic cases

### After Processing

1. **Data Backup**:
   - Back up both Excel file and heatmaps
   - Keep original data
   - Version your results

2. **Quality Control**:
   - Check statistical outliers
   - Compare with expected values
   - Document anomalies

3. **Documentation**:
   - Note Slicer version
   - Document extension version
   - Describe your workflow for publications

## FAQ

**Q: Can I use other file formats?**
A: No, currently only PLY (reference) and STL (comparison) are supported. However, you can convert other formats with tools like MeshLab.

**Q: Why do I have to place landmarks every time?**
A: Manual landmark placement allows flexible, anatomically correct alignment that works for various geometries.

**Q: Can I use more than 3 landmarks?**
A: Currently, exactly 3 landmarks are required. This is sufficient for stable rigid-body transformation.

**Q: What does "Rigid-Body" mean?**
A: The transformation uses only translation (shifting) and rotation (turning), but no scaling or distortion.

**Q: How do I cite this tool?**
A: [Citation info will be added after publication]

**Q: Is the code Open Source?**
A: Yes, the entire code is available on GitHub and can be freely used and modified.

## Support and Feedback

For questions, issues, or suggestions:

- **GitHub Issues**: [Link to your repository]/issues
- **Email**: [Your Email]
- **Documentation**: [Link to online documentation]

## License

[Your chosen license]

---

**Version**: 1.0.0
**Author**: [Your Name]
**Institution**: [Your Institution]
**Date**: [Current Date]
