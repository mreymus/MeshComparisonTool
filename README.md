# Mesh Comparison Tool for 3D Slicer

A 3D Slicer extension for batch comparison of PLY (reference) and STL (comparison) mesh files with multiple distance metrics suitable for scientific publications.

## Features

- **Batch Processing**: Automatically processes all matching PLY/STL file pairs in a directory
- **Landmark-Based Initial Alignment**: Manual placement of 3 anatomical landmarks for initial registration
- **ICP Fine Registration**: Automatic Iterative Closest Point (ICP) algorithm for precise alignment
- **Visual Verification**: Visual inspection of alignment before distance calculation
- **Multiple Distance Metrics**:
  - Hausdorff Distance (maximum distance)
  - RMS (Root Mean Square) Distance
  - Mean Absolute Distance
  - Median Distance
  - 95th Percentile Distance
- **Heatmap Generation**: Automatic creation of distance heatmap visualizations (saved as PNG)
- **Excel Export**: All results exported to a single Excel file with comprehensive metrics
- **Transform Documentation**: Complete transformation matrix stored for reproducibility

## Scientific Background

This tool implements unsigned distance metrics, which are appropriate for mesh comparison when:
- Meshes may not be perfectly watertight
- Inside/outside distinction is not clearly defined
- Focus is on surface-to-surface deviation measurement

The implemented metrics are widely used in scientific publications for mesh quality assessment:
- **Hausdorff Distance**: Reports the maximum deviation, useful for identifying largest errors
- **RMS Distance**: Provides an overall accuracy measure, commonly reported in mesh validation studies
- **Mean Absolute Distance**: Average deviation across all points
- **95th Percentile**: Robust metric less sensitive to outliers
- **Median Distance**: Central tendency of the distance distribution

## Installation

### Prerequisites

- 3D Slicer 5.0 or later
- **No additional Slicer extensions required** (works with core Slicer functionality)

### Option 1: Install from Extension Manager (Recommended - After Publication)

1. Open 3D Slicer
2. Go to: `View` → `Extension Manager`
3. Search for "Mesh Comparison Tool"
4. Click `Install`
5. Restart 3D Slicer

### Option 2: Install from GitHub (For Development/Testing)

1. Download or clone this repository:
   ```bash
   git clone https://github.com/yourusername/MeshComparisonTool.git
   ```

2. Open 3D Slicer

3. Add the module to Slicer:
   - **Method A** (Drag & Drop - Easiest):
     - Drag the `MeshComparisonTool.py` file into the Slicer application window
     - Select "Add Python scripted modules to the application"
     - Click "Yes"
   
   - **Method B** (Application Settings):
     - Go to: `Edit` → `Application Settings` → `Modules`
     - In "Additional module paths", click the `>>` button
     - Navigate to the `MeshComparisonTool` folder
     - Select the folder and click `OK`
     - Restart 3D Slicer

4. The module will appear under: `Modules` → `Surface Models` → `Mesh Comparison Tool`

## Python Dependencies

The extension automatically installs required Python packages on first use:
- `pandas` - For Excel export
- `openpyxl` - For Excel file creation
- `numpy` - For numerical calculations (usually pre-installed with Slicer)

## Usage

### File Preparation

1. Prepare your mesh files:
   - **Reference files**: `.ply` format (ground truth)
   - **Comparison files**: `.stl` format (to be compared)
   - **Naming convention**: Files must have identical names (except extension)
     - Example: `model1.ply` and `model1.stl` will be paired
     - Example: `scan_tooth_12.ply` and `scan_tooth_12.stl` will be paired

2. Place all files in a single input directory

### Workflow

#### 1. Setup

- Open the module: `Modules` → `Surface Models` → `Mesh Comparison Tool`
- Select **Input Directory**: Folder containing your PLY and STL files
- Select **Output Directory**: Where results and heatmaps will be saved
- Click **"Scan for File Pairs"**
  - The module will list all matching file pairs found

#### 2. Process Each Pair

For each file pair, follow these steps:

##### Step 2.1: Load Files
- Click **"Load Next Pair"**
- Reference mesh (PLY) appears in **green**
- Comparison mesh (STL) appears in **red** (semi-transparent)

##### Step 2.2: Place Landmarks
- Click **"Set Reference Landmarks (Green)"**
  - Place 3 anatomical landmarks on the reference mesh
  - Use consistent anatomical features (e.g., cusps, ridges)
- Click **"Set Comparison Landmarks (Red)"**
  - Place 3 corresponding landmarks on the comparison mesh
  - Order matters: place landmarks in the same sequence

##### Step 2.3: Perform Alignment
- Click **"Perform Alignment (Landmark + ICP)"**
- The tool performs:
  1. Landmark-based rigid transformation
  2. ICP fine registration for optimal alignment
