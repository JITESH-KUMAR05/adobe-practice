import cv2
import numpy as np

def detect_shapes(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edge map
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        shape = detect_shape(contour)
        # Draw the contour and label the shape
        M = cv2.moments(contour)
        if M["m00"] > 0:
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))
        else:
            continue
        
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Save the output image to a file
    output_path = 'image2_output.jpg'
    cv2.imwrite(output_path, image)
    print(f"Output image saved to {output_path}")

def detect_shape(contour):
    shape = "unidentified"
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    
    # If the shape has 3 vertices, it is a triangle
    if len(approx) == 3:
        shape = "triangle"
    # If the shape has 4 vertices, it is either a square or a rectangle
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    # If the shape has 5 vertices, it is a pentagon
    elif len(approx) == 5:
        shape = "pentagon"
    # If the shape has more than 5 vertices, we consider it to be a circle or an ellipse
    else:
        (x, y), (MA, ma), angle = cv2.fitEllipse(contour)
        if np.abs(MA - ma) < 0.1 * max(MA, ma):
            shape = "circle"
        else:
            shape = "ellipse"
    
    return shape

# Example usage
image_path = 'image2.jpg'
detect_shapes(image_path)