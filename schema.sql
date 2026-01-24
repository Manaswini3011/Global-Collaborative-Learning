-- Intent-Based Assessment Orchestrator Database Schema
-- Database: MySQL (XAMPP)
-- Database Name: assessment_orchestrator
-- Server: localhost:3306
-- All questions are stored in the 'questions' table
-- Questions dataset is used for training Gemini API for question generation

CREATE DATABASE IF NOT EXISTS assessment_orchestrator;
USE assessment_orchestrator;

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Intents table - stores parsed user intents
CREATE TABLE IF NOT EXISTS intents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    original_prompt TEXT NOT NULL,
    parsed_role VARCHAR(255),
    parsed_seniority VARCHAR(100),
    parsed_skills JSON,
    parsed_difficulty VARCHAR(50),
    parsed_duration INT,
    parsed_question_types JSON,
    parsed_num_questions INT,
    nlp_extraction JSON,
    llm_enhancement JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Questions table - question bank
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    skill VARCHAR(255) NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    question_type ENUM('coding', 'mcq', 'debugging', 'system_design') NOT NULL,
    estimated_time_minutes INT NOT NULL,
    tags JSON,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_skill (skill),
    INDEX idx_difficulty (difficulty),
    INDEX idx_question_type (question_type),
    INDEX idx_skill_difficulty (skill, difficulty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Assessments table
CREATE TABLE IF NOT EXISTS assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    intent_id INT NOT NULL,
    title VARCHAR(500),
    total_duration_minutes INT NOT NULL,
    total_questions INT NOT NULL,
    status ENUM('draft', 'preview', 'finalized', 'submitted') DEFAULT 'draft',
    configuration JSON,
    proctoring_rules JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    finalized_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Assessment questions - many-to-many relationship
CREATE TABLE IF NOT EXISTS assessment_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT NOT NULL,
    question_id INT NOT NULL,
    display_order INT NOT NULL,
    allocated_time_minutes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_assessment_question (assessment_id, question_id),
    INDEX idx_assessment_id (assessment_id),
    INDEX idx_display_order (assessment_id, display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Configurations table - assessment settings
CREATE TABLE IF NOT EXISTS configurations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT NOT NULL,
    time_limit_per_question INT,
    allow_retakes BOOLEAN DEFAULT FALSE,
    proctoring_enabled BOOLEAN DEFAULT TRUE,
    show_hints BOOLEAN DEFAULT FALSE,
    auto_submit BOOLEAN DEFAULT TRUE,
    settings JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE,
    UNIQUE KEY unique_assessment_config (assessment_id),
    INDEX idx_assessment_id (assessment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Explainability logs - AI decision traces
CREATE TABLE IF NOT EXISTS explainability_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT NOT NULL,
    question_id INT,
    decision_type VARCHAR(100) NOT NULL,
    explanation TEXT NOT NULL,
    reasoning_data JSON,
    llm_model_used VARCHAR(255),
    confidence_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE SET NULL,
    INDEX idx_assessment_id (assessment_id),
    INDEX idx_decision_type (decision_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- API audit logs - tracks all API calls
CREATE TABLE IF NOT EXISTS api_audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(10) NOT NULL,
    request_body JSON,
    response_status INT,
    response_body JSON,
    internal_api_called VARCHAR(255),
    llm_provider_used VARCHAR(100),
    correlation_id VARCHAR(255),
    execution_time_ms INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_endpoint (endpoint),
    INDEX idx_correlation_id (correlation_id),
    INDEX idx_created_at (created_at),
    INDEX idx_internal_api (internal_api_called)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed data: Default admin user
-- Password: admin123
-- Note: This is a bcrypt hash for 'admin123'. If it doesn't work, regenerate using:
-- python backend/generate_password_hash.py
INSERT INTO users (email, password_hash, full_name) VALUES
('admin@hackerrank.com', '$2b$12$du8C0YBHBAHDK72r5aQhs.E.J6nxH6nA6E4rVQvfNadNTdoP/VNdm', 'Admin User')
ON DUPLICATE KEY UPDATE email=email;

-- Seed data: Sample questions
INSERT INTO questions (title, description, skill, difficulty, question_type, estimated_time_minutes, tags, metadata) VALUES
('Two Sum', 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.', 'arrays', 'easy', 'coding', 15, '["arrays", "hash-table"]', '{"leetcode_id": 1}'),
('Reverse Linked List', 'Reverse a singly linked list.', 'linked-lists', 'easy', 'coding', 20, '["linked-lists", "recursion"]', '{}'),
('Binary Search', 'Implement binary search algorithm.', 'algorithms', 'medium', 'coding', 25, '["binary-search", "arrays"]', '{}'),
('Merge Two Sorted Lists', 'Merge two sorted linked lists and return it as a sorted list.', 'linked-lists', 'medium', 'coding', 30, '["linked-lists", "recursion"]', '{}'),
('Valid Parentheses', 'Given a string containing just the characters "(", ")", "{", "}", "[" and "]", determine if the input string is valid.', 'stacks', 'easy', 'coding', 15, '["stack", "string"]', '{}'),
('Longest Substring Without Repeating Characters', 'Find the length of the longest substring without repeating characters.', 'strings', 'medium', 'coding', 30, '["sliding-window", "hash-table"]', '{}'),
('Design LRU Cache', 'Design and implement a data structure for Least Recently Used (LRU) cache.', 'design', 'hard', 'system_design', 45, '["design", "hash-table", "doubly-linked-list"]', '{}'),
('OOP Principles', 'Explain the four pillars of Object-Oriented Programming.', 'oop', 'easy', 'mcq', 10, '["oop", "java", "python"]', '{}'),
('Multithreading Basics', 'What is the difference between process and thread?', 'multithreading', 'medium', 'mcq', 15, '["multithreading", "concurrency"]', '{}'),
('Java Exception Handling', 'Identify the issue in the given Java code snippet.', 'java', 'medium', 'debugging', 20, '["java", "exceptions", "debugging"]', '{}'),
('Python Decorators', 'Explain how Python decorators work.', 'python', 'medium', 'mcq', 15, '["python", "decorators"]', '{}'),
('Database Normalization', 'What is the purpose of database normalization?', 'databases', 'medium', 'mcq', 12, '["databases", "sql"]', '{}'),
('REST API Design', 'Design a RESTful API for a blog system.', 'api-design', 'hard', 'system_design', 50, '["rest", "api", "design"]', '{}'),
('Graph Traversal', 'Implement BFS and DFS for a graph.', 'graphs', 'hard', 'coding', 40, '["graphs", "bfs", "dfs"]', '{}'),
('Dynamic Programming: Fibonacci', 'Implement an efficient Fibonacci sequence generator.', 'algorithms', 'medium', 'coding', 25, '["dynamic-programming", "recursion"]', '{}'),
('Maximum Subarray', 'Find the contiguous subarray within an array which has the largest sum.', 'arrays', 'medium', 'coding', 25, '["arrays", "dynamic-programming"]', '{}'),
('Container With Most Water', 'Find two lines that together with the x-axis form a container, such that the container contains the most water.', 'arrays', 'medium', 'coding', 30, '["arrays", "two-pointers"]', '{}'),
('3Sum', 'Find all unique triplets in the array which gives the sum of zero.', 'arrays', 'medium', 'coding', 35, '["arrays", "two-pointers"]', '{}'),
('Remove Duplicates from Sorted Array', 'Remove duplicates in-place such that each element appears only once.', 'arrays', 'easy', 'coding', 15, '["arrays", "two-pointers"]', '{}'),
('Best Time to Buy and Sell Stock', 'Find the maximum profit you can achieve from buying and selling a stock.', 'arrays', 'easy', 'coding', 20, '["arrays", "greedy"]', '{}'),
('Product of Array Except Self', 'Return an array such that each element is the product of all other elements.', 'arrays', 'medium', 'coding', 30, '["arrays", "prefix-sum"]', '{}'),
('Group Anagrams', 'Group strings that are anagrams of each other together.', 'strings', 'medium', 'coding', 25, '["strings", "hash-table"]', '{}'),
('Longest Palindromic Substring', 'Find the longest palindromic substring in a given string.', 'strings', 'medium', 'coding', 35, '["strings", "dynamic-programming"]', '{}'),
('Valid Anagram', 'Determine if two strings are anagrams of each other.', 'strings', 'easy', 'coding', 10, '["strings", "hash-table"]', '{}'),
('Add Two Numbers', 'Add two numbers represented as linked lists.', 'linked-lists', 'medium', 'coding', 30, '["linked-lists", "math"]', '{}'),
('Remove Nth Node From End', 'Remove the nth node from the end of a linked list.', 'linked-lists', 'medium', 'coding', 25, '["linked-lists", "two-pointers"]', '{}'),
('Linked List Cycle', 'Detect if a linked list has a cycle.', 'linked-lists', 'easy', 'coding', 20, '["linked-lists", "two-pointers"]', '{}'),
('Merge K Sorted Lists', 'Merge k sorted linked lists into one sorted list.', 'linked-lists', 'hard', 'coding', 45, '["linked-lists", "heap"]', '{}'),
('Invert Binary Tree', 'Invert a binary tree (mirror it).', 'trees', 'easy', 'coding', 20, '["trees", "recursion"]', '{}'),
('Maximum Depth of Binary Tree', 'Find the maximum depth of a binary tree.', 'trees', 'easy', 'coding', 15, '["trees", "recursion"]', '{}'),
('Same Tree', 'Check if two binary trees are the same.', 'trees', 'easy', 'coding', 15, '["trees", "recursion"]', '{}'),
('Binary Tree Level Order Traversal', 'Return the level order traversal of a binary tree.', 'trees', 'medium', 'coding', 30, '["trees", "bfs"]', '{}'),
('Validate Binary Search Tree', 'Determine if a binary tree is a valid BST.', 'trees', 'medium', 'coding', 30, '["trees", "recursion"]', '{}'),
('Lowest Common Ancestor', 'Find the lowest common ancestor of two nodes in a binary tree.', 'trees', 'medium', 'coding', 35, '["trees", "recursion"]', '{}'),
('Climbing Stairs', 'Find the number of distinct ways to climb n stairs.', 'algorithms', 'easy', 'coding', 15, '["dynamic-programming"]', '{}'),
('House Robber', 'Find the maximum amount of money you can rob from houses.', 'algorithms', 'medium', 'coding', 30, '["dynamic-programming"]', '{}'),
('Coin Change', 'Find the fewest number of coins needed to make up an amount.', 'algorithms', 'medium', 'coding', 35, '["dynamic-programming"]', '{}'),
('Longest Increasing Subsequence', 'Find the length of the longest increasing subsequence.', 'algorithms', 'medium', 'coding', 40, '["dynamic-programming", "binary-search"]', '{}'),
('Word Break', 'Determine if a string can be segmented into dictionary words.', 'algorithms', 'medium', 'coding', 35, '["dynamic-programming", "strings"]', '{}'),
('Number of Islands', 'Count the number of islands in a 2D grid.', 'graphs', 'medium', 'coding', 35, '["graphs", "dfs"]', '{}'),
('Course Schedule', 'Determine if you can finish all courses given prerequisites.', 'graphs', 'medium', 'coding', 40, '["graphs", "topological-sort"]', '{}'),
('Clone Graph', 'Return a deep copy of a connected undirected graph.', 'graphs', 'medium', 'coding', 35, '["graphs", "dfs"]', '{}'),
('Pacific Atlantic Water Flow', 'Find cells that can flow to both Pacific and Atlantic oceans.', 'graphs', 'medium', 'coding', 45, '["graphs", "dfs", "bfs"]', '{}'),
('Implement Trie', 'Implement a trie data structure with insert, search, and startsWith methods.', 'design', 'medium', 'coding', 40, '["design", "trie"]', '{}'),
('Design Twitter', 'Design a simplified version of Twitter.', 'design', 'hard', 'system_design', 60, '["design", "system-design"]', '{}'),
('Design Parking Lot', 'Design a parking lot system with multiple levels and spots.', 'design', 'medium', 'system_design', 50, '["design", "oop"]', '{}'),
('Design Snake Game', 'Design a classic Snake game.', 'design', 'medium', 'system_design', 45, '["design", "game"]', '{}'),
('Java Memory Model', 'Explain the Java Memory Model and its implications.', 'java', 'hard', 'mcq', 20, '["java", "memory", "concurrency"]', '{}'),
('Python GIL', 'What is the Global Interpreter Lock in Python?', 'python', 'medium', 'mcq', 15, '["python", "concurrency", "gil"]', '{}'),
('SQL Joins', 'Explain different types of SQL joins with examples.', 'databases', 'medium', 'mcq', 18, '["databases", "sql", "joins"]', '{}'),
('ACID Properties', 'Explain ACID properties in database transactions.', 'databases', 'medium', 'mcq', 15, '["databases", "transactions"]', '{}'),
('REST vs GraphQL', 'Compare REST and GraphQL APIs.', 'api-design', 'medium', 'mcq', 20, '["api", "rest", "graphql"]', '{}'),
('HTTP Methods', 'Explain different HTTP methods and when to use them.', 'api-design', 'easy', 'mcq', 12, '["api", "http"]', '{}'),
('Singleton Pattern', 'Implement the Singleton design pattern in Java.', 'oop', 'medium', 'coding', 25, '["oop", "design-patterns", "java"]', '{}'),
('Factory Pattern', 'Implement the Factory design pattern.', 'oop', 'medium', 'coding', 30, '["oop", "design-patterns"]', '{}'),
('Observer Pattern', 'Implement the Observer design pattern.', 'oop', 'medium', 'coding', 30, '["oop", "design-patterns"]', '{}'),
('Deadlock Detection', 'Identify and fix a deadlock scenario in multithreaded code.', 'multithreading', 'hard', 'debugging', 35, '["multithreading", "concurrency", "debugging"]', '{}'),
('Race Condition', 'Identify and fix a race condition in concurrent code.', 'multithreading', 'hard', 'debugging', 30, '["multithreading", "concurrency", "debugging"]', '{}'),
('Thread Pool Implementation', 'Implement a thread pool from scratch.', 'multithreading', 'hard', 'coding', 50, '["multithreading", "concurrency"]', '{}'),
('Async/Await in JavaScript', 'Explain async/await and Promises in JavaScript.', 'javascript', 'medium', 'mcq', 18, '["javascript", "async"]', '{}'),
('Closure in JavaScript', 'Explain closures in JavaScript with examples.', 'javascript', 'medium', 'mcq', 15, '["javascript", "closures"]', '{}'),
('React Hooks', 'Explain React Hooks and their usage.', 'javascript', 'medium', 'mcq', 20, '["javascript", "react"]', '{}'),
('Virtual DOM', 'Explain the concept of Virtual DOM in React.', 'javascript', 'medium', 'mcq', 15, '["javascript", "react"]', '{}'),
('Docker Basics', 'Explain Docker containers and images.', 'devops', 'easy', 'mcq', 15, '["docker", "devops"]', '{}'),
('Kubernetes Basics', 'Explain Kubernetes pods and services.', 'devops', 'medium', 'mcq', 20, '["kubernetes", "devops"]', '{}'),
('CI/CD Pipeline', 'Design a CI/CD pipeline for a web application.', 'devops', 'medium', 'system_design', 45, '["devops", "ci-cd"]', '{}'),
('Load Balancing', 'Explain different load balancing strategies.', 'system_design', 'medium', 'mcq', 20, '["system-design", "networking"]', '{}'),
('Caching Strategies', 'Compare different caching strategies (LRU, LFU, etc.).', 'system_design', 'medium', 'mcq', 18, '["system-design", "caching"]', '{}'),
('Database Sharding', 'Explain database sharding and its benefits.', 'databases', 'hard', 'mcq', 25, '["databases", "sharding"]', '{}'),
('CAP Theorem', 'Explain the CAP theorem and its implications.', 'system_design', 'hard', 'mcq', 20, '["system-design", "distributed-systems"]', '{}')
ON DUPLICATE KEY UPDATE title=title;

