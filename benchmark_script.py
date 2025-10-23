import time
import json
import requests
import os
from collections import defaultdict
from datetime import datetime

# --- Configuration ---
# Set the API endpoint for your server.
API_URL = "http://localhost:8001/v1/chat/completions"

# Define the folder to save the results.
OUTPUT_FOLDER = "benchmark_output"

# Generate a unique filename with the current date and time
timestamp = datetime.now().strftime("%m_%d_%H%M")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, f"benchmark_results_{timestamp}.txt")

# Define the number of requests to send for the benchmark.
NUM_REQUESTS = 50  # Number of requests per category

# Define categorized prompts for the benchmark.
# Total requests will be 4 categories * 50 requests/category = 200 requests.
CATEGORIZED_PROMPTS = {
    "information_retrieval": [
        "What is the capital of France?",
        "What is the longest river in the world?",
        "Who was the first person to walk on the moon?",
        "What is the chemical formula for water?",
        "In what year did World War II end?",
        "What is the population of Tokyo?",
        "Who wrote 'To Kill a Mockingbird'?",
        "What is the speed of light in a vacuum?",
        "How many bones are in the adult human body?",
        "What is the boiling point of water at sea level in Celsius?",
        "What is the largest ocean on Earth?",
        "Who painted the Mona Lisa?",
        "What is the chemical symbol for gold?",
        "What is the main function of the heart?",
        "What is the name of the fourth planet from the sun?",
        "Who invented the telephone?",
        "What is the capital of Brazil?",
        "What is the square root of 144?",
        "What is the smallest country in the world by area?",
        "What is the main ingredient in guacamole?",
        "What is the deepest point in the ocean?",
        "Who discovered penicillin?",
        "What is the capital of Canada?",
        "What is the largest land animal?",
        "What is the process of photosynthesis?",
        "What is the chemical symbol for oxygen?",
        "What is the freezing point of water in Celsius?",
        "What is the theory of evolution?",
        "Who was Albert Einstein?",
        "What is a supernova?",
        "What is the Earth's atmosphere made of?",
        "What is the capital of Russia?",
        "Who was Leonardo da Vinci?",
        "What is the main purpose of the lungs?",
        "What is a galaxy?",
        "What is the capital of India?",
        "Who was Stephen Hawking?",
        "What is a black hole?",
        "What is the capital of Egypt?",
        "Who was Nikola Tesla?",
        "What is the main function of the stomach?",
        "What is the process of cell division?",
        "What is the capital of Germany?",
        "Who was Alan Turing?",
        "What is the main function of the liver?",
        "What is the capital of Italy?",
        "Who was Johann Sebastian Bach?",
        "What is the main function of the pancreas?",
        "What is the capital of Spain?",
        "Who was Ludwig van Beethoven?",
    ],
    "reasoning": [
        "Explain the relationship between supply and demand.",
        "Describe the pros and cons of nuclear energy.",
        "How can you prove the Pythagorean theorem?",
        "If all humans are mortal and I am a human, what can you conclude?",
        "What is the difference between weather and climate?",
        "Explain why a ship floats but a rock sinks.",
        "Given a list of numbers, how would you find the median?",
        "Explain the domino effect in a political context.",
        "How would you sort a list of names alphabetically?",
        "Explain the concept of a balanced diet using a metaphor.",
        "If you have a 3-gallon jug and a 5-gallon jug, how do you measure out exactly 4 gallons of water?",
        "What logical steps would you take to debug a simple computer program?",
        "Explain why the seasons change.",
        "Why is it important to recycle?",
        "Explain the process of creating a new law in the United States.",
        "How does a computer processor execute instructions?",
        "What are the arguments for and against raising the minimum wage?",
        "Explain the concept of compound interest.",
        "How would you explain the value of education to a young child?",
        "Describe a strategy for winning a game of chess.",
        "What are the ethical implications of artificial intelligence?",
        "Explain the steps to solve a Rubik's Cube.",
        "Why do birds migrate?",
        "Explain how the internet works in simple terms.",
        "Describe the process of a bill becoming a law.",
        "How would you plan a road trip across the country?",
        "Explain the theory of relativity using a simple analogy.",
        "Why is it important to have a budget?",
        "What are the logical fallacies in the statement, 'Everyone is doing it, so it must be right'?",
        "Describe how to make a perfect cup of coffee.",
        "Explain the difference between a virus and a bacterium.",
        "How does a cell's nucleus function?",
        "What is the reasoning behind daylight saving time?",
        "Explain how a steam engine works.",
        "What are the benefits of a diverse team?",
        "Describe the steps to build a simple wooden chair.",
        "Why do we have a leap year?",
        "Explain the concept of a food chain.",
        "How would you design a personal fitness plan?",
        "Explain the difference between a polygon and a circle.",
        "What is the logic behind a negotiation strategy?",
        "Describe the steps to set up a small business.",
        "How does the Earth's rotation affect our daily lives?",
        "Explain the concept of gravity.",
        "How would you prepare for a natural disaster?",
        "What is the rationale for traffic laws?",
        "Explain the difference between a hypothesis and a theory.",
        "How would you convince someone to adopt a pet?",
        "What is the logic behind an algorithm?",
        "Explain why it's a good idea to back up your data.",
    ],
    "creative_text_generation": [
        "Write a short poem about a forgotten toy.",
        "Describe a perfect day in your own words.",
        "Write a short story about a talking animal.",
        "What is the most beautiful color and why?",
        "Write a haiku about a rainy day.",
        "Describe the feeling of joy without using the word 'happy'.",
        "What would you do if you could fly?",
        "Write a dialogue between a curious robot and a wise tree.",
        "What is the sound of silence?",
        "Write a poem about the ocean.",
        "Describe the taste of a summer breeze.",
        "Imagine a world without music.",
        "What does freedom mean to you?",
        "Write a short story about a message in a bottle.",
        "If you could travel anywhere in time, where would you go?",
        "Describe your favorite memory.",
        "Write a poem about the color blue.",
        "What is the most important invention of all time?",
        "Describe the perfect pizza.",
        "Write a journal entry from the perspective of a dog.",
        "What is the meaning of life?",
        "Write a short story about a time traveler who loses their way.",
        "Describe a magical forest.",
        "What is a dream?",
        "Write a poem about the first day of spring.",
        "What is the most powerful emotion?",
        "Describe the feeling of nostalgia.",
        "What is the most challenging thing you've ever done?",
        "Write a short story about a forgotten toy.",
        "Describe the taste of fresh-baked bread.",
        "What is a lie?",
        "Write a poem about the moon.",
        "What is a good way to relax?",
        "Describe a day in the life of a cloud.",
        "What is the biggest mystery of the universe?",
        "Write a short story about a brave knight and a timid dragon.",
        "What is the meaning of a smile?",
        "Write a poem about the sound of rain.",
        "What is a fun way to learn something new?",
        "Describe a new kind of animal.",
        "What is courage?",
        "Write a short story about a lonely alien.",
        "What is a bad habit you'd like to break?",
        "Write a poem about the first snow of the year.",
        "What is the best piece of advice you've ever received?",
        "Describe a city in the future.",
        "What is a good joke?",
        "Write a short story about a magical key.",
        "What is the best way to make a friend?",
        "Write a poem about a firefly.",
    ],
    "task_completion": [
        "Generate a Python function to check if a number is prime.",
        "Write an HTML form for a user login.",
        "Create a CSS snippet to make a button hover effect.",
        "Write a short, professional email to request a meeting.",
        "Generate a grocery list for a week of meals.",
        "Write a 5-step plan to organize a closet.",
        "Create a recipe for a simple chocolate cake.",
        "Write a short guide on how to change a tire.",
        "Generate a list of 10 common houseplants that are easy to care for.",
        "Create a workout plan for a beginner, focusing on core strength.",
        "Write a thank-you note for a job interview.",
        "Generate a simple budget template in a list format.",
        "Create a short speech for a best friend's wedding.",
        "Write a short script for a commercial selling a new coffee machine.",
        "Generate a list of 5 things to do to prepare for a job interview.",
        "Create a list of 10 essential items for a hiking trip.",
        "Write a short summary of a research paper on climate change.",
        "Generate a simple to-do list for a productive workday.",
        "Create a checklist for moving into a new apartment.",
        "Write a short guide on how to plant a tomato plant.",
        "Generate a list of 5 popular tourist attractions in Paris.",
        "Create a simple meal plan for a week.",
        "Write a short guide on how to save money.",
        "Generate a list of 10 classic books everyone should read.",
        "Create a short guide on how to bake bread.",
        "Write a simple resume template.",
        "Generate a list of 5 tips for public speaking.",
        "Create a short guide on how to start a podcast.",
        "Write a short guide on how to write a good blog post.",
        "Generate a list of 5 ways to reduce your carbon footprint.",
        "Create a short guide on how to meditate.",
        "Write a simple cover letter template.",
        "Generate a list of 5 tips for learning a new language.",
        "Create a short guide on how to write a good email.",
        "Write a simple itinerary for a weekend trip.",
        "Generate a list of 5 tips for time management.",
        "Create a short guide on how to create a good presentation.",
        "Write a simple plan for a birthday party.",
        "Generate a list of 5 tips for staying motivated.",
        "Create a short guide on how to be a good leader.",
        "Write a simple plan for a hiking trip.",
        "Generate a list of 5 tips for a healthy diet.",
        "Create a short guide on how to be a good friend.",
        "Write a simple plan for a study session.",
        "Generate a list of 5 tips for stress management.",
        "Create a short guide on how to write a good story.",
        "Write a simple plan for a workout routine.",
        "Generate a list of 5 tips for giving a good speech.",
        "Create a short guide on how to be a good listener.",
        "Write a simple plan for a garden.",
    ]
}


