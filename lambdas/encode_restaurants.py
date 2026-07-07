# Lambda function to encode restaurant data into vectors and store them in DynamoDB.

import json
import boto3
from decimal import Decimal


# AWS clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("restaurants")


# cuisine list
all_cuisines = [
    "Italian",
    "Korean",
    "Mexican",
    "Japanese",
    "American"
]


# Convert restaurant into vector
def restaurant_to_vector(restaurant):
    cuisine_vector = []
    for cuisine in all_cuisines:
        if restaurant["cuisine"] == cuisine:
            cuisine_vector.append(1)
        else:
            cuisine_vector.append(0)

    min_price = 10
    max_price = 100
    mid_price = (restaurant["priceMin"] + restaurant["priceMax"]) / 2

    price_normalized = (mid_price - min_price) / (max_price - min_price)
    distance_normalized = 1 / (1 + restaurant["distance"])
    rating_normalized = restaurant["rating"] / 5

    return cuisine_vector + [
        price_normalized,
        distance_normalized,
        rating_normalized
    ]


# Lambda handler
def lambda_handler(event, context):

    try:
        print("**Call to encode restaurants")

        if "body" not in event:
            raise Exception("request has no body")

        body = json.loads(event["body"])

        if "bucket" not in body:
            raise Exception("request has no key 'bucket'")

        if "key" not in body:
            raise Exception("request has no key 'key'")

        bucket = body["bucket"]
        key = body["key"]

        # Read restaurant dataset from S3
        print("**Reading restaurants from S3")

        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        file_content = response["Body"].read().decode("utf-8")
        restaurants = json.loads(file_content)

        # Encode restaurants and store in DynamoDB
        print("**Encoding restaurants")

        processed = []

        for r in restaurants:
            vector = restaurant_to_vector(r)
            vector_decimal = [Decimal(str(x)) for x in vector]

            table.put_item(
                Item={
                    "name": r["name"],
                    "cuisine": r["cuisine"],
                    "priceMin": Decimal(str(r["priceMin"])),
                    "priceMax": Decimal(str(r["priceMax"])),
                    "distance": Decimal(str(r["distance"])),
                    "rating": Decimal(str(r["rating"])),
                    "vector": vector_decimal
                }
            )

            processed.append({
                "name": r["name"]
            })

        body = {
            "message": "success",
            "data": processed
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