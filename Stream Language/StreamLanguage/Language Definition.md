# Streaming Language

## Introduction
In the modern world, data is constantly being generated. Sensors, telemetry, and other data sources are constantly producing data that needs to be processed and analyzed.
The Streaming Language is designed to handle this data in a way that is both efficient and easy to use. 
The language is designed to be used in a variety of applications, from embedded systems to large scale data processing.
The language is designed to be easy to use and understand, while still being powerful enough to handle complex data processing tasks and provide near real time feedback.


## Overview


## Goals
- The language is designed to be easy to use and understand, while still being powerful enough to handle complex data processing tasks and provide near real time feedback.


## Design Principles
- The language is designed to be easy to use and understand, while still being powerful enough to handle complex data processing tasks and provide near real time feedback.


## Language Definition

This language's core is based on the concept of streams. A stream is a sequence of data that is constantly being generated. 
Streams can be taken from sockets, TCP connections, or any other source of data.
Streams can be processed and analyzed in real time, and can be used to generate other streams of data or to store data in a database.

### Lexical Structure

#### Identifier: 
- A sequence of letters, digits, and underscores that does not start with a digit. These are used to name variables, functions, and other objects. Identifiers are case-sensitive. And can be made of ascii or utf-8 characters. An Identifier cannot be a keyword.

#### Keywords
Keywords are reserved words that have special meaning in the language. They cannot be used as identifiers.
  
- `var identifier`: Declares a variable . If the type can be inferred, it can be omitted. Otherwise not specifying a type will result in an error
- `var identifier: type = value`: Define a variable. If the type can be inferred, it can be omitted. Otherwise not specifying a type will result in an error
- `var: type<type>`: Define a variable that encompasses a type such as a stream or array
- `struct [A-Za-z][A-Za-z0-9]* der (classname1, classname1)`: Define an object that derives from the listed objects
- `if (condition)`: Conditional statement
- `for (condition, start, incrementer)`: Loop statement
- `while (condition)`: Loop statement
- `else`: Only valid after if or elif
- `elif (condition)`: Only valid after if
- `try`: Exception handling
- `catch (exception)`: Only valid after try
- `fn functionname(argument: type): returntype { ... }`: Define a function
- `fn => (argument: type): return type { ... }`: Define a function variable
- `vol`: Variable can be accessed or modified from other threads, all operations are atomic
- `varname.attach(function pointer)`: Attach a function to an object during runtime. This function can be called later using `varname.functionname`  
- `global`: Define a global variable or an array of global variables

#### Literals
- `int`: Variable length integer 
- `float`: Variable length floating point
- `array`: A finite indexed collection of data
- `string`: ASCII null delimited or UTF8 array of contiguous characters
- `boolean`: A boolean value (T, F)

#### Advanced Data Types

- `stream`
An extension to the array, actually a queue.
- Represents an infinite sequence of data.
- Unlike an array, not every element can be accessed via its index.
- Every stream has a Mouth where data can be added and a sink where data is outputted.
- A Basic Stream:
  - Has a limited buffer (If data is being added at a faster rate than it is consumed, a basic stream will begin to drop the elements currently at its sink)
  - Can only add data at its mouth and retrieve it at its sink [queue idea]
  - Is strongly typed. Can only carry information of one type or derived types
  - Is asynchronous - A new element arriving at the sink will produce an event that the user can write a handler to follow.
  - It's mouth can be attached to a data source, whether it be a socket, file, or another stream's sink.

#### Operators
- `+`: Addition
- `-`: Subtraction
- `*`: Multiplication
- `/`: Division
- `%`: Modulus
- `==`: Equality
- `!=`: Inequality
- `>`: Greater than
- `<`: Less than
- `>=`: Greater than or equal to
- `<=`: Less than or equal to
- `++`: Increment
- `--`: Decrement
- `>>`: Stream flow: Stream attachment operator
- `=` : Assignment
- `+=`: Add and assign
- `-=`: Subtract and assign
- `*=`: Multiply and assign
- `/=`: Divide and assign
- `%=`: Modulus and assign
- `=>`: Function pointer

#### Comments
- `//`: Single line comment
- `/* ... */`: Multi-line comment


## Examples
```code
/* 
    This program takes in a stream of temperature data from a socket and converts it to celcius.
    It then stores the data in a database and calculates the average temperature.
*/
var dataIn = socket.toStream(); // Create a stream from a socket

struct Database {  // Define a database object
    in: basicStream<float>; // Define the input to be a basic stream
    out: createHTTPResp(host, port, data, table, ...); // Define the output to be an HTTP response
}
var stream<int> temperatureStream;  // Define a stream to hold the temperature data
vol var stream<int> celciusStream;  // Define a stream to hold the temperature data in celcius

var HTTPResp dbOutC = HTTPResp("localhost", 8080, "temperature", "celcius);  // Create an HTTP response object

var Database db;  // Create a database object
db.out = dbOutC;  // Attach the HTTP response to the database object


dataIn  >> temperatureStream;  // Attach the socket stream to the temperature stream
celciusStream >> db.in;  // Attach the celcius stream to the database input

vol var average: int = 0;  // Define a variable to hold the average temperature
vol var sum: int = 0;  // Define a variable to hold the sum of the temperatures
vol var total: int = 0;  // Define a variable to hold the total number of temperatures


fn calculateAverage(sum: int, total: int): int {  // Define a function to calculate the average temperature
    return sum / total;
}

temperatureStream.onEntry(eventH => (input: int): int{  // Define a function to handle the temperature data
    global [sum, total, average];
    total++;
    sum += input;
    average = calculateAverage(sum, total);  // Calculate the average temperature
    
    celciusStream.push((input - 32) * (5 / 9))  // Convert the temperature to celcius and push it to the celcius stream
}
```

