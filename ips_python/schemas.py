from marshmallow import Schema, fields, validate


class IATIQuery(Schema):
    search_method = fields.String(
        required=True, validate=validate.OneOf(["cosine", "elastic", "embeddings"])
    )
    query = fields.String(required=True,)


class IATIResult(Schema):
    iati_identifier = fields.String(required=True)
    reporting_org = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    processed_description = fields.String(required=False)


class IATIQueryResponse(IATIQuery):
    timestamp = fields.String(required=True)
    # TODO: implement versioning feature
    # version = fields.String(required=True)
    processed_query = fields.String(required=False)
    results = fields.List(fields.Nested(IATIResult))
