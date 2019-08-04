"""
Module for schema validation
"""
from abc import abstractmethod
from marshmallow import Schema, post_load, fields


class DictSchema(Schema):
    """
    Schema that serializes into a dictionary. turns on strict validation by default.
    """
    def __init__(self, strict=True, **kwargs):
        super(DictSchema, self).__init__(strict=strict, **kwargs)


class ObjectSchema(DictSchema):
    """
    Schema that serializes into a python object. Turns on strict validation by default.
    _object_class should return the class to construct with the data. Each field will
    be passed to the constructor as kwargs.
    """
    @property
    @abstractmethod
    def _object_class(self):
        pass

    @post_load
    def _construct_object(self, data, **_kwargs):
        return self._object_class(*data)


class JsonApiSchema(DictSchema):
    """
    Schema for simple API responses
    """
    msg = fields.Str()


JSON_CT = {'Content-Type': 'application/json; charset=utf-8'}

BAD_REQUEST_JSON_RESPONSE = {
    'msg': 'Bad Request'
}, 400, JSON_CT

INTERNAL_SERVER_ERROR_JSON_RESPONSE = {
    'msg': 'Internal server error'
}, 500, JSON_CT


def ok_response(msg):
    """
    Create OK JsonApiSchema compliant response with status code 200 and JSON Content-type.
    :param str msg: Human readable API response status.
    :return: Tuple of JsonApiSchema compliant dict, http status code, and http headers.
    :rtype: tuple[dict, int, dict]
    """
    return {
        'msg': msg
    }, 200, JSON_CT
