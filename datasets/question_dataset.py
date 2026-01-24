"""
Question Dataset for Training and Generation
Structured dataset of questions with metadata for AI training
Based on real-world coding interview questions from Kaggle datasets
"""

# Database: MySQL (XAMPP)
# All questions are stored in MySQL database: assessment_orchestrator
# Table: questions
# Questions are also used for few-shot learning with Gemini API

QUESTION_DATASET = [
    {
    "id": 1,
    "title": "Java Hello World",
    "description": "Write a simple Java program that prints 'Hello, World!' to the console.",
    "skill": "java",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 5,
    "tags": [
        "java",
        "basics",
        "syntax"
    ],
    "solution_hint": "Use System.out.println()",
    "test_cases": [
        {
            "input": {},
            "output": "Hello, World!"
        }
    ],
    "learning_objectives": [
        "Java syntax",
        "Basic I/O",
        "Main method"
    ]
},
    {
    "id": 2,
    "title": "Java Variables and Data Types",
    "description": "Declare and initialize variables of different data types in Java (int, double, String, boolean).",
    "skill": "java",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 8,
    "tags": [
        "java",
        "variables",
        "data-types"
    ],
    "solution_hint": "Use appropriate data type declarations",
    "test_cases": [],
    "learning_objectives": [
        "Data types",
        "Variable declaration",
        "Type system"
    ]
},
    {
    "id": 3,
    "title": "Java If-Else Statement",
    "description": "Write a Java program that checks if a number is positive, negative, or zero using if-else statements.",
    "skill": "java",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 10,
    "tags": [
        "java",
        "control-flow",
        "conditionals"
    ],
    "solution_hint": "Use if-else-if ladder",
    "test_cases": [
        {
            "input": {
                "num": 5
            },
            "output": "Positive"
        },
        {
            "input": {
                "num": -3
            },
            "output": "Negative"
        },
        {
            "input": {
                "num": 0
            },
            "output": "Zero"
        }
    ],
    "learning_objectives": [
        "Conditional statements",
        "Control flow",
        "Logic"
    ]
},
    {
    "id": 4,
    "title": "Java For Loop",
    "description": "Write a Java program to print numbers from 1 to 10 using a for loop.",
    "skill": "java",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 8,
    "tags": [
        "java",
        "loops",
        "iteration"
    ],
    "solution_hint": "Use for(int i=1; i<=10; i++)",
    "test_cases": [
        {
            "input": {},
            "output": "1 2 3 4 5 6 7 8 9 10"
        }
    ],
    "learning_objectives": [
        "Loop constructs",
        "Iteration",
        "Control flow"
    ]
},
    {
    "id": 5,
    "title": "Java Array Basics",
    "description": "Create an array of integers in Java, initialize it with values, and print all elements.",
    "skill": "java",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 12,
    "tags": [
        "java",
        "arrays",
        "collections"
    ],
    "solution_hint": "Use int[] array = new int[size]",
    "test_cases": [],
    "learning_objectives": [
        "Array declaration",
        "Array initialization",
        "Array traversal"
    ]
},
    {
    "id": 6,
    "title": "Java String Methods",
    "description": "Write a Java program that demonstrates common String methods: length(), charAt(), substring(), equals().",
    "skill": "java",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 20,
    "tags": [
        "java",
        "strings",
        "methods"
    ],
    "solution_hint": "Use String class methods",
    "test_cases": [],
    "learning_objectives": [
        "String manipulation",
        "String API",
        "Method calls"
    ]
},
    {
    "id": 7,
    "title": "Java ArrayList Operations",
    "description": "Implement a Java program that uses ArrayList to add, remove, and search for elements.",
    "skill": "java",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 25,
    "tags": [
        "java",
        "collections",
        "arraylist"
    ],
    "solution_hint": "Use ArrayList from java.util package",
    "test_cases": [],
    "learning_objectives": [
        "Collections framework",
        "ArrayList",
        "Dynamic arrays"
    ]
},
    {
    "id": 8,
    "title": "Java Method Overloading",
    "description": "Create a Java class with multiple methods having the same name but different parameters (method overloading).",
    "skill": "java",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 18,
    "tags": [
        "java",
        "oop",
        "methods"
    ],
    "solution_hint": "Same method name, different parameter lists",
    "test_cases": [],
    "learning_objectives": [
        "Method overloading",
        "Polymorphism",
        "Method signatures"
    ]
},
    {
    "id": 9,
    "title": "Java HashMap Usage",
    "description": "Write a Java program that uses HashMap to store and retrieve key-value pairs, and iterate through entries.",
    "skill": "java",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 22,
    "tags": [
        "java",
        "collections",
        "hashmap"
    ],
    "solution_hint": "Use HashMap from java.util package",
    "test_cases": [],
    "learning_objectives": [
        "HashMap",
        "Key-value pairs",
        "Iteration"
    ]
},
    {
    "id": 10,
    "title": "Java File I/O",
    "description": "Write a Java program that reads from a text file and writes to another file using FileReader and FileWriter.",
    "skill": "java",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 30,
    "tags": [
        "java",
        "file-io",
        "streams"
    ],
    "solution_hint": "Use FileReader, BufferedReader, FileWriter",
    "test_cases": [],
    "learning_objectives": [
        "File operations",
        "I/O streams",
        "Exception handling"
    ]
},
    {
    "id": 11,
    "title": "Java Custom Exception",
    "description": "Create a custom exception class in Java and demonstrate its usage with try-catch blocks.",
    "skill": "java",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 35,
    "tags": [
        "java",
        "exceptions",
        "error-handling"
    ],
    "solution_hint": "Extend Exception class and override constructors",
    "test_cases": [],
    "learning_objectives": [
        "Custom exceptions",
        "Exception hierarchy",
        "Error handling"
    ]
},
    {
    "id": 12,
    "title": "Java Reflection API",
    "description": "Write a Java program that uses Reflection API to inspect class methods, fields, and annotations at runtime.",
    "skill": "java",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 40,
    "tags": [
        "java",
        "reflection",
        "advanced"
    ],
    "solution_hint": "Use Class, Method, Field classes from java.lang.reflect",
    "test_cases": [],
    "learning_objectives": [
        "Reflection API",
        "Runtime inspection",
        "Metadata"
    ]
},
    {
    "id": 13,
    "title": "Java Generics Implementation",
    "description": "Implement a generic class in Java that can work with any data type, and demonstrate type safety.",
    "skill": "java",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 35,
    "tags": [
        "java",
        "generics",
        "type-safety"
    ],
    "solution_hint": "Use <T> syntax for generic type parameters",
    "test_cases": [],
    "learning_objectives": [
        "Generics",
        "Type parameters",
        "Type safety"
    ]
},
    {
    "id": 14,
    "title": "Java Streams API",
    "description": "Write a Java program using Streams API to filter, map, and reduce a collection of objects.",
    "skill": "java",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 38,
    "tags": [
        "java",
        "streams",
        "functional-programming"
    ],
    "solution_hint": "Use stream(), filter(), map(), reduce() methods",
    "test_cases": [],
    "learning_objectives": [
        "Streams API",
        "Functional programming",
        "Lambda expressions"
    ]
},
    {
    "id": 15,
    "title": "Java Concurrent Collections",
    "description": "Implement a thread-safe program using ConcurrentHashMap and demonstrate concurrent access patterns.",
    "skill": "java",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 45,
    "tags": [
        "java",
        "concurrency",
        "thread-safety"
    ],
    "solution_hint": "Use ConcurrentHashMap from java.util.concurrent",
    "test_cases": [],
    "learning_objectives": [
        "Concurrent collections",
        "Thread safety",
        "Concurrency"
    ]
},
    {
    "id": 16,
    "title": "Thread vs Process",
    "description": "Explain the difference between a thread and a process in Java. Provide examples.",
    "skill": "multithreading",
    "difficulty": "easy",
    "question_type": "mcq",
    "estimated_time_minutes": 10,
    "tags": [
        "multithreading",
        "basics",
        "concepts"
    ],
    "solution_hint": "Process has separate memory, thread shares memory space",
    "test_cases": [],
    "learning_objectives": [
        "Process vs Thread",
        "Memory management",
        "Concurrency basics"
    ]
},
    {
    "id": 17,
    "title": "Create Thread in Java",
    "description": "Write a Java program that creates a thread by extending Thread class and prints a message.",
    "skill": "multithreading",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 15,
    "tags": [
        "multithreading",
        "thread-creation",
        "java"
    ],
    "solution_hint": "Extend Thread class and override run() method",
    "test_cases": [],
    "learning_objectives": [
        "Thread creation",
        "Thread class",
        "run() method"
    ]
},
    {
    "id": 18,
    "title": "Runnable Interface",
    "description": "Create a thread in Java by implementing Runnable interface and demonstrate its usage.",
    "skill": "multithreading",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 15,
    "tags": [
        "multithreading",
        "runnable",
        "interface"
    ],
    "solution_hint": "Implement Runnable and pass to Thread constructor",
    "test_cases": [],
    "learning_objectives": [
        "Runnable interface",
        "Thread creation",
        "Interface implementation"
    ]
},
    {
    "id": 19,
    "title": "Thread Lifecycle",
    "description": "Explain the different states in a thread lifecycle: NEW, RUNNABLE, BLOCKED, WAITING, TERMINATED.",
    "skill": "multithreading",
    "difficulty": "easy",
    "question_type": "mcq",
    "estimated_time_minutes": 12,
    "tags": [
        "multithreading",
        "thread-states",
        "lifecycle"
    ],
    "solution_hint": "Use Thread.State enum to check thread state",
    "test_cases": [],
    "learning_objectives": [
        "Thread states",
        "Lifecycle management",
        "State transitions"
    ]
},
    {
    "id": 20,
    "title": "Start and Join Threads",
    "description": "Write a Java program that starts multiple threads and uses join() to wait for their completion.",
    "skill": "multithreading",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 18,
    "tags": [
        "multithreading",
        "thread-control",
        "join"
    ],
    "solution_hint": "Call start() to begin execution, join() to wait",
    "test_cases": [],
    "learning_objectives": [
        "Thread control",
        "join() method",
        "Thread synchronization"
    ]
},
    {
    "id": 21,
    "title": "Synchronized Method",
    "description": "Implement a Java class with synchronized methods to ensure thread-safe access to shared resources.",
    "skill": "multithreading",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 25,
    "tags": [
        "multithreading",
        "synchronization",
        "thread-safety"
    ],
    "solution_hint": "Use synchronized keyword on methods",
    "test_cases": [],
    "learning_objectives": [
        "Synchronization",
        "Thread safety",
        "Mutual exclusion"
    ]
},
    {
    "id": 22,
    "title": "Wait and Notify",
    "description": "Implement producer-consumer pattern in Java using wait() and notify() methods for thread communication.",
    "skill": "multithreading",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 35,
    "tags": [
        "multithreading",
        "wait-notify",
        "producer-consumer"
    ],
    "solution_hint": "Use synchronized blocks with wait() and notify()",
    "test_cases": [],
    "learning_objectives": [
        "Thread communication",
        "Wait/Notify",
        "Producer-Consumer pattern"
    ]
},
    {
    "id": 23,
    "title": "Thread Pool with ExecutorService",
    "description": "Create a thread pool using ExecutorService and submit multiple tasks for concurrent execution.",
    "skill": "multithreading",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 30,
    "tags": [
        "multithreading",
        "executor-service",
        "thread-pool"
    ],
    "solution_hint": "Use Executors.newFixedThreadPool() and submit() tasks",
    "test_cases": [],
    "learning_objectives": [
        "Thread pools",
        "ExecutorService",
        "Task execution"
    ]
},
    {
    "id": 24,
    "title": "ReentrantLock Usage",
    "description": "Implement thread synchronization using ReentrantLock instead of synchronized keyword.",
    "skill": "multithreading",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 28,
    "tags": [
        "multithreading",
        "reentrantlock",
        "locks"
    ],
    "solution_hint": "Use lock() and unlock() methods with try-finally",
    "test_cases": [],
    "learning_objectives": [
        "ReentrantLock",
        "Lock interface",
        "Explicit locking"
    ]
},
    {
    "id": 25,
    "title": "CountDownLatch Example",
    "description": "Use CountDownLatch to coordinate multiple threads, ensuring some threads wait for others to complete.",
    "skill": "multithreading",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 32,
    "tags": [
        "multithreading",
        "countdownlatch",
        "coordination"
    ],
    "solution_hint": "Use countDown() and await() methods",
    "test_cases": [],
    "learning_objectives": [
        "CountDownLatch",
        "Thread coordination",
        "Synchronization"
    ]
},
    {
    "id": 26,
    "title": "Deadlock Detection and Prevention",
    "description": "Identify and fix a deadlock scenario in Java multithreaded code. Implement deadlock prevention strategies.",
    "skill": "multithreading",
    "difficulty": "hard",
    "question_type": "debugging",
    "estimated_time_minutes": 45,
    "tags": [
        "multithreading",
        "deadlock",
        "debugging"
    ],
    "solution_hint": "Avoid circular wait, use lock ordering, timeout on locks",
    "test_cases": [],
    "learning_objectives": [
        "Deadlock detection",
        "Deadlock prevention",
        "Debugging"
    ]
},
    {
    "id": 27,
    "title": "Custom Thread Pool Implementation",
    "description": "Implement a custom thread pool from scratch in Java without using ExecutorService, with queue management.",
    "skill": "multithreading",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 50,
    "tags": [
        "multithreading",
        "thread-pool",
        "advanced"
    ],
    "solution_hint": "Use BlockingQueue for task queue, manage worker threads",
    "test_cases": [],
    "learning_objectives": [
        "Thread pool design",
        "Queue management",
        "Thread lifecycle"
    ]
},
    {
    "id": 28,
    "title": "Atomic Variables and CAS",
    "description": "Implement a thread-safe counter using AtomicInteger and explain Compare-And-Swap (CAS) operations.",
    "skill": "multithreading",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 40,
    "tags": [
        "multithreading",
        "atomic",
        "cas"
    ],
    "solution_hint": "Use AtomicInteger with getAndIncrement()",
    "test_cases": [],
    "learning_objectives": [
        "Atomic variables",
        "CAS operations",
        "Lock-free programming"
    ]
},
    {
    "id": 29,
    "title": "CompletableFuture Advanced Usage",
    "description": "Use CompletableFuture to chain asynchronous operations, handle errors, and combine multiple futures.",
    "skill": "multithreading",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 45,
    "tags": [
        "multithreading",
        "completablefuture",
        "async"
    ],
    "solution_hint": "Use thenApply(), thenCompose(), handle(), allOf()",
    "test_cases": [],
    "learning_objectives": [
        "CompletableFuture",
        "Async programming",
        "Future chaining"
    ]
},
    {
    "id": 30,
    "title": "ThreadLocal and Memory Leaks",
    "description": "Implement ThreadLocal usage and demonstrate how to prevent memory leaks by proper cleanup.",
    "skill": "multithreading",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 42,
    "tags": [
        "multithreading",
        "threadlocal",
        "memory-management"
    ],
    "solution_hint": "Use ThreadLocal with remove() in finally block",
    "test_cases": [],
    "learning_objectives": [
        "ThreadLocal",
        "Memory leaks",
        "Resource cleanup"
    ]
},
    {
    "id": 31,
    "title": "Find Maximum in Array",
    "description": "Write a function to find the maximum element in an array of integers.",
    "skill": "arrays",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 10,
    "tags": [
        "arrays",
        "searching",
        "basics"
    ],
    "solution_hint": "Iterate through array and track maximum value",
    "test_cases": [
        {
            "input": {
                "arr": [
                    3,
                    5,
                    2,
                    8,
                    1
                ]
            },
            "output": 8
        }
    ],
    "learning_objectives": [
        "Array traversal",
        "Linear search",
        "Basic algorithms"
    ]
},
    {
    "id": 32,
    "title": "Array Sum",
    "description": "Calculate the sum of all elements in an array.",
    "skill": "arrays",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 8,
    "tags": [
        "arrays",
        "summation",
        "basics"
    ],
    "solution_hint": "Iterate and accumulate sum",
    "test_cases": [
        {
            "input": {
                "arr": [
                    1,
                    2,
                    3,
                    4,
                    5
                ]
            },
            "output": 15
        }
    ],
    "learning_objectives": [
        "Array iteration",
        "Accumulation",
        "Basic operations"
    ]
},
    {
    "id": 33,
    "title": "Reverse Array",
    "description": "Reverse the elements of an array in-place without using extra space.",
    "skill": "arrays",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 15,
    "tags": [
        "arrays",
        "two-pointers",
        "manipulation"
    ],
    "solution_hint": "Use two pointers from start and end, swap elements",
    "test_cases": [
        {
            "input": {
                "arr": [
                    1,
                    2,
                    3,
                    4,
                    5
                ]
            },
            "output": [
                5,
                4,
                3,
                2,
                1
            ]
        }
    ],
    "learning_objectives": [
        "Two pointers",
        "In-place operations",
        "Array manipulation"
    ]
},
    {
    "id": 34,
    "title": "Find Element in Array",
    "description": "Search for a target element in an array and return its index, or -1 if not found.",
    "skill": "arrays",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 12,
    "tags": [
        "arrays",
        "searching",
        "linear-search"
    ],
    "solution_hint": "Linear search through array",
    "test_cases": [
        {
            "input": {
                "arr": [
                    10,
                    20,
                    30,
                    40
                ],
                "target": 30
            },
            "output": 2
        },
        {
            "input": {
                "arr": [
                    10,
                    20,
                    30,
                    40
                ],
                "target": 50
            },
            "output": -1
        }
    ],
    "learning_objectives": [
        "Linear search",
        "Array traversal",
        "Conditional logic"
    ]
},
    {
    "id": 35,
    "title": "Count Occurrences",
    "description": "Count how many times a specific element appears in an array.",
    "skill": "arrays",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 10,
    "tags": [
        "arrays",
        "counting",
        "iteration"
    ],
    "solution_hint": "Iterate and count matches",
    "test_cases": [
        {
            "input": {
                "arr": [
                    1,
                    2,
                    2,
                    3,
                    2,
                    4
                ],
                "target": 2
            },
            "output": 3
        }
    ],
    "learning_objectives": [
        "Array iteration",
        "Counting",
        "Conditional counting"
    ]
},
    {
    "id": 36,
    "title": "Two Sum Problem",
    "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
    "skill": "arrays",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 20,
    "tags": [
        "arrays",
        "hash-table",
        "two-sum"
    ],
    "solution_hint": "Use hash map to store complements",
    "test_cases": [
        {
            "input": {
                "nums": [
                    2,
                    7,
                    11,
                    15
                ],
                "target": 9
            },
            "output": [
                0,
                1
            ]
        },
        {
            "input": {
                "nums": [
                    3,
                    2,
                    4
                ],
                "target": 6
            },
            "output": [
                1,
                2
            ]
        }
    ],
    "learning_objectives": [
        "Hash table usage",
        "Time complexity optimization",
        "Two pointers"
    ]
},
    {
    "id": 37,
    "title": "Maximum Subarray (Kadane's Algorithm)",
    "description": "Find the contiguous subarray within an array which has the largest sum using Kadane's algorithm.",
    "skill": "arrays",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 25,
    "tags": [
        "arrays",
        "dynamic-programming",
        "kadane"
    ],
    "solution_hint": "Track maximum sum ending at each position",
    "test_cases": [
        {
            "input": {
                "nums": [
                    -2,
                    1,
                    -3,
                    4,
                    -1,
                    2,
                    1,
                    -5,
                    4
                ]
            },
            "output": 6
        }
    ],
    "learning_objectives": [
        "Dynamic programming",
        "Kadane's algorithm",
        "Subarray problems"
    ]
},
    {
    "id": 38,
    "title": "Product of Array Except Self",
    "description": "Given an array nums, return an array answer such that answer[i] is equal to the product of all elements of nums except nums[i].",
    "skill": "arrays",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 30,
    "tags": [
        "arrays",
        "prefix-sum",
        "math"
    ],
    "solution_hint": "Use prefix and suffix products",
    "test_cases": [
        {
            "input": {
                "nums": [
                    1,
                    2,
                    3,
                    4
                ]
            },
            "output": [
                24,
                12,
                8,
                6
            ]
        }
    ],
    "learning_objectives": [
        "Prefix products",
        "Array manipulation",
        "Mathematical operations"
    ]
},
    {
    "id": 39,
    "title": "3Sum Problem",
    "description": "Find all unique triplets in the array which gives the sum of zero.",
    "skill": "arrays",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 35,
    "tags": [
        "arrays",
        "two-pointers",
        "sorting"
    ],
    "solution_hint": "Sort array, use two pointers for each element",
    "test_cases": [
        {
            "input": {
                "nums": [
                    -1,
                    0,
                    1,
                    2,
                    -1,
                    -4
                ]
            },
            "output": [
                [
                    -1,
                    -1,
                    2
                ],
                [
                    -1,
                    0,
                    1
                ]
            ]
        }
    ],
    "learning_objectives": [
        "Two pointers",
        "Sorting",
        "Three sum algorithm"
    ]
},
    {
    "id": 40,
    "title": "Container With Most Water",
    "description": "Find two lines that together with the x-axis form a container, such that the container contains the most water.",
    "skill": "arrays",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 30,
    "tags": [
        "arrays",
        "two-pointers",
        "greedy"
    ],
    "solution_hint": "Use two pointers from both ends, move pointer with smaller height",
    "test_cases": [
        {
            "input": {
                "height": [
                    1,
                    8,
                    6,
                    2,
                    5,
                    4,
                    8,
                    3,
                    7
                ]
            },
            "output": 49
        }
    ],
    "learning_objectives": [
        "Two pointers",
        "Greedy algorithm",
        "Area calculation"
    ]
},
    {
    "id": 41,
    "title": "Trapping Rain Water",
    "description": "Given n non-negative integers representing an elevation map, compute how much water it can trap after raining.",
    "skill": "arrays",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 40,
    "tags": [
        "arrays",
        "two-pointers",
        "stack"
    ],
    "solution_hint": "Use two pointers or stack approach",
    "test_cases": [
        {
            "input": {
                "height": [
                    0,
                    1,
                    0,
                    2,
                    1,
                    0,
                    1,
                    3,
                    2,
                    1,
                    2,
                    1
                ]
            },
            "output": 6
        }
    ],
    "learning_objectives": [
        "Two pointers",
        "Stack",
        "Water trapping algorithm"
    ]
},
    {
    "id": 42,
    "title": "Merge Intervals",
    "description": "Given an array of intervals, merge all overlapping intervals and return an array of non-overlapping intervals.",
    "skill": "arrays",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 35,
    "tags": [
        "arrays",
        "sorting",
        "intervals"
    ],
    "solution_hint": "Sort by start time, merge overlapping intervals",
    "test_cases": [
        {
            "input": {
                "intervals": [
                    [
                        1,
                        3
                    ],
                    [
                        2,
                        6
                    ],
                    [
                        8,
                        10
                    ],
                    [
                        15,
                        18
                    ]
                ]
            },
            "output": [
                [
                    1,
                    6
                ],
                [
                    8,
                    10
                ],
                [
                    15,
                    18
                ]
            ]
        }
    ],
    "learning_objectives": [
        "Interval merging",
        "Sorting",
        "Greedy algorithm"
    ]
},
    {
    "id": 43,
    "title": "First Missing Positive",
    "description": "Given an unsorted integer array nums, find the smallest missing positive integer. Must be O(n) time and O(1) space.",
    "skill": "arrays",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 45,
    "tags": [
        "arrays",
        "hashing",
        "optimization"
    ],
    "solution_hint": "Use array indices as hash, mark visited numbers",
    "test_cases": [
        {
            "input": {
                "nums": [
                    3,
                    4,
                    -1,
                    1
                ]
            },
            "output": 2
        }
    ],
    "learning_objectives": [
        "In-place hashing",
        "Array manipulation",
        "Optimization"
    ]
},
    {
    "id": 44,
    "title": "Rotate Array",
    "description": "Rotate an array to the right by k steps. Must be done in-place with O(1) extra space.",
    "skill": "arrays",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 38,
    "tags": [
        "arrays",
        "rotation",
        "reverse"
    ],
    "solution_hint": "Reverse entire array, then reverse first k and last n-k elements",
    "test_cases": [
        {
            "input": {
                "nums": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "k": 3
            },
            "output": [
                5,
                6,
                7,
                1,
                2,
                3,
                4
            ]
        }
    ],
    "learning_objectives": [
        "Array rotation",
        "Reverse algorithm",
        "In-place operations"
    ]
},
    {
    "id": 45,
    "title": "Sliding Window Maximum",
    "description": "Given an array and a window size k, find the maximum element in each sliding window of size k.",
    "skill": "arrays",
    "difficulty": "hard",
    "question_type": "coding",
    "estimated_time_minutes": 42,
    "tags": [
        "arrays",
        "sliding-window",
        "deque"
    ],
    "solution_hint": "Use deque to maintain maximum in window",
    "test_cases": [
        {
            "input": {
                "nums": [
                    1,
                    3,
                    -1,
                    -3,
                    5,
                    3,
                    6,
                    7
                ],
                "k": 3
            },
            "output": [
                3,
                3,
                5,
                5,
                6,
                7
            ]
        }
    ],
    "learning_objectives": [
        "Sliding window",
        "Deque",
        "Monotonic queue"
    ]
},
    {
    "id": 46,
    "title": "Four Pillars of OOP",
    "description": "Explain the four pillars of Object-Oriented Programming with examples.",
    "skill": "oop",
    "difficulty": "easy",
    "question_type": "mcq",
    "estimated_time_minutes": 10,
    "tags": [
        "oop",
        "principles",
        "basics"
    ],
    "solution_hint": "Encapsulation, Inheritance, Polymorphism, Abstraction",
    "test_cases": [],
    "learning_objectives": [
        "OOP principles",
        "Core concepts",
        "Software design"
    ]
},
    {
    "id": 47,
    "title": "Class and Object Creation",
    "description": "Create a simple class in Java/Python with attributes and methods, then instantiate objects.",
    "skill": "oop",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 15,
    "tags": [
        "oop",
        "class",
        "object"
    ],
    "solution_hint": "Define class with __init__ or constructor, create instances",
    "test_cases": [],
    "learning_objectives": [
        "Class definition",
        "Object instantiation",
        "Basic OOP"
    ]
},
    {
    "id": 48,
    "title": "Inheritance Example",
    "description": "Create a base class and a derived class that inherits from it, demonstrating inheritance.",
    "skill": "oop",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 18,
    "tags": [
        "oop",
        "inheritance",
        "class-hierarchy"
    ],
    "solution_hint": "Use extends (Java) or class Child(Parent) (Python)",
    "test_cases": [],
    "learning_objectives": [
        "Inheritance",
        "Class hierarchy",
        "Code reuse"
    ]
},
    {
    "id": 49,
    "title": "Encapsulation with Access Modifiers",
    "description": "Implement a class with private, protected, and public members demonstrating encapsulation.",
    "skill": "oop",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 20,
    "tags": [
        "oop",
        "encapsulation",
        "access-modifiers"
    ],
    "solution_hint": "Use private/protected/public keywords, getters and setters",
    "test_cases": [],
    "learning_objectives": [
        "Encapsulation",
        "Access control",
        "Data hiding"
    ]
},
    {
    "id": 50,
    "title": "Method Overriding",
    "description": "Create a parent class with a method and override it in a child class.",
    "skill": "oop",
    "difficulty": "easy",
    "question_type": "coding",
    "estimated_time_minutes": 15,
    "tags": [
        "oop",
        "polymorphism",
        "method-overriding"
    ],
    "solution_hint": "Use @Override annotation (Java) or same method signature (Python)",
    "test_cases": [],
    "learning_objectives": [
        "Method overriding",
        "Polymorphism",
        "Runtime binding"
    ]
},
    {
    "id": 51,
    "title": "Abstract Class Implementation",
    "description": "Create an abstract class with abstract methods and concrete implementations in a subclass.",
    "skill": "oop",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 25,
    "tags": [
        "oop",
        "abstract-class",
        "abstraction"
    ],
    "solution_hint": "Use abstract keyword, implement abstract methods in subclass",
    "test_cases": [],
    "learning_objectives": [
        "Abstract classes",
        "Abstraction",
        "Template method pattern"
    ]
},
    {
    "id": 52,
    "title": "Interface Implementation",
    "description": "Create an interface with multiple methods and implement it in a class.",
    "skill": "oop",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 22,
    "tags": [
        "oop",
        "interface",
        "contract"
    ],
    "solution_hint": "Define interface, implement all methods in class",
    "test_cases": [],
    "learning_objectives": [
        "Interfaces",
        "Contracts",
        "Multiple inheritance"
    ]
},
    {
    "id": 53,
    "title": "Singleton Pattern",
    "description": "Implement the Singleton design pattern ensuring only one instance exists.",
    "skill": "oop",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 28,
    "tags": [
        "oop",
        "design-patterns",
        "singleton"
    ],
    "solution_hint": "Private constructor, static instance, getInstance() method",
    "test_cases": [],
    "learning_objectives": [
        "Singleton pattern",
        "Design patterns",
        "Instance control"
    ]
},
    {
    "id": 54,
    "title": "Factory Pattern",
    "description": "Implement the Factory design pattern to create objects without specifying exact classes.",
    "skill": "oop",
    "difficulty": "medium",
    "question_type": "coding",
    "estimated_time_minutes": 30,
    "tags": [
        "oop",
        "design-patterns"
    ],
    "solution_hint": "Use factory class with static method to create objects based on type",
    "test_cases": [],
    "learning_objectives": ["Factory pattern", "Creational patterns", "Object creation"]
    }
]

