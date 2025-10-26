# Max Ghenis - CV

Professional CV built with modern web technologies, using PolicyEngine's design system.

## Features

- **Markdown source** - Easy to edit and version control
- **Modern HTML/CSS** - Responsive design with PolicyEngine color palette
- **PDF generation** - Automated build script for PDF output
- **Test-driven** - Comprehensive test suite validates CV structure
- **CI/CD** - Automated builds and testing on every commit

## Building

### Prerequisites

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Build Commands

```bash
# Build both HTML and PDF
python build.py

# Build HTML only
python build.py --html

# Build PDF only
python build.py --pdf
```

Output files:
- `cv.html` - Styled HTML version
- `cv.pdf` - PDF version (generated from HTML)

### Testing

```bash
# Run all tests
pytest test_cv.py -v

# Run specific test
pytest test_cv.py::test_cv_has_required_sections -v
```

## Manual PDF Generation

If automated PDF generation fails, you can create a PDF manually:

1. Open `cv.html` in a web browser
2. Print to PDF (Cmd+P on Mac, Ctrl+P on Windows)
3. Save as `cv.pdf`

The CSS is optimized for both screen and print media.

## Project Structure

```
cv/
├── cv.md              # CV content in Markdown
├── template.html      # HTML template with CSS styling
├── build.py           # Build script for HTML/PDF generation
├── test_cv.py         # Test suite
├── requirements.txt   # Python dependencies
├── .github/
│   └── workflows/
│       └── build.yml  # CI workflow
├── cv.html            # Generated HTML (not in git)
└── cv.pdf             # Generated PDF (not in git)
```

## Design

The CV uses the PolicyEngine color palette from [policyengine-app-v2](https://github.com/PolicyEngine/policyengine-app-v2):

- **Primary**: Teal (#319795)
- **Secondary**: Blue (#0EA5E9)
- **Text**: Black (#000000) with gray variants
- **Background**: Light blue (#F5F9FF)

The design is clean, professional, and optimized for both digital viewing and printing.

## Customization

### Content

Edit `cv.md` to update CV content. The file uses standard Markdown syntax.

### Styling

Modify the `<style>` section in `template.html` to customize colors, fonts, spacing, etc.

### Colors

Update CSS variables in `template.html`:

```css
:root {
    --primary-color: #319795;
    --secondary-color: #0EA5E9;
    /* etc. */
}
```

## CI/CD

GitHub Actions automatically:
- Runs tests on every push
- Builds HTML and PDF versions
- Uploads artifacts for download

## License

© 2024 Max Ghenis. All rights reserved.
