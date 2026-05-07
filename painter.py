from datetime import datetime
from config import IMAGE_OUTPUT_DIR
from services import describe_image_for_generation, download_generated_image


def generate_image_with_dalle(prompt):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = IMAGE_OUTPUT_DIR / f"generated_image_{timestamp}.png"

    IMAGE_OUTPUT_DIR.mkdir(exist_ok=True)
    image_bytes = download_generated_image(prompt)

    with open(filename, "wb") as f:
        f.write(image_bytes.getbuffer())

    return str(filename)


def gemini_vision_with_local_file(image_path, prompt):
    return describe_image_for_generation(image_path, prompt)

def generate_image(image_path, prompt):

    img_based_prompt = gemini_vision_with_local_file(image_path, prompt)
    filename = generate_image_with_dalle(img_based_prompt)

    return filename
















