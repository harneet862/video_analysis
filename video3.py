import cv2 
import numpy as np

# Initialize video capture from the uploaded video file
video_path = "/home/harneetk/projects/def-olav/harneetk/Video_analysis/Videos09-05-2024/video05_09-06-2024.mp4"  # Change this to your video file path
cap = cv2.VideoCapture(video_path)

# Kernel for morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

count = 0
fps = cap.get(cv2.CAP_PROP_FPS)
skip_frame = int(3 * 60 * fps)  # Skip the first 3 minutes of video

bee_ids = {}
bee_count = 0

# Define interaction areas
# Define interaction areas based on the provided ranges
interaction_areas = {
    'A1f': [(0, 320, 1350, 1500)],  # Combined A1f, A2f
    'A1e': [(300, 630, 1350, 1550)],  # Combined A1e, A2e
    'B1f': [(0, 320, 1200, 1350)],  # Combined B1f, B2f
    'B1e': [(300, 630, 1200, 1350)],  # Combined B1e, B2e
    'C1f': [(0, 320, 1050, 1200)],  # Combined C1f, C2f
    'C1e': [(300, 630, 1050, 1200)],  # Combined C1e, C2e
    'D1e': [(300, 630, 900, 1050)],  # Combined D1e, D2e
    'D1f': [(0, 320, 900, 1050)],  # Combined D1f, D2f
    'E1e': [(300, 630, 750, 900)],  # Combined E1e, E2e
    'E1f': [(0, 320, 750, 900)],  # Combined E1f, E2f
    'F1f': [(0, 320, 600, 750)],  # Combined F1f, F2f
    'F1e': [(320, 630, 600, 750)],  # Combined F1e, F2e
    'G1f': [(0, 320, 450, 600)],  # Combined G1f, G2f
    'G1e': [(320, 630, 450, 600)],  # Combined G1e, G2e
    'H1f': [(0, 320, 300, 450)],  # Combined H1f, H2f
    'H1e': [(320, 630, 300, 450)],  # Combined H1e, H2e
    'I1e': [(320, 630, 150, 300)],  # Combined I1e, I2e
    'I1f': [(0, 320, 150, 300)],  # Combined I1f, I2f
    'J1f': [(0, 320, 0, 150)],  # Combined J1f, J2f
    'J1e': [(320, 630, 0, 150)],  # Combined J1e, J2e
}


# Function to check if a bee is in a defined area
def is_in_area(bee_position, area):
    x, y = bee_position
    for (x1, x2, y1, y2) in area:
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False

# Dictionary to store interaction counts for each area
interaction_counts = {key: 0 for key in interaction_areas}

total_frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = frame[150:800, 100:1630] 

    if count < skip_frame:
        count += 1
        continue

    # Preprocess the frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    lower_black = 0
    upper_black = 75
    binary_mask = cv2.inRange(blurred_frame, lower_black, upper_black)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:40]

    current_bees = []  # Store current detected bees

    total_frame_count += 1
    for contour in contours:
        if cv2.contourArea(contour) > 30:  # Minimum area threshold
            # Calculate centroid
            M = cv2.moments(contour)
            if M["m00"] != 0:  # Avoid division by zero
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                current_bees.append((cX, cY))

                # Assign ID to each bee
                if bee_count < 40:
                    bee_ids[bee_count + 1] = (cX, cY)  # Assign ID starting from 1
                    bee_count += 1

                # Draw bounding box and circle for centroid
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cX, cY), 4, (255, 0, 0), -1)  # Draw centroid as a blue dot

    # Check for interactions in defined areas
    for area_key, area in interaction_areas.items():
        bees_in_area = [bee for bee in current_bees if is_in_area(bee, area)]
        n = len(bees_in_area)
        
        # Count interactions
        for i in range(n):
            for j in range(i + 1, n):
                distance = np.linalg.norm(np.array(bees_in_area[i]) - np.array(bees_in_area[j]))
                if distance < 100:  # Adjust this threshold based on your criteria
                    cv2.line(frame, bees_in_area[i], bees_in_area[j], (0, 0, 255), 2)
                    interaction_counts[area_key] += 1
                    #print(f"interaction detected in {area_key}")

    # Save the frame with detected bees
    #cv2.imwrite(f"Detected_Bees_{total_frame_count}.jpg", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Output detected bee IDs and their positions
print("Detected Bees and their IDs:")
for bee_id, position in bee_ids.items():
    print(f"Bee {bee_id}: Position {position}")

# Output interaction counts for each area
print("Interaction counts for each area:")
for area_key, interaction_count in interaction_counts.items():
    probability_of_interaction = interaction_count / total_frame_count
    print(f"Area {area_key}: {interaction_count} interactions in {total_frame_count} frames, {probability_of_interaction:.4f}")
