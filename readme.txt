This is to test a basic fastAPI application.

We will test basic CRUD operations and
also validation using pydantic.

To start api server with stripe run the following command:

export STRIPE_SECRET_KEY="sk_test_51TAH3PE7rYRx0IKgQmToO1TXIvqELPEg3HktCd8BhDCZul3zhRZCHCFMTD3HEU0FpTFQKPkga7HDjfWX3ek5QHv000ynfxx16o"
echo $STRIPE_SECRET_KEY
uvicorn main:app --reload
