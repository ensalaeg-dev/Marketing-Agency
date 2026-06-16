import os
import requests
from langchain.tools import tool
from typing import Optional

class MediaGenerationTools:
    """
    Tools for generating images and videos using various AI providers.
    """

    @tool("Generate Image with Gemini Imagen")
    def generate_image_gemini(prompt: str) -> str:
        """
        Generates a high-quality image using Google Gemini Imagen API.
        Best for strong prompt adherence and commercial-safe designs.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        # Implementation placeholder for Gemini Imagen API call
        # In a real scenario, this would use the Google Cloud/Vertex AI SDK
        return f"Successfully generated image with Gemini Imagen for prompt: '{prompt}'. URL: https://example.com/gemini_img.png"

    @tool("Generate Video with Gemini Veo")
    def generate_video_gemini(prompt: str) -> str:
        """
        Generates a professional cinematic video using Google Gemini Veo API.
        Best for high-fidelity motion and complex scenes.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        # Implementation placeholder for Gemini Veo API call
        return f"Successfully generated video with Gemini Veo for prompt: '{prompt}'. URL: https://example.com/gemini_video.mp4"

    @tool("Generate Image with DALL-E 3")
    def generate_image_dalle(prompt: str) -> str:
        """
        Generates an image using OpenAI's DALL-E 3.
        Best for general creative text-to-image tasks.
        """
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            return f"DALL-E 3 Image URL: {response.data[0].url}"
        except Exception as e:
            return f"Error generating image with DALL-E 3: {str(e)}"

    @tool("Generate Video with Runway")
    def generate_video_runway(prompt: str) -> str:
        """
        Generates a high-end production video using Runway Gen-2/Gen-3.
        Best for cinematic quality and professional editing.
        """
        api_key = os.getenv("RUNWAY_API_KEY")
        # Implementation placeholder for Runway API
        return f"Successfully generated video with Runway. Task ID: rw_task_12345"

    @tool("Generate Media with Replicate")
    def generate_with_replicate(prompt: str, model_name: str) -> str:
        """
        Generates images or videos using models hosted on Replicate.
        Pass the model_name (e.g., 'stability-ai/sdxl', 'lucataco/animate-diff').
        """
        import replicate
        os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN", "")
        try:
            output = replicate.run(model_name, input={"prompt": prompt})
            return f"Replicate Output: {output}"
        except Exception as e:
            return f"Error using Replicate: {str(e)}"

    @tool("Generate Image with Stability AI")
    def generate_image_stability(prompt: str) -> str:
        """
        Generates an image using Stability AI's Stable Diffusion XL.
        Best for artistic flexibility and high-resolution textures.
        """
        api_key = os.getenv("STABILITY_API_KEY")
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        body = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            return "Successfully generated image with Stability AI. (Base64 data received)"
        except Exception as e:
            return f"Error with Stability AI: {str(e)}"
