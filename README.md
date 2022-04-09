# flowly
A platform for authoring and executing workflow content

## Installation
Install Flowly `default` branch:
```bash
python -m pip install git+https://github.com/dylrei/flowly.git
```

Install Flowly `flow-5-foo` branch:
```bash
python -m pip install git+https://github.com/dylrei/flowly.git@flow-5-foo
```

Install Flowly `v0.1` release/tag:
```bash
python -m pip install git+https://github.com/dylrei/flowly.git@v0.1
```


## Version History: 
### v0.1
 * FLOW-20 Create Python package boilerplate
 * FLOW-17 Implement VersionedExecutor and @versioned_executor
 * FLOW-57 Define and load core YAML tags
 * FLOW-69 Implement VersionedDocumentStore and MethodExecutor
 * FLOW-70 Implement MethodStore and load method into MethodExecutor
 * FLOW-71 Create SourceOfTruth to hold single runtime configuration values, such as content_root
 * FLOW-96 Implement ContentRoot
 * FLOW-97 Implement identified_executor, IdentifiedExecutorStore
 * FLOW-100 Implement IdentifiedDocumentStore
 * FLOW-13 Load versioned specification and use for validation
 * FLOW-116 Finalize YAML->object loading
### v0.2
 * FLOW-29 Load and execute a simple Method
