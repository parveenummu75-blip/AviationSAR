import os
import glob
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load trained satellite model
model = load_model("satellite_terrain_model.h5")

# Class names
class_names = [
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Pasture",
    "PermanentCrop",
    "Residential",
    "River",
    "SeaLake"
]

# Find satellite images
image_extensions = ["*.jpg", "*.jpeg", "*.png"]

images = []

for ext in image_extensions:
    images.extend(
        glob.glob(os.path.join("dataset", "satellite", "**", ext), recursive=True)
    )

if len(images) == 0:
    print("No satellite images found!")
    exit()

# Select first image
img_path = images[0]

print("\nTesting image:")
print(img_path)

# Load image
img = image.load_img(img_path, target_size=(64, 64))
img_array = image.img_to_array(img)

# Normalize
img_array = img_array / 255.0

# Add batch dimension
img_array = np.expand_dims(img_array, axis=0)

# Prediction
prediction = model.predict(img_array, verbose=0)

predicted_class = np.argmax(prediction[0])
confidence = prediction[0][predicted_class] * 100

print("\n========== SATELLITE PREDICTION ==========")
print("Predicted Terrain :", class_names[predicted_class])
print("Confidence        :", round(confidence, 2), "%")
print("==========================================")
# Select first image
img_path = images[0]

print("\nTesting image:")
print(img_path)

# Load image
img = image.load_img(img_path, target_size=(64, 64))
img_array = image.img_to_array(img)

# Normalize
img_array = img_array / 255.0

# Add batch dimension
img_array = np.expand_dims(img_array, axis=0)

# Prediction
prediction = model.predict(img_array, verbose=0)

predicted_class = np.argmax(prediction[0])
confidence = prediction[0][predicted_class] * 100

print("\n==============================")
print("SATELLITE TERRAIN PREDICTION")
print("==============================")
print("Predicted Class :", class_names[predicted_class])
print("Confidence      :", round(confidence, 2), "%")
print("==============================")