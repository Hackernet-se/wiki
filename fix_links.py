import os
import re
from pathlib import Path

def get_all_md_files(docs_dir):
    """Creates a mapping of filename_without_ext -> relative_path_from_docs_root"""
    mapping = {}
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                stem = Path(file).stem
                rel_path = os.path.relpath(os.path.join(root, file), docs_dir).replace('\\', '/')
                mapping[stem.lower()] = rel_path
    return mapping

def calculate_relative_path(current_file_rel_path, target_file_rel_path):
    """Calculates the relative path from current_file to target_file"""
    # current_file_rel_path: e.g., 'cisco/Cisco_MVPN.md'
    # target_file_rel_path: e.g., 'cisco/Cisco_MPLS.md'
    
    current_dir = os.path.dirname(current_file_rel_path)
    
    # Use os.path.relpath but ensure forward slashes
    try:
        rel = os.path.relpath(target_file_rel_path, current_dir).replace('\\', '/')
        # If it doesn't start with . or /, it's in the same dir. 
        # MkDocs/Markdown usually prefers ./ or just the name.
        return rel
    except ValueError:
        return target_file_rel_path

def fix_internal_links(content, file_rel_path, file_mapping):
    """
    Fixes links in the format [Text](/Link "wikilink") or [Text](/Link)
    to point to the actual relative path of the target .md file.
    """
    # Pattern for [Text](/Link "title") or [Text](/Link)
    # Group 1: Text, Group 2: Link (including possible anchor)
    link_pattern = r'\[([^\]]+)\]\(([^ \)]+)(?:\s+"[^"]+")?\)'
    
    def replace_link(match):
        text = match.group(1)
        link_target = match.group(2)
        
        # Handle anchors: /Cisco_MPLS#VPN -> target='Cisco_MPLS', anchor='#VPN'
        if '#' in link_target:
            target_stem, anchor = link_target.split('#', 1)
            anchor = '#' + anchor
        else:
            target_stem = link_target
            anchor = ''
            
        # Remove leading slash for lookup and make case-insensitive
        lookup_stem = target_stem.lstrip('/').lower()
        
        # Check if target_stem is in our mapping
        if lookup_stem in file_mapping:
            target_path = file_mapping[lookup_stem]
            rel_path = calculate_relative_path(file_rel_path, target_path)
            return f'[{text}]({rel_path}{anchor})'
        
        # Special case: image files or other non-md files
        # If the target looks like a file (has extension) and it exists in the docs tree
        # (even if not in file_mapping which only has .md), we should try to resolve it.
        # Since we don't have a full file map, we can check if it exists on disk.
        
        # Try to find the file in the docs directory
        # We check: 1. relative to current file, 2. relative to docs root
        # (The user's warning 'cisco/Cisco_MVPN.PNG' not found suggests it's looking at docs root)
        
        # Try relative to docs root (most common for /Link)
        full_target_path = os.path.join('docs', lookup_stem)
        if os.path.exists(full_target_path):
            rel_path = calculate_relative_path(file_rel_path, lookup_stem)
            return f'[{text}]({rel_path}{anchor})'

        # Try relative to current file
        if os.path.exists(os.path.join(os.path.dirname(os.path.join('docs', file_rel_path)), lookup_stem)):
            return f'[{text}]({link_target}{anchor})'
        
        # If it's a :en: Wikipedia link, keep it as is (external)
        if link_target.startswith(':en:'):
            return f'[{text}]({link_target})'
        
        return f'[{text}]({link_target})'

    # Remove Category:Guider links as requested by user
    content = content.replace('[Category:Guider](Category:Guider)', '')
    return re.sub(link_pattern, replace_link, content)

def main():
    docs_dir = 'docs'
    if not os.path.exists(docs_dir):
        print(f"Error: {docs_dir} directory not found.")
        return

    print("Mapping files...")
    file_mapping = get_all_md_files(docs_dir)
    print(f"Found {len(file_mapping)} markdown files.")

    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, docs_dir).replace('\\', '/')
                
                print(f"Processing {rel_path}...")
                
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = fix_internal_links(content, rel_path, file_mapping)
                
                if new_content != content:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"  Updated links in {rel_path}")

    print("Done!")

if __name__ == '__main__':
    main()
