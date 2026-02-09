import requests
import base64


def test_gen():
    """Test the image generation endpoint locally."""
    url = "http://localhost:8000/generate_image"
    prompt = {"prompt": "A cute dragon"}
    try:
        res = requests.post(url, json=prompt)
        res.raise_for_status()
        data = res.json()
        if "image_base64" in data and len(data["image_base64"]) > 100:
            print("SUCCESS: Image generated.")
            with open("test_output.png", "wb") as f:
                f.write(base64.b64decode(data["image_base64"]))
            print("Saved to test_output.png")
        else:
            print("FAILURE: No image data returned.")
            print(data)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_gen()
