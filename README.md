##Overview##

This project implements a cloud-based group dining recommendation system that allows a group of users to input dining preferences and returns restaurant recommendations that maximize overall group satisfaction.
The recommendation algorithm uses vector encoding and cosine similarity to compare group preferences with restaurant attributes.

The app consists of:
- Streamlit frontend 
- AWS API Gateway 
- AWS Lambda functions 
- S3 (restaurant dataset storage)
- DynamoDB (restaurant vector storage)

The system returns the top 3 restaurants that best match the group’s preferences.

##Running the Application##

1. Install dependencies

Create a virtual environment and install required packages:

python3 -m venv venv
source venv/bin/activate
pip install streamlit requests

2. Run the Streamlit UI

streamlit run app.py

3. Using the Application

1) Click "Get Started" to call the endpoint /encode-restaurants, which encodes the restaurant data into vectors. 
2) Select number of users, and enter dining preferences for each user in the group.
3) Click "Get Recommendations" to call the endpoints /build-group-vector and /get-recommendations. 
4) Then, the top 3 recommended restaurants are displayed.
