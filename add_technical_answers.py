from pathlib import Path
import json

# Project folder
BASE_DIR = Path(__file__).resolve().parent

# Answers file
ANSWERS_FILE = (
    BASE_DIR
    / "04 . templates"
    / "07 . sevices"
    / "08 . data"
    / "3 . answers.json"
)

# Load existing answers
with open(ANSWERS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# =========================================================
# TECHNICAL ANSWERS
# =========================================================

data["technical"] = {

    # =====================================================
    # C
    # =====================================================
    "C": {
        "intermediate": [
            "C provides basic data types such as int, char, float, double, and void.",
            "An array stores multiple elements of the same type in contiguous memory, while a pointer stores the address of another variable.",
            "A function is a reusable block of code that performs a specific task. Functions improve code organization and reuse.",
            "A local variable is declared inside a function or block and is accessible only there. A global variable is declared outside functions and can be accessed by multiple functions.",
            "A structure is a user-defined data type that groups variables of different data types under one name.",
            "A pointer is a variable that stores the memory address of another variable. Example: int x = 10; int *p = &x;",
            "A while loop checks the condition before executing the loop body. A do-while loop executes the body at least once before checking the condition.",
            "C normally uses call by value, meaning a copy of the value is passed. A pointer can be passed so the function can modify the original variable.",
            "Recursion occurs when a function calls itself. It is useful for problems such as tree traversal, factorial calculation, and divide-and-conquer algorithms.",
            "malloc allocates uninitialized memory, while calloc allocates memory and initializes it to zero."
        ],

        "medium": [
            "Dynamic memory allocation allows memory to be allocated during program execution using malloc, calloc, realloc, and released using free.",
            "A segmentation fault usually occurs when a program accesses invalid memory, such as dereferencing a NULL or dangling pointer.",
            "Stack memory is automatically managed and is commonly used for local variables and function calls. Heap memory is dynamically allocated and manually managed.",
            "A dangling pointer points to memory that has already been freed or is no longer valid.",
            "A memory leak occurs when allocated memory is no longer accessible but has not been released using free.",
            "A structure can contain members of different types and each member has separate storage. A union shares the same memory among all members.",
            "A function pointer stores the address of a function and can be used to call functions indirectly or implement callbacks.",
            "malloc allocates memory, calloc allocates and initializes memory to zero, realloc changes an existing allocation size, and free releases allocated memory.",
            "Pointer arithmetic changes a pointer based on the size of its data type. For example, incrementing an int pointer moves it by sizeof(int) bytes.",
            "A C program's memory is generally organized into text/code, initialized data, uninitialized data, heap, and stack regions."
        ],

        "advanced": [
            "To debug a complex segmentation fault, I would reproduce the issue, inspect the stack trace, use a debugger such as GDB, check pointer values and memory access, and use tools such as AddressSanitizer.",
            "A memory-efficient C application should use appropriate data structures, avoid unnecessary allocations, release memory correctly, reuse buffers when practical, and minimize memory fragmentation.",
            "A buffer overflow occurs when data is written beyond the allocated boundary of a buffer. It can cause crashes, data corruption, or security vulnerabilities.",
            "Memory leaks can be detected using tools such as Valgrind or AddressSanitizer and prevented through disciplined ownership and correct use of free.",
            "Multithreaded C programs must consider synchronization, race conditions, shared memory, mutexes, deadlocks, and thread-safe data access.",
            "I would optimize C code by profiling first, identifying bottlenecks, improving algorithms and data structures, reducing unnecessary operations, and using compiler optimization carefully.",
            "Undefined behavior means the C standard does not define what should happen. Examples include accessing an array outside its bounds and using an invalid pointer.",
            "A safe dynamic memory strategy should clearly define ownership, check allocation results, initialize memory when required, release resources exactly once, and avoid dangling pointers.",
            "A race condition occurs when multiple threads access shared data concurrently and the result depends on execution order. Mutexes or other synchronization mechanisms can prevent it.",
            "For a production C application, I would reproduce the issue if possible, collect logs and core dumps, inspect stack traces, use debugging tools, analyze memory and concurrency problems, and create a controlled fix."
        ]
    },

    # =====================================================
    # PYTHON
    # =====================================================
    "Python": {
        "intermediate": [
            "Common Python data types include int, float, str, bool, list, tuple, set, and dict.",
            "A list is mutable, while a tuple is immutable. Lists are generally used when the collection may change.",
            "A dictionary stores data as key-value pairs and provides fast lookup by key.",
            "A function is a reusable block of code defined using the def keyword.",
            "if, elif, and else are used to execute different blocks of code depending on conditions.",
            "A list comprehension is a concise way to create a list from an iterable, optionally using a condition.",
            "== checks whether two values are equal, while is checks whether two references point to the same object.",
            "Mutable objects can be changed after creation, such as lists and dictionaries. Immutable objects cannot be changed, such as strings, integers, and tuples.",
            "Exception handling uses try and except to catch runtime errors. else and finally can also be used for additional control.",
            "A module is a Python file containing code. A package is a directory containing related modules, typically organized as a Python package."
        ],

        "medium": [
            "Object-oriented programming organizes software around classes and objects and supports concepts such as encapsulation, inheritance, polymorphism, and abstraction.",
            "Inheritance allows a class to reuse and extend the attributes and methods of another class.",
            "A decorator is a function that modifies or extends the behavior of another function without changing its source code.",
            "A generator produces values lazily using yield, which can reduce memory usage for large data sequences.",
            "A shallow copy copies the outer object while nested objects may still be shared. A deep copy recursively copies nested objects.",
            "A lambda is a small anonymous function, commonly used with functions such as map, filter, and sorted.",
            "Python manages memory automatically using reference counting and a garbage collector that handles reference cycles.",
            "*args collects extra positional arguments, while **kwargs collects extra keyword arguments.",
            "A virtual environment provides an isolated Python environment so project dependencies do not conflict with other projects.",
            "I would debug a Python runtime error by reading the traceback, identifying the failing line, checking variable values and assumptions, reproducing the problem, and testing the fix."
        ],

        "advanced": [
            "The Python Global Interpreter Lock allows only one thread at a time to execute Python bytecode in the standard CPython implementation. It can limit CPU-bound multithreaded workloads, while threads remain useful for many I/O-bound tasks.",
            "I would optimize a slow Python application by profiling it first, identifying bottlenecks, improving algorithms, reducing unnecessary work, optimizing database queries, caching repeated operations, and using concurrency where appropriate.",
            "Multithreading uses multiple threads within one process and is useful for many I/O-bound workloads. Multiprocessing uses separate processes and can execute CPU-bound Python code in parallel.",
            "Python primarily uses reference counting for memory management and also has a cyclic garbage collector to detect reference cycles.",
            "A scalable Python backend should use modular architecture, efficient database access, caching, asynchronous or background processing where appropriate, horizontal scaling, monitoring, and secure APIs.",
            "Asynchronous programming allows a program to handle other tasks while waiting for I/O. async defines asynchronous functions and await waits for asynchronous operations without blocking the event loop.",
            "I would investigate a Python memory leak using memory profilers, tracemalloc, heap analysis, object lifetime inspection, and by checking for growing collections or resources that are not released.",
            "A secure Python web application should validate input, use parameterized queries, secure authentication, protect secrets, configure HTTPS, prevent common web attacks, and keep dependencies updated.",
            "Caching strategies include application-level caching, database query caching, distributed caches such as Redis, HTTP caching, and CDN caching depending on the workload.",
            "For production debugging, I would inspect logs, metrics, traces, error reports, recent deployments, resource usage, database performance, and reproduce the issue safely before applying and validating a fix."
        ]
    },

    # =====================================================
    # JAVA
    # =====================================================
    "Java": {
        "intermediate": [
            "Java is object-oriented, platform independent, robust, secure, portable, and supports automatic memory management.",
            "JDK is used to develop Java applications, JRE provides the environment to run Java applications, and JVM executes Java bytecode.",
            "A class is a blueprint defining data and behavior. An object is an instance of a class.",
            "Inheritance allows a class to acquire properties and methods from another class.",
            "Method overloading means defining multiple methods with the same name but different parameter lists.",
            "Method overriding occurs when a subclass provides its own implementation of a method inherited from a superclass.",
            "An interface defines a contract that classes can implement. It can contain abstract methods and, in modern Java, default and static methods.",
            "Java exception handling uses try, catch, finally, throw, and throws to manage exceptional conditions.",
            "ArrayList provides fast indexed access and is backed by a dynamic array. LinkedList is based on linked nodes and can be useful for certain insertion and removal operations.",
            "== compares primitive values or object references, while equals() is generally used to compare object content when properly implemented."
        ],

        "medium": [
            "The four main OOP principles are encapsulation, inheritance, polymorphism, and abstraction.",
            "Java garbage collection automatically identifies objects that are no longer reachable and reclaims their memory.",
            "Multithreading allows multiple threads to execute concurrently within a Java application.",
            "HashMap is generally unsynchronized and allows one null key, while Hashtable is synchronized and does not allow null keys or values.",
            "Checked exceptions are checked by the compiler, while unchecked exceptions are subclasses of RuntimeException and are not required to be declared.",
            "The Java Collections Framework provides interfaces and implementations such as List, Set, Map, Queue, ArrayList, HashSet, and HashMap.",
            "Synchronization controls concurrent access to shared resources to prevent inconsistent results and race conditions.",
            "An abstract class can contain state, constructors, concrete methods, and abstract methods. An interface primarily defines a contract and supports multiple implementation inheritance.",
            "String is immutable, StringBuilder is mutable and generally preferred for single-threaded string modification, while StringBuffer is synchronized.",
            "I would debug a Java runtime exception by reading the stack trace, identifying the root cause, inspecting the relevant code and values, reproducing the issue, and testing the fix."
        ],

        "advanced": [
            "JVM memory includes areas such as heap, stacks, metaspace, program counters, and native memory. Objects are mainly stored on the heap while each thread has its own stack.",
            "I would optimize a high-performance Java application by profiling it, optimizing algorithms and database access, tuning garbage collection, improving concurrency, reducing allocations, and monitoring system behavior.",
            "Java concurrency provides threads, executors, thread pools, synchronization primitives, locks, concurrent collections, and atomic operations for safe concurrent execution.",
            "Garbage collection can temporarily affect application performance through CPU consumption and pause times. Appropriate collectors and heap configuration can reduce these effects.",
            "A scalable Java backend should use stateless services, efficient database access, caching, asynchronous processing where appropriate, load balancing, monitoring, and horizontal scaling.",
            "Deadlock occurs when threads wait indefinitely for locks held by each other. It can be prevented using consistent lock ordering, timeouts, and careful synchronization design.",
            "A Java memory leak can be investigated using heap dumps, profilers, garbage collection logs, object-retention analysis, and monitoring heap growth.",
            "The Java Memory Model defines how threads interact through memory, including visibility, ordering, and atomicity guarantees.",
            "A secure Java web application should use secure authentication, authorization, input validation, parameterized queries, HTTPS, secure configuration, dependency updates, and protection against common web vulnerabilities.",
            "Production debugging involves examining logs, metrics, traces, thread dumps, heap dumps, database behavior, recent changes, and reproducing the problem safely."
        ]
    },

    # =====================================================
    # SQL
    # =====================================================
    "SQL": {
        "intermediate": [
            "SQL stands for Structured Query Language and is used to create, read, update, and delete data in relational databases.",
            "A primary key uniquely identifies each row in a table and cannot contain duplicate or NULL values.",
            "A foreign key is a column or group of columns that references a key in another table and helps maintain referential integrity.",
            "A unique key ensures that values in a column or group of columns are unique. Database systems may allow NULL depending on the implementation.",
            "DELETE removes selected rows and can use a WHERE clause, while TRUNCATE removes all rows more directly and generally cannot use WHERE.",
            "WHERE filters rows before grouping, while HAVING filters groups after GROUP BY.",
            "An INNER JOIN returns rows where matching values exist in both joined tables.",
            "GROUP BY groups rows with the same values so aggregate functions such as COUNT, SUM, AVG, MIN, and MAX can be applied.",
            "Normalization organizes data to reduce redundancy and prevent update, insertion, and deletion anomalies.",
            "An index is a data structure that can speed up data retrieval but adds storage overhead and can slow inserts and updates."
        ],

        "medium": [
            "Common SQL joins include INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN. They determine how matching and non-matching rows are returned.",
            "A subquery is a query nested inside another query and can be used in SELECT, FROM, WHERE, or HAVING clauses.",
            "A correlated subquery depends on values from the outer query and is evaluated in relation to each outer row.",
            "Normalization up to 3NF generally removes repeating groups, partial dependencies, and transitive dependencies while preserving appropriate relationships.",
            "A composite key consists of multiple columns that together uniquely identify a row.",
            "ACID stands for Atomicity, Consistency, Isolation, and Durability and describes important properties of reliable transactions.",
            "A transaction is a sequence of database operations treated as a single logical unit of work.",
            "A view is a virtual table defined by a SQL query. It can simplify complex queries and provide controlled access to data.",
            "SQL queries can be optimized using suitable indexes, efficient joins, filtering early, avoiding unnecessary columns, examining execution plans, and improving schema design.",
            "UNION combines query results and removes duplicates, while UNION ALL combines results without removing duplicates and is usually faster."
        ],

        "advanced": [
            "I would optimize a slow SQL query by examining its execution plan, checking indexes, reviewing joins and filters, reducing unnecessary data retrieval, and addressing expensive operations.",
            "Indexes improve read performance but consume storage and increase the cost of inserts, updates, and deletes. Choosing indexes requires balancing read and write workloads.",
            "A database for thousands of concurrent users should use proper normalization, indexing, connection pooling, transactions, caching where appropriate, monitoring, and scaling strategies.",
            "Transactions provide reliable changes to data. Isolation levels control how concurrent transactions can see each other's changes and balance consistency with concurrency.",
            "Database deadlocks occur when transactions hold locks and wait for resources held by each other. They can be reduced using consistent access order, short transactions, and appropriate isolation and locking strategies.",
            "Performance bottlenecks can be identified using query execution plans, database monitoring, slow-query logs, CPU and I/O metrics, lock analysis, and workload profiling.",
            "Database partitioning divides large tables or indexes into smaller logical pieces based on a partition key, improving manageability and potentially query performance.",
            "Replication maintains copies of database data on multiple servers. It can improve availability and read scalability depending on the replication design.",
            "A production database should use strong authentication, least-privilege access, encryption, secure backups, auditing, patching, network controls, and protection of sensitive credentials.",
            "A scalable relational architecture may use normalized transactional storage, carefully designed indexes, connection pooling, read replicas, caching, partitioning where needed, backups, monitoring, and horizontal service scaling."
        ]
    },

    # =====================================================
    # WEB DEVELOPMENT
    # =====================================================
    "Web Development": {
        "intermediate": [
            "HTML stands for HyperText Markup Language and defines the structure and content of web pages.",
            "HTML provides the structure of a page, while CSS controls presentation such as colors, spacing, fonts, and layout.",
            "JavaScript adds behavior and interactivity to web pages and can also be used for server-side development.",
            "An id identifies a specific element and should normally be unique on a page, while a class can be applied to multiple elements.",
            "Semantic HTML elements such as header, nav, main, section, article, and footer describe the meaning and structure of content.",
            "The CSS box model describes an element as content surrounded by padding, border, and margin.",
            "Responsive web design allows a website to adapt to different screen sizes and devices using flexible layouts, media queries, and responsive units.",
            "Inline CSS is written directly on an element, internal CSS is placed in a style block, and external CSS is stored in a separate stylesheet.",
            "The DOM is a programming representation of an HTML document that JavaScript can use to read and modify page content and structure.",
            "let and const provide block scope. const cannot be reassigned, while let can be reassigned. var has function scope and older JavaScript behavior."
        ],

        "medium": [
            "Flexbox is mainly designed for one-dimensional layouts, while CSS Grid is designed for two-dimensional rows and columns.",
            "Event bubbling means an event triggered on a child element can propagate upward through its parent elements.",
            "Promises represent eventual completion or failure of asynchronous operations. async and await provide a cleaner syntax for working with promises.",
            "localStorage persists data across browser sessions, while sessionStorage normally lasts only for the current browser tab or session.",
            "Form validation checks user input against expected rules before submitting data. Validation can be performed on the client and must also be performed securely on the server.",
            "A REST API exposes resources through HTTP endpoints and allows clients to communicate with server-side applications.",
            "GET retrieves data, POST creates or submits data, PUT generally replaces or updates a resource, and DELETE removes a resource.",
            "Authentication verifies who a user is, while authorization determines what an authenticated user is allowed to access.",
            "Page loading can be optimized using compressed assets, caching, image optimization, lazy loading, code splitting, minimizing requests, and efficient server responses.",
            "Responsive design uses flexible layouts and CSS media queries to adjust styles based on viewport characteristics."
        ],

        "advanced": [
            "A scalable full-stack application can use a CDN and load balancer in front of stateless application servers, caching, scalable databases, background workers, monitoring, and automated deployment.",
            "Browser caching stores resources locally, CDN caching stores content near users, and server-side caching stores reusable results closer to application logic or data sources.",
            "Secure token authentication should use short-lived access tokens, securely managed refresh tokens, HTTPS, appropriate storage, token rotation where appropriate, expiration, and server-side authorization checks.",
            "WebSockets provide persistent two-way communication between client and server and are useful for real-time applications such as chat, live notifications, and collaborative systems.",
            "A JavaScript memory leak can be investigated using browser developer tools, heap snapshots, allocation profiling, and checking event listeners, timers, closures, and retained objects.",
            "A large single-page application can be optimized through code splitting, lazy loading, tree shaking, efficient rendering, caching, optimized assets, and reducing unnecessary state updates.",
            "Code splitting divides JavaScript into smaller bundles that can be loaded when needed. Lazy loading delays loading resources until they are required.",
            "A secure API should enforce authentication and authorization, validate input, use HTTPS, apply rate limiting, protect secrets, use secure headers, and prevent injection and other common attacks.",
            "High traffic and sudden load spikes can be handled using load balancing, horizontal scaling, caching, CDN delivery, queues, autoscaling, database scaling, rate limiting, and graceful degradation.",
            "Production debugging should combine logs, metrics, traces, browser performance tools, server monitoring, API timings, database analysis, and controlled reproduction."
        ]
    }
}

# =========================================================
# SAVE FILE
# =========================================================

with open(ANSWERS_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Technical answers added successfully.")