"""
Collection of prompts for code debloating.
"""

PROMPTS = {
    "1": """
Goal*
You are an experienced software engineer. Please debloat the code in this file while maintaining its functional correctness. Simplify logic, remove redundancies, and optimize for readability and maintainability without introducing new bugs.

IMPORTANT 
1. All rewritten code must remain within the file it originated from.  
2. No new files or services may be introduced as part of the solution.  
3. Adding helper methods within the file is allowed but must not break functional correctness.  
4. Do not modify OR remove comments, as they do not count as code.  Imports also do not count as code.

Context
Software bloat refers to unnecessary or inefficient CODE that increases a program’s size or reduces its performance without contributing meaningful functionality.
""",

    "2": """
Debloat this file while maintaining functional correctness
"""
}
