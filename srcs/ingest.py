import os
import argparse
from gitingest import ingest
import json
from remoteModel import CustomLLM
from langchain_core.prompts import PromptTemplate


LLM_URL=os.getenv("LLM_URL")

llm = CustomLLM(
	url=LLM_URL,
	model="mistral-8192" #feel free to change model name here based on your local config
)

def format_markdown(raw_doc: str, max_retries: int = 2) -> str:
	"""Improves the Markdown formatting of the generated documentation."""
	markdown_prompt = PromptTemplate(
		input_variables=["raw_doc"],
		template="""\
You are an expert in technical writing and Markdown.

Reformat and translate the text below into English if necessary, correcting all spelling and grammar mistakes. Transform it into a clear, structured, and professional Markdown document.

**Instructions:**
- Use hierarchical headings (#, ##, ###) in English
- Properly format lists, tables, and code blocks
- Add an automatic table of contents at the beginning of the document
- dont use '```markdown`
- Ensure all text is written in correct and natural English
- Correct all language or syntax errors
- If the text contains technical terms or code, keep them as they are
- Only return the reformatted content for direct use.

Text to reformat:
{raw_doc}
"""
	)
	
	chain = markdown_prompt | llm
	best_response = raw_doc
	
	for attempt in range(max_retries):
		try:
			response = chain.invoke({"raw_doc": raw_doc})
			return response

		except Exception as e:
			print(f"Error while formating (attempt {attempt+1}): {e}")

def list_subdirectories(root_dir):
	"""Lists all immediate subdirectories of a folder."""
	subdirs = []
	for dirpath, dirnames, filenames in os.walk(root_dir):
		if dirpath == root_dir:
			subdirs = [os.path.join(dirpath, d) for d in dirnames]
			break
	return subdirs

def should_skip(directory_path):
	"""Check if the folder should be ignored."""
	skip_dirs = {".git", "__pycache__", "node_modules", "venv", ".DS_Store", "docs", "env"}
	return any(os.path.basename(directory_path) in skip_dirs for dirpath, dirnames, filenames in os.walk(directory_path))

def analyze_directory(directory_path):
	"""Analyzes a folder with GitIngest."""
	try:
		print(f"Analyzing folder: {directory_path}")
		if should_skip(directory_path):
			print(f"Folder ignored: {directory_path}")
			return None
		summary, tree, content = ingest(
			directory_path,
			max_file_size=10485760,
			exclude_patterns={"*.pyc", "./__pycache__", ".git", "./node_modules", "./venv", ".DS_Store", "./docs", "*.log"},
			output=None
		)
		return {
			"directory": directory_path,
			"summary": summary,
			"tree": tree,
			"content": content
		}
	except Exception as e:
		print(f"Error analyzing {directory_path}: {e}")
		return None

def generate_documentation(analysis_result):
	"""Generates documentation using a local LLM."""
	if not analysis_result:
		return "Analysis not avaible"
	
	print(f"Generating documentation for: {analysis_result['directory']}")
	
	prompt_template = PromptTemplate(
		input_variables=["summary", "tree", "content"],
		template="""\
Analyze and explain the following source code in detail, IN ENGLISH, for a technical audience.

**Instructions:**
- Describe the general purpose of the project and its main functionality.
- Explain the role of each important file or folder.
- Detail the functionality of key modules, classes, and functions.
- Highlight specific algorithms or logic, with examples if possible.
- Specify the dependencies or libraries used and their purpose.
- If parts of the code are complex, break them down step by step.
- Add advice or remarks on the architecture or code style if relevant.

**Input Data:**
Summary: {summary}
Tree: {tree}
File Contents: {content}
"""
	)
	
	chain = prompt_template | llm
	
	response = chain.invoke({
		"summary": analysis_result["summary"],
		"tree": analysis_result["tree"],
		"content": analysis_result["content"][:100000]
	})
	
	return response

def main():
	parser = argparse.ArgumentParser(description="Automatic project documentation generator")
	parser.add_argument("root_dir", help="Root folder containing the projects to document")
	parser.add_argument("--output", "-o", help="Output folder for the documentation", default="./docs")
	args = parser.parse_args()
	
	os.makedirs(args.output, exist_ok=True)
	
	subdirs = list_subdirectories(args.root_dir)
	print(f"Subdirectories found: {len(subdirs)}")
	
	for subdir in subdirs:
		analysis = analyze_directory(subdir)
		
		if analysis:
			doc = generate_documentation(analysis)
			
			final_doc = format_markdown(doc)

			dir_name = os.path.basename(subdir)
			output_path = os.path.join(args.output, f"{dir_name}_doc.md")
			with open(output_path, "w", encoding="utf-8") as f:
				f.write(f"# Project Documentation {dir_name}\n\n")
				f.write(final_doc)
			
			print(f"Documentation generated: {output_path}")

if __name__ == "__main__":
	main()
