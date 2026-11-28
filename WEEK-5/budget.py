import os
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv()

# Read configuration values
INPUT_PRICE = float(os.getenv("INPUT_PRICE_PER_MILLION"))
OUTPUT_PRICE = float(os.getenv("OUTPUT_PRICE_PER_MILLION"))

REQUESTS_PER_DAY = int(os.getenv("REQUESTS_PER_DAY"))
AVG_INPUT_TOKENS = int(os.getenv("AVG_INPUT_TOKENS"))
AVG_OUTPUT_TOKENS = int(os.getenv("AVG_OUTPUT_TOKENS"))
PEAK_RPM = int(os.getenv("PEAK_REQUESTS_PER_MINUTE"))

RPM_LIMIT = int(os.getenv("RPM_LIMIT"))
TPM_LIMIT = int(os.getenv("TPM_LIMIT"))

MONTHLY_BUDGET = float(os.getenv("MONTHLY_BUDGET_USD"))
DAILY_BUDGET = float(os.getenv("DAILY_BUDGET_USD"))
SAFETY_MARGIN = float(os.getenv("SAFETY_MARGIN_PERCENT"))


def calculate_cost(input_tokens, output_tokens):
    """Calculate API cost in USD."""
    input_cost = (input_tokens / 1_000_000) * INPUT_PRICE
    output_cost = (output_tokens / 1_000_000) * OUTPUT_PRICE
    return input_cost + output_cost


def main():

    # Calculate daily token usage
    daily_input = REQUESTS_PER_DAY * AVG_INPUT_TOKENS
    daily_output = REQUESTS_PER_DAY * AVG_OUTPUT_TOKENS
    daily_total = daily_input + daily_output

    # Calculate daily and monthly costs
    daily_cost = calculate_cost(daily_input, daily_output)
    monthly_cost = daily_cost * 30

    # Add safety margin
    safe_monthly_cost = monthly_cost * (1 + SAFETY_MARGIN / 100)

    # Calculate peak tokens per minute
    peak_tpm = PEAK_RPM * (AVG_INPUT_TOKENS + AVG_OUTPUT_TOKENS)

    print("\n===== TOKEN ECONOMICS REPORT =====")

    print("\n--- Token Usage ---")
    print(f"Daily input tokens  : {daily_input:,}")
    print(f"Daily output tokens : {daily_output:,}")
    print(f"Daily total tokens  : {daily_total:,}")
    print(f"Monthly tokens      : {daily_total * 30:,}")

    print("\n--- API Cost ---")
    print(f"Daily cost          : ${daily_cost:.4f}")
    print(f"Monthly cost        : ${monthly_cost:.4f}")
    print(f"Cost with safety margin: ${safe_monthly_cost:.4f}")

    print("\n--- Rate Limit Check ---")
    print(f"Peak RPM            : {PEAK_RPM}")
    print(f"RPM limit           : {RPM_LIMIT}")
    print(f"Peak TPM            : {peak_tpm:,}")
    print(f"TPM limit           : {TPM_LIMIT:,}")

    rpm_ok = PEAK_RPM <= RPM_LIMIT
    tpm_ok = peak_tpm <= TPM_LIMIT

    print("RPM Status          :", "PASS" if rpm_ok else "FAIL")
    print("TPM Status          :", "PASS" if tpm_ok else "FAIL")

    print("\n--- Budget Check ---")
    print(f"Daily budget        : ${DAILY_BUDGET:.2f}")
    print(f"Monthly budget      : ${MONTHLY_BUDGET:.2f}")

    print(
        "Daily budget status:",
        "PASS" if daily_cost <= DAILY_BUDGET else "EXCEEDED"
    )

    print(
        "Monthly budget status:",
        "PASS" if safe_monthly_cost <= MONTHLY_BUDGET else "EXCEEDED"
    )

    print("\n===== REPORT COMPLETED =====")


if __name__ == "__main__":
    main()