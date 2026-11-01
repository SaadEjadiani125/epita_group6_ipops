from engtoolslab2.client import fetch_live_data

if __name__ == "__main__":
    result = fetch_live_data()

    for key, value in result.items():
        print(f"{key}: {value}")