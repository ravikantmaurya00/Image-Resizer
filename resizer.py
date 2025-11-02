import os
from PIL import Image

def resize_images(input_folder, output_folder, width=None, height=None, max_dimension=None, format=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)

            # Maintain aspect ratio if only one dimension is provided
            orig_width, orig_height = img.size
            if max_dimension:
                if orig_width > orig_height:
                    new_width = max_dimension
                    new_height = int((max_dimension / orig_width) * orig_height)
                else:
                    new_height = max_dimension
                    new_width = int((max_dimension / orig_height) * orig_width)
            else:
                new_width = width if width else orig_width
                new_height = height if height else orig_height

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # Convert format if requested
            file_name, ext = os.path.splitext(filename)
            new_format = format.upper() if format else img.format
            new_ext = f".{new_format.lower()}"
            output_path = os.path.join(output_folder, file_name + new_ext)

            # Save image
            if new_format in ["JPEG", "JPG"]:
                resized_img = resized_img.convert("RGB")
                resized_img.save(output_path, new_format, quality=90)
            else:
                resized_img.save(output_path, new_format)

            print(f"✅ {filename} resized and saved as {output_path}")

def main():
    print("🖼️  IMAGE RESIZER TOOL (Interactive Mode)")
    input_folder = input("📂 Enter input folder path: ").strip('"')
    output_folder = input("💾 Enter output folder path: ").strip('"')

    # Ask user for resizing options
    choice = input("Do you want to set max dimension (y/n)? ").lower()
    max_dimension = None
    width = None
    height = None
    if choice == 'y':
        max_dimension = int(input("Enter maximum dimension (e.g. 800): "))
    else:
        w = input("Enter width (press Enter to skip): ")
        h = input("Enter height (press Enter to skip): ")
        width = int(w) if w else None
        height = int(h) if h else None

    # Ask for format conversion
    format = input("Enter output format (JPEG, PNG, WEBP, etc.) or press Enter to keep same: ").strip().upper()
    format = format if format else None

    resize_images(input_folder, output_folder, width, height, max_dimension, format)
    print("\n🎉 All images processed successfully!")

if __name__ == "__main__":
    main()
