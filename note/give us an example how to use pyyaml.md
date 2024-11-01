Certainly! Here's an example of how to use PyYAML to read, write, and manipulate YAML data in Python:

First, make sure you have PyYAML installed:

```
pip install pyyaml
```

Now, let's look at some common operations:

## Reading a YAML file

```python
import yaml

# Read YAML file
with open('config.yaml', 'r') as file:
    data = yaml.safe_load(file)

print(data)
```

## Writing to a YAML file

```python
import yaml

# Sample data
data = {
    'name': 'John Doe',
    'age': 30,
    'cities': ['New York', 'Paris', 'Tokyo'],
    'has_license': True
}

# Write YAML file
with open('output.yaml', 'w') as file:
    yaml.dump(data, file, default_flow_style=False)
```

## Parsing YAML string

```python
import yaml

yaml_string = """
name: Alice Smith
age: 28
hobbies:
  - reading
  - hiking
  - photography
"""

# Parse YAML string
parsed_data = yaml.safe_load(yaml_string)

print(parsed_data)
```

## Working with multiple YAML documents

```python
import yaml

multiple_docs = """
---
document: 1
title: First Document
---
document: 2
title: Second Document
"""

# Parse multiple YAML documents
for doc in yaml.safe_load_all(multiple_docs):
    print(doc)
```

## Error handling

```python
import yaml

invalid_yaml = """
key1: value1
key2: value2:
"""

try:
    parsed_data = yaml.safe_load(invalid_yaml)
except yaml.YAMLError as e:
    print(f"Error parsing YAML: {e}")
```

Remember to always use `yaml.safe_load()` instead of `yaml.load()` when working with untrusted YAML sources, as it prevents arbitrary code execution.

These examples cover the basic operations you can perform with PyYAML. You can read from files or strings, write Python data structures to YAML format, handle multiple documents, and manage parsing errors. PyYAML is quite versatile and can handle complex nested structures as well.

Citations:
[1] https://ioflood.com/blog/python-yaml-parser/
[2] https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python/38922434
[3] https://python.land/data-processing/python-yaml
[4] https://pynative.com/python-yaml/
[5] https://pyyaml.org/wiki/PyYAMLDocumentation
[6] https://matthewpburruss.com/post/yaml/
[7] https://earthly.dev/blog/yaml-in-python/
[8] https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started
