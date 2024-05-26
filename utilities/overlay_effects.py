import io
from PIL import Image, ImageFilter, ImageDraw


class OverlayEffectsProcessor:
    def apply_overlay_effects(self, img):
        # Create the base image with a black background
        base_width, base_height = 800, 1000
        base_img = Image.new("RGBA", (base_width, base_height), (0, 0, 0, 255))


        background_layer_width = int(base_width * 0.8)
        background_layer_height = int(base_height * 0.9)
        background_position_x = int(base_width * 0.1)  # 10% margin from the left
        background_position_y = int(base_height * 0.1)  # 10% margin from the top

        background_resized_img = img.resize((background_layer_width, background_layer_height),
                                                     Image.Resampling.LANCZOS)

        # Paste the resized background image onto the base image at the calculated position
        base_img.paste(background_resized_img, (background_position_x, background_position_y), background_resized_img)

        # Apply a blur effect to the background layer only
        blurred_img = base_img.filter(ImageFilter.GaussianBlur(49))

        # Create a semi-transparent overlay
        overlay = Image.new("RGBA", blurred_img.size, (0, 0, 0, 78))

        # Combine the blurred background with the overlay
        blurred_with_overlay_img = Image.alpha_composite(blurred_img, overlay)

        # Calculate the size and position for the unaltered foreground image
        foreground_layer_width = int(base_width * 0.6)
        foreground_layer_height = int(base_height * 0.6)
        foreground_position_x = int(base_width * 0.2)  # 25% margin from the left
        foreground_position_y = int(base_height * 0.2)  # 30% margin from the top

        # Resize the foreground image without altering its clarity
        foreground_resized_img = img.resize((foreground_layer_width, foreground_layer_height),
                                                     Image.Resampling.LANCZOS)

        # Create a new base image to assemble the final image
        final_img = Image.new("RGBA", (base_width, base_height), (0, 0, 0, 255))
        final_img.paste(blurred_with_overlay_img, (0, 0))  # Paste the blurred background with overlay
        final_img.paste(foreground_resized_img, (foreground_position_x, foreground_position_y),
                        foreground_resized_img)  # Overlay the unaltered foreground

        # Create a tea-colored semi-transparent overlay for the top layer
        top_color_overlay = Image.new("RGBA", final_img.size, (255, 255, 255, 20))  # Tea color with 50% transparency
        final_img_with_tea_overlay = Image.alpha_composite(final_img, top_color_overlay)

        return final_img_with_tea_overlay

    def process_image(self, image_path, output_path):
        original_img = Image.open(image_path).convert("RGBA")
        final_img = self.apply_overlay_effects(original_img)
        final_img.save(output_path)

    def process_bytes(self, image_bytes):
        original_img = image_bytes.convert("RGBA")
        final_img = self.apply_overlay_effects(original_img)
        final_img = final_img.convert("RGB")

        buffered = io.BytesIO()
        final_img.save(buffered, format="JPEG")
        return buffered.getvalue()


if __name__ == "__main__":
    # Call the function with the paths to your image and output file
    input_img = "imgs/input.jpg"
    output_path = "results/overlay_effects_output.png"

    processor = OverlayEffectsProcessor()
    processor.process_image(input_img, output_path)
