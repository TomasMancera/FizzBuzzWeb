# Module docstring

from data_storage.db_storage import DBStorage
from problem_solver.fizzbuzz import FizzBuzz

class MyApp:
    """Application class that integrates database storage with fizzbuzz problem solving."""

    def __init__(self):
        """Initializes the application with database storage and fizzbuzz logic components."""
        self.db_storage = DBStorage()
        self.fizzbuzz = FizzBuzz()

    def get_number(self, number):
        """Retrieves the fizzbuzz result for a given number, with status handling."""
        query = self.db_storage.get_activate_fb(number)
        result = self.db_storage.get_fb_by_number(number)
        if query is None:  
            return "Not Found", 404
        return f'{number} is {result[0]}', 200 

    def post_number(self, number):
        """Posts a number to the database and handles fizzbuzz calculation and activation status."""
        data = {'number': number, 'result': self.fizzbuzz.calc_one_fb(number)}
        active_result = self.db_storage.get_activate_fb(number)
        query = self.db_storage.get_fb_by_number(data.get("number"))
        if active_result is None:
            if query is None:
                self.db_storage.post_fb(data)
                return f'{number}, {self.fizzbuzz.calc_one_fb(number)}', 201
            self.db_storage.update_inactive_data(number)
            return f'{number} is {query[0]}', 200
        return f'{number} is {query[0]}', 409

    def get_range(self, lower_limit, upper_limit):
        """Retrieves a range of fizzbuzz records, handling errors and empty responses."""
        if lower_limit > upper_limit:
            return "Error in the definition of limits", 400
        query = self.db_storage.get_range(lower_limit, upper_limit)
        if not query:
            return "Not found", 404
        nums = {str(row[1]): row[2] for row in query}
        return nums, 200

    def delete_data(self, number):
        """Deletes or deactivates a fizzbuzz record based on its activation status."""
        query = self.db_storage.get_activate_fb(number)
        if query is None:
            return "Not Found", 404
        self.db_storage.delete_fb(number)
        return "No content, inactive", 204
    
    def hard_delete_data(self,number):
        query = self.db_storage.get_number(number)
        if query[0] is None:
            return "Not Found", 404
        self.db_storage.hard_delete_fb(number)
        return "No content-hard delete", 204