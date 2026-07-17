import random

FALLBACK_GEM = ("grey", 1, 1, {}, [])

class GemBag:
    def __init__(self, composition, gem_data):
        self.composition = composition
        self.gem_data = gem_data
        self.bag = []
        self._fill()

    def _fill(self):
        self.bag = []
        for tier_key, gem_counts in self.composition.items():
            tier = int(tier_key.split("_")[1])
            for gem_type, count in gem_counts.items():
                self.bag.extend([(gem_type, tier)] * count)
        random.shuffle(self.bag)

    def draw(self):
        if not self.bag:
            return FALLBACK_GEM

        gem_type, tier = self.bag.pop()
        star = 1
        gem_entry = self.gem_data[gem_type][f"tier_{tier}"][f"star_{star}"]
        return (gem_type, tier, star, gem_entry["stats"], gem_entry["abilities"])

    def is_empty(self):
        return len(self.bag) == 0