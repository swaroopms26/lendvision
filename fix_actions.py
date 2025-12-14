file_path = r'c:\Users\swaroop\.gemini\antigravity\scratch\loan_platform\app\templates\super_admin\dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the malformed actions column
old_actions = '''                            <td>
                                <button class="btn btn-sm btn-primary" data-bs-toggle="modal"
                                <a href="{{ url_for('super_admin.bank_admins', bank_id=item.bank.id) }}" class="btn btn-sm btn-info"><i class="bi bi-people"></i> Team</a>
                                    data-bs-target="#editModal{{ item.bank.id }}">
                                    <i class="bi bi-pencil"></i> Edit
                                </button>
                                <button class="btn btn-sm btn-danger" data-bs-toggle="modal"
                                    data-bs-target="#deleteModal{{ item.bank.id }}">
                                    <i class="bi bi-trash"></i> Delete
                                </button>
                            </td>'''

new_actions = '''                            <td>
                                <a href="{{ url_for('super_admin.bank_admins', bank_id=item.bank.id) }}" class="btn btn-sm btn-info">
                                    <i class="bi bi-people"></i> Team
                                </a>
                                <button class="btn btn-sm btn-primary" data-bs-toggle="modal"
                                    data-bs-target="#editModal{{ item.bank.id }}">
                                    <i class="bi bi-pencil"></i> Edit
                                </button>
                                <button class="btn btn-sm btn-danger" data-bs-toggle="modal"
                                    data-bs-target="#deleteModal{{ item.bank.id }}">
                                    <i class="bi bi-trash"></i> Delete
                                </button>
                            </td>'''

content = content.replace(old_actions, new_actions)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Actions column fixed correctly!')
