# Hindi Programming Language

## Overview

This project is an **AI-assisted Hindi compiler** that allows users to write programs in **Hindi (Devanagari script)** and execute them seamlessly. The system demonstrates **human-in-the-loop agentic AI behavior**, converting natural language instructions into executable code with minimal manual intervention.  

Users can write specifications in **Hindi**, which are automatically translated, processed by an AI model (Google Gemini), compiled into **LLVM IR**, and executed in real-time. This pipeline showcases **multi-lingual code synthesis**, lexical analysis, parsing, and just-in-time (JIT) execution.

---

## Features

- **Multi-lingual Input:** Accepts Hindi programs written in Devanagari script and also in the following syntax:
## Hindi DSL Grammar Tokens

| Hindi Keyword | Token Type       | Description                     |
|---------------|----------------|---------------------------------|
| `maanlo`      | LET            | Variable declaration            |
| `barabar`     | EQ             | Assignment operator (`=`)       |
| `ant`         | SEMICOLON      | Statement terminator (`;`)      |
| `kaarya`      | FN             | Function declaration            |
| `wapis`       | RETURN         | Return statement                |
| `teer`        | ARROW          | Function return type indicator (`->`) |
| `ank`         | TYPE           | Integer type                    |
| `agar`        | IF             | Conditional `if` statement      |
| `warna`       | ELSE           | Conditional `else` statement    |
| `satya`       | TRUE           | Boolean literal `true`          |
| `asatya`      | FALSE          | Boolean literal `false`         |
| `jab`         | WHILE          | While loop statement             |  

An example is shown below:

```hindi
 kaarya mukhya() -> ank {
maanlo i : ank barabar 1 ant
jab i <= 10 {
likho("%d\n", i) ant
i barabar i + 1 ant
}
wapis 0 ant
}


The same can also be written as:


कार्य मुख्य() -> अंक {

    मान लो a : अंक = 0 अंत
    जब a < 10 {
        लिखो("a = %d \n", a) अंत
        a बराबर a + 1 अंत
    }

}


- **AI-Assisted Code Generation:** Uses Google Gemini to convert Hindi instructions to Hindi DSL code.  
- **Translation Support:** Automatically translates Hindi natural language input to English before AI code generation.  
- **Lexer & Parser:** Converts code into an abstract syntax tree (AST) for compilation.  
- **LLVM IR Compilation:** Compiles Hindi DSL programs into LLVM intermediate representation.  
- **JIT Execution:** Runs compiled code and returns results in real-time.  
- **Debugging Options:** Lexer, parser, and compiler debug modes to inspect token streams, AST, and LLVM IR.  

---

## Getting Started

### Prerequisites

- Python 3.12+
- [llvmlite](https://llvmlite.readthedocs.io/en/latest/)
- [deep-translator](https://pypi.org/project/deep-translator/)
- Google Gemini API credentials
- `pip install` the following packages:

```bash
pip install llvmlite deep-translator google-genai python-dotenv