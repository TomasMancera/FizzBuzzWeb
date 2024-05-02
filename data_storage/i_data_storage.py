# data_storage/i_data_storage.py

from abc import ABC, abstractmethod
from typing import List

class IDataStorage(ABC):
    @abstractmethod
    def get_fb_by_number(self, data):
        pass
    
    def get_activate_fb(self,data):
        pass

    @abstractmethod
    def post_fb(self,data):
        pass


    @abstractmethod
    def get_range(self,lower_limit,upper_limit):
        pass

    @abstractmethod
    def update_inactive_data(self, data):
        pass


    @abstractmethod
    def delete_fb(self,data):
        pass
    

