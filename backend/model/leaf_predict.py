import random

def predict_leaf_disease(filename: str):
    # Simulate prediction based on keywords in the filename
    if "spot" in filename.lower():
        return "Tomato_Bacterial_spot", round(random.uniform(0.85, 0.98), 2)
    elif "yellow" in filename.lower():
        return "Tomato_Early_blight", round(random.uniform(0.82, 0.95), 2)
    elif "mold" in filename.lower():
        return "Tomato_Leaf_Mold", round(random.uniform(0.85, 0.97), 2)
    elif "late" in filename.lower():
        return "Tomato_Late_blight", round(random.uniform(0.84, 0.96), 2)
    else:
        return "Tomato_Healthy", round(random.uniform(0.92, 0.99), 2)
