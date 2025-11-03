def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = app.openapi()

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path_item in openapi_schema.get("paths", {}).values():
        for method in path_item.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema

    return None
