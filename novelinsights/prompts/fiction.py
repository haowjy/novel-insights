from pathlib import Path
import json

# Description: Prompt for a obtaining insights about a fiction novel or story
def task() -> str:
    return """Your task is to create a json according to the following json schema to help readers quickly access information about a novel. 
The novel is a work of fiction and can be any genre.
The information you provide should be rich and detailed, covering various aspects of the novel such as characters, plot points, world-building, themes, and more.
But remember, the information should be concise and to the point, avoiding unnecessary details or spoilers."""

def instructions() -> str:
    return """- Arrays can be empty and do not need to be filled every time.
- You must only include information based on previous information and the following excerpt."""

def schema() -> dict:
    path = Path(__file__).parent / "schemas/fiction.json"
    with path.open() as f:
        return json.load(f)

from ebook_tree_parser.toctree import TocNode
def template(excerpt: TocNode, is_structured=False, prev_json: dict = None) -> str:
    """_summary_

    Args:
        excerpt (TocNode): _description_

    Returns:
        str: _description_
    """
    prompt = f"""# Task
{task()}

## JSON Schema
```
{json.dumps(schema())}
```
"""
    if prev_json:
        prompt += f"""## Previous JSON
```
{json.dumps(prev_json, indent=2)}
````
"""
    prompt += f"""# Instructions
{instructions()}

# Excerpt
## Title: {excerpt.title}
\"\"\"
{excerpt.content}
\"\"\"
"""
    return prompt