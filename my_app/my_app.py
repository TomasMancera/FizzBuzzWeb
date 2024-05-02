from data_storage.db_storage import DBStorage
from problem_solver.fizzbuzz import FizzBuzz


class MyApp:
    def __init__(self) -> None:
        self.db = DBStorage()
        self.fizzbuzz = FizzBuzz()
    
    def get_number(self, number):
        query = self.db.get_activate_fb(number)
        result = self.db.get_fb_by_number(number)

        if query is None:  
            return "Not Found", 404
        else:
            return f'{number} is {result[0]}', 200 
            
            
        
    def post_number(self,number):
        data = {'number': number, 'result': self.fizzbuzz.calc_one_fb(number)}
        active_result = self.db.get_activate_fb(number)
        query = self.db.get_fb_by_number(data.get("number"))

        if active_result is None:
            if query is None:
                self.db.post_fb(data)
                return f'{number}, {self.fizzbuzz.calc_one_fb(number)}',201
            else:
                self.db.update_inactive_data(number)
                return f'{number} is {query[0]}',200
        else:
            return f'{number} is {query[0]}',409
            
        
    def get_range(self,lower_limit,upper_limit):
        query = self.db.get_range(lower_limit,upper_limit)

        if lower_limit > upper_limit:
            return "Error in the definition of limits",400
        
        else:
            if len(query) == 0:
                return "Not found",404
            else:
                nums = {}
                for row in query:
                    nums[str(row[1])] = row[2]
                return nums,200
            
    def delete_data(self,number):
        query = self.db.get_activate_fb(number)
        if query is None:
            return "Not Found",404
        else:
            self.db.delete_fb(number)
            return "No content",204


