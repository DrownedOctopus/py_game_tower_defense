import json

class Level:
    def __init__(self, game):
        self.name = None
        self.waves = []
        self.starting_towers = []
        self.starting_gems = []
        self.current_wave = None
        self.game = game
        self.level_data = None
        self.wave_length = 14  # if I make this too short, we could run into an issue with not spawning enough
        self.spawn_delay = None
        self.remaining_spawns = 0
        self.waves_finished = False
        self.map = None
        self.monster_spawn_pos = None
        self.base_pos = None
        self.elapsed_in_wave = 0.0
        self.elapsed_since_spawn = 0.0

    def load(self, path):
        try:
            with open(path, 'r') as f:
                self.level_data = json.load(f)
        except FileNotFoundError:
            print(f"Level file not found: {path}")
        except json.JSONDecodeError as e:
            print(f"Level file is malformed: {e}")
        except PermissionError:
            print(f"Permission denied when loading level: {path}")       
        
    def start(self):
        self.unlocks = self.level_data.get('unlocks', [])
        self.name = self.level_data['name']
        self.waves = self.level_data['waves']
        self.starting_towers = self.level_data['starting_towers']
        self.starting_gems = self.level_data['starting_gems']
        self.map = self.level_data['map']
        self.waves_finished = False
        self.game.level_ended = False
        self.monster_spawn_pos = self.level_data['monster_spawn_pos']
        self.base_pos = self.level_data['base_pos']
        self.current_wave = 0
        self.game.pause()
        self.start_wave()
        self.elapsed_since_spawn = 0.0
        
    def on_start_playing(self):
        self.elapsed_in_wave = 0.0
        self.elapsed_since_spawn = self.spawn_delay + 1.0

    def start_wave(self):
        self.spawn_delay = self.wave_length / int(self.waves[self.current_wave][0])
        self.remaining_spawns = int(self.waves[self.current_wave][0])
        self.elapsed_since_spawn = self.spawn_delay

    def update(self):        
        if self.waves_finished:
            return
        dt = self.game.dt        
        self.elapsed_in_wave += dt
        self.elapsed_since_spawn += dt

        if not self.waves_finished:
            if self.elapsed_in_wave >= self.wave_length:
                if self.current_wave + 1 >= len(self.waves):
                    self.waves_finished = True
                    return
                self.current_wave += 1
                self.game.current_wave = self.current_wave
                self.start_wave()
                self.elapsed_in_wave = 0.0

            if self.elapsed_since_spawn >= self.spawn_delay:
                if self.remaining_spawns == 0:
                    return
                self.game.spawn_monsters(self.waves[self.current_wave][1])
                self.elapsed_since_spawn = 0.0
                self.remaining_spawns -= 1