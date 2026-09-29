# AI Internship Matcher & Opportunity Scanner

An explainable end-to-end ML application that helps students discover
and evaluate internships from their resume. The system extracts resume
skills, performs semantic matching with Sentence Transformers and FAISS,
ranks opportunities, identifies skill gaps, and analyzes internship
postings for quality and red-flag signals.

## Key Features

-   Resume PDF text extraction using PyMuPDF
-   Resume text cleaning and normalization
-   Explainable technical skill extraction using a controlled vocabulary
-   Skill-name normalization such as `Springboot -> Spring Boot` and
    `Postgres -> PostgreSQL`
-   Semantic embeddings using `all-MiniLM-L6-v2`
-   384-dimensional normalized embeddings
-   FAISS vector search for internship retrieval
-   Explainable internship ranking
-   Resume-to-internship skill-gap analysis
-   Opportunity Quality & Red-Flag Analysis using heuristics
-   FastAPI REST API
-   Streamlit dashboard
-   Pytest test suite
-   Docker support
-   Reproducible local internship dataset

## Architecture

``` mermaid
flowchart TD
    A[Resume PDF/Text] --> B[Text Extraction and Cleaning]
    B --> C[Skill Extraction]
    B --> D[Resume Embedding]
    D --> E[FAISS Search]
    F[Internship Dataset] --> G[Internship Embeddings]
    G --> E
    E --> H[Semantic Matching]
    C --> I[Skill Match and Gap Analysis]
    F --> J[Opportunity Quality Analysis]
    H --> K[Explainable Ranking]
    I --> K
    J --> K
    K --> L[FastAPI]
    L --> M[Streamlit Dashboard]
```

## How It Works

### 1. Resume Processing

A user uploads a resume PDF or provides resume text.

For PDFs, PyMuPDF extracts the text. The text is then cleaned by
normalizing whitespace and preserving important technical terms.

Image-only or scanned PDFs are rejected with a clear error because OCR
is outside the scope of this project.

### 2. Skill Extraction

The system uses a curated technical skill vocabulary rather than
claiming to perform perfect NLP entity recognition.

Examples include:

-   Python
-   Java
-   C++
-   JavaScript
-   TypeScript
-   SQL
-   PostgreSQL
-   MySQL
-   MongoDB
-   Redis
-   Spring Boot
-   FastAPI
-   Flask
-   Django
-   React
-   Node.js
-   Docker
-   Kubernetes
-   AWS
-   GCP
-   Azure
-   Kafka
-   Git
-   GitHub
-   Linux
-   Machine Learning
-   Deep Learning
-   NLP
-   PyTorch
-   TensorFlow
-   Scikit-learn
-   Pandas
-   NumPy
-   FAISS
-   REST API
-   Microservices
-   System Design

Skill variants are normalized before comparison.

### 3. Semantic Embeddings

The project uses the pretrained Sentence Transformer:

``` text
all-MiniLM-L6-v2
```

The model converts resume and internship text into 384-dimensional
embeddings.

The internship representation combines:

``` text
title + description + skills
```

The transformer is not fine-tuned.

### 4. FAISS Retrieval

Internship embeddings are generated once and stored in a FAISS index.

At runtime:

``` text
Resume
  |
  v
Resume Embedding
  |
  v
FAISS Similarity Search
  |
  v
Top-N Candidate Internships
```

The API loads the prebuilt index instead of regenerating internship
embeddings for every request.

### 5. Ranking

Retrieved internships are reranked using:

``` text
final_score =
    0.65 * semantic_score
  + 0.25 * skill_match_score
  + 0.10 * quality_score
```

The weights are configurable in the ranking module.

The semantic score represents semantic relevance. It is not the
probability of getting selected for an internship.

### 6. Skill Gap Analysis

For every recommendation, the system compares resume skills with the
internship's required skills.

It returns:

-   matched skills
-   missing skills
-   match percentage

Example:

``` json
{
  "matched_skills": [
    "Java",
    "Spring Boot",
    "PostgreSQL"
  ],
  "missing_skills": [
    "Kafka",
    "AWS"
  ],
  "match_percentage": 60.0
}
```

