---
id: 1-2-python-axioms
title: "1.2 The Axioms of Code"
sidebar_label: "1.2 Python Axioms & Theory"
description: "Foundational theory of the Python language: Type systems, Scope resolution, and the CPython VM."
---

# 1.2 The Axioms of Code
**Stage I: The Substrate**

> "Code is not magic. It is a precise negotiation with the compiler about what is true."

## 1. The Ontology of Types (Type Theory)

Before writing a single line of `def`, we must understand what data *is*.
In Python, we say "Everything is an Object." This is not a metaphor. It is a memory layout strategy.

### The `PyObject` Struct
Every variable in Python is a pointer to a C struct called `PyObject`.
It contains:
1.  `ob_refcnt`: Reference Count (For Garbage Collection)
2.  `ob_type`: Pointer to the Type Object (Class)
3.  `ob_value`: The actual data (for primitives)

When you write `x = 5`, you are not putting the number 5 into a box labeled `x`.
You are creating a `PyObject` for the integer `5` on the **Heap**, and pointing the name `x` (on the **Stack** frame) to it.

```mermaid
graph LR
    Stack[Stack Frame: Main] -->|Name 'x'| Heap1[Heap: Int(5)]
    Stack -->|Name 'y'| Heap1
    Heap1 -->|ob_type| Type[PyType: Integer]
```

### Strong vs. Weak Typing
*   **Strong**: Types are strictly enforced. `5 + "5"` raises a `TypeError`. Python is Strong.
*   **Dynamic**: Type checking happens at runtime. `x` can point to an Int, then a String.

**Deep Implication**: Every addition `a + b` in Python triggers a lookup dispatch. `a.__add__(b)`. This is why Python is slower than C++, but infinitely more flexible.

---

## 2. Scope Resolution: The LEGB Rule

Where does a name live? When you type `print(x)`, how does Python find `x`?
It follows the **LEGB** Law of Physics:

1.  **L (Local)**: Inside the current function.
2.  **E (Enclosing)**: Inside the parent function (Closures).
3.  **G (Global)**: At the module level.
4.  **B (Built-in)**: The deepest layer (e.g., `len`, `str`).

### The Closure (Capturing Context)
A closure is a function that remembers the environment in which it was created. This is the seed of **State Preservation** without Classes.

```python
def make_counter():
    count = 0  # <--- This variable generally dies when make_counter returns
    
    def increment():
        nonlocal count # <--- Puncturing the scope barrier
        count += 1
        return count
        
    return increment # <--- We return the function AND its environment

# The 'count' variable is kept alive by the closure, defying the stack frame pop.
```
This is crucial for **Callbacks** in ROS 2.

---

## 3. The CPython Virtual Machine

Python code is not executed by the CPU. It is executed by a software CPU called the **Virtual Machine**.
1.  **Source** (`.py`)
2.  **Compiler**: Translates to **Bytecode** (`.pyc`)
3.  **PVM (Python Virtual Machine)**: A giant `switch/case` statement in C that runs the bytecode.

### Disassembling Reality
We can see the matrix using the `dis` module.

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

**Output (The Truth):**
```text
  2           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```
*   `LOAD_FAST`: Push variable onto the value stack.
*   `BINARY_ADD`: Pop two, add, push result.

Understanding this stack-based machine is essential for optimizing critical loops in robot perception.

---

## Deep FAQ

> **Q: Why are Python lists so memory hungry?**
> A: A Python list is not a contiguous array of data (like C `int[]`). It is a contiguous array of pointers to `PyObjects` scattered across the Heap. This causes cache misses and overhead. This is why we use **NumPy**—it brings C-style contiguous memory arrays back to Python.

> **Q: What is a Metaclass?**
> A: If an Object is an instance of a Class, what is a Class an instance of? A Metaclass. Only use this if you are writing frameworks (like `rclpy`). It allows you to intercept the creation of *types themselves*.
