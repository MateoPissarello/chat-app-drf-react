from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializers import ServerSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            description="Filter servers by category name",
            type=OpenApiTypes.STR,
            required=False,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="qty",
            description="Limit the number of results",
            type=OpenApiTypes.INT,
            required=False,
            location=OpenApiParameter.QUERY,

        ),
        OpenApiParameter(
            name="by_user",
            description="Filter servers based on the requesting user's ID",
            type=OpenApiTypes.BOOL,
            required=False,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="by_serverid",
            description="Filter servers by server ID",
            type=OpenApiTypes.INT,
            required=False,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="with_num_members",
            description="Include the number of members in the response",
            type=OpenApiTypes.BOOL,
            required=False,
            location=OpenApiParameter.QUERY,
        ),
    ],

)
