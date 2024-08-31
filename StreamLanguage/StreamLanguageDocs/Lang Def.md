

# Streaming Language Definition 

## Introduction
The Language is designed for efficient, real-time processing and analysis of continuous data streams. 

## Goals
- Provide a simple yet powerful syntax for real-time data stream processing.
- Enable near real-time feedback and analysis of streaming data.

## Language Definition

### Core Concepts
- **Streams**: Represent infinite sequences of data, modeled as queues. Streams will be basis for the data processing.
    - Streams can be created from various sources such as sockets, TCP connections, etc.
    - Streams can be processed and analyzed in real time.
    - Every stream has a single mouth and sink, and work in one direction.
    - The mouth of a stream can be attached to the sink of another stream, creating a chain of streams.
    - The sink of a stream can be attached to a function, which processes the data as it arrives using specified event handlers.
- **Events**: Represent individual data points in a stream. Events are processed asynchronously as they arrive.
- **Functions**: Encapsulate data processing logic, including event handlers for stream processing.
- **Filters**: Special functions that can be attached to streams to process data as it arrives.

### Lexical Structure

#### Identifiers
- Names for variables, functions, etc., consisting of letters, digits, and underscores, not beginning with a digit.

#### Keywords
- `var`: Declare a variable.
- `const`: Define a constant variable.
- `if`, `else`: Conditional statements.
- `for`, `while`: Loop constructs.
- `fn`: Define a function.
- `stream`: Denote a stream data type.

#### Literals
- Support for basic data types: `int`, `float`, `string`, `boolean`.
- `stream`: A special data type representing an infinite sequence of data.

#### Operators
- Basic arithmetic: `+`, `-`, `*`, `/`.
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`.
- Assignment: `=`, `+=`, `-=` etc.
- Boolean: `&&`, `||`, `!`.
- Increment/Decrement: `++`, `--`.
- Stream flow: `>>` for attaching streams.

#### Comments
- Single line: `//`
- Multi-line: `/* ... */`


#### Type System
- A variable's type can be explicitly defined as follows:
    - `var x: int = 5`
    - `var y: float = 3.14`
    - `const z: string = "hello"`
    - `var a: boolean = true`
    - `var b: stream<int>`
- If the type can be inferred, it can be omitted:
    - `const x = 5`
    - `var y = 3.14`
    - `var z = "hello"`
    - `var a = true`
    - `var b = socket.toStream()`
- A function's return type can be explicitly defined:
    - `fn add(a: int, b: int): int { return a + b }`
    - `fn multiply(a: int, b: int): int { return a * b }`
    - `fn divide(a: int, b: int): int { return a / b }`
    - `fn processData(input: int): int { return (input - 32) * 5 / 9 }`
- If the return type can be inferred, it can be omitted:
    - `fn add(a: int, b: int) { return a + b }`
    - `fn multiply(a: int, b: int) { return a * b }`
    - `fn divide(a: int, b: int) { return a / b }`
    - `fn processData(input: int) { return (input - 32) * 5 / 9 }`
- All variables are strongly typed. 
- Variables can be mutable or immutable if declared with `var` or `const`, respectively.
- Function arguments are mutable by default, but can be declared as immutable using `const`.
    - `fn add(const a: int, const b: int): int { return a + b }`
    - `fn multiply(const a: int, const b: int): int { return a * b }`

## V1 Objectives

1. **Variables & Types**: Support basic data types and inferred typing for simplicity.

2. **Control Flow**: Implement `if-else`, `for`, and `while` for basic program logic.

3. **Streams**: Introduce a basic stream concept that supports asynchronous data handling and event-driven processing.

4. **Functions**: Allow the definition of functions, including those handling stream events, to encapsulate data processing logic.

5. **Comments**: Don't run comments in the code.

## Examples 
```code
// Example: Simple stream processing
var dataStream = socket.toStream(); // Create a stream from a socket

fn processData(input: int): int {
    return (input - 32) * 5 / 9; // Convert Fahrenheit to Celsius
}

dataStream.onEntry(processData); // Process each data entry as they arrive
```

