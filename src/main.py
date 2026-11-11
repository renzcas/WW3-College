# src/main.py
from models.world import World

def main():
    world = World()
    world.add_node("usa", {"food": 100.0})
    world.add_node("japan", {"food": 50.0})
    
    world.add_flow("usa", "japan", "food", 5.0)

    print(f"Initial State: {world.nodes}")
    
    for _ in range(3):
        world.step()
        print(f"Tick {world.tick_count}: {world.nodes}")

if __name__ == "__main__":
    main()