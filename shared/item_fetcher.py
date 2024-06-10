from gql_client import GraphQLClient, PaginationQueryResult
from typing import Dict, Any, Set, List, Optional
import logging


class ItemFetcher:
    def __init__(self, client: GraphQLClient, query_by_dbids: str, query_by_cursor: str) -> None:
        self.graphql_client = client
        self.query_by_dbids = query_by_dbids
        self.query_by_cursor = query_by_cursor

    def fetch_items_by_ids(self, db_ids: List[str], first: int = 10000, add_values) -> PaginationQueryResult:
        if not db_ids:
            return []
        
        variables = {"first": first, "dbIdList": db_ids}
        return self._execute_paginated_query(self.query_by_dbids, variables)

    def fetch_all_items_after_cursor(self, after: Optional[str], first: int = 10000) -> PaginationQueryResult:
        variables = {"first": first, "after": after}
        return self._execute_paginated_query(self.query_by_cursor, variables)

    def _execute_paginated_query(self, query: str, variables: Dict[str, Any]) -> PaginationQueryResult:
        try:
            return self.graphql_client.paginate_gql_query(query, variables)
        except Exception as e:
            logging.error(f"Error fetching items: {e}")
            raise