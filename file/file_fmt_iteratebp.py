import os
import sys

def process_directory(directory_path):                                                                                                            
    """                                                                                                                                           
    Recursively iterates through a directory and processes files.                                                                                 
                                                                                                                                                  
    Args:                                                                                                                                         
        directory_path (str): The path to the directory to iterate through.                                                                       
    """                                                                                                                                           
                                                                                                                                                  
    try:                                                                                                                                          
        for item in os.listdir(directory_path):                                                                                                   
            item_path = os.path.join(directory_path, item)                                                                                        
                                                                                                                                                  
            if os.path.isfile(item_path):                                                                                                         
                if os.path.splitext(item_path)[1] == ".md":  # Process only markdown files                                                        
                    try:                                                                                                                          
                        with open(item_path, 'r') as f:                                                                                           
                            print(f"Opened markdown file: {item_path} and closed.")                                                               
                    except Exception as e:                                                                                                        
                        print(f"Error opening/closing {item_path}: {e}")                                                                          
                                                                                                                                                  
            elif os.path.isdir(item_path):                                                                                                        
                process_directory(item_path)  # Recursive call for subdirectories                                                                 
                                                                                                                                                  
    except OSError as e:                                                                                                                          
        print(f"Error accessing directory {directory_path}: {e}")                                                                                 


if __name__ == "__main__":
    if len(sys.argv) > 1:                                                                                                                         
        directory_to_process = sys.argv[1]                                                                                                        
    else:                                                                                                                                         
        directory_to_process = "."  # Current directory                                                                                           
                                                                                                                                                  
    process_directory(directory_to_process) 


