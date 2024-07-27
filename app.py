import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

def download_image(url, save_filename):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        save_path = os.path.join(os.getcwd(), save_filename)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully!")
    except ConnectionError:
        print("Error: Connection error occurred while trying to download the image.")
    except Timeout:
        print("Error: The request timed out while trying to download the image.")
    except RequestException as e:
        print(f"Error: An error occurred while trying to download the image: {e}")

# Example usage
image_url = "https://imgs.search.brave.com/Ow9kOLgtSzxd-QN0_qD6yKvzCovMJNhExO68eVR9_Ss/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9oaHNw/cmluZ3MuYml0YnVj/a2V0LmlvL2RvY3Mv/cHJvZ3JhbW1pbmcv/ZXhhbXBsZXMvcHl0/aG9uL1BJTC9faW1h/Z2VzL0ltYWdlRHJh/d19lbGxpcHNlXzAx/LmpwZw"
save_filename = "image2.jpg"
download_image(image_url, save_filename)