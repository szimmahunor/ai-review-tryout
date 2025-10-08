# 03_python_fastapi_project

This is a new topic scaffold. Environment is managed by **uv** and auto-activated by **direnv**.

## Set-up

### `direnv` (if you are not using direnv, do it manually)
```bash
    cd 03_python_fastapi_project
    direnv allow # do this the first time you cd to the folder
```

### `.env`

Create a `.env` file in the config folder, then set the following variables:
```
DATABASE_URL=<your_database_url> (example: mysql+aiomysql://user:password@localhost/dbname)
```

## Start the project

To start the project run:
```bash
    -m uvicorn src.python_fastapi_project.main:app
```
