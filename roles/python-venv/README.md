Meant for importing and using instead of plain pip module.

Use like this:

```yaml
- name: Create python3 virtualenv
  import_role:
    name: "python-venv"
  vars:
    python_venv_dir: ""
    python_venv_requirements: ""
```
