# What Happens When You Click Run? From Source Code to Output

When you write code and click **Run**, it feels as if the computer instantly understands your program. In reality, several layers cooperate: the editor, run configuration, language toolchain or runtime, operating system, CPU and memory, input/output streams, and the interface that displays the result.

The exact implementation depends on the language and where the code runs. Running C in a local IDE differs from executing JavaScript in a browser or submitting Python to an online compiler. This guide gives you a shared mental model, then explains the differences.

## 1. The Big Picture

A common simplified pipeline is:

```text
You write or edit source code
          |
          v
Click Run
          |
          v
Editor handles the click and chooses a command
          |
          v
Identify file/project, runtime, arguments, environment
          |
          v
Save or prepare the current code
          |
          v
Choose execution environment
(local computer, browser, or remote server)
          |
          v
Compiler and/or language runtime processes the code
          |
          v
Operating system manages the process and resources
          |
          v
CPU executes instructions while the program uses memory
          |
          v
Program requests input, produces output, or encounters an error
          |
          v
Output, errors, and completion status are captured
          |
          v
IDE, terminal, browser, or online platform displays the result
```

This is a mental model, not one universal implementation. An IDE may use an extension, terminal command, debugger, notebook kernel, build system, remote machine, browser runtime, or a combination. Some stages happen almost instantly; others may be cached or skipped when not needed.

## 2. Before Run: Your Code Is Text in an Editor

When you type:

```python
print(2 + 3)
```

the editor primarily holds characters in a text buffer. Syntax highlighting, autocomplete, bracket matching, and red underlines can be provided by editor features or language tools before you click Run.

These features do not necessarily mean the program has executed:
- Syntax highlighting can color `print` without running it.
- Autocomplete can suggest a variable using editor analysis.
- A diagnostic can warn about suspicious code before execution.
- The editor buffer can contain unsaved changes.

When Run is clicked, the tool must decide which version of the code to use. It might save automatically, ask you to save, or run the saved file. Exact behavior depends on the editor and settings. If it runs another file or an older saved version, the output may not reflect your latest edits.

## 3. What Does the Run Button Actually Do?

The button is a user-interface control. Clicking it triggers an event handled by the editor or application. That event maps to a command such as "run current Python file", "build and run C project", "start debugging", or "execute code on a server".

The tool needs to determine:
- Which file or project is the entry point?
- Which language and toolchain should be used?
- Which compiler or interpreter version is selected?
- What command-line arguments should be passed?
- What is the working directory?
- Are environment variables required?
- Where will standard input come from?
- Where will output be displayed?
- Is this a normal run or a debug session?

