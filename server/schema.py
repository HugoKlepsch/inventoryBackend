import json
from marshmallow import Schema, post_load, fields


class DictSchema(Schema):
    def __init__(self, strict=True, **kwargs):
        super(Schema, self).__init__(strict=strict, **kwargs)

    class Meta:
        strict = True


class ObjectSchema(DictSchema):
    _object_class = None

    @post_load
    def _construct_object(self, data, **_kwargs):
        return self._object_class(*data)


JSON_CT = {'Content-Type': 'application/json; charset=utf-8'}

BAD_REQUEST_JSON_RESPONSE = json.dumps({
    'msg': 'Bad Request'
}), 400, JSON_CT

INTERNAL_SERVER_ERROR_JSON_RESPONSE = json.dumps({
    'msg': 'Internal server error'
}), 500, JSON_CT


def ok_response(msg):
    return {
        'msg': msg
    }, 200, JSON_CT


class JsonApiSchema(DictSchema):
    msg = fields.Str(required=True)
