# Contributing to Mesh Comparison Tool

Thank you for your interest in contributing to the Mesh Comparison Tool! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/MeshComparisonTool.git
   cd MeshComparisonTool
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Requirements

- 3D Slicer 5.0 or later
- Python 3.9+ (included with Slicer)
- Git

### Testing Your Changes

1. Install the module in Slicer using drag-and-drop or Application Settings
2. Enable Developer Mode:
   - Edit → Application Settings → Developer → Enable developer mode
3. Use the "Reload" button to test changes without restarting Slicer

## Code Style

### Python

- Follow PEP 8 style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all functions and classes

### Example:

```python
def calculateDistances(self, referenceNode, comparisonNode, filename, outputDir):
    """
    Calculate all distance metrics and generate heatmap
    
    Parameters:
    -----------
    referenceNode : vtkMRMLModelNode
        The reference mesh node
    comparisonNode : vtkMRMLModelNode
        The comparison mesh node
    filename : str
        Name of the file being processed
    outputDir : str
        Directory for output files
        
    Returns:
    --------
    dict
        Dictionary containing all calculated metrics
    """
    # Implementation...
```

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (Add, Fix, Update, etc.)
- Reference issue numbers when applicable

### Good Examples:
```
Add support for OBJ file format
Fix ICP convergence issue for large meshes
Update documentation with new screenshots
```

### Bad Examples:
```
Changed stuff
bug fix
updates
```

## Pull Request Process

1. **Before submitting**:
   - Test your changes thoroughly
   - Update documentation if needed
   - Add entry to CHANGELOG.md
   - Ensure code follows style guidelines

2. **Submitting**:
   - Create a pull request from your fork
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

3. **Review process**:
   - Maintainers will review your PR
   - Address any requested changes
   - Once approved, your changes will be merged

## Types of Contributions

### Bug Reports

When reporting bugs, please include:
- Slicer version
- Operating system
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots if applicable
- Error messages from Python console

**Template**:
```markdown
**Slicer Version**: 5.2.2
**OS**: macOS 13.0

**Steps to Reproduce**:
1. Load file pair
2. Set landmarks
3. Click "Perform Alignment"

**Expected**: Meshes should align
**Actual**: Error message appears

**Error Message**:
[Paste error from console]

**Screenshots**:
[Attach relevant screenshots]
```

### Feature Requests

When requesting features:
- Describe the use case
- Explain why it would be valuable
- Suggest possible implementation (optional)

### Documentation

Documentation improvements are always welcome:
- Fix typos or clarify explanations
- Add examples or screenshots
- Translate to other languages
- Improve code comments

## Testing

### Manual Testing Checklist

Before submitting changes, test:
- [ ] File pair scanning works
- [ ] Loading meshes works
- [ ] Landmark placement works
- [ ] Alignment produces reasonable results
- [ ] Distance calculation completes
- [ ] Heatmap generation works
- [ ] Excel export works
- [ ] Skip and abort functions work
- [ ] UI remains responsive

### Test Data

When testing:
- Use various mesh sizes
- Test with different file naming patterns
- Try both perfect and imperfect alignments
- Test error conditions (missing files, corrupt data, etc.)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unprofessional conduct

## Questions?

If you have questions:
- Check existing issues and documentation
- Open a new issue for discussion
- Contact maintainers: [your-email]

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- CHANGELOG.md for their contributions
- Release notes

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to making mesh comparison better for everyone!
