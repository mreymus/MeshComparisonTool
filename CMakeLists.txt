cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(MeshComparisonTool)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/yourusername/MeshComparisonTool")
set(EXTENSION_CATEGORY "Surface Models")
set(EXTENSION_CONTRIBUTORS "Your Name (Your Institution)")
set(EXTENSION_DESCRIPTION "Batch comparison of PLY (reference) and STL (comparison) mesh files with multiple distance metrics suitable for scientific publications.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/yourusername/MeshComparisonTool/master/MeshComparisonTool.png")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/yourusername/MeshComparisonTool/master/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(MeshComparisonTool)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
