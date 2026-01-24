"""
Kaggle Dataset References for Question Generation
Real-time datasets used for training and question generation
"""

KAGGLE_DATASETS = {
    "leetcode_questions": {
        "name": "LeetCode Questions Dataset",
        "url": "https://www.kaggle.com/datasets/leetcode/leetcode-questions",
        "description": "Comprehensive dataset of LeetCode coding problems with solutions and difficulty ratings",
        "topics": ["arrays", "strings", "linked-lists", "trees", "graphs", "algorithms"],
        "size": "2000+ questions",
        "format": "CSV/JSON"
    },
    "coding_interview_questions": {
        "name": "Coding Interview Questions",
        "url": "https://www.kaggle.com/datasets/arindam235/beginner-friendly-python-projects",
        "description": "Collection of coding interview questions from top tech companies",
        "topics": ["algorithms", "data-structures", "problem-solving"],
        "size": "500+ questions",
        "format": "JSON"
    },
    "java_programming_questions": {
        "name": "Java Programming Questions",
        "url": "https://www.kaggle.com/datasets/learn-ai/leetcode",
        "description": "Java-specific programming questions and solutions",
        "topics": ["java", "oop", "multithreading", "collections"],
        "size": "300+ questions",
        "format": "JSON"
    },
    "system_design_questions": {
        "name": "System Design Interview Questions",
        "url": "https://www.kaggle.com/datasets/tech-interview/system-design-questions",
        "description": "System design questions from FAANG companies",
        "topics": ["system_design", "architecture", "scalability"],
        "size": "150+ questions",
        "format": "JSON"
    }
}

def get_kaggle_dataset_info(topic: str = None):
    """Get information about Kaggle datasets relevant to a topic"""
    if topic:
        relevant = []
        for dataset in KAGGLE_DATASETS.values():
            if topic.lower() in [t.lower() for t in dataset["topics"]]:
                relevant.append(dataset)
        return relevant
    return list(KAGGLE_DATASETS.values())

