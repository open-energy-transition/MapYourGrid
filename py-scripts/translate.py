import sys
import deepl
import re
import yaml
from pathlib import Path

def translate_markdown_file(source_file, target_lang):
    # Replace with your actual DeepL API key
    translator = deepl.Translator("DEEPL API KEY")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Step 1: Extract and protect YAML frontmatter
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    yaml_content = ""
    main_content = content
    
    if yaml_match:
        yaml_content = yaml_match.group(0)
        main_content = content[len(yaml_content):]
        
        # Translate specific fields in YAML frontmatter
        yaml_body = yaml_match.group(1)
        try:
            yaml_data = yaml.safe_load(yaml_body)
            if yaml_data:
                # Translate title and description if they exist
                if 'title' in yaml_data:
                    try:
                        yaml_data['title'] = translator.translate_text(yaml_data['title'], target_lang=target_lang.upper()).text
                    except:
                        pass
                if 'description' in yaml_data:
                    try:
                        yaml_data['description'] = translator.translate_text(yaml_data['description'], target_lang=target_lang.upper()).text
                    except:
                        pass
                
                # Reconstruct YAML frontmatter
                yaml_content = "---\n" + yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True) + "---\n"
        except:
            # If YAML parsing fails, keep original
            pass
    
    # Step 3: Extract and protect JavaScript/script blocks (these should NEVER be translated)
    script_blocks = []
    def replace_script(match):
        script_blocks.append(match.group(0))
        return f"__SCRIPT_BLOCK_{len(script_blocks)-1}__"
    
    main_content = re.sub(r'<script[^>]*>.*?</script>', replace_script, main_content, flags=re.DOTALL)
    
    # Step 4: Extract and protect iframe blocks (these should NEVER be translated)
    iframe_blocks = []
    def replace_iframe(match):
        iframe_blocks.append(match.group(0))
        return f"__IFRAME_BLOCK_{len(iframe_blocks)-1}__"
    
    main_content = re.sub(r'<iframe[^>]*>.*?</iframe>', replace_iframe, main_content, flags=re.DOTALL)
    
    # Step 5: Extract and protect image tags (these should NEVER be translated)
    img_blocks = []
    def replace_img(match):
        img_blocks.append(match.group(0))
        return f"__IMG_BLOCK_{len(img_blocks)-1}__"
    
    main_content = re.sub(r'<img[^>]*/?>', replace_img, main_content)
    
    # Step 5.5: NEW - Extract and protect HTML attributes including CSS classes
    protected_attrs = []
    def protect_html_attributes(match):
        full_tag = match.group(0)
        
        # Protect all HTML attributes from translation
        # This regex finds opening HTML tags with attributes
        attr_pattern = r'(\w+)="([^"]*)"'
        attrs = re.findall(attr_pattern, full_tag)
        
        # Don't translate common HTML attributes
        protected_attributes = {
            'class', 'id', 'src', 'href', 'alt', 'title', 'data-form', 'data-', 
            'target', 'rel', 'style', 'width', 'height', 'frameborder', 'allow',
            'referrerpolicy', 'allowfullscreen'
        }
        
        for attr_name, attr_value in attrs:
            if any(attr_name.startswith(prot) for prot in protected_attributes):
                # This attribute should be protected
                protected_attrs.append(f'{attr_name}="{attr_value}"')
                placeholder = f"__ATTR_BLOCK_{len(protected_attrs)-1}__"
                full_tag = full_tag.replace(f'{attr_name}="{attr_value}"', placeholder)
        
        return full_tag
    
    # Protect attributes in HTML tags
    main_content = re.sub(r'<[^>]+>', protect_html_attributes, main_content)
    
    # Step 6: Extract and protect URLs (these should NEVER be translated)
    url_blocks = []
    def replace_url(match):
        url_blocks.append(match.group(0))
        return f"__URL_BLOCK_{len(url_blocks)-1}__"
    
    # Protect all URLs (http/https)
    main_content = re.sub(r'https?://[^\s\)"\]<>]+', replace_url, main_content)
    
    def should_translate_text(text):
        """Check if text should be translated - more permissive now"""
        if not text or not isinstance(text, str):
            return False
            
        text = text.strip()
        
        # Don't translate if:
        if (len(text) < 2 or                                    # Too short (reduced from 3)
            text.startswith('__') and '_BLOCK_' in text or      # Protected block
            re.match(r'^[#\-\*\+\s]*$', text) or              # Markdown formatting only
            re.match(r'^<[^>]*>$', text) or                    # Pure HTML tag
            text.startswith('<!--') or                          # HTML comment
            re.match(r'^[\d\.\s%km\-]+$', text) or             # Numbers/percentages only
            re.match(r'^[⚡📍🗼👥️⚡️\s]+$', text) or              # Emojis only
            re.match(r'^[\.]{3,}$', text)):                    # Ellipsis like "..."
            return False
        
        # DO translate if it contains letters (any language)
        if re.search(r'[a-zA-ZáéíóúüñÁÉÍÓÚÜÑàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛçÇ]', text):
            return True
            
        return False
    
    # Step 8: Extract and protect markdown links (but translate their text)
    md_link_blocks = []
    def replace_md_link_with_translation(match):
        full_match = match.group(0)
        link_text = match.group(1)
        link_url = match.group(2)
        
        # Translate the link text if it's translatable
        translated_text = link_text
        if should_translate_text(link_text):
            try:
                translated_text = translator.translate_text(link_text, target_lang=target_lang.upper()).text
            except:
                pass
        
        result = f"[{translated_text}]({link_url})"
        md_link_blocks.append(result)
        return f"__MD_LINK_BLOCK_{len(md_link_blocks)-1}__"
    
    main_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_md_link_with_translation, main_content)
    
    # Step 9: Extract and protect only structural HTML tags (not content-bearing ones)
    html_tag_blocks = []
    def replace_html_tag(match):
        html_tag_blocks.append(match.group(0))
        return f"__HTML_TAG_BLOCK_{len(html_tag_blocks)-1}__"
    
    # Only protect truly structural tags that should never be translated
    protected_tag_patterns = [
        r'<br\s*/?>',  # Self-closing br tags
        r'<!--.*?-->',  # HTML comments
    ]
    
    for pattern in protected_tag_patterns:
        main_content = re.sub(pattern, replace_html_tag, main_content, flags=re.DOTALL)
    
    # Step 9.5: NEW - Handle MkDocs Material admonitions (???) with proper indentation
    def fix_admonition_indentation(text):
        """Fix admonition indentation to ensure 4-space indentation under ??? blocks"""
        lines = text.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check if this is an admonition line (starts with ??? and has quotes)
            if re.match(r'^\s*\?\?\?\s*"', line.strip()):
                result_lines.append(line)
                i += 1
                
                # Process following lines that should be indented under the admonition
                while i < len(lines):
                    if i >= len(lines):
                        break
                        
                    next_line = lines[i]
                    
                    # Stop if we hit another admonition, heading, or empty line followed by non-indented content
                    if (re.match(r'^\s*\?\?\?\s*"', next_line.strip()) or 
                        re.match(r'^#{1,6}\s', next_line.strip()) or
                        (next_line.strip() == '' and 
                         i + 1 < len(lines) and 
                         lines[i + 1].strip() != '' and 
                         not lines[i + 1].startswith('    '))):
                        break
                    
                    # If the line has content and is not already properly indented for admonitions
                    if next_line.strip() != '':
                        # Check if it needs indentation (content that should be under the admonition)
                        if not next_line.startswith('    ') and next_line.strip():
                            # Add 4 spaces for admonition content
                            content = next_line.lstrip()
                            next_line = '    ' + content
                    
                    result_lines.append(next_line)
                    i += 1
            else:
                result_lines.append(line)
                i += 1
                
        return '\n'.join(result_lines)
    
    def translate_text_content(text):
        """Translate text while preserving structure"""
        if not should_translate_text(text):
            return text
            
        leading_space = text[:len(text) - len(text.lstrip())]
        trailing_space = text[len(text.rstrip()):]

        try:
            # Clean up text before translation
            cleaned_text = text.strip()
            if not cleaned_text:
                return text
            translated = translator.translate_text(cleaned_text, target_lang=target_lang.upper()).text
            return leading_space + translated + trailing_space
        except Exception as e:
            print(f"Translation error for text '{text[:50]}...': {e}")
            return text
    
    # Step 11: Translate HTML content more aggressively
    def translate_html_element(match):
        full_match = match.group(0)
        tag_start = match.group(1)      # Opening tag, e.g., <p class="lead-statement">
        inner_content = match.group(2)  # Content inside the tag
        tag_end = match.group(3)        # Closing tag, e.g., </p>
        
        # This separates translatable text from non-translatable elements.
        parts = re.split(r'(<[^>]*>|__\w+_BLOCK_\d+__)', inner_content)
        
        translated_parts = []
        for part in parts:
            # Check if the part is a placeholder or an HTML tag; if so, keep it as is.
            if part.startswith('<') and part.endswith('>'):
                translated_parts.append(part)
            elif part.startswith('__') and part.endswith('__'):
                translated_parts.append(part)
            else:
                # Otherwise, it's text that needs translation.
                translated_parts.append(translate_text_content(part))
                
        translated_inner = ''.join(translated_parts)
        return f"{tag_start}{translated_inner}{tag_end}"
    
    # Apply translation to ALL content-bearing HTML tags
    html_text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'blockquote', 'li', 'div', 'span', 'a', 'figcaption']
    for tag in html_text_tags:
        # More flexible pattern that captures content across multiple lines
        pattern = f'(<{tag}[^>]*>)(.*?)(</{tag}>)'
        main_content = re.sub(pattern, translate_html_element, main_content, flags=re.DOTALL)
    
    # Step 12: Translate remaining text content line by line (more aggressive)
    lines = main_content.split('\n')
    translated_lines = []
    for line in lines:
        # This new logic correctly handles lines with mixed content, like numbered lists containing links
        parts = re.split(r'(__\w+_BLOCK_\d+__)', line)
        translated_parts = [translate_text_content(p) if not (p.startswith('__') and p.endswith('__')) else p for p in parts]
        translated_lines.append(''.join(translated_parts))

    main_content = '\n'.join(translated_lines)
    
    # Step 12.5: NEW - Apply admonition indentation fix
    main_content = fix_admonition_indentation(main_content)
    
    # Step 13: Restore all protected content in reverse order
    
    # NEW - Restore protected attributes
    for i, attr_block in enumerate(protected_attrs):
        main_content = main_content.replace(f"__ATTR_BLOCK_{i}__", attr_block)
    
    # Restore HTML tag blocks
    for i, tag_block in enumerate(html_tag_blocks):
        main_content = main_content.replace(f"__HTML_TAG_BLOCK_{i}__", tag_block)
    
    # Restore markdown links
    for i, md_link_block in enumerate(md_link_blocks):
        main_content = main_content.replace(f"__MD_LINK_BLOCK_{i}__", md_link_block)
    
    # Restore URLs
    for i, url_block in enumerate(url_blocks):
        main_content = main_content.replace(f"__URL_BLOCK_{i}__", url_block)
    
    # Restore images
    for i, img_block in enumerate(img_blocks):
        main_content = main_content.replace(f"__IMG_BLOCK_{i}__", img_block)
    
    # Restore iframes
    for i, iframe_block in enumerate(iframe_blocks):
        main_content = main_content.replace(f"__IFRAME_BLOCK_{i}__", iframe_block)
    
    # Restore scripts
    for i, script_block in enumerate(script_blocks):
        main_content = main_content.replace(f"__SCRIPT_BLOCK_{i}__", script_block)
    
    # Step 14: Final cleanup
    # Clean up any formatting issues
    main_content = re.sub(r'</a>\.', '</a>', main_content)
    main_content = re.sub(r'</div>\.', '</div>', main_content)
    main_content = re.sub(r'</h[1-6]>\.', lambda m: m.group(0)[:-1], main_content)
    
    # Remove extra spaces and normalize whitespace
    main_content = re.sub(r' +', ' ', main_content)
    main_content = re.sub(r'\n\s*\n\s*\n', '\n\n', main_content)
    
    # Step 15: Combine YAML frontmatter with translated content
    final_content = yaml_content + main_content
    
    return final_content

