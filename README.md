# Serverless Notes API

A beginner-friendly serverless CRUD API built with Amazon API Gateway, AWS Lambda, and Amazon DynamoDB. Create, list, retrieve, and delete notes through HTTP endpoints.

## Architecture

```text
Client → API Gateway HTTP API → AWS Lambda (Python) → Amazon DynamoDB
```

## API routes

| Method | Path | Description |
|---|---|---|
| `POST` | `/notes` | Create a note |
| `GET` | `/notes` | List notes |
| `GET` | `/notes/{id}` | Retrieve one note |
| `DELETE` | `/notes/{id}` | Delete a note |

Each note has an automatically generated `id` and `createdAt` timestamp, plus its `title` and `content`.

## Files

```text
.
├── src/
│   └── lambda_function.py
└── template.yaml
```

`template.yaml` defines the API Gateway HTTP API, Lambda function, DynamoDB table, and the function's table access permissions.

## Deploy with AWS SAM

### Prerequisites

- AWS account and configured AWS credentials
- AWS CLI
- AWS SAM CLI

From this project folder, run:

```bash
sam build
sam deploy --guided
```

Choose a stack name such as `serverless-notes-api`, select your AWS Region, and allow SAM to create the required IAM role. When deployment completes, SAM prints the `NotesApiUrl` output. The table uses DynamoDB on-demand billing (`PAY_PER_REQUEST`); check AWS pricing for your Region before deploying.

The API is publicly reachable by default. Add authentication before using it with private or production data.

## Test the API

Set the URL printed after deployment. In PowerShell:

```powershell
$API_URL = "https://your-api-id.execute-api.your-region.amazonaws.com"
```

In macOS/Linux:

```bash
export API_URL="https://your-api-id.execute-api.your-region.amazonaws.com"
```

Create a note:

```bash
curl -X POST "$API_URL/notes" \
  -H "Content-Type: application/json" \
  -d '{"title":"AWS practice","content":"Learn API Gateway and Lambda"}'
```

PowerShell alternative:

```powershell
Invoke-RestMethod -Method Post -Uri "$API_URL/notes" `
  -ContentType "application/json" `
  -Body '{"title":"AWS practice","content":"Learn API Gateway and Lambda"}'
```

Copy the `id` from the create response. Then list notes:

```bash
curl "$API_URL/notes"
```

Get one note:

```bash
curl "$API_URL/notes/NOTE_ID"
```

Delete one note:

```bash
curl -X DELETE "$API_URL/notes/NOTE_ID"
```

Replace `NOTE_ID` with the ID returned by the create request. You can also send these requests with Postman.

## Status codes

- `201` — note created
- `200` — request succeeded
- `400` — invalid JSON or missing title/content
- `404` — route or note not found
- `500` — unexpected server-side error

## Cleanup

From the project folder, run:

```bash
sam delete
```

Confirm the stack name and Region. This deletes the stack resources, including the API, Lambda function, DynamoDB table, and notes stored in that table.

## Notes

- The list endpoint uses DynamoDB `Scan`, suitable for a small demo. Larger datasets should use pagination and a query-friendly table design.
- CORS is configured permissively for simple demos. Restrict allowed origins and add authentication before production use.
- Never commit AWS credentials, account-specific configuration, or a live API URL.

## License

MIT. See [LICENSE](LICENSE).
