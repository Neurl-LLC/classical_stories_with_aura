# Giving Voice to Classical Stories with Deepgram’s Aura 2

This repository supports the article [Giving Voice to Classical Stories with Deepgram’s Aura 2](https://neurlcreators.substack.com/p/giving-voice-to-classical-stories) on [The Neural Blueprint](https://neurlcreators.substack.com/).

It demonstrates how to use a language model to transform classical prose into a dramatized script, then bring that script to life with lifelike text-to-speech voices. Each character is assigned a distinct voice. This project uses Deepgram’s Aura 2 and OpenAI’s GPT-4.1.

## Setup

First, create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate
```

Then install the required SDKs:

```bash
pip install openai deepgram-sdk
```

Make sure your API keys are set as environment variables:
`OPENAI_API_KEY` and `DEEPGRAM_API_KEY`

## Usage

To start, we need to generate a script from a prose passage. The repository includes Chapter One of [*A Study in Scarlet*](https://en.wikipedia.org/wiki/A_Study_in_Scarlet). Use the `script_writer.py` script to convert it into dialogue:

```bash
python script_writer.py chapter_1.txt
```

This will generate a dramatized version of the prose and save it as `script.txt`.

Next, use `main.py` to generate the full audio performance:

```bash
python main.py script.txt
```

When the script runs, you’ll be prompted to assign a voice to each character. Visit Deepgram’s Aura 2 [voice documentation](https://developers.deepgram.com/docs/tts-models) to select the right voices for your characters.

