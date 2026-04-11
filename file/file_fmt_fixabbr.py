import os
import sys

def fix_comma_formatting(root_dir):                                                                                                               
    for dirpath, dirnames, filenames in os.walk(root_dir):                                                                                        
        for filename in filenames:                                                                                                                
            if filename.endswith('.md'):                                                                                                          
                filepath = os.path.join(dirpath, filename)                                                                                        
                try:                                                                                                                              
                    with open(filepath, 'r', encoding='utf-8') as file:                                                                           
                        content = file.read()                                                                                                     
                    # Replace ' , ' with ', '                                                                                                     
                    new_content = content.replace(' pp. ', ' pages ')                                                                                    
                    # Only write if there was a change                                                                                            
                    if new_content != content:                                                                                                    
                        with open(filepath, 'w', encoding='utf-8') as file:                                                                       
                            file.write(new_content)                                                                                               
                except Exception as e:                                                                                                            
                    print(f"Error processing {filepath}: {e}") 

if __name__ == "__main__":                                                                                                                        
    if len(sys.argv) > 1:                                                                                                                         
        root_directory = sys.argv[1]                                                                                                              
        if not os.path.isdir(root_directory):                                                                                                     
            print(f"Error: '{root_directory}' is not a valid directory.")                                                                         
            sys.exit(1)                                                                                                                           
        fix_comma_formatting(root_directory)                                                                                                      
    else:                                                                                                                                         
        fix_comma_formatting('.')  # Default to current directory if no argument is provided 
