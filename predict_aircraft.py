from ultralytics import YOLO
from pathlib import Path

# Load the newly trained aircraft model
model = YOLO(
    r"D:\AviationSAR\runs\detect\aircraft_detector_clean\weights\best.pt"
)

# Validation image folder
image_folder = Path(
    r"D:\AviationSAR\dataset\aircraft\DOTAv1\images\val"
)

print("\nSearching for an image with aircraft detection...\n")

found = False

for image_path in image_folder.glob("*.jpg"):

    results = model.predict(
        source=str(image_path),
        conf=0.10,
        verbose=False
    )

    result = results[0]

    if result.boxes is not None and len(result.boxes) > 0:

        print("==========================================")
        print("AIRCRAFT DETECTION FOUND")
        print("==========================================")
        print(f"Image      : {image_path}")
        print(f"Aircraft   : {len(result.boxes)}")

        for i, box in enumerate(result.boxes):
            confidence = float(box.conf[0])
            coordinates = box.xyxy[0].tolist()

            print(f"\nAircraft {i + 1}")
            print(f"Confidence : {confidence * 100:.2f}%")
            print(f"Bounding Box : {coordinates}")

        # Save detected image
        result.save(
            filename="aircraft_detection_demo.jpg"
        )

        print("\nDemo image saved as:")
        print("aircraft_detection_demo.jpg")

        found = True
        break

if not found:
    print("==========================================")
    print("NO AIRCRAFT DETECTION FOUND")
    print("==========================================")