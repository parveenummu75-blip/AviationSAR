import os
import glob
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


# ==========================================
# STEP 1: LOAD TRAINED MODEL
# ==========================================

model = load_model("satellite_terrain_model.h5")

print("Model loaded successfully!")


# ==========================================
# STEP 2: CLASS NAMES
# ==========================================

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


# ==========================================
# STEP 3: FIND SATELLITE IMAGES
# ==========================================

image_extensions = ["*.jpg", "*.jpeg", "*.png"]

images = []

for ext in image_extensions:

    images.extend(
        glob.glob(
            os.path.join(
                "dataset",
                "satellite",
                "**",
                ext
            ),
            recursive=True
        )
    )


# ==========================================
# STEP 4: CHECK IMAGES
# ==========================================

if len(images) == 0:

    print("No satellite images found!")

    exit()


print("Total images found:", len(images))


# ==========================================
# STEP 5: TEST ONE IMAGE FROM EACH CLASS
# ==========================================

for class_name in class_names:

    # Find images belonging to this class
    class_images = []

    for img_path in images:

        if os.path.basename(os.path.dirname(img_path)) == class_name:
            class_images.append(img_path)

    # Check whether images exist
    if len(class_images) == 0:
        print("\nNo image found for:", class_name)
        continue

    # Select first image
    img_path = class_images[0]

    print("\nTesting image:")
    print(img_path)

    # ==========================================
    # LOAD IMAGE
    # ==========================================

    img = image.load_img(
        img_path,
        target_size=(64, 64)
    )

    # Convert image to array
    img_array = image.img_to_array(img)

    # Normalize
    img_array = img_array / 255.0

    # Add batch dimension
    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    # ==========================================
    # PREDICTION
    # ==========================================

    prediction = model.predict(
        img_array,
        verbose=0
    )

    predicted_class = np.argmax(
        prediction[0]
    )

    confidence = (
        prediction[0][predicted_class] * 100
    )

    # ==========================================
    # DISPLAY RESULT
    # ==========================================

    print("------------------------------------")
    print("Actual Class     :", class_name)
    print("Predicted Class  :", class_names[predicted_class])
    print("Confidence       :", round(confidence, 2), "%")
    print("------------------------------------")

print("\nTesting image:")
print(img_path)


# ==========================================
# STEP 6: LOAD IMAGE
# ==========================================

img = image.load_img(
    img_path,
    target_size=(64, 64)
)


# ==========================================
# STEP 7: CONVERT IMAGE TO ARRAY
# ==========================================

img_array = image.img_to_array(img)


# ==========================================
# STEP 8: NORMALIZE IMAGE
# ==========================================

img_array = img_array / 255.0


# ==========================================
# STEP 9: ADD BATCH DIMENSION
# ==========================================

img_array = np.expand_dims(
    img_array,
    axis=0
)


# ==========================================
# STEP 10: PREDICT
# ==========================================

prediction = model.predict(
    img_array,
    verbose=0
)


# ==========================================
# STEP 11: FIND PREDICTED CLASS
# ==========================================

predicted_class = np.argmax(
    prediction[0]
)


# ==========================================
# STEP 12: FIND CONFIDENCE
# ==========================================

confidence = (
    prediction[0][predicted_class] * 100
)


# ==========================================
# STEP 13: DISPLAY RESULT
# ==========================================

print("\n====================================")
print("     SATELLITE TERRAIN PREDICTION")
print("====================================")

print(
    "Predicted Terrain :",
    class_names[predicted_class]
)

print(
    "Confidence        :",
    round(confidence, 2),
    "%"
)

print("====================================")