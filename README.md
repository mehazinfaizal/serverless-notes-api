# Serverless Notes API

A simple API project for creating and managing notes, built with AWS API Gateway, AWS Lambda, and Amazon DynamoDB.

## Tools used

- **Amazon API Gateway** - receives API requests
- **AWS Lambda** - runs the API code
- **Amazon DynamoDB** - stores the notes
- **Python** - used to write the Lambda function
- **Postman** - used to test the API

## API endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/notes` | Create a note |
| `GET` | `/notes` | List all notes |
| `GET` | `/notes/{id}` | Get a note by ID |
| `DELETE` | `/notes/{id}` | Delete a note by ID |

## Create a note (Example)

Send a `POST` request to `/notes` with this JSON body:

```json
{
  "title": "My first note",
  "content": "I built an API using AWS"
}
