import requests

from config.config import FRANKFURTER_BASE_URL


def extract_exchange_rate(
    base_currency: str = "USD",
    target_currency: str = "INR",
) -> dict:
    """
    Fetch the latest exchange rate from the Frankfurter API.

    Args:
        base_currency: Currency to convert from.
        target_currency: Currency to convert to.

    Returns:
        dict: JSON response returned by the API.

    Raises:
        requests.HTTPError: If the API returns an unsuccessful status code.
        requests.RequestException: If the request fails.
    """
    url = f"{FRANKFURTER_BASE_URL}/latest"

    params = {
        "base": base_currency,
        "symbols": target_currency,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    exchange_data = extract_exchange_rate()

    print("Base currency:", exchange_data["base"])
    print("Date:", exchange_data["date"])
    print("Rates:", exchange_data["rates"])