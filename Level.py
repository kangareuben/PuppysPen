# python
import random

class Level:
    
    # Runs on creation of a level
    def __init__(self, _difficulty, _perimeter_level=False, _area_level=False, _grid_size=(6, 6)):
        self.difficulty = _difficulty
        self.perimeter_level = _perimeter_level
        self.area_level = _area_level
        self.grid_size = _grid_size
        
        if _perimeter_level == _area_level == False:
            # Throw exception
        elif _area_level == False:
            self.generate_perimeter_level()
        elif _perimeter_level == False:
            self.generate_area_level()
        else:
            self.generate_both_level()
    
    # Generates a random perimeter for this puzzle
    def generate_perimeter_level(self):
        # Get a random even integer between 4 and the
        # maximum perimeter for the grid size
        _perimeter = random.randrange(2, (self.grid_size[0] + self.grid_size[1] + 1)) * 2
        
        return _perimeter
    
    # Generates a random area for this puzzle
    def generate_area_level(self):
        _possible_areas = []
        
        # Check all possible combinations of width and height
        # Only add products greater than 3, and only add them once
        for x in range(1, self.grid_size[0]):
            for y in range(1, self.grid_size[1]):
                _product = x * y
                if _product > 3 and _product not in _possible_areas:
                    _possible_areas.append(_product)
        
        # Get a random index within the number of possible areas
        _random_index = random.randrange(len(_possible_areas))
        
        return _possible_areas[_random_index]
        
    # Generates a compatible set of perimeter and area for this puzzle
    def generate_both_level(self):
        _area = generate_area_level()
        _perimeters = find_perimeters_from_area(_area)
        
        # Get a random index within the number of possible perimeters
        _random_index = random.randrange(len(_perimeters))
        
        _perimeter = _perimeters[_random_index]
        
        return (_area, _perimeter)
        
    # Find all possible factors given an area
    def find_factors_from_area(self, _area):
        _factors = []
        
        if(_area < 1):
            return _factors
        
        # 1 is always a factor
        _factors.append(1)
        
        # Find factors between 2 and area/2 (inclusive)
        for x in range(2, _area / 2 + 1):
            _potential_factor = float(area) / float(x)
            if _potential_factor % 1 == 0:
                _factors.append(_potential_factor)
        
        # The only factor that can be above area/2 is area itself
        _factors.append(_area)
        
        # Remove factors that won't fit on the grid
        # Loop backward to avoid deletion errors
        for x in range(len(_factors) - 1, -1, -1):
            if _factors[x] > self.grid_size[0] and _factors[x] > self.grid_size[1]:
                _factors.remove(_factors[x])
                _factors.remove(_area / _factors[x])
                
                # Deleted two factors, so have to decrement x to compensate
                x--
                
            # Reaching a factor that isn't too big means removal is done,
            # as you're looping through highest to lowest
            else:
                break
        
        return _factors
    
    # Find all possible perimeters given a list of factors
    def find_perimeters_from_factors(self, _factors):
        _perimeters = []
        
        # Pairs are (0, length-1), (1, length-2), etc.
        _bottom = 0
        _top = len(_factors) - 1
        
        while (_top - _bottom) > 1:
            # Get pair of corresponding values
            _bottom_value = _factors[_bottom]
            _top_value = _factors[_top]
            
            # Perimeter formula
            _perimeter = (2 * _bottom_value) + (2 * _top_value)
            _perimeters.append(_perimeter)
            
            # Next pair
            _bottom++
            _top--
        
        return _perimeters
    
    # Find all possible perimeters given an area
    def find_perimeters_from_area(self, _area):
        _factors = find_factors_from_area(_area)
        _perimeters = find_perimeters_from_factors(_factors)
        
        return _perimeters