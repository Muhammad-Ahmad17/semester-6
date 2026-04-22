# LaTeX Document Writer

Create professional LaTeX presentations (Beamer) and reports. For academic documents, FYP proposals, technical presentations.

---

## 1. Document Classes

```latex
\documentclass[aspectratio=169,11pt]{beamer}    % Presentations
\documentclass[12pt,a4paper]{article}           % Reports/proposals
\documentclass[12pt,a4paper]{report}            % Longer documents (chapters)
```

---

## 2. Color Palette (Use Consistently)

```latex
\definecolor{primary}{RGB}{0,82,147}       % Headings, main elements
\definecolor{secondary}{RGB}{52,152,219}   % Subheadings
\definecolor{accent}{RGB}{39,174,96}       % Input sources, success
\definecolor{highlight}{RGB}{230,126,34}   % Warnings, external systems
\definecolor{danger}{RGB}{231,76,60}       % Alerts, errors
\definecolor{light}{RGB}{236,240,241}      % Backgrounds
```

---

## 3. Compilation

### Why Two Passes?

LaTeX needs two compilation passes:
- **Pass 1**: Builds structure, creates `.aux` files with reference positions
- **Pass 2**: Resolves cross-references (TOC page numbers, figure numbers, `\ref{}`)

Without second pass: `\ref{fig:arch}` shows `??` instead of actual number.

### Quick Compilation

```bash
# Basic (run twice for TOC/references)
pdflatex -interaction=nonstopmode document.tex && pdflatex -interaction=nonstopmode document.tex

# With log capture
pdflatex -interaction=nonstopmode document.tex > /tmp/compile.log 2>&1 && \
pdflatex -interaction=nonstopmode document.tex >> /tmp/compile.log 2>&1

# Check success
[ -f document.pdf ] && echo "✓ PDF created" || echo "✗ Check /tmp/compile.log"
```

### Robust Compilation Script

```bash
#!/bin/bash
# Usage: ./compile.sh document.tex

FILE="${1%.tex}"
LOG="/tmp/${FILE}_compile.log"

compile() {
    pdflatex -interaction=nonstopmode "$FILE.tex" > "$LOG" 2>&1
    return $?
}

echo "Compiling $FILE.tex..."

# Pass 1
compile || { echo "✗ Pass 1 failed"; grep -i "error\|undefined" "$LOG" | head -5; exit 1; }
echo "✓ Pass 1"

# Pass 2
compile || { echo "✗ Pass 2 failed"; grep -i "error\|undefined" "$LOG" | head -5; exit 1; }
echo "✓ Pass 2"

# Verify
[ -f "$FILE.pdf" ] && echo "✓ Created: $FILE.pdf ($(du -h "$FILE.pdf" | cut -f1))" || echo "✗ No PDF"
```

### Troubleshooting

| Error | Fix |
|-------|-----|
| `Missing $ inserted` | Use math mode: `$>$`, `$\times$` |
| `Undefined control sequence` | Missing package (add `\usepackage{}`) |
| `Too many unprocessed floats` | Add `[H]` to figures or `\clearpage` |
| `Overfull hbox` | Use `\resizebox` or shorten content |
| References show `??` | Run pdflatex twice |

---

## 4. TikZ Diagrams: Design Principles

### Core Rules

1. **Single flow direction**: Left→Right or Top→Bottom
2. **No crossing arrows**: Position nodes to avoid intersections
3. **Color hierarchy**: Input=accent, Process=primary, Logic=secondary, Alert=danger, External=highlight
4. **Consistent spacing**: Use `node distance=0.4cm` uniformly
5. **Always scalable**: Wrap in `\resizebox{\textwidth}{!}{...}`

### Base Style Definition

```latex
\begin{tikzpicture}[
    node distance=0.4cm,
    box/.style={rectangle, rounded corners=5pt, draw=#1, fill=#1!10, 
               minimum width=2cm, minimum height=0.8cm, 
               font=\small\bfseries, align=center},
    arrow/.style={-{Stealth}, thick, #1}
]
```

### Pattern: Linear Pipeline

```latex
\node[box=accent] (input) {Camera\\Feed};
\node[box=primary, right=0.6cm of input] (m1) {Model 1};
\node[box=primary, right=0.5cm of m1] (m2) {Model 2};
\node[box=highlight, right=0.6cm of m2] (output) {Output};

\draw[arrow=accent] (input) -- (m1);
\draw[arrow=primary] (m1) -- (m2);
\draw[arrow=highlight] (m2) -- (output);
```

### Pattern: Fan-Out (Branching)

Position branches **vertically** (above/center/below) to avoid crossing:

```latex
\node[box=secondary] (logic) {Logic\\Engine};

% Fan-out: three outputs positioned vertically
\node[box=danger, above right=0.3cm and 0.6cm of logic] (a1) {Alert 1};
\node[box=danger, right=0.6cm of logic] (a2) {Alert 2};
\node[box=danger, below right=0.3cm and 0.6cm of logic] (a3) {Alert 3};

\draw[arrow=danger] (logic) -- (a1);
\draw[arrow=danger] (logic) -- (a2);
\draw[arrow=danger] (logic) -- (a3);
```

### Pattern: Fan-In (Convergence)

```latex
% Multiple inputs converge to single node
\draw[arrow=highlight] (a1) -- (dest);
\draw[arrow=highlight] (a2) -- (dest);
\draw[arrow=highlight] (a3) -- (dest);
```

### Complete Example: Processing Pipeline

```latex
\begin{center}
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
    node distance=0.4cm,
    box/.style={rectangle, rounded corners=5pt, draw=#1, fill=#1!10, 
               minimum width=2cm, minimum height=0.8cm, 
               font=\small\bfseries, align=center},
    arrow/.style={-{Stealth}, thick, #1}
]

% Input
\node[box=accent] (cam) {Camera\\Feed};

% Processing chain
\node[box=primary, right=0.6cm of cam] (m1) {Model 1\\Person};
\node[box=primary, right=0.5cm of m1] (m2) {Model 2\\Pose};
\node[box=primary, right=0.5cm of m2] (m3) {Model 3\\Object};
\node[box=primary, right=0.5cm of m3] (m4) {Model 4\\Face};

% Logic
\node[box=secondary, right=0.6cm of m4] (logic) {Logic\\Engine};

% Alerts (fan-out, positioned vertically)
\node[box=danger, above right=0.3cm and 0.6cm of logic] (a1) {Zone\\Alert};
\node[box=danger, right=0.6cm of logic] (a2) {Loiter\\Alert};
\node[box=danger, below right=0.3cm and 0.6cm of logic] (a3) {Anomaly\\Alert};

% Destination (fan-in)
\node[box=highlight, right=1cm of a2] (cloud) {Cloud\\Server};
\node[box=accent, right=0.6cm of cloud] (dash) {Dashboard};

% Connections
\draw[arrow=accent] (cam) -- (m1);
\draw[arrow=primary] (m1) -- (m2);
\draw[arrow=primary] (m2) -- (m3);
\draw[arrow=primary] (m3) -- (m4);
\draw[arrow=primary] (m4) -- (logic);
\draw[arrow=danger] (logic) -- (a1);
\draw[arrow=danger] (logic) -- (a2);
\draw[arrow=danger] (logic) -- (a3);
\draw[arrow=highlight] (a1) -- (cloud);
\draw[arrow=highlight] (a2) -- (cloud);
\draw[arrow=highlight] (a3) -- (cloud);
\draw[arrow=accent] (cloud) -- (dash);

\end{tikzpicture}
}
\end{center}
```

### Anti-Pattern: Crossing Arrows

```latex
% ❌ DON'T: Random positioning causes chaos
\node (a) {A};
\node[right of=a] (b) {B};
\node[below of=a] (c) {C};
\draw (a) -- (b);
\draw (c) -- (b);  % Crosses other elements
\draw (b) -- (a);  % Circular, confusing

% ✓ DO: Consistent flow direction
\node (a) {A};
\node[right=0.6cm of a] (b) {B};
\node[right=0.6cm of b] (c) {C};
\draw[->] (a) -- (b);
\draw[->] (b) -- (c);  % Clean left-to-right flow
```

---

## 5. Presentation (Beamer)

### Setup

```latex
\documentclass[aspectratio=169,11pt]{beamer}

\usetheme{Madrid}
\usecolortheme{whale}

% Colors
\definecolor{primary}{RGB}{0,82,147}
\definecolor{secondary}{RGB}{52,152,219}
\definecolor{accent}{RGB}{39,174,96}
\definecolor{highlight}{RGB}{230,126,34}
\definecolor{danger}{RGB}{231,76,60}

\setbeamercolor{structure}{fg=primary}
\setbeamercolor{title}{fg=white,bg=primary}
\setbeamercolor{frametitle}{fg=white,bg=primary}

% Packages
\usepackage{tikz}
\usepackage{booktabs}
\usepackage{pgfgantt}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning}

\title{Project Title}
\author{Author Name}
\date{\today}

\begin{document}
```

### Layout Guidelines

| Element | Guideline |
|---------|-----------|
| Margins | 0.5cm all sides, use 0.95\textwidth max |
| Columns | Use 0.45\textwidth each (leave gap) |
| Diagrams | Wrap in `\resizebox{0.95\textwidth}{!}{}` |
| Font | Frame title=28pt, body=11pt, captions=9pt |
| Spacing | 0.2cm after headings, 0.3cm between sections |

