import os
import subprocess
from pathlib import Path
import shutil
import re
from datetime import datetime
import logging
import argparse
import platform
import time
from colorama import init, Fore, Style

"""
Inno Setup Unpacker Script v4.20
--------------------------------
Built on innounp by quickener
https://innounp.sourceforge.net/

This script extracts Inno Setup installer files using 'innounp.exe'. It dynamically processes
the files and directories, identifies variants (e.g., x64, ARM64), and copies them into 
architecture-specific output directories.

After processing the script will output a fully built directory for each detected architecture,
as well as the raw extracted setup.

Key Features:
- Automatically handles extraction of setup files using innounp.
- Processes metadata from the .iss script.
- Dynamically detects and categorizes file variants (x64, ARM64, etc.).
- Outputs a structured summary with logging support.

Usage:
1. With file argument:
   python innounpakNrebuild.py --file "inno_setup_file.exe"

2. Without file argument (prompts user):
   python innounpakNrebuild.py

Requirements:
- 'innounp.exe' must be located in the 'bin' directory.
- Python 3.x with the following libraries:
    - os, subprocess, shutil, re, datetime, logging, argparse, platform, colorama

xoxo,
--Whale Linguini
"""

# Initialize colorama
init(autoreset=True)

# Helper function to clear console
def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Helper function to rename files or directories with placeholders
def rename_placeholder(name):
    return name.replace("{", "").replace("}", "")

# Helper function to rename folders and files with placeholders during processing
def rename_extracted_directories(extracted_dir):
    for root, dirs, files in os.walk(extracted_dir):
        for directory in dirs:
            new_dir_name = rename_placeholder(directory)
            if new_dir_name != directory:
                old_path = Path(root) / directory
                new_path = Path(root) / new_dir_name
                shutil.move(str(old_path), str(new_path))
                logging.info(f"Renamed directory {old_path} to {new_path}")
        
        for file in files:
            new_file_name = rename_placeholder(file)
            if new_file_name != file:
                old_path = Path(root) / file
                new_path = Path(root) / new_file_name
                shutil.move(str(old_path), str(new_path))
                logging.info(f"Renamed file {old_path} to {new_path}")

# Helper function to parse metadata from the ISS file
def parse_metadata(iss_content):
    metadata = {}
    metadata_keys = [
        "AppName", "AppVerName", "AppId", "AppVersion",
        "AppPublisher", "AppPublisherURL", "AppSupportURL",
        "AppUpdatesURL", "AppComments"
    ]
    for key in metadata_keys:
        match = re.search(rf'{key}=(.+)', iss_content)
        if match:
            metadata[key] = match.group(1).strip()
    return metadata

# Parse the ISS file to extract source, destination, check conditions, and metadata
def parse_iss_file(iss_file_path):
    files_info = []
    metadata = {}
    variant_arch_mapping = {}

    try:
        # Try reading the file using 'utf-8-sig' and ignoring decoding errors
        with open(iss_file_path, 'r', encoding='utf-8-sig', errors='ignore') as iss_file:
            content = iss_file.read()
    except UnicodeDecodeError as e:
        print(f"Error decoding file: {e}")
        return [], {}, {}

    # Parse metadata from the ISS file
    metadata = parse_metadata(content)

    # Extract the [Files] section
    files_section_match = re.search(r'\[Files\](.*?)\n\n', content, re.DOTALL)
    if files_section_match:
        files_section = files_section_match.group(1)

        # Parse each file entry
        file_pattern = re.compile(
            r'Source:\s*"([^"]+)";\s*DestDir:\s*"([^"]+)";\s*DestName:\s*"([^"]+)";\s*(Check:\s*"([^"]+)";)?')

        for match in file_pattern.finditer(files_section):
            source = match.group(1)
            dest_dir = match.group(2)
            dest_name = match.group(3)
            check = match.group(5)

            files_info.append({
                "source": source,
                "dest_dir": dest_dir,
                "dest_name": dest_name,
                "check": check
            })

            # Map the variant suffix (e.g., 1, 2, 3) to architecture based on the Check condition
            variant_match = re.search(r',(\d)', source)
            if variant_match:
                variant = variant_match.group(1)
                if check == "InstallX64":
                    variant_arch_mapping[variant] = "x64"
                elif check == "InstallARM64":
                    variant_arch_mapping[variant] = "ARM64"
                else:
                    variant_arch_mapping[variant] = "Other"

    return files_info, metadata, variant_arch_mapping


