# Mesh Comparison Tool - Installation & Setup Guide

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installing 3D Slicer](#installing-3d-slicer)
3. [Installing the Extension](#installing-the-extension)
4. [Verifying Installation](#verifying-installation)
5. [First-Time Setup](#first-time-setup)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **Operating System**: 
  - macOS 10.13 or later
  - Windows 10 or later
  - Linux (Ubuntu 18.04 or later, CentOS 7 or later)

- **RAM**: 8 GB minimum, 16 GB recommended

- **Disk Space**: 
  - 2 GB for 3D Slicer installation
  - Additional space for your mesh files and results

- **Display**: 1920x1080 resolution or higher recommended

### Recommended Requirements

- **RAM**: 32 GB for large mesh datasets
- **Graphics**: Dedicated GPU with OpenGL 3.2+ support
- **CPU**: Multi-core processor (4+ cores)

---

## Installing 3D Slicer

### Step 1: Download 3D Slicer

1. Visit the official website: **https://www.slicer.org**

2. Click on "Download" button

3. Select your operating system:
   - **macOS**: Download the .dmg file
   - **Windows**: Download the .exe installer
   - **Linux**: Download the .tar.gz archive

### Step 2: Install 3D Slicer

#### macOS Installation

1. Open the downloaded .dmg file
2. Drag the Slicer application to your Applications folder
3. Open Applications folder
4. Right-click on Slicer → "Open"
5. Click "Open" in the security dialog (first launch only)

#### Windows Installation

1. Run the downloaded .exe installer
2. Follow the installation wizard
3. Choose installation directory (default recommended)
4. Click "Install"
5. Launch 3D Slicer from Start Menu

#### Linux Installation

```bash
# Extract the archive
tar -xzvf Slicer-*-linux-amd64.tar.gz

# Move to preferred location
sudo mv Slicer-* /opt/Slicer

# Create symbolic link (optional)
sudo ln -s /opt/Slicer/Slicer /usr/local/bin/Slicer

# Launch Slicer
Slicer
```

### Step 3: Verify 3D Slicer Installation

1. Launch 3D Slicer
2. You should see the welcome screen
3. Close any welcome popups
4. The main interface should be visible

---

## Installing the Extension

### Method 1: Drag & Drop Installation (Easiest)

This is the recommended method for most users.

#### Step 1: Download the Extension

1. Go to GitHub repository: [your-repository-url]
2. Click on "Code" → "Download ZIP"
3. Extract the ZIP file
4. Locate the file: `MeshComparisonTool/MeshComparisonTool/MeshComparisonTool.py`

#### Step 2: Install via Drag & Drop

1. Launch 3D Slicer
2. Locate the `MeshComparisonTool.py` file in your file manager
3. **Drag and drop** the file into the Slicer window
4. A dialog appears: "Add Python scripted modules?"
5. Select "Add Python scripted modules to the application"
6. Click "OK"
7. In the next dialog, ensure "MeshComparisonTool" is checked
8. **Check** "Add selected modules to 'Additional module paths'"
9. Click "Yes"

#### Step 3: Verify Installation

1. In Slicer, click the modules dropdown (shows "Welcome to Slicer")
2. Navigate to: **Surface Models** → **Mesh Comparison Tool**
3. The module interface should load

### Method 2: Manual Installation via Application Settings

Use this method if drag & drop doesn't work.

#### Step 1: Download the Extension

1. Download the complete repository from GitHub
2. Extract to a permanent location on your computer
   - Example (Mac): `/Users/YourName/Documents/SlicerExtensions/MeshComparisonTool`
   - Example (Windows): `C:\SlicerExtensions\MeshComparisonTool`
   - Example (Linux): `~/SlicerExtensions/MeshComparisonTool`

**Important**: Do not move or delete this folder after installation!

#### Step 2: Configure Slicer

1. Launch 3D Slicer
2. Go to: **Edit** → **Application Settings**
3. Select **Modules** in the left panel
4. Under "Additional module paths", click the **>>** button
5. Navigate to and select the `MeshComparisonTool/MeshComparisonTool` folder
   - **Not** the main MeshComparisonTool folder
   - **Yes** the subfolder named MeshComparisonTool
6. Click "OK"
7. **Restart 3D Slicer**

#### Step 3: Verify Installation

1. After restart, click the modules dropdown
2. Navigate to: **Surface Models** → **Mesh Comparison Tool**
3. The module interface should load

### Method 3: Development Installation (For Developers)

For active development and testing.

#### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/MeshComparisonTool.git
cd MeshComparisonTool
```

#### Step 2: Enable Developer Mode

1. Launch 3D Slicer
2. Go to: **Edit** → **Application Settings** → **Developer**
3. Check: **"Enable developer mode"**
4. Click "OK"
5. **Restart Slicer**

#### Step 3: Add Module Path

Follow Method 2, Step 2 above to add the module path.

#### Step 4: Development Features

With developer mode enabled:
- "Reload" button appears at top of module
- Can edit code and reload without restarting Slicer
- "Edit" button opens module code in text editor

---

## Verifying Installation

### Quick Verification Checklist

✅ **Module appears in list**
- Open modules dropdown
- Find "Surface Models" category
- See "Mesh Comparison Tool" listed

✅ **Module loads without errors**
- Select the module
- Interface appears
- No error messages in Python console

✅ **All UI elements present**
- Input/Output Settings section
- File Pairs section
- Workflow section
- Results section

### Checking Python Console

1. In Slicer, go to: **View** → **Python Interactor**
2. Python console appears at bottom
3. Type: `import MeshComparisonTool`
4. Press Enter
5. No error should appear

### Test Installation

1. Open the module
2. Try clicking "Scan for File Pairs" (will show error if no directory selected - this is normal)
3. If button responds, installation is successful

---

## First-Time Setup

### Python Dependencies

The extension automatically installs required packages on first use:
- pandas
- openpyxl

**First-time users**: The first time you export to Excel, there may be a brief delay (10-30 seconds) while these packages are installed automatically.

### Setting Up Your Workspace

1. **Create project folders**:
   ```
   MyProject/
     ├── input/        ← Place your PLY and STL files here
     └── output/       ← Results will be saved here
   ```

2. **Organize your files**:
   - Reference files: `.ply` format
   - Comparison files: `.stl` format
   - Matching names: `model1.ply` and `model1.stl`

3. **Test with sample data**:
   - Start with 1-2 file pairs
   - Verify workflow before batch processing

---

## Troubleshooting

### Module Doesn't Appear

**Problem**: Module not in list after installation

**Solutions**:
1. **Restart 3D Slicer completely**
   - Quit application
   - Relaunch

2. **Check module path**:
   - Edit → Application Settings → Modules
   - Verify path is correct
   - Path should point to `MeshComparisonTool/MeshComparisonTool/` subfolder

3. **Check Python console for errors**:
   - View → Python Interactor
   - Look for red error messages
   - Copy error and search documentation

### Module Loads with Errors

**Problem**: Error messages when loading module

**Solutions**:
1. **Check file structure**:
   ```
   MeshComparisonTool/
     ├── MeshComparisonTool/
     │   ├── MeshComparisonTool.py       ← Must exist
     │   ├── Resources/
     │   │   ├── UI/
     │   │   │   └── MeshComparisonTool.ui   ← Must exist
     │   │   └── Icons/
     │   │       └── MeshComparisonTool.png  ← Must exist
     ```

2. **Verify file permissions** (Linux/Mac):
   ```bash
   chmod +x MeshComparisonTool/MeshComparisonTool/*.py
   ```

3. **Check Slicer version**:
   - Help → About 3D Slicer
   - Must be version 5.0 or later

### Drag & Drop Not Working

**Problem**: Dragging .py file does nothing

**Solutions**:
1. **Use Method 2** (Application Settings) instead

2. **Check file extension**:
   - Must be `.py` file
   - Not `.txt` or other extension

3. **Try different approach**:
   - File → Add Data
   - Select the .py file
   - Choose "Module" as data type

### "Module not found" Error

**Problem**: Error: "No module named 'MeshComparisonTool'"

**Solutions**:
1. **Check module path** is added correctly

2. **Ensure folder name** is exactly `MeshComparisonTool`
   - Case sensitive on Linux/Mac

3. **Restart Slicer** after adding path

### UI File Missing Error

**Problem**: Error about .ui file not found

**Solution**:
Ensure complete folder structure with Resources/UI/ subfolder containing MeshComparisonTool.ui

### macOS Security Warning

**Problem**: Mac won't open Slicer - "unidentified developer"

**Solution**:
1. Right-click on Slicer app
2. Select "Open"
3. Click "Open" in security dialog
4. This is only needed once

### Linux Library Errors

**Problem**: Missing library errors on Linux

**Solutions**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libgl1-mesa-glx libglib2.0-0

# CentOS/RHEL
sudo yum install mesa-libGL glib2
```

---

## Getting Help

### Documentation

- **README.md**: Full documentation
- **QUICKSTART.md**: Quick start guide
- **USER_MANUAL.md**: User Manual
- **REFERENCES.md**: Scientific background

### Support Channels

1. **GitHub Issues**: Report bugs or request features
   - [your-repository-url]/issues

2. **3D Slicer Forum**: General Slicer questions
   - https://discourse.slicer.org

3. **Email Support**: [your-email]

### Useful Commands

**Check Python packages**:
```python
# In Slicer Python console
import pandas
import openpyxl
print("Packages OK")
```

**Check module location**:
```python
# In Slicer Python console
import MeshComparisonTool
print(MeshComparisonTool.__file__)
```

**View module list**:
```python
# In Slicer Python console
import slicer
modules = slicer.moduleNames
print("Mesh Comparison Tool" in modules)
```

---

## Next Steps

After successful installation:

1. ✅ Read [QUICKSTART.md](QUICKSTART.md)
2. ✅ Prepare your first file pair
3. ✅ Run your first comparison
4. ✅ Read full [README.md](README.md) for details

---

## Updating the Extension

### To Update

1. **Download new version** from GitHub
2. **Replace old files** with new ones
3. **Restart Slicer**
4. Module automatically uses new version

### To Uninstall

#### Method 1 (Drag & Drop Installation)
1. Edit → Application Settings → Modules
2. Find path in "Additional module paths"
3. Select and click **<<** to remove
4. Delete downloaded files
5. Restart Slicer

#### Method 2 (Manual Installation)
1. Remove folder from disk
2. Edit → Application Settings → Modules
3. Remove path from "Additional module paths"
4. Restart Slicer

---

**Installation Complete!** 🎉

You're now ready to start comparing meshes. Proceed to [QUICKSTART.md](QUICKSTART.md) for your first comparison.
