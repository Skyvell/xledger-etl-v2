from typing import List, Dict, Any, Optional
import logging
from delta_fetcher import DeltaFetcher
from item_fetcher import ItemFetcher
from configuration_manager import ConfigurationManager


class ChangedItemsResult:
    def __init__(self, items: List[Dict[str, Any]], last_deltas_cursor: str):
        self.items = items
        self.last_deltas_cursor = last_deltas_cursor


# This one will also have a data lake writer class.
class DataSynchronizer:
    def __init__(self, 
                 synchronizer_name: str, 
                 delta_fetcher: DeltaFetcher, 
                 item_fetcher: ItemFetcher,
                 config_manager: ConfigurationManager) -> None:
        self.synchronizer_name = synchronizer_name
        self.delta_fetcher = delta_fetcher
        self.item_fetcher = item_fetcher
        self.config_manager = config_manager

        # These should be fetched from configuration manager.
        self.deltas_cursor = None

    def synchronize(self) -> None:
        try:
            if self.config_manager.get('initial_sync_complete', True):
                changed_items = self.fetch_changed_items()
                self.process_and_store(changed_items, "deltas_cursor")
            else:
                all_items = self.fetch_all_items()
                self.process_and_store(all_items, "initial_sync_cursor")
                self.config_manager.set('initial_sync_complete', True)
        except Exception as e:
            logging.error(f"Error in synchronization: {e}")
            raise

    def fetch_changed_items(self) -> ChangedItemsResult:
        # Fetch all deltas since last deltas sync cursor.
        deltas_result = self.delta_fetcher.fetch_deltas(
            {"first": 10000, "after": self.config_manager.get('deltas_cursor')})
        
        # If no new changes, return empty list.
        if not deltas_result.has_changes():
            ChangedItemsResult([], None)

        # Fetch all changed items.
        all_changed_items = []
        if deltas_result.has_additions():
            all_changed_items.extend(self.item_fetcher.fetch_items_by_ids(deltas_result.get_additions(), "ADDED"))
        
        if deltas_result.has_updates():
            all_changed_items.extend(self.item_fetcher.fetch_items_by_ids(deltas_result.get_updates(), "UPDATED"))

        if deltas_result.has_deletions():
            all_changed_items.extend({"dbIDd"}deltas_result.)  # Corrected

        return all_changed_items

    def fetch_all_items(self) -> List[Dict[str, Any]]:
        query_results = self.item_fetcher.fetch_all_items(
            self.config_manager.get('initial_sync_cursor'))
        return self.add_mutation_type(query_results.get_nodes(), "ADDED")

    def process_and_store(self, items: List[Dict[str, Any]], cursor_key: str) -> None:
        try:
            logging.debug(f"Processing and storing items: {items}")
            # Update cursor after successful write
            self.update_cursor_position(cursor_key, items[-1]["cursor"] if items else None)
        except Exception as e:
            logging.error(f"Error processing and storing items: {e}")
            raise

    def update_cursor_position(self, cursor_key: str, cursor_value: Optional[str]) -> None:
        if cursor_value:
            self.config_manager.set(cursor_key, cursor_value)
            logging.debug(f"Updated cursor {cursor_key} to {cursor_value}")

    def add_mutation_type(self, nodes: List[Dict[str, Any]], mutation_type: str) -> List[Dict[str, Any]]:
        for node in nodes:
            node["mutationType"] = mutation_type
        return nodes
