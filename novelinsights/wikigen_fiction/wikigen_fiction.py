from novelinsights.wikigen_fiction.agents import read_chapter_agent

def main():
    print(read_chapter_agent.task())
    print(read_chapter_agent.instructions())
    
if __name__ == "__main__":
    main()