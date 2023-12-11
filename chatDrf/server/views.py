# Import necessary modules from Django and REST framework
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

# Import the Server model and its serializer
from .models import Server
from .schema import server_list_docs
from .serializers import ServerSerializer


# Define a custom ViewSet for the Server model
@server_list_docs
class ServerListViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling server list views.

    This ViewSet provides functionality for retrieving a list of servers based on various query parameters.
    The list view supports GET requests and allows filtering servers by category, user, server ID,
    and number of members.

    Query Parameters:
    - category: Filter servers by category name.
    - qty: Limit the number of results returned.
    - by_user: Filter servers based on the requesting user's ID.
    - by_serverid: Filter servers by server ID.
    - with_num_members: Include the number of members in the response.

    Raises:
    - AuthenticationFailed: If the request requires user authentication but the user is not authenticated.
    - ValidationError: If the server with the specified ID is not found or if an invalid server ID is provided.

    Returns:
    - Response: A serialized representation of the server queryset based on the provided query parameters.
    """
    # Set the initial queryset and serializer class for the ViewSet
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    # Define the list view for handling GET requests
    def list(self, request):
        # Retrieve query parameters from the request
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == "true"
        by_serverid = request.query_params.get('by_serverid')
        with_num_members = request.query_params.get('with_num_members') == "true"
        # Check authentication for queries involving user information

        # Apply filters based on query parameters
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if request.user.is_authenticated:
                # Filter servers based on the requesting user's ID
                user_id = request.user.id
                self.queryset = self.queryset.filter(members=user_id)
            else:
                raise AuthenticationFailed()

        if with_num_members:
            # Annotate queryset with the number of members if specified
            self.queryset = self.queryset.annotate(num_members=Count("members"))

        if qty:
            # Limit the number of results if a quantity is specified
            self.queryset = self.queryset[:int(qty)]

        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                # Attempt to filter servers by server ID
                self.queryset = self.queryset.filter(id=by_serverid)
                # Raise an error if the server with the specified ID is not found
                if not self.queryset:
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                # Raise an error for invalid server ID values
                raise ValidationError(detail="Server value error")

        # Serialize the queryset using the ServerSerializer
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        # Return the serialized data in the response
        return Response(serializer.data)
