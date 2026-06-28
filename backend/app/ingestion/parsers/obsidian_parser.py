import re
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document


def extract_note_title(content: str, filename: str) -> str:
    """Extract title: 1. First # Heading, 2. Filename"""
    # First H1 heading
    match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    # Fallback to filename
    return Path(filename).stem


def extract_tags(content: str) -> List[str]:
    """Extract #tags and frontmatter tags"""
    tags = set()

    # Inline tags
    tag_pattern = r'(?<![a-zA-Z0-9_/])#([a-zA-Z0-9_/][a-zA-Z0-9_/-]+)'
    for match in re.finditer(tag_pattern, content):
        tag = match.group(1).strip()
        if tag:
            tags.add(tag)

    # YAML frontmatter tags
    frontmatter = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter:
        fm = frontmatter.group(1)
        tags_match = re.search(r'tags?[:\s]+\[?(.*?)\]?', fm, re.IGNORECASE)
        if tags_match:
            tag_str = tags_match.group(1)
            for t in re.findall(r'["\']?([^"\',\s]+)["\']?', tag_str):
                if t.strip():
                    tags.add(t.strip())

    return sorted(list(tags))


def extract_wikilinks(content: str) -> List[str]:
    """Extract [[Link]] and [[Link|Alias]]"""
    links = []
    pattern = r'\[\[([^\[\]]+?)\]\]'
    for match in re.finditer(pattern, content):
        text = match.group(1).strip()
        # Handle alias
        if '|' in text:
            link = text.split('|')[0].strip()
        else:
            link = text
        if link:
            links.append(link)
    return list(dict.fromkeys(links))  # preserve order, remove duplicates


def clean_content(content: str) -> str:
    """Clean markdown content"""
    # Remove YAML frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # Remove excessive newlines
    content = re.sub(r'\n\s*\n', '\n\n', content)
    return content.strip()


def parse_obsidian_file(file_path: str) -> Optional[Document]:
    """Parse single .md file into Document with rich metadata"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        path = Path(file_path)
        filename = path.name

        title = extract_note_title(content, filename)
        tags = extract_tags(content)
        wikilinks = extract_wikilinks(content)
        clean_text = clean_content(content)

        # Relative path from vault root (you can adjust this)
        relative_path = str(path)

        metadata = {
            "source": "obsidian",
            "file_path": relative_path,
            "filename": filename,
            "note_title": title,
            "subject": title,                       # shared alias used by subject filter
            "tags": tags,
            "wikilinks": wikilinks,
            "folder": path.parent.name,
            "file_extension": ".md",
            "date_ts": path.stat().st_mtime,        # file last-modified time as Unix float
        }

        return Document(
            page_content=clean_text,
            metadata=metadata
        )

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None