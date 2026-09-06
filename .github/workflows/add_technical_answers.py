from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

answers_file = (
    BASE_DIR
    / "04 . templates"
    / "07 . sevices"
    / "08 . data"
    / "3 . answers.json"
)

with open(answers_file, "r", encoding="utf-8") as f:
    data = json.load(f)

data["technical"] = {
    "C": {
        "intermediate": [
            "C provides basic data types such as char, int, float, double and void.",
            "An array stores multiple values of the same type in contiguous memory, while a pointer stores the address of another variable.",
            "A function is a reusable block of code that performs a specific task. Functions improve modularity and code reuse.",
            "A local variable is declared inside a function or block and has limited scope. A global variable is declared outside functions.",
            "A structure is a user-defined data type that groups variables of different data types.",
            "A pointer stores the memory address of another variable. Example: int x = 10; int *p = &x;",
            "A while loop checks the condition before execution. A do-while loop executes at least once before checking the condition.",
            "C passes arguments by value. Pointers can be used to modify the original variable through its address.",
            "Recursion occurs when a function calls itself. It is useful for factorials, tree traversal and divide-and-conquer algorithms.",
            "malloc allocates uninitialized memory, while calloc allocates memory and initializes it to zero."
        ],
        "medium": [
            "Dynamic memory allocation allows memory to be allocated during runtime using malloc, calloc or realloc and released using free.",
            "A segmentation fault occurs when a program accesses invalid or unauthorized memory.",
            "Stack memory is generally used for local variables and function calls, while heap memory is used for dynamically allocated memory.",
            "A dangling pointer points to memory that has already been freed or is no longer valid.",
            "A memory leak occurs when dynamically allocated memory is not released after use.",
            "A structure stores members separately, while a union shares the same memory location among its members.",
            "A function pointer stores the address of a function and can be used for callbacks.",
            "malloc allocates memory, calloc allocates and initializes memory, realloc changes its size and free releases it.",
            "Pointer arithmetic changes an address based on the size of the pointed data type.",
            "Segmentation faults can be debugged using GDB, Valgrind and sanitizers."
        ],
        "advanced": [
            "I would reproduce the fault, inspect the stack trace, use GDB and check pointer values and memory boundaries.",
            "I would minimize unnecessary allocations, reuse buffers and choose memory-efficient data structures.",
            "A buffer overflow happens when data is written beyond the allocated buffer and can cause crashes or security vulnerabilities.",
            "Memory leaks can be detected using Valgrind, AddressSanitizer and heap profiling.",
            "C multithreading requires synchronization when multiple threads access shared data.",
            "I would profile the program first, identify bottlenecks and optimize algorithms and data structures.",
            "Undefined behavior means the C standard does not define what the program must do.",
            "Safe memory management requires checking allocations, defining ownership and freeing memory exactly once.",
            "A race condition occurs when multiple threads access shared data and the result depends on execution order.",
            "Production debugging involves logs, crash dumps, stack traces, testing and root-cause analysis."
        ]
    },

    "Python": {
        "intermediate": [
            "Common Python data types include int, float, str, bool, list, tuple, set and dict.",
            "A list is mutable, while a tuple is immutable.",
            "A dictionary stores data as key-value pairs.",
            "A function is a reusable block of code defined using def.",
            "if, elif and else are used for conditional execution.",
            "A list comprehension is a compact way to create a list from an iterable.",
            "== compares values, while is checks object identity.",
            "Mutable objects can be changed after creation, while immutable objects cannot.",
            "Exception handling uses try, except, else and finally.",
            "A module is usually a Python file, while a package organizes multiple modules."
        ],
        "medium": [
            "Lists are ordered and mutable, tuples are immutable, sets contain unique values and dictionaries store key-value pairs.",
            "Decorators modify or extend the behavior of functions or classes.",
            "An iterator produces values one at a time, while generators use yield to create iterators.",
            "A shallow copy may share nested objects, while a deep copy recursively copies nested objects.",
            "Inheritance allows a class to reuse functionality from another class. Polymorphism allows different implementations.",
            "Lambda functions are small anonymous functions useful for short operations.",
            "try contains risky code, except handles errors, else runs without errors and finally always runs.",
            "*args collects positional arguments and **kwargs collects keyword arguments.",
            "Modules organize Python code and packages organize related modules.",
            "Debugging involves reproducing the issue, inspecting variables, logging and testing."
        ],
        "advanced": [
            "The Python Global Interpreter Lock allows only one thread to execute Python bytecode at a time in CPython.",
            "I would profile the application, identify bottlenecks, optimize algorithms and database access and use caching.",
            "Multithreading is useful for many I/O-bound tasks, while multiprocessing is useful for CPU-bound tasks.",
            "Python uses reference counting and cyclic garbage collection.",
            "A scalable Python backend can use stateless services, load balancing, caching and horizontal scaling.",
            "async and await provide asynchronous programming using an event loop.",
            "Memory leaks can be investigated using memory profiling and by finding objects that remain referenced unexpectedly.",
            "A secure Python web application should validate input, use parameterized queries and enforce authentication and authorization.",
            "Caching can use memory caches, Redis, database caching or CDN caching.",
            "Production debugging uses logs, metrics, traces, profiling and recent deployment information."
        ]
    },

    "Java": {
        "intermediate": [
            "Java features include object-oriented programming, platform independence, strong typing and automatic memory management.",
            "JDK is used for development, JRE provides the runtime environment and JVM executes Java bytecode.",
            "A class is a blueprint and an object is an instance of a class.",
            "Inheritance allows one class to acquire properties and methods from another.",
            "Method overloading means methods have the same name but different parameters.",
            "Method overriding occurs when a subclass provides its own implementation.",
            "An interface defines a contract that classes can implement.",
            "Java uses try, catch, finally, throw and throws for exception handling.",
            "ArrayList provides dynamic-array behavior, while LinkedList is node-based.",
            "== compares primitive values or object references, while equals() normally compares object contents."
        ],
        "medium": [
            "Encapsulation hides internal state, inheritance enables reuse, polymorphism supports multiple implementations and abstraction hides unnecessary details.",
            "An abstract class can contain state and implemented methods, while an interface defines a contract.",
            "Overloading uses different parameters. Overriding replaces inherited behavior.",
            "Java exception handling uses try, catch, finally, throw and throws.",
            "ArrayList is a dynamic array, HashSet stores unique values and HashMap stores key-value pairs.",
            "final prevents reassignment, finally is used during exception handling and finalize should not be relied upon.",
            "A constructor initializes an object and has the same name as the class.",
            "Access modifiers include private, default, protected and public.",
            "String is immutable, while StringBuilder is mutable.",
            "Threads can be created using Thread, Runnable or ExecutorService."
        ],
        "advanced": [
            "JVM memory includes heap, thread stacks, metaspace and other runtime structures.",
            "I would profile the application, optimize algorithms, reduce allocations and improve database and network operations.",
            "Java concurrency provides threads, synchronization, locks, executors and concurrent collections.",
            "Garbage collection can consume CPU and affect application latency.",
            "A scalable Java backend can use load balancing, caching, stateless services and horizontal scaling.",
            "Deadlocks occur when threads wait indefinitely for each other's resources.",
            "Java memory leaks can be investigated using heap dumps, GC logs and allocation profiling.",
            "The Java Memory Model defines visibility, ordering and atomicity between threads.",
            "A secure Java application needs authentication, authorization, encryption, validation and secure secret management.",
            "Production debugging uses logs, stack traces, thread dumps, heap dumps and metrics."
        ]
    },

    "SQL": {
        "intermediate": [
            "SQL stands for Structured Query Language and is used to manage relational databases.",
            "A primary key uniquely identifies each row.",
            "A foreign key references a key in another table.",
            "A unique key ensures that values are unique.",
            "DELETE removes selected rows, while TRUNCATE removes all rows.",
            "WHERE filters rows before grouping, while HAVING filters groups after GROUP BY.",
            "INNER JOIN returns matching rows from both tables.",
            "GROUP BY groups rows so aggregate functions can be applied.",
            "Normalization reduces data redundancy and improves data integrity.",
            "An index can speed up searches but requires storage and can increase write overhead."
        ],
        "medium": [
            "INNER JOIN returns matches, LEFT JOIN keeps all left rows and RIGHT JOIN keeps all right rows.",
            "Normalization reduces redundancy and update anomalies.",
            "A primary key identifies rows, a foreign key references another table and a composite key uses multiple columns.",
            "A subquery is a query nested inside another query.",
            "GROUP BY creates groups and HAVING filters those groups.",
            "A transaction is a logical unit of database operations.",
            "ACID means Atomicity, Consistency, Isolation and Durability.",
            "UNION removes duplicates while UNION ALL keeps duplicates.",
            "A view is a virtual table based on a query.",
            "Query optimization involves execution plans, indexes, filtering and efficient joins."
        ],
        "advanced": [
            "I would inspect the execution plan, indexes, joins, statistics and I/O to optimize a slow query.",
            "Indexes improve reads but consume storage and increase write overhead.",
            "A scalable database can use indexing, connection pooling, caching, replication and partitioning.",
            "Transactions provide reliable units of work and isolation levels control concurrent behavior.",
            "Deadlocks occur when transactions wait for each other's locks.",
            "Database bottlenecks can be identified using query latency, CPU, memory, I/O and lock monitoring.",
            "Partitioning divides large tables into smaller logical pieces.",
            "Replication maintains copies of data across database servers.",
            "Production databases require least-privilege access, encryption, secure credentials and backups.",
            "A scalable relational architecture can use optimized schema design, indexes, read replicas, caching and partitioning."
        ]
    },

    "Web Development": {
        "intermediate": [
            "HTML defines the structure and content of web pages.",
            "HTML defines structure while CSS controls presentation and layout.",
            "JavaScript provides behavior and interactivity.",
            "An id identifies an element, while a class can be shared by multiple elements.",
            "Semantic elements such as header, nav, main and footer describe content meaning.",
            "The CSS box model consists of content, padding, border and margin.",
            "Responsive design allows websites to adapt to different screen sizes.",
            "Inline CSS is on an element, internal CSS is inside a style element and external CSS is in a separate file.",
            "The DOM is a tree representation of an HTML document.",
            "let and const are block-scoped, while var is function-scoped."
        ],
        "medium": [
            "Flexbox is mainly one-dimensional, while CSS Grid supports two-dimensional layouts.",
            "Event bubbling allows an event to propagate from a child element toward its parents.",
            "Promises represent asynchronous results and async/await provides cleaner syntax for promises.",
            "localStorage persists data while sessionStorage normally lasts for the browser session.",
            "Form validation checks whether submitted data meets required rules.",
            "A REST API exposes resources using HTTP methods.",
            "GET retrieves data, POST creates data, PUT updates data and DELETE removes data.",
            "Authentication verifies identity while authorization determines permissions.",
            "Web performance can be improved using compression, caching, optimized images and lazy loading.",
            "Media queries allow CSS to change based on screen characteristics."
        ],
        "advanced": [
            "A scalable full-stack application can use CDN, load balancing, stateless servers, caching, scalable databases and queues.",
            "Browser, CDN and server-side caching reduce repeated resource and computation costs.",
            "Secure authentication can use short-lived access tokens, protected refresh tokens and HTTPS.",
            "WebSockets provide persistent bidirectional communication and are useful for real-time applications.",
            "JavaScript memory leaks can be investigated using heap snapshots and browser developer tools.",
            "Large applications can be optimized using code splitting, lazy loading and efficient rendering.",
            "Code splitting divides an application into smaller bundles and lazy loading loads them when required.",
            "A secure API should validate input, enforce authorization, use HTTPS and rate limiting.",
            "High traffic can be handled through load balancing, caching, horizontal scaling and database scaling.",
            "Production debugging involves browser performance tools, network analysis, API latency and server logs."
        ]
    }
}

with open(answers_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Technical answers added successfully.")