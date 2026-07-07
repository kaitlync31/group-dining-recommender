# Lambda function to encode user preferences into vectors and aggregate them into a single group preference vector.

import json

# cuisine list 
all_cuisines = [
  "Italian",
  "Korean",
  "Mexican",
  "Japanese",
  "American"
]


# Convert each user's preferences into a vector
def user_to_vector(user):

  cuisine_vector = []

  for cuisine in all_cuisines:
    if cuisine in user["cuisines"]:
      cuisine_vector.append(1)
    else:
      cuisine_vector.append(0)

  min_price = 10
  max_price = 100
  budget_mid = (user["budgetMin"] + user["budgetMax"]) / 2

  budget_normalized = (budget_mid - min_price) / (max_price - min_price)
  distance_normalized = 1  # closer is better
  rating_normalized = 1 # 5 stars is best

  return cuisine_vector + [
    budget_normalized,
    distance_normalized,
    rating_normalized
  ]


# Average each users' vectors into a group preference vector
def average_vectors(vectors):

  vector_length = len(vectors[0])
  avg = [0] * vector_length

  for v in vectors:
    for i in range(vector_length):
      avg[i] += v[i]

  return [x / len(vectors) for x in avg]


# Lambda handler
def lambda_handler(event, context):

  try:
    print("**Call to build group vector")

    if "body" not in event:
      raise Exception("request has no body")

    body = json.loads(event["body"])

    if "groupPreferences" not in body:
      raise Exception("request has no key 'groupPreferences'")

    user_preferences = body["groupPreferences"]

    # Convert users to vectors
    user_vectors = []

    for user in user_preferences:
      v = user_to_vector(user)
      user_vectors.append(v)

    # Compute group vector
    group_vector = average_vectors(user_vectors)

    body = {
      "message": "success",
      "data": {
        "groupVector": group_vector
      }
    }

    return {
      "statusCode": 200,
      "body": json.dumps(body)
    }

  except Exception as e:

    print("**Exception")
    print("**Message:", str(e))

    body = {
      "message": str(e),
      "data": []
    }

    if str(e).startswith("request has no"):
      return {
        "statusCode": 400,
        "body": json.dumps(body)
      }
    else:
      return {
        "statusCode": 500,
        "body": json.dumps(body)
      }