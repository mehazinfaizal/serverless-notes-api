import json
import os
import uuid
from datetime import datetime, timezone

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "Notes")
table = boto3.resource("dynamodb").Table(TABLE_NAME)


def response(status_code, payload):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(payload),
    }


def lambda_handler(event, context):
    http = event.get("requestContext", {}).get("http", {})
    method = http.get("method", "")
    path = event.get("rawPath", "").rstrip("/") or "/"
    note_id = (event.get("pathParameters") or {}).get("id")

    try:
        if method == "POST" and path == "/notes":
            return create_note(event)
        if method == "GET" and path == "/notes":
            return list_notes()
        if method == "GET" and note_id:
            return get_note(note_id)
        if method == "DELETE" and note_id:
            return delete_note(note_id)
        return response(404, {"message": "Route not found"})
    except Exception as exc:
        print(f"Request failed: {type(exc).__name__}: {exc}")
        return response(500, {"message": "Internal server error"})


def create_note(event):
    try:
        body = json.loads(event.get("body") or "{}")
    except (TypeError, json.JSONDecodeError):
        return response(400, {"message": "Request body must be valid JSON"})

    title = body.get("title") if isinstance(body, dict) else None
    content = body.get("content") if isinstance(body, dict) else None
    if not isinstance(title, str) or not title.strip():
        return response(400, {"message": "title is required"})
    if not isinstance(content, str) or not content.strip():
        return response(400, {"message": "content is required"})

    note = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "content": content.strip(),
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=note)
    return response(201, note)


def list_notes():
    result = table.scan()
    return response(200, {"notes": result.get("Items", [])})


def get_note(note_id):
    result = table.get_item(Key={"id": note_id})
    note = result.get("Item")
    if not note:
        return response(404, {"message": "Note not found"})
    return response(200, note)


def delete_note(note_id):
    result = table.get_item(Key={"id": note_id})
    if not result.get("Item"):
        return response(404, {"message": "Note not found"})
    table.delete_item(Key={"id": note_id})
    return response(200, {"message": "Note deleted", "id": note_id})
