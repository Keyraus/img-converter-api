import ffmpeg

def compress_to_jpegxl(input_path, output_path):
    ffmpeg.input(input_path).output(output_path, vcodec='libjxl').run()

if __name__ == "__main__":
    input_image_path = "./input.jpg"  # Replace with your input image path
    output_image_path = "output.jxl"  # Replace with your desired output image path

    compress_to_jpegxl(input_image_path, output_image_path)
    