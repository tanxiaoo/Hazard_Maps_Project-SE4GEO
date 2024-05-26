import os
import requests

# Define file URL and local save path
url = 'https://test.idrogeo.isprambiente.it/api/pir/italia'
local_filename = 'italia_pir.csv'
save_path = os.path.join(os.path.dirname(__file__), '../data/raw', local_filename)

# Create saving directory
os.makedirs(os.path.dirname(save_path), exist_ok=True)


def fetch_data(url, save_path):
    """
    Download file and save it to the specified path
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"File saved to: {save_path}")
    else:
        print(f"Download failed, status code: {response.status_code}")


if __name__ == "__main__":
    fetch_data(url, save_path)
