import re
import os

def process_content(content):
    # 1. Fix image links
    # [<File:Cisco_BGP_Open.PNG>](/File:Cisco_BGP_Open.PNG "wikilink") -> ![Cisco_BGP_Open.PNG](../images/Cisco_BGP_Open.PNG)
    content = re.sub(r'\[<File:([^>]+)>\]\(/File:[^>]+ "wikilink"\)', r'![\1](../images/\1)', content)
    # Fix relative img/ links to ../images/
    content = re.sub(r'\(img/([^)]+)\)', r'(../images/\1)', content)

    # 2. Remove Category links
    # [Category:Cisco](/Category:Cisco "wikilink") -> 
    content = re.sub(r'\[Category:[^\]]+\]\(/Category:[^>]+ "wikilink"\)', '', content)

    # 3. Remove DIV tags (specifically mw-collapsible and mw-collapsible-content)
    content = re.sub(r'<div [^>]*class="[^"]*mw-collapsible[^"]*"[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<div class="mw-collapsible-content">', '', content)
    # Note: removing all </div> might be risky if there are other divs, 
    # but based on the TODO it seems they want to clean up these wiki-artifacts.
    # We'll remove </div> tags.
    content = re.sub(r'</div>', '', content, flags=re.IGNORECASE)

    # 4. Fix code blocks
    # Convert sequences of single backtick lines to a single code block
    lines = content.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Check if line is wrapped in backticks: `command`
        if line.startswith('`') and line.endswith('`') and line.count('`') == 2:
            block = []
            while i < len(lines):
                l = lines[i].strip()
                if l.startswith('`') and l.endswith('`') and l.count('`') == 2:
                    # Remove the backticks and add to block
                    block.append(lines[i].strip()[1:-1])
                    i += 1
                else:
                    break
            new_lines.append('```')
            new_lines.extend(block)
            new_lines.append('```')
        else:
            new_lines.append(lines[i])
            i += 1
    
    content = '\n'.join(new_lines)
    return content

def main():
    todo_path = 'TODO.md'
    with open(todo_path, 'r', encoding='utf-8') as f:
        todo_content = f.read()

    # Find all lines with "- [ ] Review and process: "
    files_to_process = re.findall(r'- \[ \] Review and process: (.*?)\n', todo_content)
    
    for file_rel_path in files_to_process:
        # Convert backslash to forward slash for consistency
        file_rel_path = file_rel_path.replace('\\', '/')
        full_path = os.path.join('docs', file_rel_path)
        
        if os.path.exists(full_path):
            print(f"Processing {full_path}...")
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = process_content(content)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Mark as done in TODO.md
            todo_content = todo_content.replace(f'- [ ] Review and process: {file_rel_path}', f'- [x] Review and process: {file_rel_path}')
            todo_content = todo_content.replace(f'- [ ] Review and process: {file_rel_path.replace("/", "\\")}', f'- [x] Review and process: {file_rel_path.replace("/", "\\")}')

    with open(todo_path, 'w', encoding='utf-8') as f:
        f.write(todo_content)

    print("Done!")

if __name__ == "__main__":
    main()