from sqlalchemy.orm import Session
from math import ceil
from flask import jsonify

from ..pydantic.schemas import PaginationSchema


def get_paginated_response(query, request, schema):
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))

    # Fetch total items and calculate pagination
    total_items = query.count()
    total_pages = ceil(total_items / page_size)
    offset = (page - 1) * page_size

    # Fetch items with pagination
    items = query.offset(offset).limit(page_size).all()

    # Dynamically use the schema to serialize the items
    serialized_items = schema(items=items).model_dump()
    response = {
        "items": serialized_items["items"],
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_items": total_items,
    }
    # Construct the paginated response

    # Return the response as JSON
    return jsonify(response)
