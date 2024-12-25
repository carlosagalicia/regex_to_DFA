# Regex to NFA and DFA Conversion
## Overview
This project implements a program to convert regular expressions into their corresponding NFA (Non-deterministic Finite Automaton) and subsequently into a DFA (Deterministic Finite Automaton). The program includes functionality for:
- Parsing regular expressions with operators like concatenation (.), union (|), Kleene star (*), and Kleene plus (+).
- Constructing an NFA using the Thompson construction algorithm.
- Converting the NFA into a DFA using the subset construction algorithm.
- Visualizing the NFA and DFA states and transitions.

## Key Learning
This project emphasizes several computer science concepts:
- **Regular Expressions:** Parsing and transforming expressions for processing.
- **Finite Automata Theory:** Understanding NFA and DFA construction and differences.
- **Algorithms:** Thompson and subset construction algorithms for finite automata.
- **Data Structures:** Efficient use of lists, sets, and dictionaries for state management.

## Tools and Languages
- **Programming Language:** Python
- **Libraries:** No external libraries are required; the implementation is purely algorithmic.

## Installation and Usage

### Requirements
- Python 3.7 or higher

## Instructions
1. Clone the repository
  ```bash
  git clone https://github.com/carlosagalicia/regex_to_DFA.git
  ```

2. Run the script
  ```bash
  python actividad_integradora_1.py
  ```
3. Input the alphabet and the regular expression when prompted. The program will display the NFA and DFA transitions.

## Example Input and Output
Input:
```bash
  Alphabet: ab
  Regex: ab|a*
```
Output:
```bash
  ---RESULTS---
  INPUT:
  ab|a*
  NFA:
  0 => [(1, 'a')]
  1 => [(2, '#')]
  2 => [(3, 'b')]
  3 => [(9, '#')]
  4 => [(5, 'a')]
  5 => [(4, '#'), (7, '#')]
  6 => [(4, '#'), (7, '#')]
  7 => [(9, '#')]
  8 => [(0, '#'), (6, '#')]
  Accepting state: 9
  DFA:
  A => [('B', 'a')]
  B => [('C', 'a'), ('D', 'b')]
  C => [('C', 'a')]
  D => []
  Accepting states: ['A', 'B', 'C', 'D']
```