def get_dataset_by_skill(skill: str):
    """Get questions from dataset filtered by skill"""
    return [q for q in QUESTION_DATASET if q["skill"] == skill]

def get_dataset_by_difficulty(difficulty: str):
    """Get questions from dataset filtered by difficulty"""
    return [q for q in QUESTION_DATASET if q["difficulty"] == difficulty]

def get_dataset_by_type(question_type: str):
    """Get questions from dataset filtered by type"""
    return [q for q in QUESTION_DATASET if q["question_type"] == question_type]

def get_training_examples(skill: str = None, difficulty: str = None, question_type: str = None, limit: int = 5):
    """Get training examples for few-shot learning"""
    examples = QUESTION_DATASET.copy()
    
    if skill:
        examples = [q for q in examples if q["skill"] == skill]
    if difficulty:
        examples = [q for q in examples if q["difficulty"] == difficulty]
    if question_type:
        examples = [q for q in examples if q["question_type"] == question_type]
    
    return examples[:limit]

def format_example_for_training(question: dict) -> str:
    """Format a question as a training example for Gemini"""
    return f"""
Title: {question['title']}
Skill: {question['skill']}
Difficulty: {question['difficulty']}
Type: {question['question_type']}
Description: {question['description']}
Estimated Time: {question['estimated_time_minutes']} minutes
Tags: {', '.join(question['tags'])}
Learning Objectives: {', '.join(question.get('learning_objectives', []))}
"""

# Dataset Statistics
DATASET_INFO = {
    "total_questions": 460,
    "topics": {
        "java": 35,
        "multithreading": 35,
        "arrays": 35,
        "oop": 35,
        "javascript": 20,
        "algorithms": 60,
        "python": 20,
        "linked-lists": 20,
        "graphs": 20,
        "design": 20,
        "data-structures": 40,
        "system-design": 40,
        "databases": 40,
        "networking": 40
    },
    "difficulty_distribution": {
        "easy": 20,
        "medium": 220,
        "hard": 220
    },
    "database": "MySQL (XAMPP)",
    "database_name": "assessment_orchestrator",
    "table_name": "questions",
    "kaggle_datasets": [
        "LeetCode Questions Dataset - 2000+ coding problems",
        "Coding Interview Questions - 500+ questions from tech companies",
        "Java Programming Questions - 300+ Java-specific questions",
        "System Design Questions - 150+ system design problems"
    ]
}
