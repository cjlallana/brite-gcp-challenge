# FastAPI Movies API

## Overview
This is a FastAPI-based REST API that allows users to:
- Fetch movies from the OMDB API and store them in **Google Firestore**.
- Retrieve movies with pagination and filtering.
- Add new movies by fetching details from OMDB.
- Delete movies.

## Features
- **FastAPI** for a lightweight, high-performance API.
- **Firestore** as a NoSQL database.
- **Google App Engine Standard** deployment.
- **Unit tests** for all API endpoints.

---

## API Endpoints
### Public endpoints
#### List Movies (Paginated)
```http
GET /v1/movies?limit=10&page=1
```
- **Parameters**:
  - `limit` (default: `10`): Number of movies per page.
  - `page` (default: `1`): Page number.
- **Response**: JSON list of movies ordered by title.

#### Get a Movie by ID
```http
GET /v1/movies/{movie_id}
```
- _Note that it's the Firestore ID of the movie, not IMDB id._

#### Get a Movie by Title
```http
GET /v1/movies/search?title=Gladiator
```
- **Parameters**:
  - `title` (_required_): Title of the movie, case insensitive, but needs to be the complete title, as there's no partial search.

#### Add a Movie (Fetched from OMDB API)
```http
POST /movies
```
- **Request Body**: `{ "title": "The Matrix" }`
- Internally fetches movie details from OMDB API (based on the provided title) and saves them in Firestore.

### Private endpoints (requires authentication)

#### Initialize database
```http
GET /v1/internal/initialize
```
- Populates the database for the first time, in case there are no movies stored yet. It fetches 100 movies from OMDB API and saves them in Firestore.

#### Delete a Movie
```http
DELETE /v1/internal/movies/{movie_id}
```
- Removes a movie from Firestore.

---

## Deployment to Google App Engine Standard
### 1️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 2️⃣ Create `app.yaml` (for App Engine)
Create an **`app.yaml`** file in the project root:
```yaml
runtime: python312
entrypoint: uvicorn core.fastapi_config:app --port 8080

handlers:
  - url: /.*
    script: auto
```

### 3️⃣ Authenticate with Google Cloud
```sh
gcloud auth application-default login
```

### 4️⃣ Deploy to App Engine
```sh
gcloud app deploy
```

### 5️⃣ Access the API
Once deployed, get the service URL:
```sh
gcloud app browse
```
The API will be accessible at `https://your-app-id.appspot.com`.

---

## Running Locally
### 1️⃣ Start Firestore Emulator (Optional for Local Development)
```sh
gcloud emulators firestore start --host-port=localhost:8080
```

### 2️⃣ Run the API Locally
```sh
uvicorn core.fastapi_config:app --reload
```
- Access at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Running Tests
```sh
pytest
```
Tests are written using `pytest` with **mocked Firestore**.

---

## Notes
- We could have used Cloud Run instead of App Engine, as it is a more modern alternative.
- For the /initilize endpoint (for populating the database), a Cloud Function could have been a smart option.
- Authentication for the internal endpoints can be improved in several ways.
- The OMDB API requires an API key, which should be stored securely. [Secret Manager](https://cloud.google.com/secret-manager/docs/reference/libraries#client-libraries-usage-python) would be a good option for it.

🚀 **Enjoy your FastAPI Movies API!**

