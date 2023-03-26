#!/usr/bin/env python3
"""
GPT-3 API Command Line Wrapper

This Python script allows you to easily interact with the GPT-3 API from the command line.
You can provide various parameters as command-line options and get the generated text in the output.

Usage:
./gpt3 [prompts] [options]

Arguments:
prompts: A list of input prompts for GPT-3, separated by spaces. If '-' is present, it will read from stdin.
The prompts will be concatenated with newline characters.

Options:
-e, --engine: The OpenAI GPT-3 engine to use (default: gpt-3.5-turbo)
-m, --max-tokens: Maximum number of tokens in the response (default: 100)
-t, --temperature: Sampling temperature for randomness (default: 0.5)
-d, --debug: Show the full response and request parameters in JSON format, with Unicode characters preserved (default: False)
-k, --key: OpenAI API key (optional, overrides OPENAI_API_KEY environment variable)

Note:
    To use this script, you need to have the 'openai' library installed. You can install it using pip:
    pip install openai

    The API key can be provided using the --key option or set as the OPENAI_API_KEY environment variable.
"""

import openai
import argparse
import os
import sys
import json

def cli():
    parser = argparse.ArgumentParser(description="GPT-3 API command line wrapper")

    parser.add_argument("prompts", nargs="*", type=str, help="Input prompts for GPT-3 or '-' to read from stdin")
    parser.add_argument("-e", "--engine", type=str, default="gpt-3.5-turbo", help="OpenAI GPT-3 engine (default: gpt-3.5-turbo)")
    parser.add_argument("-m", "--max-tokens", type=int, default=100, help="Maximum number of tokens in the response (default: 100)")
    parser.add_argument("-t", "--temperature", type=float, default=0.5, help="Sampling temperature for randomness (default: 0.5)")
    parser.add_argument("-d", "--debug", action="store_true", help="Show the request parameters and the full response in JSON format (default: False)")
    parser.add_argument("-k", "--key", type=str, default=None, help="OpenAI API key (optional, overrides OPENAI_API_KEY environment variable)")

    args = parser.parse_args()

    api_key = args.key or os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("Please set the environment variable OPENAI_API_KEY or provide the API key using the --key option.")
    openai.api_key = api_key

    prompt_parts = []
    for p in args.prompts:
        if p == "-":
            prompt_parts.append(sys.stdin.read())
        else:
            prompt_parts.append(p)

    prompt = "\n".join(prompt_parts)

    response = openai.ChatCompletion.create(
        model=args.engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=args.max_tokens,
        n=1,
        stop=None,
        temperature=args.temperature,
    )

    request_params = {
        "model": args.engine,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": args.max_tokens,
        "n": 1,
        "stop": None,
        "temperature": args.temperature,
        "timeout": 60,
    }

    if args.debug:
        print("\nRequest Parameters:")
        print(json.dumps(request_params, indent=2, ensure_ascii=False))

    response = openai.ChatCompletion.create(**request_params)

    if args.debug:
        print("\nFull JSON Response:")
        print(json.dumps(response, indent=2, ensure_ascii=False))

    generated_text = response.choices[0].message['content'].strip()
    print(generated_text)

if __name__ == "__main__":
    cli()
