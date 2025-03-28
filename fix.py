with open('main.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Create a new list to store the fixed lines
fixed_lines = []
i = 0
while i < len(lines):
    # Fix add_bg_from_url function indentation
    if 'def add_bg_from_url():' in lines[i] and i+1 < len(lines) and 'st.markdown' in lines[i+1]:
        fixed_lines.append(lines[i])
        fixed_lines.append('    ' + lines[i+1])
        i += 2
    # Fix the roadmap section indentation in the About page
    elif 'with col1:' in lines[i].strip() and not lines[i].strip().endswith(':'):
        fixed_lines.append(lines[i])
        if i+1 < len(lines) and lines[i+1].strip().startswith('st.markdown'):
            fixed_lines.append('    ' + lines[i+1])
            i += 2
        else:
            i += 1
    else:
        fixed_lines.append(lines[i])
        i += 1

# Write the fixed lines back to the file
with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("All indentation issues fixed in main.py") 