# Quick Start Guide

Get started with Mesh Comparison Tool in 5 minutes!

## 1. Install 3D Slicer

Download and install 3D Slicer from https://www.slicer.org

## 2. Install the Extension

### Easy Method (Drag & Drop)

1. Download `MeshComparisonTool.py` from GitHub
2. Drag the file into Slicer window
3. Click "Yes" when prompted
4. Find module under: `Modules` → `Surface Models` → `Mesh Comparison Tool`

### Alternative Method

1. Download the entire repository
2. In Slicer: `Edit` → `Application Settings` → `Modules`
3. Click `>>` next to "Additional module paths"
4. Select the `MeshComparisonTool` folder
5. Restart Slicer

## 3. Prepare Your Files

Create two folders:
```
YourProject/
  ├── input/
  │   ├── scan1.ply
  │   ├── scan1.stl
  │   ├── scan2.ply
  │   ├── scan2.stl
  │   └── ...
  └── output/  (will be created automatically)
```

**Important**: PLY and STL files must have identical names!

## 4. Run Your First Comparison

### Step 1: Setup
- Open module: `Modules` → `Surface Models` → `Mesh Comparison Tool`
- Select `input/` folder
- Select `output/` folder
- Click "Scan for File Pairs"

### Step 2: Process First Pair
- Click "Load Next Pair"
- Green mesh = Reference (PLY)
- Red mesh = Comparison (STL)

### Step 3: Set Landmarks
- Click "Set Reference Landmarks (Green)"
- Place 3 points on green mesh (click on anatomical features)
- Click "Set Comparison Landmarks (Red)"  
- Place 3 corresponding points on red mesh (same order!)

### Step 4: Align
- Click "Perform Alignment (Landmark + ICP)"
- Rotate view to verify alignment from different angles

### Step 5: Calculate
- If alignment looks good: Click "Accept && Calculate Distances"
- Heatmap is saved automatically
- Next pair loads automatically

### Step 6: Export
- After processing all pairs: Click "Export Results to Excel"
- Find results in `output/mesh_comparison_results.xlsx`
- Find heatmaps in `output/heatmaps/`

## 5. Interpret Results

Open the Excel file:
- **Hausdorff Distance**: Maximum deviation (look for outliers)
- **RMS Distance**: Overall accuracy (most commonly reported)
- **Mean Distance**: Average deviation
- **95th Percentile**: 95% of points are closer than this value

Check heatmaps:
- Blue = good (close match)
- Red = problematic (large deviation)

## Tips for Best Results

✅ **DO**:
- Choose clear anatomical landmarks
- Spread landmarks across the mesh
- Check alignment from multiple angles
- Use consistent landmark selection

❌ **DON'T**:
- Place landmarks on flat surfaces
- Cluster all landmarks in one area
- Accept poor alignments
- Rush the process

## Common Issues

### "No file pairs found"
- Check file names match exactly (except .ply/.stl)
- Ensure files are in the input folder (not subfolders)

### Poor alignment
- Select better landmarks
- Ensure landmarks are in the same order
- Try placing landmarks again

### Module not appearing
- Restart 3D Slicer
- Check Python console for errors
- Verify module path in Application Settings

## Need Help?

- Read full [README.md](README.md)
- Check [User Manual](USER_MANUAL.md)
- Open issue on GitHub
- Contact: [your-email]

## Next Steps

- Read the full documentation for advanced features
- Learn about the scientific background
- Explore workflow customization options
- Consider contributing to the project

---

**Time to first results**: ~5-10 minutes per pair (including landmark placement)

**Happy comparing! 🎉**
