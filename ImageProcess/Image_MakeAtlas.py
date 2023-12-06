import os
import random
from PIL import Image

def resize_image(img, size=(256, 256)):
    return img.resize(size)

def create_collage(images, collage_size, tile_size=(256, 256)):
    collage = Image.new("RGB", (collage_size[1] * tile_size[1], collage_size[0] * tile_size[0]))

    used_images = set()

    for row in range(collage_size[0]):
        for col in range(collage_size[1]):
            while True:
                img = random.choice(images)
                if img not in used_images:
                    used_images.add(img)
                    break

            img = Image.open(img)
            img = resize_image(img, tile_size)
            collage.paste(img, (col * tile_size[1], row * tile_size[0]))

    return collage

def save_collage(collage, output_folder, counter, collage_size):
    # Format the counter with leading zeros
    counter_str = f"{counter:06d}"
    
    # Construct the output filename with collage size information
    output_filename = f"collage_{counter_str}_{collage_size[0]}x{collage_size[1]}.png"
    output_path = os.path.join(output_folder, output_filename)

    # Save the collage
    collage.save(output_path)

    print(f"Collage saved to: {output_path}")

if __name__ == "__main__":
    input_folder = r"D:\ImageCenter\slied2\shipLike\out"
    output_folder = os.path.join(input_folder, "out")

    images = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith(".png")]

    # Specify the collage size for each iteration
    collage_size = (2, 2)  # You can manually adjust this to your desired collage size

    # Counter for numbering collages
    counter = 0

    # Generate and save collages
    while images:
        current_images = images[:collage_size[0] * collage_size[1]]
        collage = create_collage(current_images, collage_size)
        save_collage(collage, output_folder, counter, collage_size)
        counter += 1
        images = images[collage_size[0] * collage_size[1]:]
