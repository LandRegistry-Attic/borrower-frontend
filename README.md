# dm-borrower-frontend

The Borrower Frontend provides a service for a Borrower to view and sign their
mortgage deeds online.

## Contents
- [Usage](#usage)
- [Install The Requirements](#install-the-requirements)
- [Run The App](#run-the-app)
- [Run The Tests](#run-the-tests)
- [Frontend](#frontend)

## Usage
```
GET     /                               -- renders borrower landing page
GET     /health                         -- renders standard Gov UK template
```

## Install the requirements

1. Clone the repo

2. Install the requirements
```
pip install -r requirements.txt
```

Optional: export variable for deed-api
```
> export DEED_API_BASE_HOST=http://localhost:8000
```

> default is localhost:9030


## Run the app
```
python run.py runserver --host 0.0.0.0
```
> optional ```--port 9000``` where 9000 is the number of a port you can supply to start the server on.


## Run the Tests

Install the requirements
```
pip install -r requirements_test.txt
```

Run unit tests and provide coverage report

```
source unit_test.sh
```

and

```
source integration_test.sh
```


## Frontend

See [application/assets](application/assets)
