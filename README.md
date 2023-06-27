# About

The project was created along with the [Python API Development](https://www.youtube.com/watch?v=0sOvCWFmrtA) course.

In the project, I worked with the basic concepts of FastAPI, the principles of API, database migrations, and the authorization process.
In addition, I have deployed project on Render instead of Heroku and set up CI/CD for Render.

## Installation

```bash
https://github.com/entl/fastapi-course.git
cd fastapi-couse
```
Install requirements - **Python 3.10.4**
```bash
pip install -r requirements.txt
```

## Prerequisites
Firstly, you need to create a database. The project was tested with a Postgresql database.

After that, you need to create the file ".env" which will contain all variables specified in the "app\config.py" file.

Then migrations have to be applied.
```bash
alembic upgrade head
```

## Run

```bash
uvicorn app.main:app --host localhost --port 8000
```

Docs for the API are generated automatically. They are available at http://localhost:8000/docs

## Contributing

Pull requests are welcome. For major changes, please open an issue first.
to discuss what you would like to change.

Please make sure to update the tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