### 7. Opportunity Quality & Red-Flag Analysis

The project uses explainable heuristics instead of a fabricated scam
classifier.

Signals can include:

-   Very short descriptions
-   Missing company information
-   Missing salary information
-   Unrealistic experience requirements
-   Excessive urgency
-   Requests for payment or deposits
-   Suspicious contact information
-   Vague responsibilities
-   Missing application URL
-   Unusually high internship compensation

The result contains a quality score, warnings, and detected signals.

These signals are heuristics. They do not prove that an internship
posting is fraudulent.

## Dataset

The included `data/internships.csv` contains 600 realistic synthetic
internship records generated from role-specific templates.

Required fields are:

``` text
job_id
title
company
location
description
skills
experience_required
employment_type
salary
remote
application_url
```

The included dataset is intended to make the project reproducible
without requiring an external API.

It should not be described as live market data. For production
deployment, the dataset can be replaced with data obtained through a
permitted internship/job API, feed, or other legally usable source.

## Project Structure

``` text
ai-internship-matcher/
|
├── data/
│   └── internships.csv
|
├── notebooks/
│   └── exploration.ipynb
|
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   └── preprocessing.py
│   |
│   ├── embeddings/
│   │   └── embedding_service.py
│   |
│   ├── vector_store/
│   │   └── faiss_index.py
│   |
│   ├── matching/
│   │   ├── semantic_matcher.py
│   │   └── ranking.py
│   |
│   ├── skills/
│   │   ├── extractor.py
│   │   └── vocabulary.py
│   |
│   └── quality/
│       └── analyzer.py
|
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── dependencies.py
│   └── services/
│       ├── resume_service.py
│       ├── matching_service.py
│       └── recommendation_service.py
|
├── models/
│   ├── internship_index.faiss
│   ├── internship_metadata.joblib
│   └── embedding_config.joblib
|
├── scripts/
│   ├── build_index.py
│   └── generate_dataset.py
|
├── tests/
│   ├── test_embeddings.py
│   ├── test_skills.py
│   ├── test_matching.py
│   ├── test_quality.py
│   └── test_api.py
|
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## Technology Stack

-   Python
-   Pandas
-   NumPy
-   PyMuPDF
-   Sentence Transformers
-   Hugging Face Transformers
-   `all-MiniLM-L6-v2`
-   FAISS
-   scikit-learn
-   FastAPI
-   Uvicorn
-   Pydantic
-   Streamlit
-   Joblib
-   Pytest
-   Matplotlib
-   Docker

No database, Kafka, Redis, Kubernetes, LangChain, or authentication
layer is required.

## Installation

Create a virtual environment:

``` bash
python -m venv .venv
```

Windows:

``` powershell
.venv\Scripts\activate
```

Linux/macOS:

``` bash
source .venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

## Build the FAISS Index

From the project root:

``` bash
python -m scripts.build_index
```

This generates:

``` text
models/
├── internship_index.faiss
├── internship_metadata.joblib
└── embedding_config.joblib
```

The first run downloads the pretrained `all-MiniLM-L6-v2` model through
Sentence Transformers.

Internship embeddings are generated during index construction and are
reused at runtime.

## Run FastAPI

From the project root:

``` bash
python -m uvicorn app.main:app --reload
```

Open:

``` text
http://127.0.0.1:8000/docs
```

The Swagger interface provides interactive access to the API.

## API Endpoints

### GET /health

Checks whether the embedding model and FAISS index are available.

Example response:

``` json
{
  "status": "healthy",
  "model_loaded": true,
  "index_loaded": true
}
```

### POST /analyze-resume

Accepts a PDF resume and extracts:

-   detected skills
-   extracted text length

### POST /match-internships

Accepts resume text and returns semantically relevant internships.

Example request:

``` json
{
  "resume_text": "Java backend developer with Spring Boot, PostgreSQL, Docker and REST API experience.",
  "top_k": 5
}
```

