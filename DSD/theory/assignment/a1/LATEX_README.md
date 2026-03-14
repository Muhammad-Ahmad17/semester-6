# LaTeX and PDF Documentation

## Overview

This directory now contains a professional LaTeX document with high-end diagrams for Assignment 1, compiled into a beautiful PDF.

## Files Created

### 1. **Assignment_1_Solution.tex** (Main LaTeX Source)
- Complete LaTeX source code with professional formatting
- Uses TikZ and CircuiTikZ for high-quality circuit diagrams
- Professional state diagrams using TikZ automata library
- Booktabs for beautiful tables
- Tcolorbox for highlighted sections
- Full 17-page document with comprehensive solutions

### 2. **Assignment_1_Solution.pdf** (Compiled PDF - 212KB)
- 17-page professionally formatted document
- High-quality vector graphics (not ASCII art!)
- All diagrams are publication-ready
- Professional typography and layout

### 3. **.gitignore**
- Excludes LaTeX auxiliary files (.aux, .log, .toc, etc.)
- Keeps the important files (.tex and .pdf)

## Features

### Professional Circuit Diagrams

The LaTeX document includes:

#### Question 1: Fuel Sensor Circuit
- **2×4 Decoder Symbol** - Professional CircuiTikZ diagram
- **Complete 5-Decoder Hierarchical Circuit** - Color-coded TikZ diagram showing all connections
- **Truth Tables** - Using booktabs for professional formatting
- **Verification Tables** - Clear presentation of test cases

#### Question 2: Photo Booth FSM
- **State Diagram** - Beautiful TikZ automata with curved transitions
- **State Transition Table** - Professional multirow/multicolumn formatting
- **Block Diagram** - System architecture with TikZ
- **All transitions clearly labeled** with inputs and outputs

#### Question 3: Sequence Controller FSM
- **Part (a) State Diagram** - Stop/Reset behavior with color coding
- **Part (b) State Diagram** - 3-cycle postpone with pause states
- **Part (c) System Architecture** - Counter integration with MSI components
- **All diagrams use professional symbols and layouts**

### Professional Formatting Features

1. **Color-Coded Sections**
   - Blue boxes for decoder circuits
   - Green boxes for normal FSM states
   - Orange/Yellow boxes for different components
   - Red boxes for pause states
   - Tcolorbox for important notes

2. **Typography**
   - Professional headers and footers (fancyhdr)
   - Table of contents
   - Proper equation numbering
   - Mathematical notation using amsmath
   - Consistent spacing and margins

3. **Tables**
   - Booktabs for publication-quality tables
   - Truth tables with clear separators
   - State transition tables with multirow support
   - Alignment optimized for readability

4. **Document Structure**
   - Cover page with course information
   - Table of contents
   - Prerequisite knowledge section
   - Three main questions with subsections
   - Summary and conclusion

## How to Compile

### Prerequisites
```bash
sudo apt-get install texlive-latex-extra texlive-fonts-recommended texlive-pictures texlive-science
```

### Compilation Commands
```bash
# First pass
pdflatex Assignment_1_Solution.tex

# Second pass (for references and TOC)
pdflatex Assignment_1_Solution.tex

# Or use latexmk for automatic compilation
latexmk -pdf Assignment_1_Solution.tex
```

### Single Command
```bash
pdflatex -interaction=nonstopmode Assignment_1_Solution.tex
```

## LaTeX Packages Used

### Core Packages
- `inputenc` - UTF-8 encoding
- `geometry` - Page margins
- `amsmath, amssymb` - Mathematical symbols and equations
- `graphicx` - Image inclusion

### Diagram Packages
- `tikz` - Vector graphics engine
- `circuitikz` - Circuit diagrams
- `tikzlibrary{shapes,arrows,positioning,automata,calc,fit,backgrounds}` - TikZ extensions

### Table Packages
- `booktabs` - Professional tables
- `array` - Extended table features
- `multirow` - Multi-row cells

### Layout Packages
- `float` - Figure positioning
- `enumitem` - List customization
- `fancyhdr` - Headers and footers
- `tcolorbox` - Colored boxes
- `xcolor` - Color support

### Specialized Packages
- `karnaugh-map` - K-map support (included but not heavily used)

## Diagram Quality Comparison

### Before (ASCII Diagrams)
```
                    ┌──────────────┐
         G₃ ────────┤A₁            │
         G₂ ────────┤A₀   DEC 1    │
         1  ────────┤E   (2×4)     │
                    └──────────────┘
```

### After (TikZ/CircuiTikZ)
- Vector graphics that scale perfectly
- Professional circuit symbols
- Color coding for different sections
- Publication-ready quality
- Can be zoomed infinitely without pixelation

## Document Statistics

- **Total Pages:** 17
- **File Size:** 212 KB (very efficient!)
- **Figures:** 7+ high-quality TikZ diagrams
- **Tables:** 8+ professional tables
- **Equations:** 20+ properly formatted equations
- **Sections:** 3 main questions + prerequisites + summary

## Usage Tips

1. **Viewing the PDF:**
   - Use any PDF viewer (Adobe Reader, Evince, Preview, etc.)
   - Zoom in to see the diagram details - they're vector graphics!
   - Print quality is excellent

2. **Editing the LaTeX:**
   - Modify the .tex file in any text editor
   - VSCode with LaTeX Workshop extension is recommended
   - TeXstudio or Overleaf are also great options

3. **Customization:**
   - Change colors by modifying the `\definecolor` commands
   - Adjust diagram sizes by changing the scale parameter in TikZ
   - Modify table formatting in the tabular environments

## Advantages Over ASCII Diagrams

1. **Professional Appearance:** Publication-ready quality
2. **Scalability:** Vector graphics scale perfectly
3. **Customization:** Easy to change colors, sizes, styles
4. **Portability:** PDF works everywhere
5. **Printing:** Perfect print quality
6. **Academic Standards:** Meets university submission requirements

## Next Steps

You can now:
1. ✅ View the beautiful PDF with high-quality diagrams
2. ✅ Submit this for your assignment
3. ✅ Use this as a template for future LaTeX documents
4. ✅ Modify the diagrams as needed
5. ✅ Learn from the LaTeX code for your own projects

## Support

If you need to modify the diagrams:
- TikZ documentation: https://tikz.dev/
- CircuiTikZ manual: https://ctan.org/pkg/circuitikz
- Overleaf tutorials: https://www.overleaf.com/learn

## License

This document is for educational purposes for the Digital System Design course (CPE344) at your institution.

---

**Generated on:** March 14, 2026
**Course:** CPE344 - Digital System Design
**Assignment:** Assignment 1 - Spring 2026

Enjoy your professional-quality documentation! 🎓✨
