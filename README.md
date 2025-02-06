# Novel Insights

Quickly obtain insights about text.

## Dev Set Up

### Backend

#### Running the Backend (and Database)

  ```bash
  cd novelinsights/backend
  ```

  ```bash
  # Start containers in foreground (see logs directly)
  docker-compose up

  # Start containers in background (detached mode)
  docker-compose up -d

  # Rebuild containers and start (use after dependency changes)
  docker-compose up --build
  ```

- The FastAPI server will be running on `http://localhost:8000`
- The database will be running on `http://localhost:5432`
- The database adminer will be running on `http://localhost:5050`

#### Running the database

To just run the database:

  ```bash
  docker-compose up postgres pgadmin
  ```

To update the database:

  ```bash
  ./migrate.sh "migration message"
  ```

#### Running fastapi without docker (local development)

1. [Poetry Installation Guide](https://python-poetry.org/docs/#installing-with-pipx)

2. (Optional) Make sure that poetry creates a virtual environment in the backend directory

    ```bash
    poetry config virtualenvs.in-project true
    ```

3. Navigate to the backend fastapi directory
  
    ```bash
    cd novelinsights/backend
    ```

4. Install all dependencies including development ones

    ```bash
    poetry install --with dev
    ```

5. Activate the virtual environment

    ```bash
    poetry shell
    ```

6. Run the FastAPI server

    ```bash
    uvicorn novelinsights.main:app --reload
    ```

7. Gracefully exit the virtual environment

    ```bash
    deactivate
    ```

### Frontend

1. !!TODO

## Roadmap Design

### Development Roadmap

- [ ] Simple LLM agent that can generate a summary of a book
- [ ] Web interface to interact with the agent
- [ ] Website to host the "wiki" of the book as it progresses -> users can get a wiki "up to a point" to avoid spoilers
- [ ] Optimze costs
  - [ ] Try smaller models (use GPT4 or Claude first) -> see if there are potentially cheaper models to use
  - [ ] LLM Model Router
  - [ ] LLMlingua
- [ ] Custom "GPT"?
- [ ] Chrome Extension?

### Agent Roadmap

- [ ] Use RAG split to be able to chat over a book
  - [ ] Generate a summary of the book
  - [ ] Generate summary of each chapter - pre-summarize chapters to use with RAG
  - GPT4-turbo? Claude?
  - use cognitive architecture to help guide the agent in future prompts [ACE Framework](https://github.com/daveshap/ACE_Framework), [paper on cognitive architecture](https://arxiv.org/pdf/2309.02427.pdf)
- [ ] Generate a "wiki" of the entire book
  - [ ] Generate summary of the book
  - [ ] Generate summary of each chapter - pre-summarize chapters to use with RAG
  - [ ] Determine the genre and major themes of the book to help guide future prompts
  - [ ] Determine the POV of the book and who the main character(s) are
  - [ ] Gather information about specific things
    - [ ] Characters
    - [ ] Places
    - [ ] Things
    - [ ] Events
  - [ ] Define unique vocabulary or terminology
  - [ ] Chronological timeline... this may not necessarily be the list of chapters, will require the agent to understand the book... flashbacks, describing past events, etc.

### Key Features

- Chatbot that can give analysis of a book
- be able to only use information up to certain "Chapters" to avoid spoilers. Later chapters can have information about earlier chapters.
- Use the "wiki" to help guide the agent in conversations
