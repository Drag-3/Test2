Here’s a quick log of what you’ve worked on and tried so far for your senior project:

### **General Overview:**
You are developing a custom programming language with the following components:
- **Custom AST (Abstract Syntax Tree)** for representing program structure.
- **Parser** based on PLY for transforming code into the AST.
- **Custom exceptions** for error handling in the language (SLBaseException, SLException, ParserError, etc.).
- **Primitive types** (int, float, string, boolean) with the option to add more or allow custom types.
- **Custom symbol tables** for managing variable and function declarations.
- **Node-based execution logic** for evaluating programs.

### **Things You’ve Worked On and Tested:**

1. **AST Structure:**
   - **PrimitiveDataNode** for primitive values (int, float, bool, string).
   - **ArrayNode** for array structures with type checking and evaluation.
   - **Control Flow Nodes** like `IfNode`, `WhileNode`, `ForNode`, and `TryCatchNode`.
   - **LambdaNode** and **ApplyNode** for lambda functions and their application.
   - **FunctionNode** and **FunctionCallNode** for function definition and invocation.

2. **Parser and Lexing:**
   - You have implemented the lexer and the PLY parser to parse your language’s syntax and generate AST nodes.
   - **Grammar Testing** to ensure that the PLY parser correctly translates code into the correct AST structure.
   
3. **Context and Symbol Table:**
   - **Global and Local Symbol Tables** are designed to manage variables, constants, and functions.
   - **SymbolTableEntry** handles variable types, values, and constants.
   - **Context class** for managing function calls, recursion depth, and block scope.

4. **Exception Handling:**
   - You’ve developed a custom exception hierarchy and are handling errors like:
     - VariableNotDeclaredError for uninitialized variables.
     - ParserError for syntax or logical issues in AST generation.
     - Custom return exceptions to handle function returns even in complex scenarios (e.g., nested control flow).
   
5. **Return Handling in Functions:**
   - You’ve refactored the `ReturnNode` and `FunctionNode` logic to ensure that `ReturnException` is caught and returned correctly, even within nested blocks (e.g., inside `IfNode` or `WhileNode`).
   
6. **Execution Logic:**
   - The overall logic in your nodes evaluates to return values and manage block entry and exit via the `Context`.
   - Control flow nodes like `IfNode` have been modified to not return values directly but pass return values through nested blocks to the function handler.

### **Things You’ve Tried (Including Failures and Fixes):**

1. **Type Checking Issues:**
   - You encountered a problem where types were not being set or checked correctly during variable assignments. You adjusted the `update()` method to handle missing types and mismatches.

2. **Function Invocation Bug:**
   - You ran into issues where `FunctionNode` and `FunctionCallNode` would not correctly handle argument lists, especially empty argument lists, which you fixed by updating the argument handling logic.

3. **Return Handling in Nested Blocks:**
   - You had difficulty managing `ReturnNode` propagation through nested structures like `IfNode`. The issue was resolved by catching the return exception and ensuring block-level return management.

4. **Performance and Test Coverage:**
   - You started writing tests for the AST model, adding additional test coverage for corner cases. There’s ongoing benchmarking and performance analysis to ensure efficient execution.

5. **Splitting Codebase for Better Organization:**
   - You started reorganizing the codebase by moving nodes and core logic into separate files (e.g., structure nodes, flow control nodes, primitives).

6. **Future Implementation Plans:**
   - **Lambda logic** is planned for final implementation in the parser.
   - You will be adding more complex types and potentially user-defined custom types.
   - **Stream processing functions** and system I/O logic are upcoming, planned for October.

This log can be continuously updated as you work on more features or fix any additional issues.