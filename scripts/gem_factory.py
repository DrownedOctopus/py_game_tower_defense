import json

from scripts.gem import Gem

class GemFactory:
    
    def __init__(self, game):
        self.game = game
        self.gem_data = None
        
    def load(self, path):
        try:
            with open(path, 'r') as f:
                self.gem_data = json.load(f)
        except FileNotFoundError:
            print(f"Gem data file not found: {path}")
        except json.JSONDecodeError as e:
            print(f"Gem data file is malformed: {e}")    
        
    def build_gem(self, gem_type, tier, star, tower, surf) -> Gem:
        "Factory that creates Gems"
        if self.gem_data is None:
            raise RuntimeError("GemFactory.load() must be called before build_gem()")
        
        gem_config = self.gem_data[gem_type][f"tier_{tier}"][f"star_{star}"] 
               
        gem_stats = gem_config["stats"]
        gem_abilities = gem_config["abilities"]
        
        return Gem(gem_type, tier, star, gem_stats, gem_abilities, tower, surf, self.game)