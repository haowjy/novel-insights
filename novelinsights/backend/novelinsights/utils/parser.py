from dataclasses import dataclass
import textwrap

@dataclass
class Block:
    content: str
    language: str | None = None

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
