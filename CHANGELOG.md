# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-09

### Added
- Initial release of Mesh Comparison Tool
- Batch processing of PLY/STL file pairs
- Manual 3-point landmark placement for initial alignment
- Automatic ICP fine registration
- Visual verification workflow before distance calculation
- Multiple distance metrics calculation:
  - Hausdorff Distance (maximum)
  - RMS Distance
  - Mean Absolute Distance
  - Median Distance
  - 95th Percentile Distance
- Automatic heatmap generation and export as PNG
- Excel export of all metrics with transformation matrix
- Support for abort/skip during batch processing
- Comprehensive documentation in English and German
- User interface with collapsible sections
- Progress tracking for batch processing

### Technical Details
- VTK-based mesh loading for PLY and STL formats
- Landmark-based rigid transformation
- ICP algorithm for precise alignment
- Point-to-surface distance calculation
- Unsigned distance metrics for non-watertight meshes
- Automatic installation of Python dependencies (pandas, openpyxl)

### Documentation
- README.md (English)
- USER_MANUAL.md (User Manual)
- Inline code documentation
- GitHub-ready repository structure

## [Unreleased]

### Planned Features
- Support for additional mesh formats (OBJ, OFF)
- Configurable ICP parameters
- Statistical summary report generation
- Batch export of multiple heatmap views
- Command-line interface for automation
- Distance histogram visualization
- Signed distance option for watertight meshes
- Multi-view heatmap export (front, back, side views)
