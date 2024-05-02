from typing import List
from .i_problem_solver import IProblemSolver


class FizzBuzz(IProblemSolver):

  def compute_results(self, data: List) -> List:
      result = []
      line = ""
      for element in data:
          line =  self.__fizz_buzz(int(element))
          result.append(element + " " +line)
      return result

  def calc_one_fb(self,data: any) -> any:
     return self.__fizz_buzz(int(data))

  def __fizz_buzz(self,number: int) -> str:      
      result = str(number)
      fizz_flag = False
      
      if number % 3 == 0:
        result = "Fizz"
        fizz_flag = True

      if number % 5 == 0:
        if fizz_flag:
          result += "Buzz"
          return result
        result = "Buzz"
        
      return result