import requests

def invoke_chute():
	api_token = "$CHUTES_API_TOKEN"  # Replace with your actual API token

	headers = {
		"Authorization": "Bearer " + api_token,
        "Content-Type": "application/json"
	}
	
	body =     {
      "fps": 24,
      "seed": 42,
      "shift": 8,
      "prompt": "example-string",
      "ar_step": 0,
      "num_frames": 97,
      "resolution": "540P",
      "img_b64_last": null,
      "inference_steps": 30,
      "negative_prompt": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走"
    }

	response = requests.post(
		"https://kikakkz-skyreels-v2-14b-540p.chutes.ai/image2video",
		headers=headers,
		json=body
	)

	# Print status code and response
	print(f"Status code: {response.status_code}")
	print(response.json())

invoke_chute()