def translate_single_file(file_path, target_lang):
    source_file = Path(file_path)
    
    if not source_file.exists():
        print(f"File {file_path} not found!")
        return
    
    # Determine target folder based on language
    if target_lang.lower() in ['es', 'spanish']:
        lang_code = 'es'
        lang_folder = 'es'
    elif target_lang.lower() in ['fr', 'french']:
        lang_code = 'fr'  
        lang_folder = 'fr'
    else:
        print(f"Unsupported language: {target_lang}")
        print("Supported languages: es, spanish, fr, french")
        return
    
    # Create target directory structure
    docs_path = Path('docs')
    
    try:
        # Check if the file is within the docs directory
        relative_path = source_file.relative_to(docs_path)
        target_file = docs_path / lang_folder / relative_path
    except ValueError:
        # File is not in docs directory
        print(f"File must be in the docs/ directory. Got: {source_file}")
        print(f"Expected something like: docs/index.md")
        return
    
    # Create target directory if it doesn't exist
    target_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Translating {source_file} to {target_file}...")
    
    # Translate the file
    translated_content = translate_markdown_file(source_file, lang_code)
    
    # Write translated content
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    print(f"Translation complete: {target_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translate_single.py <file_path> <language>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    target_lang = sys.argv[2]
    translate_single_file(file_path, target_lang)