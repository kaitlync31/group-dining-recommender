# Lambda function to recommend  top 3 restaurants by comparing a group preference vector against restaurant vectors stored in DynamoDB.

import json
import boto3
from decimal import Decimal
import math

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("restaurants")


# Convert decimal values to float
def to_float_list(values):
  return [float(v) if isinstance(v, Decimal) else v for v in values]

# Compute cosine similarity between two vectors
def cosine_similarity(a, b):

  dot_product = 0
  for i in range(len(a)):
    dot_product += a[i] * b[i]

  magnitude_a = math.sqrt(sum(x * x for x in a))
  magnitude_b = math.sqrt(sum(x * x for x in b))

  if magnitude_a == 0 or magnitude_b == 0:
    return 0

  return dot_product / (magnitude_a * magnitude_b)


# Lambda handler
def lambda_handler(event, context):

  try:
    print("**Call to recommend restaurants")

    if "body" not in event:
      raise Exception("request has no body")

    body = json.loads(event["body"])

    if "groupVector" not in body:
      raise Exception("request has no key 'groupVector'")

    group_vector = body["groupVector"]

  
    # Get all restaurant vectors from DynamoDB
    print("**Reading restaurant vectors from DynamoDB")

    response = table.scan()
    items = response["Items"]

    # Compute similarity scores
    print("**Computing cosine similarities")

    score_results = []

    for item in items:

      restaurant_name = item["name"]
      restaurant_vector = to_float_list(item["vector"])

      score = cosine_similarity(group_vector, restaurant_vector)

      score_results.append({
        "name": item["name"],
        "cuisine": item.get("cuisine", "N/A"),
        "priceMin": float(item.get("priceMin", "N/A")),
        "priceMax": float(item.get("priceMax", "N/A")),
        "distance": float(item.get("distance", "N/A")),
        "score": score
    })


    # Sort descending by score and take top 3
    score_results.sort(key=lambda x: x["score"], reverse=True)
    top_3_restaurants = score_results[:3]

    print("**Responding to client")

    body = {
      "message": "success",
      "data": top_3_restaurants
    }

    return {
      "statusCode": 200,
      "body": json.dumps(body)
    }

  # Exception handling
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