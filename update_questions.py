import json
from pathlib import Path

file = Path(r".\04 . templates\07 . sevices\08 . data\1 . question.json")

with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)

technical = data["technical"]

technical["C"]["medium"] = [
    "Explain pointers and pointer-to-pointer concepts in C.",
    "Explain the difference between structure and union in C.",
    "How does dynamic memory allocation work in C?",
    "Explain function pointers with an example.",
    "What is the difference between static and dynamic memory allocation?",
    "Explain command line arguments in C.",
    "How does recursion work in C? Give an example.",
    "Explain storage classes in C.",
    "What is the difference between an array and a pointer?",
    "How would you debug a segmentation fault in C?"
]

technical["Java"]["medium"] = [
    "Explain encapsulation, inheritance, polymorphism and abstraction in Java.",
    "What is the difference between an abstract class and an interface?",
    "Explain method overloading and method overriding with examples.",
    "How does exception handling work in Java?",
    "What is the difference between ArrayList, HashSet and HashMap?",
    "Explain the difference between final, finally and finalize.",
    "What is a constructor in Java?",
    "Explain Java access modifiers.",
    "What is the difference between String and StringBuilder?",
    "Explain how threads are created in Java."
]

technical["Python"]["medium"] = [
    "Explain the difference between list, tuple, set and dictionary in Python.",
    "What are decorators and where are they useful?",
    "Explain generators and iterators in Python.",
    "What is the difference between shallow copy and deep copy?",
    "Explain inheritance and polymorphism in Python.",
    "What are lambda functions and where would you use them?",
    "Explain exception handling using try, except, else and finally.",
    "What are *args and **kwargs?",
    "Explain Python modules and packages.",
    "How would you debug a Python program that produces an unexpected result?"
]

technical["SQL"]["medium"] = [
    "Explain the difference between INNER JOIN, LEFT JOIN and RIGHT JOIN.",
    "What is normalization and why is it used?",
    "Explain primary key, foreign key and composite key.",
    "What is a subquery and when would you use one?",
    "Explain GROUP BY and HAVING with an example.",
    "What is a database transaction?",
    "Explain the ACID properties of a transaction.",
    "What is the difference between UNION and UNION ALL?",
    "What is a view and why would you use it?",
    "How would you optimize a query that is taking too long?"
]

technical["Web Development"] = {
    "intermediate": [
        "What is HTML and what is it used for?",
        "What is the difference between HTML and CSS?",
        "What is JavaScript and why is it used in web development?",
        "What is the difference between id and class in HTML?",
        "What are semantic HTML elements?",
        "What is the CSS box model?",
        "What is responsive web design?",
        "What is the difference between inline, internal and external CSS?",
        "What is the DOM in JavaScript?",
        "What is the difference between let, const and var in JavaScript"
    ],
    "medium": [
        "Explain the difference between Flexbox and CSS Grid.",
        "What is event bubbling in JavaScript?",
        "Explain JavaScript promises and async/await.",
        "What is the difference between localStorage and sessionStorage?",
        "How does form validation work in JavaScript?",
        "What is REST API and how is it used in web applications?",
        "Explain HTTP GET, POST, PUT and DELETE methods.",
        "What is the difference between authentication and authorization?",
        "How would you optimize the loading performance of a web page?",
        "Explain responsive design using media queries."
    ],
    "hard": [
        "Explain how the browser renders an HTML page from request to screen.",
        "How would you design a scalable frontend application?",
        "Explain CORS and why it occurs in web applications.",
        "How would you secure a web application against XSS attacks?",
        "How would you protect a web application against CSRF attacks?",
        "Explain debouncing and throttling in JavaScript.",
        "How would you optimize a web application with slow API responses?",
        "Explain client-side and server-side rendering.",
        "How would you design a frontend application that consumes multiple REST APIs?",
        "Describe how you would debug a production web application performance issue."
    ],
    "advanced": [
        "How would you architect a scalable full-stack web application for thousands of concurrent users?",
        "Explain browser caching, CDN caching and server-side caching strategies.",
        "How would you design authentication using secure tokens and refresh tokens?",
        "Explain how WebSockets work and when you would use them instead of REST APIs.",
        "How would you investigate a memory leak in a JavaScript application?",
        "How would you optimize a large single-page application?",
        "Explain code splitting and lazy loading in modern web applications.",
        "How would you design a secure API consumed by a web frontend?",
        "How would you handle high traffic and sudden load spikes in a web application?",
        "Describe how you would debug a production-level full-stack web application."
    ]
}

with open(file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("question.json updated successfully.")
print("Technical tracks:", ", ".join(technical.keys()))
print("C:", len(technical["C"]["intermediate"]), len(technical["C"]["medium"]), len(technical["C"]["hard"]), len(technical["C"]["advanced"]))
print("Java:", len(technical["Java"]["intermediate"]), len(technical["Java"]["medium"]), len(technical["Java"]["hard"]), len(technical["Java"]["advanced"]))
print("Python:", len(technical["Python"]["intermediate"]), len(technical["Python"]["medium"]), len(technical["Python"]["hard"]), len(technical["Python"]["advanced"]))
print("SQL:", len(technical["SQL"]["intermediate"]), len(technical["SQL"]["medium"]), len(technical["SQL"]["hard"]), len(technical["SQL"]["advanced"]))
print("Web Development:", len(technical["Web Development"]["intermediate"]), len(technical["Web Development"]["medium"]), len(technical["Web Development"]["hard"]), len(technical["Web Development"]["advanced"]))
