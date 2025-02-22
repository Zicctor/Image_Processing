import sys
import cv2 as cv

def resize_with_aspect_ratio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    
    # If both width and height are None, return original image
    if width is None and height is None:
        return image
    
    # If width is None, calculate width from height maintaining aspect ratio
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    # If height is None, calculate height from width maintaining aspect ratio
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    
    # Resize the image
    return cv.resize(image, dim, interpolation=inter)

def main(argv):
    # [variables]
    # Declare the variables we are going to use
    ddepth = cv.CV_16S
    kernel_size = 3
    window_name = "Laplace Demo"
    max_width = 800  # Maximum width for display
    # [variables]
    
    # [load]
    imageName = argv[0] if len(argv) > 0 else '../data/lotus.jpg'
    
    src = cv.imread(cv.samples.findFile(imageName), cv.IMREAD_COLOR) # load an image
    
    # Check if image is loaded fine
    if src is None:
        print('Error opening image')
        print('Program Arguments: [image_name -- default lotus.jpg]')
        return -1
    
    # [resize]
    # Resize image to a reasonable size for display
    src = resize_with_aspect_ratio(src, width=max_width)
    # [resize]
    
    # [reduce_noise]
    # Remove noise by blurring with a Gaussian filter
    src = cv.GaussianBlur(src, (3,3), 0)
    # [reduce_noise]
    
    # [convert_to_gray]
    # Convert the image to grayscale
    src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # [convert_to_gray]
    
    # Create window
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    
    # [laplacian]
    # Apply Laplace function
    dst = cv.Laplacian(src_gray, ddepth, ksize=kernel_size)
    # [laplacian]
    
    # [convert]
    # converting back to uint8
    abs_dst = cv.convertScaleAbs(dst)
    # [convert]
    
    # [display]
    cv.imshow(window_name, abs_dst)
    cv.waitKey(0)
    cv.destroyAllWindows()  # Added to properly close windows
    # [display]
    
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])