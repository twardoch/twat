import requests

def invoke_chute():
	api_token = "$CHUTES_API_TOKEN"  # Replace with your actual API token

	headers = {
		"Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
	}
	
	body =     {
      "fps": 16,
      "steps": 25,
      "frames": 81,
      "prompt": "example-string",
      "single_frame": False,
      "guidance_scale": 5,
      "last_image_b64": "example-string",
      "first_image_b64": "example-string"
    }

	response = requests.post(
		"https://kikakkz-wan2-1-14b-flf2v.chutes.ai/flf2video",
		headers=headers,
		json=body
	)

	# Print status code and response
	print(f"Status code: {response.status_code}")
	print(response.json())

invoke_chute()