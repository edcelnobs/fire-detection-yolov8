from ultralytics import YOLO
import cv2

# ---------------- LOAD MODEL ----------------
model = YOLO("best_nano_111.pt")

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found")
    exit()

print("✅ Camera started... Press 'q' to exit.")

# ---------------- LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO inference
    results = model.predict(
        source=frame,
        conf=0.35,
        iou=0.1,
        imgsz=640,
        verbose=False
    )

    detected = False
    annotated_frame = frame

    # Process results
    for r in results:
        boxes = r.boxes
        if boxes is not None and len(boxes) > 0:
            detected = True

        annotated_frame = r.plot()

    # ---------------- STATUS OUTPUT ----------------
    if detected:
        print("🔥 Fire/Smoke Detected!")
    else:
        print("✅ No detection")

    # ---------------- DISPLAY ----------------
    cv2.imshow("YOLO Fire Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()
