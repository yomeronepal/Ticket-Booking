from flask import jsonify


def handle_validation_error(error):
    """
    Handles Pydantic ValidationError and formats it for Flask responses.
    """
    formatted_errors = []
    for err in error.errors():
        ctx = (
            {k: str(v) for k, v in err.get("ctx", {}).items()}
            if err.get("ctx")
            else None
        )
        message = ctx.get("error") if ctx else err.get("msg")
        formatted_errors.append(
            {
                "type": err.get("type"),
                "loc": err.get("loc"),
                "msg": message,
                "input": err.get("input"),
            }
        )
    return jsonify({"errors": formatted_errors}), 400


def handle_value_error(error):
    response = {
        "error": "ValueError",
        "message": str(error),
    }
    return jsonify(response), 400
