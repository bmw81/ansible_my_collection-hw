#!/usr/bin/python

# Copyright: (c) 2024, Your Name <your.email@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This module creates a text file on a remote host

version_added: "1.0.0"

description: This module creates a text file with specified content at the specified path on the remote host.

options:
    path:
        description: The path where the file should be created on the remote host.
        required: true
        type: str
    content:
        description: The content to write to the file.
        required: true
        type: str
    force:
        description: If 'yes', will overwrite the file if it already exists. If 'no', will not modify an existing file.
        required: false
        type: bool
        default: false

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Create a file with content
- name: Create a text file
  my_namespace.my_collection.my_own_module:
    path: /tmp/testfile.txt
    content: "Hello, World!"

# Create a file with content and overwrite if exists
- name: Create a text file with force overwrite
  my_namespace.my_collection.my_own_module:
    path: /tmp/testfile.txt
    content: "New content"
    force: true
'''

RETURN = r'''
original_path:
    description: The original path that was passed in.
    type: str
    returned: always
    sample: '/tmp/testfile.txt'
original_content:
    description: The original content that was passed in.
    type: str
    returned: always
    sample: 'Hello, World!'
message:
    description: The status message about the file operation.
    type: str
    returned: always
    sample: 'File created successfully'
'''

import os
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        force=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
        original_path='',
        original_content='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Store original parameters
    result['original_path'] = module.params['path']
    result['original_content'] = module.params['content']
    
    # Check if file already exists
    file_exists = os.path.exists(module.params['path'])
    
    # In check mode, determine if changes would be made
    if module.check_mode:
        if file_exists:
            # Read existing content
            try:
                with open(module.params['path'], 'r') as f:
                    existing_content = f.read()
                if existing_content != module.params['content'] and module.params['force']:
                    result['changed'] = True
                    result['message'] = 'File content would be updated (check mode)'
                elif not module.params['force']:
                    result['message'] = 'File exists and force is false - no changes would be made (check mode)'
                else:
                    result['message'] = 'File exists with same content - no changes needed (check mode)'
            except Exception as e:
                module.fail_json(msg=f"Error reading file: {str(e)}", **result)
        else:
            result['changed'] = True
            result['message'] = 'File would be created (check mode)'
        
        module.exit_json(**result)

    # Perform actual file operations
    try:
        # Get directory path and create directories if they don't exist
        directory = os.path.dirname(module.params['path'])
        if directory and not os.path.exists(directory):
            os.makedirs(directory, mode=0o755)
        
        # Check if file exists and handle force parameter
        if file_exists:
            # Read existing content
            with open(module.params['path'], 'r') as f:
                existing_content = f.read()
            
            # Compare content
            if existing_content != module.params['content']:
                if module.params['force']:
                    # Overwrite file with new content
                    with open(module.params['path'], 'w') as f:
                        f.write(module.params['content'])
                    result['changed'] = True
                    result['message'] = 'File updated with new content'
                else:
                    result['message'] = 'File exists with different content, but force is false - no changes made'
            else:
                result['message'] = 'File exists with same content - no changes needed'
        else:
            # Create new file
            with open(module.params['path'], 'w') as f:
                f.write(module.params['content'])
            result['changed'] = True
            result['message'] = 'File created successfully'
            
    except Exception as e:
        module.fail_json(msg=f"Error during file operation: {str(e)}", **result)

    # Return success
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
