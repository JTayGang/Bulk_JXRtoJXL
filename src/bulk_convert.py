import os
import subprocess

def convert_jxr_to_jxl(input_path, output_path):
    """
    Converts an HDR JXR image to JXL while preserving HDR data.
    
    Args:
        input_path (str): Path to the input JXR file.
        output_path (str): Path to save the converted JXL file.
    """
    temp_hdr_path = input_path.replace(".jxr", ".exr")  # Temporary HDR format

    try:
        # Step 1: Convert JXR to HDR (EXR) using ffmpeg
        print(f"Converting {input_path} to EXR...")
        ffmpeg_command = [
            "ffmpeg", 
            "-i", input_path,  # Input JXR file
            "-pix_fmt", "rgb48le",  # Ensure high bit depth
            temp_hdr_path  # Temporary EXR file
        ]
        subprocess.run(ffmpeg_command, check=True)

        # Step 2: Convert EXR to JXL using cjxl
        print(f"Converting {temp_hdr_path} to JXL...")
        cjxl_command = [
            "cjxl",
            temp_hdr_path,  # Input EXR file
            output_path,  # Output JXL file
            "--effort=9",  # Maximum compression effort
            "--distance=1.0"  # High quality
        ]
        subprocess.run(cjxl_command, check=True)

        print(f"Conversion complete: {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up temporary EXR file
        if os.path.exists(temp_hdr_path):
            os.remove(temp_hdr_path)
            print(f"Deleted temporary file: {temp_hdr_path}")

# Example usage
input_jxr = "example.jxr"  # Replace with your JXR file path
output_jxl = "example.jxl"  # Replace with desired JXL output path
convert_jxr_to_jxl(input_jxr, output_jxl)
