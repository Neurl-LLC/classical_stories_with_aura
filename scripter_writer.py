import sys
from openai import OpenAI

def load_file(filepath: str) -> str:
    """Load and return the content of a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Error reading {filepath}: {e}")

def save_file(filepath: str, content: str) -> None:
    """Save the given content to a file."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
            print(f"✅ Output saved to {filepath}")
    except Exception as e:
        raise RuntimeError(f"Error writing to {filepath}: {e}")

def generate_script(client: OpenAI, instruction: str, prose: str) -> str:
    """Generate a script using the OpenAI API based on instruction and prose."""
    try:
        response = client.responses.create(
            model="gpt-4.1",
            instructions=instruction,
            input=f"Generate a script based on the following prose:\n\n{prose}"
        )
        return response.output_text
    except Exception as e:
        raise RuntimeError(f"Error generating script: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_writer.py <prose_file.txt>")
        sys.exit(1)

    prose_path = sys.argv[1]
    instruction = load_file("instruction.txt")
    prose = load_file(prose_path)

    print("📘 Instruction and prose loaded. Generating script...")

    client = OpenAI()
    script = generate_script(client, instruction, prose)

    save_file("script.txt", script)

if __name__ == "__main__":
    main()