### POST /skill-gap

Compares resume skills with one internship.

Example request:

``` json
{
  "resume_text": "Java developer with Spring Boot and PostgreSQL experience.",
  "job_id": "INT0123"
}
```

### POST /opportunity-analysis

Analyzes the quality signals of one internship posting.

Example request:

``` json
{
  "job_id": "INT0123"
}
```

### POST /recommendations

Primary end-to-end recommendation endpoint.

Example request:

``` json
{
  "resume_text": "Java backend developer with Spring Boot, PostgreSQL, Docker and REST API experience.",
  "top_k": 5
}
```

Typical response:

``` json
{
  "recommendations": [
    {
      "job_id": "INT0123",
      "title": "Java Backend Intern",
      "company": "NovaTech",
      "semantic_score": 88.2,
      "skill_match_score": 83.33,
      "quality_score": 100,
      "final_score": 87.92,
      "matched_skills": [
        "Docker",
        "Java",
        "PostgreSQL",
        "REST API",
        "Spring Boot"
      ],
      "missing_skills": [
        "Kafka"
      ],
      "warnings": []
    }
  ]
}
```

Scores depend on the dataset, model version, and internship
descriptions.

## Run Streamlit

Start the dashboard:

``` bash
streamlit run streamlit_app.py
```

The dashboard allows the user to:

1.  Upload a resume PDF
2.  Analyze the resume
3.  View detected skills
4.  View recommended internships
5.  View semantic match scores
6.  View skill match scores
7.  View matched skills
8.  View missing skills
9.  View opportunity quality
10. View warnings
11. Open the provided application URL

## Testing

Run:

``` bash
python -m pytest -q
```

The test suite covers:

-   Skill normalization
-   Skill extraction
-   Embedding generation
-   Similarity and ranking logic
-   Opportunity quality analysis
-   API validation

The embedding test may be skipped when the pretrained model cannot be
downloaded in an offline environment.

No fake recommendation or evaluation metrics are claimed.

## Exploratory Analysis

The notebook:

``` text
notebooks/exploration.ipynb
```

covers basic dataset analysis such as:

-   Internship distribution
-   Location distribution
-   Remote versus non-remote roles
-   Common skills
-   Salary availability
-   Experience requirements
-   Description length

## Docker

Build the API image:

``` bash
docker build -t ai-internship-matcher .
```

Run it:

``` bash
docker run -p 8000:8000 ai-internship-matcher
```

Or use Docker Compose:

``` bash
docker compose up --build
```

The API runs on:

``` text
http://localhost:8000
```

The Streamlit service runs on:

``` text
http://localhost:8501
```

## Evaluation

A recommendation system should ideally be evaluated using manually
labeled resume-internship relevance pairs.

Useful metrics include:

-   Precision@K
-   Recall@K
-   Mean Reciprocal Rank (MRR)

The included synthetic dataset does not contain human relevance labels,
so the project does not claim fabricated recommendation-quality metrics.

## Limitations

-   The skill extractor only recognizes skills in its controlled
    vocabulary.
-   Semantic similarity can miss domain-specific nuances.
-   Semantic similarity is not an employment or selection probability.
-   The included internship dataset is synthetic and is not live market
    data.
-   Application URLs in a synthetic dataset should not be treated as
    verified live listings.
-   Opportunity quality analysis uses heuristics and cannot establish
    that an internship is fraudulent.
-   Image-only/scanned PDFs are not processed because OCR is outside the
    project scope.
-   The current system uses a local FAISS index rather than a
    production-scale distributed vector database.

## Future Improvements

Possible production extensions include:

-   Connecting the ingestion layer to a permitted internship/job API or
    feed
-   Periodically refreshing internship listings
-   Incrementally updating the FAISS index
-   Adding human-labeled relevance data
-   Evaluating Precision@K, Recall@K and MRR
-   Improving skill extraction with a dedicated NLP model
-   Adding personalized ranking based on user preferences
-   Adding a production vector database when the dataset becomes large
-   Adding monitoring and scheduled data refresh





