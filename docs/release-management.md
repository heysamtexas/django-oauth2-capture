# How to do release management for the project

* uses [Flit](https://flit.pypa.io/en/stable/) inside the github action to publish the
  package to pypi
* uses [Commitizen](https://commitizen-tools.github.io/commitizen/) to create
changelog and version bump


## Release Management

1. **Install commitizen**: If you haven't already, install commitizen globally
or in your virtual environment:
   ```bash
   pip install commitizen
   ```
2. **Initialize commitizen**: If you haven't already, initialize commitizen in
your project:
   ```bash
    cz init
    ```
3. **Create a new release**: Use commitizen to create a new release. This will
prompt you to enter information about the release, including the version number
and any changes made:
4. ```bash
   cz release
   ```