### Multi-Slide Topics

When content exceeds one slide, split logically:

```latex
% Slide 1: Introduction
\begin{frame}{Topic - Overview}
    \begin{itemize}
        \item Main concept
        \item Key components
    \end{itemize}
\end{frame}

% Slide 2: Details
\begin{frame}{Topic - Details}
    \begin{itemize}
        \item Technical specification 1
        \item Technical specification 2
    \end{itemize}
\end{frame}

% Slide 3: Summary (optional)
\begin{frame}{Topic - Summary}
    \textbf{Key Takeaways:}
    \begin{itemize}[noitemsep]
        \item Point 1
        \item Point 2
    \end{itemize}
\end{frame}DentalCavityDetection&SeverityAnalysisSystem
```

### Slide Types

**Title Slide:**
```latex
\begin{frame}[plain]
    \titlepage
\end{frame}
```

**Content Slide:**
```latex
\begin{frame}{Frame Title}
    \textbf{Section:}
    \begin{itemize}
        \item Point 1
        \item Point 2
    \end{itemize}
\end{frame}
```

**Two-Column Slide:**
```latex
\begin{frame}{Comparison}
    \begin{columns}[T]
        \column{0.45\textwidth}
        \textbf{Option A}
        \begin{itemize}
            \item Feature 1
        \end{itemize}
        
        \column{0.45\textwidth}
        \textbf{Option B}
        \begin{itemize}
            \item Feature 1
        \end{itemize}
    \end{columns}
\end{frame}
```

**Diagram Slide:**
```latex
\begin{frame}{Architecture}
    \begin{center}
    \resizebox{0.95\textwidth}{!}{%
        \begin{tikzpicture}
            % diagram code
        \end{tikzpicture}
    }
    \end{center}
\end{frame}
```

**Timeline Slide (Gantt):**
```latex
\begin{frame}{Project Timeline}
    \begin{center}
    \resizebox{\textwidth}{!}{%
    \begin{ganttchart}[
        hgrid, vgrid,
        x unit=0.35cm, y unit chart=0.45cm,
        bar/.append style={fill=primary!70},
        title label font=\tiny\bfseries,
        bar label font=\tiny
    ]{1}{32}
    \gantttitle{Weeks 1-32}{32} \\
    \gantttitlelist{1,...,32}{1} \\
    \ganttbar{Phase 1}{1}{8} \\
    \ganttbar{Phase 2}{9}{20} \\
    \ganttbar{Phase 3}{21}{32}
    \end{ganttchart}
    }
    \end{center}
\end{frame}
```

**Thank You Slide:**
```latex
\begin{frame}[plain]
    \begin{center}
        \vspace{2cm}
        {\Huge\textcolor{primary}{\textbf{Thank You}}}
        \vspace{1cm}
        {\Large Questions?}
    \end{center}
\end{frame}
```

---

## 6. Report/Proposal

### Setup

```latex
\documentclass[12pt,a4paper]{article}

\usepackage[margin=0.9in]{geometry}
\usepackage{tikz}
\usepackage{pgfgantt}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{colortbl}
\usepackage{multirow}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{float}
\usepackage{tcolorbox}

\usetikzlibrary{shapes.geometric, arrows.meta, positioning}
\tcbuselibrary{skins,breakable}

% Colors
\definecolor{primary}{RGB}{0,82,147}
\definecolor{secondary}{RGB}{52,152,219}
\definecolor{accent}{RGB}{39,174,96}
\definecolor{highlight}{RGB}{230,126,34}
\definecolor{danger}{RGB}{231,76,60}
\definecolor{light}{RGB}{236,240,241}

% Section formatting
\titleformat{\section}{\Large\bfseries\color{primary}}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries\color{secondary}}{\thesubsection}{1em}{}

% Header/Footer
\pagestyle{fancy}
\fancyhf{}
\lhead{\textcolor{primary}{Project Name}}
\rhead{\textcolor{primary}{Document Type}}
\rfoot{Page \thepage}

\hypersetup{colorlinks=true,linkcolor=primary,urlcolor=secondary}

\begin{document}
```

### Custom Boxes

```latex
% Technical spec box
\newtcolorbox{specbox}[1]{
    colback=primary!5, colframe=primary,
    title=#1, fonttitle=\bfseries,
    rounded corners, boxrule=1pt
}

% Warning box
\newtcolorbox{warningbox}{
    colback=highlight!10, colframe=highlight,
    rounded corners, boxrule=1pt
}

% Usage
\begin{specbox}{Model Specifications}
\textbf{Architecture:} YOLOv8\\
\textbf{Input:} 640×640 RGB\\
\textbf{Output:} Bounding boxes + confidence
\end{specbox}
```