In a configurable IDE, these decisions may live in a run or launch configuration. For example, VS Code debug configurations can set the program entry point, arguments, environment variables, startup tasks, and whether to launch a process or attach to one already running. See [VS Code: Configure debugging](https://code.visualstudio.com/docs/debugtest/debugging-configuration).

**Clicking Run does not mean the editor itself executes every programming language.** Often it delegates the work to a compiler, interpreter, debugger, build system, or remote execution service.

## 4. First Branch: Where Does the Code Run?

### A. Local execution

The code runs on your own computer. The editor may start a compiler, interpreter, terminal, or another process. Your operating system manages processes and access to CPU, memory, files, and other resources.

Example: you click Run in a C IDE; it compiles the source file, starts the executable, and shows its output in a terminal panel.

### B. In-browser execution

Some code runs inside the browser. JavaScript in a web page is executed by a JavaScript engine hosted by the browser. The browser also supplies APIs for the page, events, networking, and rendering.

Example: an HTML/JavaScript playground may execute a click handler in the browser and show the result by changing the page's DOM.

### C. Remote or online execution

An online compiler or coding platform may send source code and options to a server. A backend prepares an execution environment, runs or compiles the code, captures the result, and sends it back to the browser. Robust services isolate untrusted code and enforce limits.

Example: you submit C code to an online judge. The actual compiler and program may run on a server rather than on your laptop.

These paths can be combined. A browser-based IDE may have its interface in the browser but run the terminal and code inside a remote container or virtual machine.

## 5. C and C++: Preprocess, Compile, Assemble, Link

A typical native C build using GCC can involve these stages:

```text
hello.c
  |
  v
Preprocessor: handles directives, headers, and macros
  |
  v
Preprocessed source
  |
  v
Compiler: checks language rules and translates source
  |
  v
Assembly instructions
  |
  v
Assembler: creates object file(s)
  |
  v
Object file(s)
  |
  v
Linker: combines object files and required libraries
  |
  v
Executable program
```

For example:

```c
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");
    return 0;
}
```

In a typical GCC build, `#include` is handled by the preprocessor. The compiler translates the program, the assembler produces object code, and the linker combines it with required object files and library references to produce an executable. The compiler driver coordinates these stages, so for a small file they can look like one action.

Not every compiler exposes these exact intermediate files; some toolchains combine stages or optimize them. The distinction is still useful because a program can fail before execution:
- A missing header or invalid directive may cause a preprocessing/build error.
- Invalid syntax may cause a compiler error.
- An unresolved function may cause a linker error.
- A successfully compiled program can still contain a runtime or logic bug.

Reference: [GCC documentation: compilation stages](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html).

## 6. Python: Interpreter and Bytecode

With CPython, the usual implementation of Python, running a script is different from building a standalone native executable every time.

A useful simplified view is:

```text
hello.py
   |
   v
Python parses and compiles the source
   |
   v
Code objects containing bytecode and metadata
   |
   v
CPython bytecode interpreter executes instructions
   |
   v
Output, returned values, or exceptions
```

When you run `python hello.py`, the operating system starts the Python interpreter. Python reads and parses the script, compiles it to internal code objects/bytecode as appropriate, and executes it. Python may cache compiled bytecode in some circumstances, but that is an implementation detail rather than something you should assume always happens.

Example:

```python
name = "Ganesh"
print("Hello,", name)
```

The interpreter executes the assignment and the print call. The output is a side effect of that call, not a screenshot of the source code.

"Interpreted language" is a useful introductory label, but real runtimes have more machinery than an interpreter reading each source character one at a time. CPython has a compiler and bytecode interpreter; other Python implementations may differ.

Sources: [Python documentation](https://docs.python.org/3/), [CPython interpreter internals](https://github.com/python/cpython/blob/main/InternalDocs/interpreter.md).

## 7. Java: Bytecode and the JVM

A common Java workflow looks like this:

```text
Hello.java
   |
   v
Java compiler (javac)
   |
   v
Java bytecode (.class)
   |
   v
Java Virtual Machine (JVM)
   |
   v
Execution through runtime interpretation and/or JIT compilation
```

The JVM provides an execution environment for Java bytecode. A JVM implementation may interpret bytecode and compile frequently used code to native machine code at runtime through just-in-time (JIT) compilation.

This is why "compiled" and "interpreted" are not always mutually exclusive labels for an entire language. Compilation can happen before execution and again during runtime, depending on the platform.

Official starting point: [Java documentation](https://docs.oracle.com/en/java/).

## 8. JavaScript: Engine Plus Host Environment

JavaScript varies by environment. In a browser, the JavaScript engine parses and executes language code; the browser is the host environment and provides APIs such as the DOM, timers, events, and network requests. Node.js is another host environment with different APIs.

```text
JavaScript source
       |
       v
JavaScript engine parses and processes it
       |
       v
Engine executes and may optimize code
       |
       +----> Browser APIs / page updates
       |
       +----> Async work and event-loop scheduling
```

Modern engines may use internal strategies involving bytecode, interpreters, and optimizing compilers. The exact implementation depends on the engine and version.

Reference: [MDN: JavaScript execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model).

## 9. The Operating System Starts and Manages Execution

After preparing the run command, a local environment typically launches a process to do the work. It might launch a compiler first and then an executable; start an interpreter that loads a source file; or start several processes for a larger project.

The operating system manages processes, memory, file access, scheduling, and other resources. On Unix-like systems, process creation and program execution are separate concepts: an operation such as `execve` replaces the program image of the calling process; it does not, by itself, create a brand-new process.

While a program runs:
- The OS allocates/manages resources and schedules threads.
- Instructions operate on data held in memory.
- The program may request files, network activity, input, or other OS services.
- The process may finish normally, return an error status, crash, or be stopped.

A useful beginner mental model is "the OS starts my program and gives it resources." The exact system calls and loader steps differ among operating systems and tools.

Reference: [Linux manual: execve](https://www.man7.org/linux/man-pages/man2/execve.2.html).

## 10. CPU, Instructions, Memory, Stack, and Heap

The editor is not doing your calculation itself. The running program's instructions are executed by the CPU while data is held in memory.

A simplified view of program memory includes:
- **Code/instructions:** executable instructions or runtime-managed code.
- **Stack:** commonly used for function calls, local execution context, and return information.
- **Heap:** commonly used for dynamically allocated objects and data.
- **Other regions:** global values, runtime structures, mapped files, and implementation-specific areas.

Exact memory layout depends on the language implementation, operating system, and runtime.

Consider:

```python
a = 10
b = 20
total = a + b
print(total)
```

Conceptually, the runtime creates and updates values associated with `a`, `b`, and `total`, evaluates the addition, and calls `print`. Python's object model is more complex than assigning fixed physical memory boxes to variable names, so this is a logical trace rather than a literal diagram of CPython memory.

In lower-level languages such as C, addresses, stack storage, heap allocation, and compiled instructions relate to variables differently and are more directly affected by compiler and language rules.

## 11. How Output Travels from the Program to the Screen

Many command-line programs start with three standard streams:

- **stdin (standard input):** a source of input.
- **stdout (standard output):** the normal output stream.
- **stderr (standard error):** commonly used for diagnostic messages.

These streams may connect to a terminal, file, pipe, or another destination chosen by the parent process. In a coding IDE, stdout and stderr are often captured by a terminal or output panel. An online runner may capture them on a server and send the data back to the browser.

Python example:

```python
print("This is normal output")
print("This is also normal output")
```

Both calls write to stdout by default. To write to stderr:

```python
import sys

print("Normal result")
print("Something needs attention", file=sys.stderr)
```

C example:

```c
#include <stdio.h>

int main(void) {
    printf("Normal output\n");
    fprintf(stderr, "Diagnostic message\n");
    return 0;
}
```

The C standard library's `printf` writes to stdout, while `fprintf(stderr, ...)` targets stderr. The user interface may display both in the same panel or style them differently.

The general path is:

```text
Program calls print() / printf() / writes data
                  |
                  v
Language runtime or I/O library
                  |
                  v
stdout or stderr stream
                  |
                  v
OS-level stream, terminal, pipe, or capture mechanism
                  |
                  v
IDE / terminal / server response / browser UI
                  |
                  v
Text appears in the output area
```

The program usually does not tell the IDE "draw these exact pixels here." It writes output through an agreed stream or interface. The terminal emulator or IDE renders the text. A web app may instead update the page using browser APIs. These are different routes to visible output.

There can also be buffering: output is not necessarily displayed character-by-character immediately. Libraries may buffer text and flush it at particular times, such as on a newline or normal termination, depending on the stream and runtime.

Reference: [Linux manual: standard streams](https://www.man7.org/linux/man-pages/man3/stdout.3.html).

## 12. How Does the Program Receive Input?

The tool must decide where input comes from when a program needs it.

Examples:
- In a terminal, Python's `input()` or C's `scanf()` may read from stdin.
- In an online judge, text typed in an input box can be supplied to the program's standard input.
- A program can also read command-line arguments, environment variables, files, or network responses.
- A browser app might get input from HTML form controls and event handlers, not terminal stdin.

Python example:

```python
name = input("Enter your name: ")
print("Hello,", name)
```

In a terminal, the program can pause until the user enters input and presses Enter. In a tool that does not provide interactive stdin, the program might appear stuck, receive end-of-file, or fail, depending on configuration.

A run configuration may include the working directory, arguments, environment variables, and input settings. These values influence execution even if the source code is unchanged.

## 13. What Happens in an Online Compiler or Coding Website?

A website that executes arbitrary code needs more infrastructure than a text editor. A typical architecture might look like this:

```text
Browser editor
    |
    | code + language + compiler choice + input + options
    v
HTTP/API request
    |
    v
Backend validates request and creates a job
    |
    v
Queue / execution service
    |
    v
Isolated worker or sandbox
    |
    +--> Compiler, when needed
    |
    +--> Program execution with input and limits
    |
    v
Capture stdout, stderr, exit status, timing, errors
    |
    v
Return result to the browser
    |
    v
Render output / build log / runtime error
```

This is a representative architecture, not a guarantee about every website. A service may run code in containers, virtual machines, sandboxed workers, or other isolation mechanisms. It may process the job synchronously or put it in a queue, then poll or stream for results.

The browser generally sends code and execution options to the service. The service chooses the compiler or runtime, provides any submitted input, enforces limits, collects results, and returns structured information to the UI.

Open-source project [Judge0](https://github.com/judge0/judge0) is one example of a code-execution system designed to run source code in a sandbox and return execution details. Its design is an example, not a specification for every online IDE.

### Why does the website need a server?

The browser can run some code itself, especially JavaScript intended for the browser. But a site supporting many languages or native compilation often needs a backend with the required compilers, runtimes, filesystem support, and resource controls.

The code editor visible on your screen and the machine executing the code can be in completely different places.

## 14. Why Sandboxing and Resource Limits Matter

If a site executed every user's code with unlimited server access, one program could try to read private files, contact internal services, consume excessive CPU or memory, or interfere with other users.

Code-execution services therefore need isolation and scoped permissions. Depending on the service, controls may include:
- Separate containers, virtual machines, or other sandboxes.
- CPU and wall-clock time limits.
- Memory limits.
- Restrictions on filesystem and network access.
- A low-privilege user or restricted capabilities.
- Limits on process counts and output size.
- Cleanup of temporary files after execution.

These are possible controls, not features to assume every platform has. Sandboxes can also have vulnerabilities and must be configured carefully.

**Security rule for your own computer:** running a script is not just displaying text. Code may read or change files available to your account, use network access, or run other commands. Do not run unknown code simply because it is labelled a test or demo. Review it and use an appropriately isolated environment.

## 15. What Happens When the Run Fails?

"Nothing appeared" can mean several different things. Identifying the stage that failed makes debugging faster.

| Stage | Example failure | What you might see |
|---|---|---|
| Editor/configuration | Wrong file selected or unsaved code | Old output or unexpected program |
| Toolchain setup | Compiler/interpreter missing | Command not found or toolchain error |
| Parsing/compilation | Invalid syntax or type error | Syntax, compiler, or build messages |
| Linking/loading | Required symbol, library, or module unavailable | Linker or loader error |
| Runtime | Division by zero, missing file, exception | Runtime exception or crash |
| Logic | Wrong algorithm | Plausible but incorrect output |
| Input | Program waits for missing input | Appears stuck or receives end-of-file |
| Resource limits | Infinite loop, excessive memory, huge output | Timeout, termination, or limit message |
| Output routing | Result went to another terminal or stderr panel | Output exists, but elsewhere |
| Remote execution | Network or server job fails | Request error or job failure status |

### Compile-time vs runtime vs logic errors

- A **compile-time error** prevents a required build stage from succeeding.
- A **runtime error** happens while the program or runtime is executing.
- A **logical error** is a mistake in the program's reasoning; it may run and produce output, but that output is wrong.

A program that compiles is not automatically correct. A program that prints something is not necessarily finished.

## 16. Why Does a Coding Platform Sometimes Say "Wrong Answer"?

On coding practice websites, visible output may be only one part of evaluation.

A typical judge may:
1. Compile or prepare the code.
2. Run it with one or more inputs, including hidden test cases.
3. Collect output and process status.
4. Compare results with expected outputs using the problem's rules.
5. Report a verdict such as Accepted, Wrong Answer, Compilation Error, Runtime Error, or Time Limit Exceeded.

Names and comparison behavior vary by platform and problem. Some tasks require exact text output; others use specialized checkers. A solution can pass the visible sample and fail hidden cases, or be logically correct but exceed the time or memory limit.

For input-based problems, sample input is normally supplied to stdin by the runner. You generally should not hard-code the sample output into your program.

## 17. Run vs Debug: Similar Button, Different Goal

**Run** asks the tool to execute a program and show what happens.

**Debug** starts or attaches to execution with debugging facilities. You can pause at breakpoints, step through statements, inspect variables, view the call stack, and examine program state. The IDE may launch a process or attach to one already running, depending on configuration.

A debugger can change timing and behavior slightly, especially in concurrent or timing-sensitive programs. Debugging is a way to observe and control execution, not a guarantee the program is correct.

See [VS Code debug configuration](https://code.visualstudio.com/docs/debugtest/debugging-configuration).

## 18. Full Trace: Python from Click to Output

Suppose your file contains:

```python
price = 100
quantity = 3
total = price * quantity
print(total)
```

A common local execution path is:

1. You click Run in the editor.
2. The editor identifies the active Python file and selected run command.
3. Depending on settings, it saves the current buffer or runs the saved file.
4. The editor asks the OS to start a Python interpreter, typically with the script path and selected environment.
5. Python reads and parses the file, compiles it to internal code objects/bytecode as appropriate, and executes the code.
6. The runtime performs the assignments and multiplication.
7. `print(total)` writes the text representation of the value to stdout.
8. Stdout is connected to a terminal or captured by the IDE.
9. The terminal/IDE displays `300`.
10. When the script finishes, the process reports completion and the editor indicates the run has ended.

You see one line, but multiple tools and runtime layers cooperate to produce it.

## 19. Full Trace: C from Click to Output

Suppose your C file contains:

```c
#include <stdio.h>

int main(void) {
    int answer = 6 * 7;
    printf("%d\n", answer);
    return 0;
}
```

In a typical local GCC-based workflow:

1. You click Run.
2. The IDE selects the C project or current source file.
3. The IDE invokes the compiler driver with the required options.
4. The preprocessor handles directives such as `#include`.
5. The compiler translates the source; the assembler generates object code.
6. The linker combines object code and required libraries into an executable.
7. The IDE asks the OS to start the executable as a process.
8. The OS loads the executable and its needed components into the process environment.
9. The CPU executes program instructions.
10. `printf` sends formatted text to stdout.
11. The terminal or IDE displays `42`.
12. The program returns status `0`, conventionally indicating successful completion.

Build systems may reuse existing outputs and rebuild only files that need it. Clicking Run therefore does not necessarily repeat every compilation stage.

## 20. Full Trace: JavaScript in a Browser

Consider an HTML page with a button and a small script. After the page loads:

1. The browser parses the HTML and creates a document structure.
2. The browser loads and processes JavaScript.
3. The JavaScript engine executes code that registers a click handler.
4. When the user clicks the button, the browser dispatches an event.
5. The handler runs and may update the DOM.
6. The browser calculates and paints the updated visual result.

For asynchronous work, such as a network request or timer, completion handling is scheduled through the runtime's task mechanisms. The browser can do other work while an asynchronous operation is pending. Long-running synchronous JavaScript on the main thread, however, can delay user interactions and rendering.

This differs from running a C executable in a terminal. A browser page may display results by modifying the user interface rather than writing characters to stdout.

Sources: [MDN JavaScript execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model) and [MDN: Main thread](https://developer.mozilla.org/en-US/docs/Glossary/Main_thread).

## 21. What Can Change Between Two Runs?

Even if the source code is unchanged, the result can differ because of:
- Different input.
- Different compiler, interpreter, or runtime versions.
- Different environment variables or command-line arguments.
- Different working directories or files.
- Different dependency versions.
- Random values or current time.
- Network responses and service availability.
- Operating-system differences.
- Concurrency or timing.
- Cached build artifacts or generated files.

This is why reliable projects document environment setup, manage dependencies, use predictable test input, and test important behavior.

## 22. A Checklist When Output Does Not Match

Check in this order:

1. **Correct file:** Is the editor running the file you edited?
2. **Saved changes:** Were your latest changes saved or otherwise included?
3. **Correct environment:** Is the expected interpreter, compiler, runtime, or project selected?
4. **Input and arguments:** Did the program receive the input you expected?
5. **Output location:** Did stdout or stderr appear in a different panel or terminal?
6. **Errors:** Is there a compilation message, exception, or non-zero exit status?
7. **Program logic:** Trace values and conditions; do not assume successful execution means correct logic.
8. **Dependencies and files:** Is the working directory correct, and are needed dependencies available?
9. **Resource limits:** Is a loop, large memory use, or huge output preventing completion?
10. **Environment:** Does the result depend on time, randomness, network services, or cached outputs?

## 23. Beginner Glossary

| Term | Simple meaning |
|---|---|
| Source code | Human-readable instructions you write |
| Editor/IDE | Tool for editing code and coordinating development tasks |
| Compiler | Tool that translates source code or an intermediate form into another form, often machine code |
| Interpreter | Runtime component that executes program instructions or code objects |
| Runtime | The environment and support components used while a program executes |
| Build | Prepare the program and its required artifacts for execution |
| Executable | A program file the OS can load and run on a compatible system |
| Process | A running program instance managed by the OS |
| Thread | A sequence of execution within a process |
| CPU | Hardware that executes machine instructions |
| Memory | Storage used for code, values, stacks, heaps, and runtime data |
| stdin | Standard input stream |
| stdout | Standard output stream |
| stderr | Standard error stream, commonly for diagnostics |
| Exit status | A value indicating how a process ended; zero commonly means success by convention |
| Sandbox | An isolated environment intended to limit what code can access or do |
| Debugger | A tool for pausing and inspecting program execution |
| Event loop | A runtime mechanism that coordinates queued work, including asynchronous callbacks in environments such as browser JavaScript |

## 24. Official References and Further Reading

- [GCC: overall compilation stages](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html)
- [Python documentation](https://docs.python.org/3/)
- [CPython interpreter internals](https://github.com/python/cpython/blob/main/InternalDocs/interpreter.md)
- [Java documentation](https://docs.oracle.com/en/java/)
- [MDN: JavaScript execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model)
- [MDN: main thread](https://developer.mozilla.org/en-US/docs/Glossary/Main_thread)
- [VS Code: configure debugging](https://code.visualstudio.com/docs/debugtest/debugging-configuration)
- [Linux: execve](https://www.man7.org/linux/man-pages/man2/execve.2.html)
- [Linux: stdin, stdout, and stderr](https://www.man7.org/linux/man-pages/man3/stdout.3.html)
- [Judge0: code-execution system](https://github.com/judge0/judge0)

## 25. Quick Self-Test

1. Why is clicking Run not the same as the editor executing source text itself?
2. Why does a typical C workflow have compilation and linking stages?
3. What does the Python interpreter do when a script is run?
4. Why can two code editors run the same file in different ways?
5. What are stdin, stdout, and stderr used for?
6. Why might output be captured before the UI displays it?
7. How is an online code runner different from local execution?
8. Why do online execution platforms need sandboxing and time/memory limits?
9. How does a runtime error differ from a logical error?
10. Why can JavaScript in a browser block page interactions?
11. Does successful compilation guarantee correct output?
12. Why can the same source code behave differently in different environments?

### Answer key

1. The editor handles the click and delegates work to a compiler, interpreter, process, browser runtime, debugger, or remote service.
2. Source code must be processed into object code and executable form; the linker combines needed object files and libraries.
3. In CPython, Python reads and parses source, creates code objects/bytecode as appropriate, and the interpreter executes them.
4. Editors can choose different run configurations, runtimes, compiler options, input sources, working directories, or remote environments.
5. stdin supplies input; stdout carries normal output; stderr commonly carries diagnostic messages.
6. The process writes to streams or a protocol; the terminal, IDE, or service captures that data and renders it.
7. A remote runner sends code/options to a service that executes them on a server and returns results.
8. Submitted code is untrusted and could consume resources or attempt to access files, networks, or other users' data.
9. A runtime error occurs during execution; a logical error may execute normally but calculate the wrong result.
10. Browser JavaScript often runs on the main thread shared with event handling and rendering; long synchronous work can delay both.
11. No. Successful compilation only means the relevant build stage succeeded; logic and runtime behavior can still be wrong.
12. Input, runtime version, dependencies, directory, environment variables, OS behavior, randomness, and external services can affect execution.

---

**Core mental model:** the Run button is a trigger. A chain of tools and runtime layers prepares your code, executes it, routes input and output, and reports how the run ended.
