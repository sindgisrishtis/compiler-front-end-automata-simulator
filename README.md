# 🚀 Compiler Front-End Automata Simulator

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Graphviz](https://img.shields.io/badge/Graphviz-Visualization-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Compiler](https://img.shields.io/badge/Compiler-Front--End-orange)
![TOC](https://img.shields.io/badge/Theory%20of%20Computation-DFA%20%7C%20PDA-purple)

</p>

<p align="center">

An interactive **Compiler Front-End Simulation System** that demonstrates how **Deterministic Finite Automata (DFA)** and **Pushdown Automata (PDA)** are used in modern compiler design for **lexical analysis**, **syntax validation**, and **compiler front-end visualization**.

</p>

---

# 🌐 Live Demo

### 🚀 Try the application here

**https://compiler-front-end-automata-simulator.streamlit.app**

---

# 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Screenshots](#-screenshots)
- [System Architecture](#-system-architecture)
- [Compiler Workflow](#-compiler-workflow)
- [Algorithms & TOC Concepts](#-algorithms--toc-concepts)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Example Input & Output](#-example-input--output)
- [Getting Started](#-getting-started)
- [Docker](#-docker)
- [Deployment](#-deployment)
- [Learning Outcomes](#-learning-outcomes)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

# 📖 Overview

Compiler construction is one of the most practical applications of the **Theory of Computation (TOC)**, yet concepts such as **Deterministic Finite Automata (DFA)**, **Pushdown Automata (PDA)**, **Regular Expressions**, and **Context-Free Grammars (CFG)** are often taught only through mathematical notation and static diagrams.

This project bridges that gap by providing an **interactive compiler front-end simulator** capable of visualizing the complete workflow of lexical and syntax analysis.

The simulator accepts **C-style source code**, performs **lexical analysis** through DFA-based token recognition, validates syntax using **PDA-inspired stack operations**, and presents compiler execution through intuitive visualizations including token streams, state transitions, compiler workflow, and automata concepts.

Instead of simply explaining automata theory, the project demonstrates how these computational models are used inside real compiler front-end systems.

---

# ✨ Features

## 🚀 Compiler Front-End Simulation

- Interactive C-style source code editor
- Real-time lexical analysis
- Syntax validation
- Compiler workflow visualization

---

## 🔤 Lexical Analysis

- DFA-inspired token recognition
- Automatic token generation
- Keyword identification
- Identifier validation
- Numeric literal recognition
- Operator recognition
- Symbol recognition
- Lexical error detection

---

## 📚 Syntax Validation

- PDA-inspired stack simulation
- Balanced parentheses validation
- Nested block verification
- Bracket mismatch detection
- Missing semicolon detection
- Invalid statement detection
- Compiler syntax diagnostics

---

## 📊 Interactive Visualizations

- Token stream visualization
- DFA state simulation
- PDA stack operations
- Compiler architecture diagrams
- Token statistics dashboard
- Automata theory reference

---

## 🎓 Educational Features

- Theory of Computation concepts
- Compiler front-end architecture
- Regular expression examples
- Context-Free Grammar (CFG)
- DFA and PDA explanations
- Interactive learning interface

---

## 🐳 Deployment Ready

- Dockerized application
- Streamlit Cloud deployment
- Cross-platform compatibility
- Easy local setup

---

# 🎥 Demo

> **Demo GIF will be added here.**

The demonstration showcases the complete compiler front-end pipeline:

- Source code input
- Lexical analysis
- Token generation
- DFA visualization
- PDA stack simulation
- Syntax validation
- Compiler output

---

# 📸 Screenshots

## 🏠 Main Interface

<p align="center">
<img src="assets/main-interface.png" width="95%">
</p>

The interactive compiler dashboard allows users to write C-style source code, perform lexical analysis, validate syntax, and visualize compiler front-end operations through an intuitive interface.

---

## 🔤 DFA-Based Lexical Analysis

<p align="center">
<img src="assets/dfa-simulation.png" width="95%">
</p>

The lexical analyzer uses Deterministic Finite Automata (DFA) concepts to recognize programming language tokens including keywords, identifiers, literals, operators, and symbols. Each token follows regular language patterns and is validated through deterministic state transitions.

---

## 📚 PDA-Based Syntax Validation

<p align="center">
<img src="assets/pda-simulation.png" width="95%">
</p>

The syntax validator demonstrates Pushdown Automata (PDA) concepts using stack-based processing to verify balanced delimiters, nested program blocks, and context-free language structures commonly found in compiler front-end parsing.

---

# 🏛 System Architecture

<p align="center">

```text
                    ┌─────────────────────────┐
                    │     Source Code Input   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Streamlit UI        │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┴───────────────────┐
             ▼                                       ▼
┌────────────────────────┐              ┌────────────────────────┐
│     Lexical Analyzer   │              │     Syntax Validator   │
│      (DFA Concepts)    │              │    (PDA + CFG Logic)   │
└────────────┬───────────┘              └────────────┬───────────┘
             │                                       │
             ▼                                       ▼
      Token Generation                     Stack-Based Validation
             │                                       │
             └───────────────────┬───────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │  Compiler Visualization │
                    │ DFA • PDA • Statistics  │
                    └─────────────────────────┘
```

</p>

---

# ⚙ Compiler Workflow

The simulator follows the same logical stages as a traditional compiler front-end.

```text
          Source Code
               │
               ▼
      Lexical Analysis
      (DFA-Based Scanner)
               │
               ▼
        Token Generation
               │
               ▼
     Syntax Validation
     (PDA + CFG Rules)
               │
               ▼
      Compiler Front-End
          Result
```

### Phase 1 – Source Code Input

The user enters a C-style program through the interactive editor.

### Phase 2 – Lexical Analysis

The lexer scans the source code character by character and generates a sequence of tokens using DFA-inspired logic and regular expressions.

### Phase 3 – Token Stream

The generated tokens are categorized into keywords, identifiers, literals, operators, and symbols.

### Phase 4 – Syntax Validation

The parser validates the token sequence using stack-based PDA concepts and Context-Free Grammar (CFG) rules.

### Phase 5 – Compiler Output

The simulator displays lexical validity, syntax validity, detected errors, generated tokens, and compiler statistics.

---

# 🧠 Algorithms & TOC Concepts

## Algorithms Used

- Deterministic Finite Automata (DFA)
- Pushdown Automata (PDA)
- Stack-Based Parsing
- Regular Expression Matching
- Tokenization
- Context-Free Grammar Validation
- Compiler Front-End Simulation

---

## Theory of Computation Concepts

### Deterministic Finite Automata (DFA)

Used for lexical analysis and token recognition.

---

### Pushdown Automata (PDA)

Used for syntax validation through stack-based memory operations.

---

### Regular Expressions

Used to define token patterns including identifiers, keywords, literals, operators, and symbols.

---

### Context-Free Grammar (CFG)

Defines the syntactic structure of declarations, expressions, conditional statements, loops, and program blocks.

---

### Compiler Front-End

Demonstrates the practical application of TOC concepts in lexical analysis and syntax validation.

---

# 💻 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Programming Language | Python 3.11 |
| User Interface | Streamlit |
| Compiler Components | Lexer, Parser |
| Automata Concepts | DFA, PDA |
| Formal Language Theory | Regular Expressions, CFG |
| Visualization | Graphviz |
| Data Processing | Pandas |
| Containerization | Docker |
| Version Control | Git & GitHub |
| Deployment | Streamlit Community Cloud |

---

## Core Functionalities

### Lexical Analysis

- Keyword recognition
- Identifier validation
- Number recognition
- Floating-point literals
- Operators
- Symbols
- Invalid token detection

---

### Syntax Validation

- Parentheses balancing
- Curly brace validation
- Nested block validation
- Missing semicolon detection
- Invalid statement detection
- Stack-based parsing simulation

---

## Supported Language Constructs

- Variable declarations
- Assignment statements
- Arithmetic expressions
- Conditional statements
- For loops
- Return statements
- Nested code blocks
- Compiler syntax checking
# 📁 Project Structure

```
compiler-front-end-automata-simulator/
│
├── app.py                  # Streamlit application entry point
├── lexer.py                # DFA-inspired lexical analyzer
├── parser.py               # PDA-inspired syntax validator
├── simulator.py            # Compiler simulation engine
├── automata.py             # DFA and PDA implementation logic
├── diagrams.py             # Graphviz automata visualization
├── utils.py                # Helper functions
│
├── assets/
│   ├── main-interface.png
│   ├── dfa-simulation.png
│   ├── pda-simulation.png
│   └── architecture.png
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── LICENSE (optional)
```

---

# 📂 Folder Description

| File / Folder | Description |
|---------------|-------------|
| **app.py** | Main Streamlit application and user interface |
| **lexer.py** | Performs lexical analysis using DFA-inspired logic and regular expressions |
| **parser.py** | Validates syntax using PDA-inspired stack operations and CFG rules |
| **simulator.py** | Integrates lexical and syntax analysis into a compiler front-end workflow |
| **automata.py** | Implements automata state transitions and simulation logic |
| **diagrams.py** | Generates DFA and PDA visualizations using Graphviz |
| **utils.py** | Utility functions and helper methods |
| **assets/** | Project screenshots and visual resources |
| **Dockerfile** | Docker configuration for containerized deployment |
| **requirements.txt** | Python package dependencies |

---

# 💡 Example Input & Output

## Valid Program

```c
int a = 10;

if(a > 5){
    a = a + 1;
}
```

### Compiler Output

```text
✓ Lexically Valid

✓ Syntactically Valid

Generated Tokens

KEYWORD      int
IDENTIFIER   a
OPERATOR     =
NUMBER       10
SYMBOL       ;

KEYWORD      if
SYMBOL       (
IDENTIFIER   a
OPERATOR     >
NUMBER       5
SYMBOL       )

SYMBOL       {
IDENTIFIER   a
OPERATOR     =
IDENTIFIER   a
OPERATOR     +
NUMBER       1
SYMBOL       ;
SYMBOL       }
```

---

## Invalid Program

```c
int 1abc = 10;
```

### Compiler Output

```text
✗ Lexical Error

UNKNOWN TOKEN

1abc

Reason:
Identifiers cannot begin with a numeric digit.
```

---

## Missing Semicolon

```c
int a = 10
```

### Compiler Output

```text
✗ Syntax Error

Missing semicolon ';'
```

---

## Bracket Mismatch

```c
if(a > 5{

    a = a + 1;

}
```

### Compiler Output

```text
✗ Syntax Error

Bracket mismatch detected.

Expected ')'
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.11 or above
- Git
- Graphviz
- Streamlit

---

## Clone the Repository

```bash
git clone https://github.com/sindgisrishtis/compiler-front-end-automata-simulator.git

cd compiler-front-end-automata-simulator
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

# 🐳 Docker

The project includes full Docker support for consistent deployment across different environments.

---

## Build Docker Image

```bash
docker build -t compiler-front-end-automata .
```

---

## Run Docker Container

```bash
docker run -p 8501:8501 compiler-front-end-automata
```

---

Open your browser and visit

```
http://localhost:8501
```

---

# ☁️ Deployment

The application is publicly deployed using **Streamlit Community Cloud**.

### 🌐 Live Application

https://compiler-front-end-automata-simulator.streamlit.app

The deployment automatically updates whenever new changes are pushed to the GitHub repository.

---

## Deployment Features

- Docker Support
- Streamlit Cloud Deployment
- Cross-Platform Compatibility
- GitHub Integration
- Automatic Redeployment
- Responsive User Interface
- Browser-Based Execution
  # 🎓 Learning Outcomes

This project strengthened both theoretical understanding and practical implementation of compiler front-end systems and formal language concepts.

## Compiler Design

- Implemented lexical analysis using DFA-inspired state transitions.
- Developed syntax validation using PDA-inspired stack operations.
- Simulated compiler front-end processing for C-style source code.
- Designed token generation and syntax error reporting mechanisms.

---

## Theory of Computation

- Applied Deterministic Finite Automata (DFA) for lexical analysis.
- Applied Pushdown Automata (PDA) concepts for syntax validation.
- Used Regular Expressions for token recognition.
- Implemented Context-Free Grammar (CFG) rules for program validation.
- Understood the relationship between formal languages and compiler construction.

---

## Software Engineering

- Developed an interactive web application using Streamlit.
- Created modular Python components for lexer, parser, and automata simulation.
- Visualized compiler stages through Graphviz diagrams.
- Containerized the application using Docker.
- Deployed the application using Streamlit Community Cloud.
- Managed project development using Git and GitHub.

---

# 🚀 Future Enhancements

The current project focuses on compiler front-end simulation. Future versions can extend the implementation toward a complete compiler pipeline.

## Planned Improvements

- Abstract Syntax Tree (AST) generation
- Symbol Table implementation
- Semantic Analysis
- Type Checking
- Intermediate Code Generation (Three Address Code)
- Parse Tree visualization
- CFG-based recursive descent parser
- Support for functions and arrays
- Enhanced compiler diagnostics and error recovery
- Additional programming language constructs
- Dark/Light theme support
- Animated compiler execution timeline

---

# 🌟 Highlights

- Interactive Compiler Front-End Simulator
- DFA-Based Lexical Analysis
- PDA-Based Syntax Validation
- Context-Free Grammar Demonstration
- Compiler Architecture Visualization
- Streamlit Web Application
- Graphviz Automata Diagrams
- Dockerized Deployment
- Live Cloud Deployment
- Educational Compiler Design Tool

---

# 📊 Project Metrics

| Feature | Status |
|----------|--------|
| C-Style Language Support | ✅ |
| DFA-Based Token Recognition | ✅ |
| PDA-Based Syntax Validation | ✅ |
| Regular Expression Matching | ✅ |
| Context-Free Grammar Validation | ✅ |
| Token Stream Generation | ✅ |
| Syntax Error Detection | ✅ |
| Interactive Dashboard | ✅ |
| Docker Support | ✅ |
| Cloud Deployment | ✅ |

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

If you would like to enhance the project, feel free to:

- Fork the repository
- Create a feature branch
- Commit your changes
- Open a Pull Request

---

# 👩‍💻 Author

**Srishti Sindgi**

Artificial Intelligence & Machine Learning Undergraduate  
BMS Institute of Technology and Management

**GitHub**

https://github.com/sindgisrishtis

**Project Repository**

https://github.com/sindgisrishtis/compiler-front-end-automata-simulator

**Live Demo**

https://compiler-front-end-automata-simulator.streamlit.app

---

# ⭐ If you found this project useful

If this repository helped you understand compiler front-end design, automata theory, or Theory of Computation concepts, consider giving it a ⭐ on GitHub.

It helps the project reach more students and developers interested in compiler construction and formal language theory.