### Title Page

```latex
\begin{titlepage}
\centering
\vspace*{0.5cm}
{\Large\color{primary}\textbf{FYP Proposal}}\\[0.3cm]
\rule{\textwidth}{2pt}\\[0.5cm]
{\Huge\bfseries\color{primary} Project Title}\\[0.3cm]
{\Large Subtitle}\\[0.2cm]
\rule{\textwidth}{2pt}\\[1cm]

\begin{tabular}{rl}
\textbf{Team:} & Member 1 (Role) \\
               & Member 2 (Role) \\[0.3cm]
\textbf{Supervisor:} & Name \\[0.3cm]
\textbf{Duration:} & X Months \\
\end{tabular}

\vfill
{\large Department}\\
{\large Institution}\\[0.3cm]
{\large Year}
\end{titlepage}

\tableofcontents
\newpage
```

### Section Templates

```latex
%===============================================================================
\section{Executive Summary}
%===============================================================================

\begin{tcolorbox}[colback=light,colframe=primary,title=\textbf{Project at a Glance}]
\begin{tabularx}{\textwidth}{lX}
\textbf{Problem:} & Brief statement \\
\textbf{Solution:} & Approach \\
\textbf{Platform:} & Technologies \\
\textbf{Deliverables:} & Expected outputs \\
\end{tabularx}
\end{tcolorbox}

%===============================================================================
\section{Technical Specifications}
%===============================================================================

\begin{specbox}{Component Name}
\textbf{Technology:} Framework\\
\textbf{Input:} Format\\
\textbf{Output:} Format
\end{specbox}

%===============================================================================
\section{Timeline}
%===============================================================================

\begin{center}
\resizebox{\textwidth}{!}{%
\begin{ganttchart}[
    hgrid, vgrid,
    x unit=0.45cm, y unit chart=0.5cm,
    bar/.append style={fill=primary!70},
    group/.append style={fill=accent!70},
    title label font=\tiny\bfseries,
    bar label font=\tiny
]{1}{32}
\gantttitle{Timeline (32 Weeks)}{32} \\
\gantttitlelist{1,...,32}{1} \\
\ganttgroup{Phase 1}{1}{8} \\
\ganttbar{Task 1.1}{1}{4} \\
\ganttbar{Task 1.2}{5}{8} \\
\ganttgroup{Phase 2}{9}{20} \\
\ganttbar{Task 2.1}{9}{14} \\
\ganttbar{Task 2.2}{15}{20}
\end{ganttchart}
}
\end{center}

%===============================================================================
\section{Technology Stack}
%===============================================================================

\begin{center}
\begin{tabular}{lll}
\toprule
\textbf{Layer} & \textbf{Technology} & \textbf{Purpose} \\
\midrule
Frontend & React.js & UI \\
Backend & Node.js & API \\
Database & PostgreSQL & Storage \\
\bottomrule
\end{tabular}
\end{center}
```

---

## 7. Quick Reference

### Text Formatting
```latex
\textbf{Bold}  \textit{Italic}  \texttt{Code}
\textcolor{primary}{Colored}
{\Large Large}  {\small Small}
```

### Math Symbols
```latex
$>$  $<$  $\geq$  $\leq$  $\times$  $\rightarrow$  $\pm$
```

### Lists
```latex
\begin{itemize}[noitemsep]  % Compact list
    \item Item
\end{itemize}
```

### Tables
```latex
\begin{tabular}{lll}
\toprule
\textbf{A} & \textbf{B} & \textbf{C} \\
\midrule
1 & 2 & 3 \\
\bottomrule
\end{tabular}
```

### Spacing
```latex
\vspace{0.3cm}   % Vertical
\hspace{1cm}     % Horizontal
\vfill           % Fill remaining space
\newpage         % Page break
```

### References
```latex
\label{sec:intro}     % Create
\ref{sec:intro}       % Reference
```

---

## 8. Alternative Color Schemes

```latex
% Modern Purple
\definecolor{primary}{RGB}{102,51,153}
\definecolor{secondary}{RGB}{147,112,219}
\definecolor{accent}{RGB}{255,105,180}

% Corporate Green
\definecolor{primary}{RGB}{0,128,0}
\definecolor{secondary}{RGB}{60,179,113}
\definecolor{accent}{RGB}{255,165,0}

% Elegant Dark
\definecolor{primary}{RGB}{44,62,80}
\definecolor{secondary}{RGB}{52,73,94}
\definecolor{accent}{RGB}{241,196,15}
```
