from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport


# Idea: create subclasses of this client and inlude the queries in tue subclients.
class GraphQLClient:
    def __init__(self, api_endpoint: str, api_key: str):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.client = self._create_client()

    def _create_client(self):
        headers = {"Authorization": f"token {self.api_key}"}
        transport = AIOHTTPTransport(url=self.api_endpoint, headers=headers)
        return Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=60)

    def execute_graphql_query(self, query, variables=None):
        try:
            return self.client.execute(query, variable_values=variables)
        except Exception as e:
            # Handle or log the exception as needed
            raise Exception(f"An error occurred: {str(e)}")