- **Visually verify** the alignment in the 3D view

##### Step 2.4: Calculate Distances
- If alignment looks good: Click **"Accept && Calculate Distances"**
  - Distance metrics are calculated
  - Heatmap is automatically saved
  - Results are stored
  - Next pair loads automatically
- If alignment needs adjustment: Modify landmarks and re-align
- To skip this pair: Click **"Skip This Pair"**

#### 3. Export Results

- After processing all pairs (or aborting batch), click **"Export Results to Excel"**
- Excel file `mesh_comparison_results.xlsx` is saved to output directory
- Heatmaps are saved to `output_directory/heatmaps/` subfolder

### Aborting Batch Processing

- Click **"Abort Batch"** to stop processing
- All results calculated so far will be kept
- You can still export results

## Output Files

### Excel Results File

File: `mesh_comparison_results.xlsx`

Columns:
- `Filename`: Name of the reference PLY file
- `Hausdorff Distance (max)`: Maximum surface deviation
- `RMS Distance`: Root mean square distance
- `Mean Distance`: Average distance
- `Median Distance`: Median distance
- `95th Percentile Distance`: 95th percentile of distances
- `Number of Points (Reference)`: Point count in reference mesh
- `Number of Points (Comparison)`: Point count in comparison mesh
- `Transform Matrix`: 4x4 transformation matrix (landmark + ICP combined)
- `Timestamp`: Date and time of calculation

### Heatmap Images

Location: `output_directory/heatmaps/`

Files: `[filename]_heatmap.png`

- Visual representation of distance distribution
- Color scale: Blue (close) → Red (far)
- Useful for identifying regions of high deviation

## Tips for Best Results

### Landmark Placement

1. **Choose distinct anatomical features**:
   - Cusps, corners, or prominent ridges
   - Avoid flat or featureless regions

2. **Maintain consistent order**:
   - Place landmarks in the same sequence on both meshes
   - Example: anterior cusp → posterior cusp → buccal cusp

3. **Spread landmarks across the mesh**:
   - Don't cluster all landmarks in one area
   - Triangular configuration works best

### Alignment Verification

Before clicking "Accept", check:
- Meshes overlap well in all views
- No obvious misalignments
- Major features coincide
- Rotate the 3D view to check from multiple angles

### Troubleshooting

**Q: "No matching PLY/STL file pairs found"**
- Verify files have identical names (except extension)
- Check files are directly in the input directory (not in subfolders)

**Q: Alignment fails or looks incorrect**
- Verify you placed exactly 3 landmarks on each mesh
- Check landmarks are in corresponding positions
- Try replacing landmarks with more distinct features

**Q: "Error loading files"**
- Ensure PLY and STL files are valid mesh files
- Check files are not corrupted
- Try opening files in another mesh viewer first

**Q: Module doesn't appear after installation**
- Restart 3D Slicer
- Check `Application Settings` → `Modules` for the correct path
- Check Slicer's Python console for error messages

## Technical Details

### Algorithms

#### Landmark-Based Registration
- Uses VTK's `vtkLandmarkTransform` with rigid body mode
- Computes optimal rotation and translation from point correspondences

#### ICP Registration
- VTK's `vtkIterativeClosestPointTransform`
- Parameters:
  - Maximum iterations: 100
  - Maximum mean distance: 0.001
  - Maximum landmarks: 1000
  - Start by matching centroids: ON
  - Mode: Rigid body (translation + rotation only, no scaling)

#### Distance Calculation
- Point-to-surface distance using `vtkCellLocator`
- Unsigned distance (always positive)
- Calculated from comparison mesh points to reference surface

### Data Format

The tool uses VTK's native readers:
- PLY: `vtkPLYReader`
- STL: `vtkSTLReader`

Both ASCII and binary formats are supported.

## Citation

If you use this tool in your research, please cite:

```
[Your publication details]
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Choose appropriate license - e.g., MIT, BSD, Apache 2.0]

## Authors

- Your Name - [Your Institution]

## Acknowledgments

- Developed using 3D Slicer Python API
- VTK library for mesh processing
- Pandas for data export

## Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact: [your email]

## Version History

### Version 1.0.0 (Initial Release)
- Batch processing of PLY/STL file pairs
- Landmark-based + ICP registration
- Multiple distance metrics
- Heatmap generation
- Excel export

## Screenshots

[Add screenshots here showing:]
1. Module interface
2. Landmark placement
3. Aligned meshes
4. Heatmap visualization
5. Excel results

---

**Keywords**: mesh comparison, surface distance, Hausdorff distance, ICP registration, 3D Slicer, mesh validation, surface analysis, scientific mesh comparison
