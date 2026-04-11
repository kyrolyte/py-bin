import subprocess                                                                                                                                 
import argparse                                                                                                                                   
import sys                                                                                                                                        
                                                                                                                                                  
def run_ollama(prompt, model, output_file=None):
    try:                                                                                                                                          
        command = ["docker", "exec", "ollamagpu", "ollama", "run", model, prompt]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout  # The output from Ollama
        if output_file:                                                                                                                           
           try:                                                                                                                                  
               with open(output_file, "w") as f:                                                                                                 
                   f.write(output)                                                                                                               
                   print(f"Output saved to {output_file}")
           except Exception as e:
               print(f"Error saving output to file: {e}")
        else:
            print(output)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a prompt against the Ollama server in a Docker container.")
    parser.add_argument("-o", "--output", help="Output file name (default: file.md)")
    parser.add_argument("-m", "--model", default="gemma3:4b", help="The model to use (default: gemma3:4b)")
    parser.add_argument("prompt", nargs="+", help="The prompt to send to Ollama")

    args = parser.parse_args()

    prompt = " ".join(args.prompt)  # Join the prompt arguments back into a single string

    if args.output:
        run_ollama(prompt, args.model, args.output)
    else:
        run_ollama(prompt, args.model)

