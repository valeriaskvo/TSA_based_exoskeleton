# TSA Exoskeleton: Computer part

## Topics

* <a href="#PREPARATION">Preparation of the project</a>
* <a href="#PROJECT_STRUCTURE">Project structure</a>
* <a href="#TODO_LIST">Todo List</a>

<div id="PREPARATION"></div>

## Prepare python project

**STEP 1:** Install python venv

```shell
pip3 install virtualenv
```

**STEP 2:** Set python venv

```shell
python3 -m venv ./venv
```

* OR

```shell
virtualenv venv
```

**STEP 3:** Activate venv

```shell
source ./venv/bin/activate
```

**STEP 4:** Install all requirements

```shell
pip3 install -r requirements.txt
```

**STEP 5:** Deactivate the venv, if you need

```shell
deactivate
```

<div id="PROJECT_STRUCTURE"></div>

## Project Structure

```
.
├── examples            Folder with examples
├── libs
│   ├── can             Folder with CAN logic module
│   ├── motors          Folder with Motor logic module
│   └── __init__.py
├── src
│   └── main.py         Main script
└── requirements.txt    File with modules to install into the venv
```

<div id="TODO_LIST"></div>

## Todo List

-[ ] TODO TASK

-[x] TODO TASK
