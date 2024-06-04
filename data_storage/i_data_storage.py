# data_storage/i_data_storage.py


from abc import ABC, abstractmethod

class IDataStorage(ABC):
    """Abstract base class that specifies data storage methods for FizzBuzz operations."""

    @abstractmethod
    def get_fb_by_number(self, data):
        """Abstract method to retrieve fizzbuzz result by number."""

    @abstractmethod
    def get_activate_fb(self, data):
        """Abstract method to fetch active fizzbuzz record by number."""

    @abstractmethod
    def post_fb(self, data):
        """Abstract method to insert a new fizzbuzz record."""

    @abstractmethod
    def get_range(self, lower_limit, upper_limit):
        """Abstract method to retrieve a range of fizzbuzz records."""

    @abstractmethod
    def update_inactive_data(self, data):
        """Abstract method to update a fizzbuzz record to active status."""

    @abstractmethod
    def delete_fb(self, data):
        """Abstract method to delete (or deactivate) a fizzbuzz record."""
