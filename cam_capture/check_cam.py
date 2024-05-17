import cv2
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

            # Display the frame
    cv2.imshow('Camera Stream', frame)

            # Check for exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        # Release the capture
cap.release()
cv2.destroyAllWindows()