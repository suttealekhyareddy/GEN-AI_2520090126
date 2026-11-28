from llm_client import generate_response
from usage_logger import log_usage


def main():
    print("\n===== LLM MONITORING SYSTEM =====")

    prompt = input("\nEnter your prompt: ")

    print("\nGenerating response...\n")

    result = generate_response(prompt)

    if result["success"]:
        print("LLM RESPONSE:")
        print(result["response"])

    else:
        print("ERROR:", result["response"])

    print("\n===== USAGE MONITORING =====")

    print("Input Tokens:", result["input_tokens"])
    print("Output Tokens:", result["output_tokens"])
    print("Total Tokens:", result["total_tokens"])
    print("Response Time:", result["response_time"], "seconds")
    print("Status:", "Success" if result["success"] else "Failed")

    log_usage(result)


if __name__ == "__main__":
    main()