def main():
    clear_console()

    # Setup argparse for command-line options
    parser = argparse.ArgumentParser(description="Inno Setup Unpacker Script")
    parser.add_argument('--file', type=str, help="Path to the Inno Setup file")
    args = parser.parse_args()

    # Initial setup
    script_dir = Path.cwd()

    # Ensure 'bin' directory exists
    bin_dir = script_dir / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    # Path to innounp.exe
    innounp_exe = bin_dir / "innounp.exe"
    print(f"{Fore.YELLOW}Innoup executable path: {innounp_exe}")

    # Ensure innounp.exe exists
    if not innounp_exe.exists():
        print(f"{Fore.RED}Error: {innounp_exe} not found in {bin_dir}.")
        exit()

    # Get the Inno Setup file
    if args.file:
        innosetup_file = Path(args.file)
        print(f"{Fore.CYAN}Inno Setup File: {innosetup_file}")
    else:
        # Prompt the user for the Inno Setup file to unpack
        innosetup_file = Path(input(f"{Fore.CYAN}Inno Setup File: "))

    # Ensure the input file exists
    if not innosetup_file.exists():
        print(f"{Fore.RED}File not found: {innosetup_file}")
        exit()

    # Generate a unique directory name using the input file name and a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_tmp_dir = script_dir / f"tmp_{innosetup_file.stem}_{timestamp}"

    # Setup the logging
    log_file = script_dir / f"log_{innosetup_file.stem}_{timestamp}.log"
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Script started.")
    logging.info(f"Input file: {innosetup_file}")
    
    print(f"{Style.BRIGHT + Fore.GREEN}\n###[ Starting InnoSetup Unpacking Process ]###")
    print(f"---------------------------------------------------")
    time.sleep(1.2)

    # Console output for stage
    print(f"{Fore.GREEN}\n===[ Setting up Environment ]===\n")
    time.sleep(0.7)
    # Ensure the unique tmp directory exists
    unique_tmp_dir.mkdir(parents=True, exist_ok=True)

    # Define the extracted subdir within unique_tmp_dir
    extracted_dir = unique_tmp_dir / f"{innosetup_file.stem}_extracted"
    extracted_dir.mkdir(parents=True, exist_ok=True)

    # Move the input file to the unique tmp directory
    tmp_innosetup_file = unique_tmp_dir / innosetup_file.name
    shutil.move(str(innosetup_file), tmp_innosetup_file)
    logging.info(f"Moved {innosetup_file.name} to {unique_tmp_dir}")
    print(f"{Fore.GREEN}Moved {innosetup_file.name} to {unique_tmp_dir}")
    time.sleep(0.2)

    # Change the working directory to the extracted directory for extraction
    os.chdir(extracted_dir)
    logging.info(f"Working directory changed to {extracted_dir}")
    print(f"{Fore.YELLOW}Working directory set to {extracted_dir}")
    time.sleep(0.2)

    # Console output for stage
    print(f"{Fore.BLUE}\n===[ Extracting Inno Setup ]===\n")
    time.sleep(0.7)
    # Run innounp.exe to unpack the Inno Setup file into the extracted subdir
    subprocess.run([str(innounp_exe), "-x", str(tmp_innosetup_file)], check=True)
    logging.info(f"Extraction completed for {tmp_innosetup_file}")
    print(f"{Fore.GREEN}Initial Extraction Finished")
    time.sleep(1.4)
    
    # Ensure proper renaming of directories and files with placeholders
    rename_extracted_directories(extracted_dir)

    # Change back to the unique_tmp_dir for further processing
    os.chdir(unique_tmp_dir)

    # Initialize common_files to store non-variant files
    common_files = []

    # Console output for stage
    print(f"{Fore.BLUE}\n===[ Parsing ISS File and Processing Files ]===\n")
    time.sleep(0.7)
    # Extracted ISS file path
    iss_file_path = extracted_dir / "install_script.iss"

    # Parse the ISS file and gather file copy details
    files_to_copy, metadata, variant_arch_mapping = parse_iss_file(iss_file_path)  # Get variant_arch_mapping

    # Display found variants and their architecture mapping
    print(f"{Fore.CYAN}\nFound Variants and Architecture Mapping:")
    for variant, arch in variant_arch_mapping.items():
        print(f"{Fore.YELLOW}  Variant {variant} -> {arch}")
    time.sleep(1.7)
    
    print(f"{Fore.BLUE}\n===[ Building Output Directories ]===\n")
    time.sleep(0.7)
    
    # Create architecture-specific output directories based on the parsed ISS file
    output_dirs = {}

    # First, handle files defined in the ISS file
    print(f"{Fore.GREEN}Mapping files detected by arch...")
    time.sleep(0.4)
    for file_info in files_to_copy:
        source_file = extracted_dir / file_info['source'].replace("{app}", "app")
        
        # Determine the architecture and create output directories as needed
        arch = variant_arch_mapping.get(re.search(r',(\d)', file_info['source']).group(1), 'Unknown')
        output_dir = unique_tmp_dir / f"Output_{arch}"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_dirs[arch] = output_dir
        
        # Copy the files to the correct directory based on the ISS file
        destination_dir = output_dir / file_info['dest_dir'].replace("{app}", "app")
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination_file = destination_dir / file_info['dest_name']
        
        if source_file.exists():
            shutil.copy2(source_file, destination_file)
            logging.info(f"Copied {source_file} to {destination_file}")
            print(f"{Fore.GREEN}Copied {source_file} (Variant: {arch})")
            time.sleep(0.1)

    # Handle files not in ISS but with variants like ,1 ,2 ,3 etc
    print(f"{Fore.GREEN}Mapping common files...\n")
    time.sleep(0.4)
    
    print(f"\n{Fore.GREEN}Starting file operations...\n")
    time.sleep(0.4)
    
    for file in extracted_dir.rglob('*'):
        renamed_file = file.with_name(rename_placeholder(file.name))
        if renamed_file != file:
            # Rename the file or directory to remove {}
            shutil.move(str(file), str(renamed_file))
            logging.info(f"Renamed {file} to {renamed_file}")
            time.sleep(0.1)
            file = renamed_file

        if ',' in file.name:
            # Extract base name and variant
            base_name, variant = file.stem.split(',')

            # Get the architecture based on the dynamic mapping from the ISS file
            arch = variant_arch_mapping.get(variant, 'Unknown')

            # Copy the file to the corresponding architecture folder
            output_dir = unique_tmp_dir / f"Output_{arch}"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Remove the variant suffix from the filename
            clean_name = file.name.replace(f",{variant}", "")

            # Determine the destination with the subdirectory preserved
            relative_path = file.relative_to(extracted_dir).parent / clean_name
            destination = output_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)  # Create subdirectories as needed

            # Copy the file
            shutil.copy2(file, destination)
            logging.info(f"Copied {file.name} to {destination}")
            print(f"Copied {file.name} (Variant: {arch})")
            time.sleep(0.2)
        else:
            # Files without variants (common files)
            common_files.append(file)

    # Copy common files to all output directories while preserving subdirectory structure
    for common_file in common_files:
        if common_file.is_file():  # Ensure it's a file, not a directory
            for arch in variant_arch_mapping.values():
                output_dir = unique_tmp_dir / f"Output_{arch}"
                output_dir.mkdir(parents=True, exist_ok=True)
                relative_path = common_file.relative_to(extracted_dir)
                destination = output_dir / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(common_file, destination)
                logging.info(f"Copied common file {common_file.name} to {destination}")
                print(f"Copied common file {common_file.name}")
                time.sleep(0.1)

    # Move the input file back to its original location
    shutil.move(str(tmp_innosetup_file), innosetup_file)
    logging.info(f"Moving {innosetup_file.name}")
    print(f"\n{Fore.GREEN}Moving {innosetup_file.name}")
    time.sleep(0.4)

    # Change back to the original script directory
    os.chdir(script_dir)
    logging.info(f"Working directory set to {script_dir}")
    print(f"\n{Fore.YELLOW}Working directory set to {script_dir}\n")
    time.sleep(0.4)
    print("finished!")

    print(f"\n{Fore.GREEN}###[ Unpacking and Rebuild Complete ]###\n")
    print(f"---------------------------------------------------\n")
    time.sleep(0.4)
    
    # Final summary of the operation
    print(f"\n{Fore.BLUE}#####--- Extraction Summary ---#####")
    print(f"\n{Fore.BLUE}------------------------------------")
    logging.info("\nExtraction Summary")
    print(f"{Fore.YELLOW}App Name: {metadata.get('AppName', 'N/A')}")
    print(f"{Fore.YELLOW}App Version: {metadata.get('AppVersion', 'N/A')}")
    print(f"{Fore.YELLOW}App Publisher: {metadata.get('AppPublisher', 'N/A')}")
    print(f"{Fore.YELLOW}App Support URL: {metadata.get('AppSupportURL', 'N/A')}")
    print(f"{Fore.YELLOW}App Comments: {metadata.get('AppComments', 'N/A')}")
    logging.info(f"App Name: {metadata.get('AppName', 'N/A')}")
    logging.info(f"App Version: {metadata.get('AppVersion', 'N/A')}")
    logging.info(f"App Publisher: {metadata.get('AppPublisher', 'N/A')}")
    logging.info(f"App Support URL: {metadata.get('AppSupportURL', 'N/A')}")
    logging.info(f"App Comments: {metadata.get('AppComments', 'N/A')}")

    print(f"\n{Fore.CYAN}Variants Processed:")
    logging.info("\nVariants Processed:")
    for variant, arch in variant_arch_mapping.items():
        print(f"{Fore.GREEN}  Variant {variant} -> {arch}")
        logging.info(f"  Variant {variant} -> {arch}")

    print(f"\n{Fore.CYAN}Output Directories by Arch Created:")
    logging.info("\nOutput Directories Created:")
    for arch, output_dir in output_dirs.items():
        print(f"{Fore.GREEN}  {output_dir}")
        logging.info(f"  {output_dir}")
        
    print(f"\n{Fore.CYAN}Output Directory with raw unpack:")
    print(f"{Fore.GREEN}  {extracted_dir}\n")

    # Completion message
    print(f"{Style.BRIGHT + Fore.GREEN}\nScript completed successfully\n")
    logging.info("\nScript completed successfully!")
    
    print("\n")
    print("       .")
    print("      :")
    print(r"    ___:____     |'\/'|")
    print("  ,'        `.    \\  /")
    print("  |  O        \\___/  |")
    print("~^~^~^~^~^~^~^~^~^~^~^~^~")
    print("")


# Entry point for the script
if __name__ == "__main__":
    main()
