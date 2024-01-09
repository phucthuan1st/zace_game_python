import random

def generate_random_name():
        # Define lists of possible characters for various name segments
        name_starts = ["Ace", "Blitz", "Comet", "Eagle", "Fang", "Fury", "Ghost", "Hawk", "Inferno", "Jagged", "Kaboom", "Lightning", "Maverick", "Nova", "Phoenix", "Reaper", "Shadow", "Spectre", "Thunder", "Viper", "Whiz"]
        name_mids = ["blade", "bolt", "claw", "crash", "dash", "fire", "fist", "gear", "hammer", "howl", "jag", "jet", "knuckle", "lash", "mane", "mask", "quake", "rage", "spark", "storm", "strike", "thunder"]
        name_ends = ["13", "37", "42", "66", "88", "99", "X7", "XP", "ZX", "Δ", "Ω", "!", "&", "#", "-", "_"]

        # Choose random elements from each list to combine into a name
        name_start = random.choice(name_starts)
        name_mid = random.choice(name_mids)
        name_end = random.choice(name_ends)

        # Generate and return the final name
        return f"{name_start}_{name_mid}_{name_end}"