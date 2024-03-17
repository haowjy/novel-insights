# Novel Insights

Quickly obtain insights about a text.

## Installation

For Nvidia GPUs and linux

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on -DLLAMA_BLAS_VENDOR=OpenBLAS" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir
```

See [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) for other installation instructions.

Then

```bash
pip install -r requirements.txt
```

## Install Models

```bash
pip3 install huggingface-hub
pip3 install hf_transfer

HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download TheBloke/Mixtral-8x7B-v0.1-GGUF mixtral-8x7b-v0.1.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
```

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
