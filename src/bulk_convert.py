import os
import subprocess
import argparse

def convert_jxr_to_jxl(input_path, output_path):
    """
    Converts an HDR JXR image to JXL while preserving HDR data.
    
    Args:
        input_path (str): Path to the input JXR file.
        output_path (str): Path to save the converted JXL file.
    """
    temp_hdr_path = input_path.replace(".jxr", ".exr")  # Temporary EXR file

    try:
        # Step 1: Convert JXR to EXR using ffmpeg
        print(f"Converting {input_path} to EXR...")
        ffmpeg_command = [
            "bin\\ffmpeg.exe",  # Hardcoded Windows binary path
            "-i", input_path,   # Input JXR file
            "-pix_fmt", "rgb48le",  # High bit depth for HDR
            temp_hdr_path       # Temporary EXR file
        ]
        subprocess.run(ffmpeg_command, check=True)

        # Step 2: Convert EXR to JXL using cjxl
        print(f"Converting {temp_hdr_path} to JXL...")
        cjxl_command = [
            "bin\\cjxl.exe",    # Hardcoded Windows binary path
            temp_hdr_path,      # Input EXR file
            output_path,        # Output JXL file
            "--effort=9",       # Maximum compression effort
            "--distance=1.0"    # High quality
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

def process_folder(input_folder, output_folder):
    """
    Processes all JXR files in a folder and converts them to JXL.
    
    Args:
        input_folder (str): Path to the folder containing JXR files.
        output_folder (str): Path to save the converted JXL files.
    """
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jxr"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".jxr", ".jxl"))
            convert_jxr_to_jxl(input_path, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch convert JXR images to JXL with HDR support (Windows only).")
    parser.add_argument("input_folder", help="Folder containing JXR files to convert.")
    parser.add_argument("output_folder", help="Folder to save the converted JXL files.")

    args = parser.parse_args()
    process_folder(args.input_folder, args.output_folder)

