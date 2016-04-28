# -*- coding: utf-8 -*-
import heuristic.utils as utils

class Customer:
    
    def __init__(self, c_id, window_start, window_end):
        self.c_id = c_id
        self.window_start = window_start
        self.window_end = window_end
        self.time_visited = None
        
    def get_id(self):
        return self.c_id
        
    def get_window_start(self):
        return self.window_start
        
    def get_window_end(self):
        return self.window_end
        
    def get_time_visited(self):
        return self.time_visited
        
    def set_time_visited(self, time_visited):
        if not isinstance(time_visited, int):
           utils.raise_value_error("time_visited", int, type(time_visited))
        
        self.time_visited = time_visited
    
    def is_valid(self):
        if self.get_time_visited() is None:
            raise ValueError("time_visited not setted yet")
        
        return self.get_window_start() <= self.get_time_visited() and \
                self.get_window_end() >= self.get_time_visited()
    
    def __str__(self):
        return "Customer {0}. Window: {1}-{2}. Visited at {3}".format(
                    self.get_id(), 
                    self.get_window_start(), 
                    self.get_window_end(), 
                    self.get_time_visited())