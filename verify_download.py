import urllib.request
import json

def verify_download():
    url = "http://127.0.0.1:5000/api/download"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                print(f"Successfully downloaded {len(data)} entries.")
                if len(data) > 0:
                    first_entry = data[0]
                    required_keys = ["device_id", "timestamp", "aqi", "pm25", "temperature", "humidity", "oxygen", "latitude", "longitude", "power", "status"]
                    missing_keys = [key for key in required_keys if key not in first_entry]
                    if not missing_keys:
                        print("Verification PASSED: All required keys present.")
                        print(json.dumps(first_entry, indent=2))
                    else:
                        print(f"Verification FAILED: Missing keys: {missing_keys}")
            else:
                print(f"Verification FAILED: Status code {response.status}")
    except Exception as e:
        print(f"Verification FAILED: {str(e)}")

if __name__ == "__main__":
    verify_download()

if __name__ == "__main__":
    verify_download()
