from rest_framework.schemas.views import SchemaView


class TokenAuth(SchemaView):
    id: str
    exp: str
    sub: str
