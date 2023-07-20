import cv2
import easyocr
import matplotlib.pyplot as plt
import base64
image = cv2.imread('sample1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
min_contour_area = 1000
table_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
reader = easyocr.Reader(['en'])
for table_contour in table_contours:
    x, y, w, h = cv2.boundingRect(table_contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Crop the table region from the image
    table_image = image[y:y + h, x:x + w]
    # Perform OCR on the table region
    result = reader.readtext(table_image)
    #print(result)
    # Extract text and confidence for each detection
    for bbox in result:
        text = bbox[1]
        confidence = bbox[2]
        print(text)

# Convert BGR image to RGB for matplotlib display
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the image with bounding boxes
plt.figure(figsize=(10, 10))
plt.imshow(image_rgb)
plt.title('Table Detection')
plt.axis('off')
plt.show()

# Convert BGR image to base64
_, buffer = cv2.imencode('.png', image)
image_base64 = base64.b64encode(buffer).decode('utf-8')