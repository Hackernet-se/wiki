import os

def generate_todos_from_docs(docs_path="docs", todo_file="TODO.md"):
    """
    Generates TODO items in a TODO.md file, with one item per file found
    under the specified docs path.

    Args:
        docs_path: The path to the directory containing the documentation files.
                   Defaults to "docs".
        todo_file: The name of the TODO file to create/update.
                   Defaults to "TODO.md".
    """
    todo_items = []
    for root, _, files in os.walk(docs_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            # Create a descriptive TODO item based on the file path
            relative_path = os.path.relpath(filepath, docs_path)
            todo_text = f"Review and process: {relative_path}"
            todo_items.append(f"- [ ] {todo_text}")

    if todo_items:
        with open(todo_file, "w", encoding="utf-8") as f:
            f.write("# TODO List from Documentation\n\n")
            for item in sorted(todo_items):  # Sort for better readability
                f.write(item + "\n")
        print(f"TODO items generated in '{todo_file}' based on files in '{docs_path}'.")
    else:
        print(f"No files found under '{docs_path}' to create TODO items.")

if __name__ == "__main__":
    # Specify the path to your documentation directory if it's not just 'docs'
    documentation_path = "docs"
    todo_filename = "TODO.md"
    generate_todos_from_docs(documentation_path, todo_filename)