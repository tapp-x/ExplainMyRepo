# Automatic Project Documentation Generator

This project automates the generation of technical documentation for software projects by analyzing their structure and content. It uses a local language model (LLM) to produce detailed Markdown documentation for each project folder.

## Features

- **Automatic Analysis**: Scans project directories and analyzes their structure, files, and content.
- **Markdown Documentation**: Generates professional, well-structured Markdown documentation.
- **Customizable LLM**: Supports integration with a local LLM for generating documentation.
- **Exclusion Rules**: Skips unnecessary directories like `.git`, `node_modules`, and `__pycache__`.

## Project Structure

```
.
├── LICENSE
├── README.md
├── requirements.txt
└── srcs
    ├── ingest.py
    └── remoteModel.py
```

### Key Files

- **`srcs/ingest.py`**: Main script for analyzing directories and generating documentation.
- **`srcs/remoteModel.py`**: Contains the implementation of the `CustomLLM` class for interacting with the local LLM.
- **`.env`**: Stores environment variables, such as the LLM URL.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `.env` file:
   ```properties
   LLM_URL="yourURL"
   ```

4. Ensure you have a local LLM running at the specified URL. You can use models like `llama2` or `gpt4all`.


## Usage

Run the main script to generate documentation for a project directory:

```bash
python 

ingest.py

 <root_directory> --output <output_directory>
```

### Example

```bash
python 

ingest.py

 ./projects --output ./docs
```

This will generate Markdown documentation for each subdirectory in the `projects` folder and save it in the `docs` folder.

## Customization

- **LLM Configuration**: Modify the `LLM_URL` in the `.env` file and the model name in `srcs/ingest.py` to use a different language model.
- **Exclusion Rules**: Update the `should_skip` function in `srcs/ingest.py` to customize which directories or files are ignored.

## Dependencies

- Python 3.9+
- `langchain`

## To-Do
- Improve response quality from the LLM.
- Add more customization options for documentation generation.
- Implement error handling for LLM requests.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).