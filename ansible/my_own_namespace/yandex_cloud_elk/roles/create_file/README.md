# Create File Role

This role uses the my_own_module to create files on remote hosts.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
create_file_path: "/tmp/ansible_default_file.txt"
create_file_content: "Default content from role"
create_file_force: false
Parameters description:
create_file_path: Path where the file should be created

create_file_content: Content to write to the file

create_file_force: If true, overwrite existing file; if false, don't modify existing file

Dependencies
None.

Example Playbook
yaml
- hosts: all
  roles:
    - role: create_file
      vars:
        create_file_path: "/tmp/my_test_file.txt"
        create_file_content: "Hello from role!"
        create_file_force: true
