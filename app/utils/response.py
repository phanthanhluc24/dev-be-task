from datetime import datetime
from fastapi.responses import JSONResponse


def serialize_data(data: any) -> any:
    """
    Serialize different types of data to JSON-compatible format.

    Args:
        data (Any): The data to be serialized.

    Returns:
        Any: Serialized data.
    """
    if hasattr(data, "__dict__"):
        data_dict: dict[str, any] = data.__dict__
        data = {k: v for k, v in data_dict.items() if not k.startswith("_")}
        return serialize_data(data)
    elif isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, (list, tuple)):
        return [serialize_data(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, (str, int, float, bool, type(None))):
        return data
    else:
        return str(data)


def response_success(data=None, message="Success"):
    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": message, "data": serialize_data(data)},
    )


def response_created(data=None, message="Created"):
    return JSONResponse(
        status_code=201,
        content={"status": "success", "message": message, "data": serialize_data(data)},
    )


def response_fail(message="Failed", status_code=400):
    return JSONResponse(
        status_code=status_code, content={"status": "fail", "message": message}
    )


def response_error(message="Server Error", status_code=500):
    return JSONResponse(
        status_code=status_code, content={"status": "error", "message": message}
    )
