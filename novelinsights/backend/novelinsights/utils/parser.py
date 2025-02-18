from dataclasses import dataclass
import textwrap
import json

@dataclass
class Block:
    content: str
    language: str | None = None
    
    def __repr__(self):
        return f"Block(language={self.language}, content={self.content[:50]}...)"
    
    def parse_json(self) -> dict:
        if self.language != "json":
            raise ValueError(f"Block is not a JSON block: {self}")
        return json.loads(self.content)

def extract_blocks(markdown_text: str) -> list[Block]:
    # Remove common indentation from the Markdown.
    markdown_text = textwrap.dedent(markdown_text)
    
    blocks = []
    lines = markdown_text.splitlines()
    in_block = False
    block_lines = []
    language = None

    for line in lines:
        stripped_line = line.strip()
        if not in_block:
            # Check for the start of a code block.
            if stripped_line.startswith("```"):
                # Everything following the opening backticks is treated as the language (if any).
                language_part = stripped_line[3:].strip()
                language = language_part if language_part else None
                in_block = True
                block_lines = []  # Reset the block content.
        else:
            # We're inside a code block.
            # Only a line that is exactly "```" (after stripping) will close the block.
            if stripped_line == "```":
                content = "\n".join(block_lines).strip()  # Remove extra whitespace.
                blocks.append(Block(content=content, language=language))
                in_block = False
                language = None
                block_lines = []
            else:
                # Append the current line to the block content.
                block_lines.append(line)
                
    # If we ended while still inside a block, treat the remaining lines as its content.
    if in_block:
        content = "\n".join(block_lines).strip()
        blocks.append(Block(content=content, language=language))
    
    return blocks

def extract_json(markdown_text: str) -> list[Block]:
    """
    Extracts a JSON block from the given markdown_text.

    First, if the text appears as markdown (i.e., contains code blocks formatted 
    with triple backticks), it will look for a block marked as "json". If one is 
    found, it is returned.

    If no markdown JSON block is found, the function falls back to searching 
    for a JSON snippet by finding the first '{' and the last '}' in the text. 
    If the candidate can be parsed as JSON, a Block is created and returned.

    If no valid JSON is found in either format, the function returns None.
    """
    # Check if text contains markdown code blocks
    if "```" in markdown_text:
        blocks = extract_blocks(markdown_text)
        return [block for block in blocks if block.language and block.language.lower() == "json"]

    # Fallback: attempt to extract a bracketed JSON snippet from the text.
    first_brace = markdown_text.find('{')
    last_brace = markdown_text.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        json_candidate = markdown_text[first_brace:last_brace+1]
        try:
            # Validate that the extracted snippet is valid JSON.
            json.loads(json_candidate)
            return [Block(content=json_candidate.strip(), language="json")]
        except json.JSONDecodeError:
            # If the candidate isn't valid JSON, we'll return None.
            pass
    
    return []

if __name__ == "__main__":
    # Test cases.
    markdown = """
    Some text here
    ```json
    {"key": "value"}
    ```
    
    Some more text
    ```
    plain text here, but nested inside is a block:
    ```sql
    SELECT * FROM users;
    ```
    
    
    ```sql
    SELECT * FROM users;
    ```
    """
    for block in extract_blocks(markdown):
        print(block)
