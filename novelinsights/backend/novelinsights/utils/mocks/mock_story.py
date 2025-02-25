import json
import os
from typing import NamedTuple
from pathlib import Path

class MockStoryMetadata(NamedTuple):
    story_title: str
    genres: list[str]
    additional_tags: list[str]
    story_description: str
    story_path: Path
    
class MockChapter(NamedTuple):
    chapter_title: str
    chapter_content: str
    chapter_index: int
    
    
class MockStory(NamedTuple):
    metadata: MockStoryMetadata
    chapters: list[MockChapter]
    
    def __str__(self):
        return f"Story(metadata={self.metadata}, chapters={self.chapters})"
    
    def __repr__(self):
        return self.__str__()
    

def load_story_metadata(file_path: Path = Path("tests/resources/pokemon_amber/_metadata.json")) -> MockStoryMetadata:
    with open(file_path, "r") as f:
        metadata = json.load(f)
        return MockStoryMetadata(
            story_title=metadata.get("story_title"),
            genres=metadata.get("genres"),
            additional_tags=metadata.get("additional_tags"),
            story_description=metadata.get("story_description"),
            story_path=file_path.parent
        )
    
def load_chapters(file_dir: Path = Path("tests/resources/pokemon_amber/")) -> list[MockChapter]:
    chapters = []
    
    file_paths = [f for f in os.listdir(file_dir) if f.startswith("chapter") and f.endswith(".json")]
    
    for i in range(len(file_paths)):
        with open(os.path.join(file_dir, f"chapter_{i}.json"), "r") as f:
            chapter = json.load(f)
            chapters.append(MockChapter(
                chapter_title=chapter.get("chapter_title"),
                chapter_content=chapter.get("chapter_content"),
                chapter_index=i
            ))
    return chapters

def load_story(file_dir: Path = Path("tests/resources/pokemon_amber/")) -> MockStory:
    return MockStory(
        metadata=load_story_metadata(file_dir / "_metadata.json"),
        chapters=load_chapters(file_dir)
    ) 

if __name__ == "__main__":
    print(load_story())