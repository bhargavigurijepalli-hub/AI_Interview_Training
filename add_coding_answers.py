from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

ANSWERS_FILE = (
    BASE_DIR
    / "04 . templates"
    / "07 . sevices"
    / "08 . data"
    / "3 . answers.json"
)

with open(ANSWERS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

data["coding"] = {
    "C": {
        "Easy": [
            """#include <stdio.h>

int main() {
    int arr[] = {10, 25, 5, 40, 15};
    int n = 5;
    int largest = arr[0];

    for (int i = 1; i < n; i++) {
        if (arr[i] > largest)
            largest = arr[i];
    }

    printf("Largest = %d", largest);
    return 0;
}""",

            """#include <stdio.h>
#include <string.h>

int main() {
    char str[] = "hello";
    int i, n = strlen(str);

    for (i = n - 1; i >= 0; i--)
        printf("%c", str[i]);

    return 0;
}""",

            """#include <stdio.h>

int main() {
    int n = 29;
    int prime = 1;

    if (n < 2)
        prime = 0;

    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            prime = 0;
            break;
        }
    }

    if (prime)
        printf("Prime");
    else
        printf("Not Prime");

    return 0;
}"""
        ],

        "Medium": [
            """#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

struct Node* reverse(struct Node *head) {
    struct Node *prev = NULL;
    struct Node *curr = head;

    while (curr != NULL) {
        struct Node *next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }

    return prev;
}""",

            """#include <stdio.h>
#include <limits.h>

int main() {
    int arr[] = {10, 25, 5, 40, 30};
    int n = 5;
    int largest = INT_MIN;
    int second = INT_MIN;

    for (int i = 0; i < n; i++) {
        if (arr[i] > largest) {
            second = largest;
            largest = arr[i];
        } else if (arr[i] > second && arr[i] != largest) {
            second = arr[i];
        }
    }

    printf("Second largest = %d", second);
    return 0;
}""",

            """#include <stdio.h>

#define MAX 100

int stack[MAX];
int top = -1;

void push(int value) {
    if (top == MAX - 1)
        printf("Stack Overflow");
    else
        stack[++top] = value;
}

int pop() {
    if (top == -1)
        return -1;

    return stack[top--];
}

int main() {
    push(10);
    push(20);
    printf("%d", pop());

    return 0;
}"""
        ],

        "Hard": [
            """#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *left;
    struct Node *right;
};

struct Node* insert(struct Node* root, int value) {
    if (root == NULL) {
        root = malloc(sizeof(struct Node));
        root->data = value;
        root->left = root->right = NULL;
        return root;
    }

    if (value < root->data)
        root->left = insert(root->left, value);
    else
        root->right = insert(root->right, value);

    return root;
}

void inorder(struct Node* root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->data);
        inorder(root->right);
    }
}""",

            """#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

int hasCycle(struct Node *head) {
    struct Node *slow = head;
    struct Node *fast = head;

    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast)
            return 1;
    }

    return 0;
}""",

            """#include <stdio.h>

#define V 5

void BFS(int graph[V][V], int start) {
    int queue[V];
    int visited[V] = {0};
    int front = 0, rear = 0;

    queue[rear++] = start;
    visited[start] = 1;

    while (front < rear) {
        int node = queue[front++];
        printf("%d ", node);

        for (int i = 0; i < V; i++) {
            if (graph[node][i] && !visited[i]) {
                visited[i] = 1;
                queue[rear++] = i;
            }
        }
    }
}"""
        ]
    },

    "Python": {
        "Easy": [
            """s = "swiss"

for ch in s:
    if s.count(ch) == 1:
        print(ch)
        break""",

            """n = 29

if n < 2:
    print("Not Prime")
else:
    prime = True

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            prime = False
            break

    print("Prime" if prime else "Not Prime")""",

            """numbers = [10, 25, 5, 40, 15]
print(max(numbers))"""
        ],

        "Medium": [
            """def longest_substring(s):
    seen = {}
    left = 0
    longest = 0

    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1

        seen[char] = right
        longest = max(longest, right - left + 1)

    return longest

print(longest_substring("abcabcbb"))""",

            """class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def reverse(head):
    prev = None
    current = head

    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    return prev""",

            """numbers = [1, 2, 3, 2, 4, 1, 5]

duplicates = []
seen = set()

for num in numbers:
    if num in seen:
        duplicates.append(num)
    else:
        seen.add(num)

print(duplicates)"""
        ],

        "Hard": [
            """from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1

        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)""",

            """class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def has_cycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False""",

            """from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        print(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)


def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()

    visited.add(node)
    print(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)"""
        ]
    },

    "Java": {
        "Easy": [
            """public class Main {
    public static void main(String[] args) {
        int[] arr = {10, 20, 5, 40, 30};

        int largest = arr[0];
        int second = Integer.MIN_VALUE;

        for (int x : arr) {
            if (x > largest) {
                second = largest;
                largest = x;
            } else if (x > second && x != largest) {
                second = x;
            }
        }

        System.out.println(second);
    }
}""",

            """public class Main {
    public static void main(String[] args) {
        String str = "hello";

        for (int i = str.length() - 1; i >= 0; i--) {
            System.out.print(str.charAt(i));
        }
    }
}""",

            """public class Main {
    public static void main(String[] args) {
        int n = 29;
        boolean prime = n >= 2;

        for (int i = 2; i * i <= n && prime; i++) {
            if (n % i == 0)
                prime = false;
        }

        System.out.println(prime ? "Prime" : "Not Prime");
    }
}"""
        ],

        "Medium": [
            """class Node {
    int data;
    Node next;

    Node(int data) {
        this.data = data;
    }
}

class Solution {
    static Node reverse(Node head) {
        Node prev = null;
        Node current = head;

        while (current != null) {
            Node next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }

        return prev;
    }
}""",

            """import java.util.Stack;

public class Main {
    public static void main(String[] args) {
        Stack<Integer> stack = new Stack<>();

        stack.push(10);
        stack.push(20);
        stack.push(30);

        System.out.println(stack.pop());
    }
}""",

            """import java.util.*;

public class Main {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 2, 4, 1};

        Set<Integer> seen = new HashSet<>();
        Set<Integer> duplicates = new HashSet<>();

        for (int x : arr) {
            if (!seen.add(x))
                duplicates.add(x);
        }

        System.out.println(duplicates);
    }
}"""
        ],

        "Hard": [
            """import java.util.*;

class LRUCache {
    private final int capacity;
    private final LinkedHashMap<Integer, Integer> cache;

    LRUCache(int capacity) {
        this.capacity = capacity;

        cache = new LinkedHashMap<Integer, Integer>(
            capacity, 0.75f, true
        ) {
            protected boolean removeEldestEntry(
                    Map.Entry<Integer, Integer> eldest) {
                return size() > LRUCache.this.capacity;
            }
        };
    }

    int get(int key) {
        return cache.getOrDefault(key, -1);
    }

    void put(int key, int value) {
        cache.put(key, value);
    }
}""",

            """class Node {
    int data;
    Node next;

    Node(int data) {
        this.data = data;
    }
}

class Solution {
    static boolean hasCycle(Node head) {
        Node slow = head;
        Node fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;

            if (slow == fast)
                return true;
        }

        return false;
    }
}""",

            """import java.util.*;

public class GraphTraversal {
    static void bfs(Map<Integer, List<Integer>> graph, int start) {
        Queue<Integer> queue = new LinkedList<>();
        Set<Integer> visited = new HashSet<>();

        queue.add(start);
        visited.add(start);

        while (!queue.isEmpty()) {
            int node = queue.poll();
            System.out.print(node + " ");

            for (int next : graph.getOrDefault(node, new ArrayList<>())) {
                if (visited.add(next))
                    queue.add(next);
            }
        }
    }

    static void dfs(
        Map<Integer, List<Integer>> graph,
        int node,
        Set<Integer> visited) {

        visited.add(node);
        System.out.print(node + " ");

        for (int next : graph.getOrDefault(node, new ArrayList<>())) {
            if (!visited.contains(next))
                dfs(graph, next, visited);
        }
    }
}"""
        ]
    },

    "SQL": {
        "Easy": [
            """SELECT MAX(salary) AS second_highest
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);""",

            """SELECT *
FROM Employee
WHERE salary > 50000;""",

            """SELECT department_id, COUNT(*) AS employee_count
FROM Employee
GROUP BY department_id;"""
        ],

        "Medium": [
            """SELECT e.*
FROM Employee e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM Employee e2
    WHERE e2.department_id = e.department_id
);""",

            """SELECT department_id, MAX(salary) AS second_highest_salary
FROM (
    SELECT department_id,
           salary,
           DENSE_RANK() OVER (
               PARTITION BY department_id
               ORDER BY salary DESC
           ) AS rnk
    FROM Employee
) ranked
WHERE rnk = 2
GROUP BY department_id;""",

            """SELECT name, email, COUNT(*) AS duplicate_count
FROM Employee
GROUP BY name, email
HAVING COUNT(*) > 1;"""
        ],

        "Hard": [
            """SELECT *
FROM (
    SELECT e.*,
           DENSE_RANK() OVER (
               PARTITION BY department_id
               ORDER BY salary DESC
           ) AS rnk
    FROM Employee e
) ranked
WHERE rnk <= 3;""",

            """SELECT department_id,
       MAX(salary) - MIN(salary) AS salary_difference
FROM Employee
GROUP BY department_id;""",

            """SELECT employee_id,
       joining_date,
       salary,
       SUM(salary) OVER (
           ORDER BY joining_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM Employee
ORDER BY joining_date;"""
        ]
    },

    "Web Development": {
        "Easy": [
            """<!DOCTYPE html>
<html>
<body>

<form>
    <input type="text" name="name" placeholder="Name">
    <input type="email" name="email" placeholder="Email">
    <input type="password" name="password" placeholder="Password">
    <button type="submit">Register</button>
</form>

</body>
</html>""",

            """function reverseString(str) {
    return str.split("").reverse().join("");
}

console.log(reverseString("hello"));""",

            """<!DOCTYPE html>
<html>
<head>
<style>
nav {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
}

@media (max-width: 600px) {
    nav {
        flex-direction: column;
    }
}
</style>
</head>

<body>
<nav>
    <a href="#">Home</a>
    <a href="#">About</a>
    <a href="#">Contact</a>
</nav>
</body>
</html>"""
        ],

        "Medium": [
            """const searchBox = document.getElementById("search");
const products = document.querySelectorAll(".product");

searchBox.addEventListener("input", function () {
    const value = this.value.toLowerCase();

    products.forEach(product => {
        const name = product.textContent.toLowerCase();
        product.style.display =
            name.includes(value) ? "block" : "none";
    });
});""",

            """<!DOCTYPE html>
<html>
<head>
<style>
.container {
    display: grid;
    grid-template-columns: repeat(
        auto-fit,
        minmax(200px, 1fr)
    );
    gap: 20px;
}
</style>
</head>

<body>
<div class="container">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
</body>
</html>""",

            """const form = document.querySelector("form");

form.addEventListener("submit", function(event) {
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;

    if (!email.includes("@") || password.length < 8) {
        event.preventDefault();
        alert("Enter a valid email and password.");
    }
});"""
        ],

        "Hard": [
            """async function loadUsers() {
    try {
        const response = await fetch(
            "https://api.example.com/users"
        );

        const users = await response.json();

        const list = document.getElementById("users");

        users.forEach(user => {
            const item = document.createElement("li");
            item.textContent = user.name;
            list.appendChild(item);
        });
    } catch (error) {
        console.error(error);
    }
}

loadUsers();""",

            """let timer;

const searchBox = document.querySelector("#search");

searchBox.addEventListener("input", function() {
    clearTimeout(timer);

    timer = setTimeout(async () => {
        const response = await fetch(
            "/api/search?q=" +
            encodeURIComponent(searchBox.value)
        );

        const data = await response.json();
        console.log(data);
    }, 500);
});""",

            """<!DOCTYPE html>
<html>
<head>
<style>
.container {
    max-width: 1000px;
    margin: auto;
    padding: 20px;
}

input, button {
    width: 100%;
    padding: 10px;
    margin: 5px 0;
}

@media (min-width: 700px) {
    input {
        width: 45%;
    }
}
</style>
</head>

<body>

<div class="container">
    <h1>Application</h1>

    <form id="form">
        <input id="name" placeholder="Name">
        <input id="email" placeholder="Email">
        <button type="submit">Submit</button>
    </form>

    <div id="result"></div>
</div>

<script>
document.getElementById("form")
.addEventListener("submit", async function(event) {
    event.preventDefault();

    const response = await fetch("/api/data");
    const data = await response.json();

    document.getElementById("result")
        .textContent = JSON.stringify(data);
});
</script>

</body>
</html>"""
        ]
    }
}

with open(ANSWERS_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Coding answers added successfully.")