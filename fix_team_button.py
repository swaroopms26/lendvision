file_path = r'c:\Users\swaroop\.gemini\antigravity\scratch\loan_platform\app\templates\super_admin\dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove the incorrectly placed line 63 (index 62)
del lines[62]

# Now insert the Team button in the correct place (after line 61, which is now index 61)
team_button = '                                <a href="{{ url_for(\'super_admin.bank_admins\', bank_id=item.bank.id) }}" class="btn btn-sm btn-info"><i class="bi bi-people"></i> Team</a>\n'
lines.insert(62, team_button)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Team button fixed!')
