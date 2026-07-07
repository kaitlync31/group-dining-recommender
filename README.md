# Overview

This project implements a **cloud-based group dining recommendation system** that allows multiple users to input their dining preferences and returns restaurant recommendations that maximize overall group satisfaction.

The recommendation engine uses **vector encoding** and **cosine similarity** to compare aggregated group preferences with restaurant attribute vectors.

## Architecture

The application consists of the following components:

- **Streamlit** – Frontend user interface
- **AWS API Gateway** – REST API endpoints
- **AWS Lambda** – Serverless backend functions
- **Amazon S3** – Restaurant dataset storage
- **Amazon DynamoDB** – Restaurant vector storage

After processing the group's preferences, the system returns the **top three restaurants** that best match the group's interests.

---

# Running the Application

## 1. Install Dependencies

Create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install streamlit requests
```

## 2. Launch the Streamlit Application

```bash
streamlit run app.py
```

## 3. Using the Application

1. Click **Get Started** to call the `/encode-restaurants` endpoint, which converts the restaurant dataset into vector embeddings.
2. Select the **number of users** in the group.
3. Enter each user's dining preferences.
4. Click **Get Recommendations** to call the `/build-group-vector` and `/get-recommendations` endpoints.
5. View the **top three restaurant recommendations** generated based on the group's combined preferences.

---

## Recommendation Workflow

```text
User Preferences
        │
        ▼
Build Group Preference Vector
        │
        ▼
Compare with Restaurant Vectors
(using Cosine Similarity)
        │
        ▼
Rank Restaurants
        │
        ▼
Return Top 3 Recommendations
```