def run_benchmark():
    """
    Runs the benchmark by sending multiple requests and calculating metrics.
    """
    print(f"Starting benchmark with {NUM_REQUESTS} requests per category...")

    # Create the output directory if it doesn't exist.
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output folder: {OUTPUT_FOLDER}")

    # A list to store metrics for all requests, regardless of category
    all_metrics = defaultdict(list)
    # A dictionary to store the metrics for each category
    category_metrics_dict = {}

    # Open the output file in write mode to clear previous content.
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"--- Benchmark Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n\n")

        # Loop through each category of prompts
        for category, prompts_list in CATEGORIZED_PROMPTS.items():
            f.write(f"--- Running Benchmark for Category: {category.replace('_', ' ').title()} ---\n\n")
            category_metrics = defaultdict(list)

            # Loop to send each request in the current category
            for i, prompt in enumerate(prompts_list):

                # Update the request payload with the current prompt
                REQUEST_PAYLOAD = {
                    "model": "openai/gpt-oss-120b",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 100,
                    "stream": True
                }

                f.write(f"--- {category.replace('_', ' ').title()} Request {i+1}/{len(prompts_list)} ---\n")

                # Record the start time of the entire request
                start_total_time = time.time()

                try:
                    with requests.post(API_URL, json=REQUEST_PAYLOAD, stream=True) as response:
                        response.raise_for_status()

                        first_token_time = None
                        tokens_count = 0
                        full_response_content = ""

                        for chunk in response.iter_lines(decode_unicode=True):
                            if chunk.startswith("data: "):
                                json_data = chunk[len("data: "):]
                                if json_data.strip() == "[DONE]":
                                    break

                                try:
                                    data = json.loads(json_data)

                                    # The content is sent in 'delta' chunks during streaming, not 'message'.
                                    # This line now safely checks for 'delta' and retrieves the content.
                                    content = data['choices'][0].get('delta', {}).get('content', '')

                                    if content:
                                        if first_token_time is None:
                                            first_token_time = time.time() - start_total_time
                                        full_response_content += content
                                        tokens_count += 1
                                except (json.JSONDecodeError, KeyError) as e:
                                    f.write(f"Error parsing JSON chunk: {e}\n")

                        end_total_time = time.time()
                        total_time = end_total_time - start_total_time

                        # Append metrics to both the category-specific and overall lists
                        category_metrics['total_time'].append(total_time)
                        category_metrics['completion_tokens'].append(tokens_count)
                        all_metrics['total_time'].append(total_time)
                        all_metrics['completion_tokens'].append(tokens_count)

                        tps = tokens_count / total_time if total_time > 0 else 0
                        category_metrics['tokens_per_second'].append(tps)
                        category_metrics['time_to_first_token'].append(first_token_time)
                        all_metrics['tokens_per_second'].append(tps)
                        all_metrics['time_to_first_token'].append(first_token_time)

                        f.write(f"Prompt: {prompt}\n")
                        f.write(f"Response: {full_response_content}\n")
                        f.write(f"Time to First Token: {first_token_time:.4f} seconds\n")
                        f.write(f"Total Request Time: {total_time:.4f} seconds\n")
                        f.write(f"Completion Tokens: {tokens_count}\n")
                        f.write(f"Tokens per Second (TPS): {tps:.2f}\n")
                        f.write("-" * 20 + "\n")

                except requests.exceptions.RequestException as e:
                    f.write(f"Error during request: {e}\n")
                    continue

            # Store the metrics for the current category
            category_metrics_dict[category] = category_metrics

        # --- Calculate and print the summary for each category ---
        for category, metrics in category_metrics_dict.items():
            f.write(f"\n--- Summary Benchmark Results for {category.replace('_', ' ').title()} ---\n")
            if metrics['total_time']:
                avg_total_time = sum(metrics['total_time']) / len(metrics['total_time'])
                min_total_time = min(metrics['total_time'])
                max_total_time = max(metrics['total_time'])

                avg_tokens_per_second = sum(metrics['tokens_per_second']) / len(metrics['tokens_per_second'])
                min_tokens_per_second = min(metrics['tokens_per_second'])
                max_tokens_per_second = max(metrics['tokens_per_second'])

                avg_time_to_first_token = sum(metrics['time_to_first_token']) / len(metrics['time_to_first_token'])
                min_time_to_first_token = min(metrics['time_to_first_token'])
                max_time_to_first_token = max(metrics['time_to_first_token'])

                f.write(f"Average Time to First Token: {avg_time_to_first_token:.4f} seconds\n")
                f.write(f"Min Time to First Token: {min_time_to_first_token:.4f} seconds\n")
                f.write(f"Max Time to First Token: {max_time_to_first_token:.4f} seconds\n")
                f.write(f"Average Total Request Time: {avg_total_time:.4f} seconds\n")
                f.write(f"Min Total Request Time: {min_total_time:.4f} seconds\n")
                f.write(f"Max Total Request Time: {max_total_time:.4f} seconds\n")
                f.write(f"Average Tokens per Second (TPS): {avg_tokens_per_second:.2f}\n")
                f.write(f"Min Tokens per Second (TPS): {min_tokens_per_second:.2f}\n")
                f.write(f"Max Tokens per Second (TPS): {max_tokens_per_second:.2f}\n\n")
            else:
                f.write("No successful requests were made for this category.\n\n")

        # --- Calculate and print the final results for all prompts ---
        if not all_metrics['total_time']:
            f.write("\nNo successful requests were made.")
            print("\nNo successful requests were made.")
            return

        avg_total_time = sum(all_metrics['total_time']) / len(all_metrics['total_time'])
        min_total_time = min(all_metrics['total_time'])
        max_total_time = max(all_metrics['total_time'])

        avg_tokens_per_second = sum(all_metrics['tokens_per_second']) / len(all_metrics['tokens_per_second'])
        min_tokens_per_second = min(all_metrics['tokens_per_second'])
        max_tokens_per_second = max(all_metrics['tokens_per_second'])

        avg_time_to_first_token = sum(all_metrics['time_to_first_token']) / len(all_metrics['time_to_first_token'])
        min_time_to_first_token = min(all_metrics['time_to_first_token'])
        max_time_to_first_token = max(all_metrics['time_to_first_token'])

        f.write("\n--- Overall Benchmark Results (All Categories Combined) ---\n")
        f.write(f"Average Time to First Token: {avg_time_to_first_token:.4f} seconds\n")
        f.write(f"Min Time to First Token: {min_time_to_first_token:.4f} seconds\n")
        f.write(f"Max Time to First Token: {max_time_to_first_token:.4f} seconds\n")
        f.write(f"Average Total Request Time: {avg_total_time:.4f} seconds\n")
        f.write(f"Min Total Request Time: {min_total_time:.4f} seconds\n")
        f.write(f"Max Total Request Time: {max_total_time:.4f} seconds\n")
        f.write(f"Average Tokens per Second (TPS): {avg_tokens_per_second:.2f}\n")
        f.write(f"Min Tokens per Second (TPS): {min_tokens_per_second:.2f}\n")
        f.write(f"Max Tokens per Second (TPS): {max_tokens_per_second:.2f}\n")

    print(f"\nBenchmark completed. Results saved to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    run_benchmark()
