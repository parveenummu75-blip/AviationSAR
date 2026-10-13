import os
import csv
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
# STEP 3: TEST CSV PATH
# ==========================================

test_csv = "dataset/satellite/EuroSAT/test.csv"


if not os.path.exists(test_csv):

    print("ERROR: test.csv not found!")

    exit()


print("Test CSV found!")


# ==========================================
# STEP 4: FIND ALL SATELLITE IMAGES
# ==========================================

image_extensions = ["*.jpg", "*.jpeg", "*.png"]

all_images = []

for ext in image_extensions:

    all_images.extend(
        glob.glob(
            os.path.join(
                "dataset",
                "satellite",
                "EuroSAT",
                "**",
                ext
            ),
            recursive=True
        )
    )


print("Total images found:", len(all_images))


# ==========================================
# STEP 5: CREATE IMAGE LOOKUP
# ==========================================

image_lookup = {}

for img_path in all_images:

    filename = os.path.basename(img_path)

    filename_without_extension = os.path.splitext(
        filename
    )[0]

    image_lookup[filename] = img_path

    image_lookup[filename_without_extension] = img_path


# ==========================================
# STEP 6: READ TEST CSV
# ==========================================

test_records = []

with open(
    test_csv,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        test_records.append(row)


print("Test images listed in CSV:", len(test_records))


# ==========================================
# STEP 7: TEST MODEL
# ==========================================

correct = 0
total = 0
missing = 0


print("\nStarting test...\n")


for row in test_records:

    filename = row["Filename"].strip()

    actual_class = row["ClassName"].strip()


    # --------------------------------------
    # Find image
    # --------------------------------------

    img_path = None

    # Direct filename search
    if filename in image_lookup:

        img_path = image_lookup[filename]

    else:

        # Remove possible folder path
        base_filename = os.path.basename(filename)

        if base_filename in image_lookup:

            img_path = image_lookup[base_filename]

        else:

            # Remove extension
            name_without_extension = os.path.splitext(
                base_filename
            )[0]

            if name_without_extension in image_lookup:

                img_path = image_lookup[
                    name_without_extension
                ]


    # --------------------------------------
    # Image not found
    # --------------------------------------

    if img_path is None:

        missing += 1

        continue


    # --------------------------------------
    # Load image
    # --------------------------------------

    img = image.load_img(
        img_path,
        target_size=(64, 64)
    )


    # --------------------------------------
    # Convert to array
    # --------------------------------------

    img_array = image.img_to_array(img)


    # --------------------------------------
    # Normalize
    # --------------------------------------

    img_array = img_array / 255.0


    # --------------------------------------
    # Add batch dimension
    # --------------------------------------

    img_array = np.expand_dims(
        img_array,
        axis=0
    )


    # --------------------------------------
    # Prediction
    # --------------------------------------

    prediction = model.predict(
        img_array,
        verbose=0
    )


    predicted_index = np.argmax(
        prediction[0]
    )

    predicted_class = class_names[
        predicted_index
    ]


    # --------------------------------------
    # Compare prediction
    # --------------------------------------

    if predicted_class == actual_class:

        correct += 1


    total += 1


    # --------------------------------------
    # Show progress
    # --------------------------------------

    if total % 100 == 0:

        print(
            "Tested:",
            total,
            "| Correct:",
            correct
        )


# ==========================================
# STEP 8: CALCULATE ACCURACY
# ==========================================

if total > 0:

    accuracy = (
        correct / total
    ) * 100

else:

    accuracy = 0


# ==========================================
# STEP 9: DISPLAY FINAL RESULT
# ==========================================

print("\n==========================================")
print("       SATELLITE MODEL TEST RESULT")
print("==========================================")

print("Total test images :", total)
print("Correct predictions:", correct)
print("Wrong predictions  :", total - correct)
print("Missing images     :", missing)

print(
    "Test Accuracy      :",
    round(accuracy, 2),
    "%"
)

print("==========================================")