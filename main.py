import asyncio
import os
import json
from datetime import datetime
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Retrieve the Bitquery API key from environment variables
BITQUERY_API_KEY = os.getenv('BITQUERY_API_KEY')

if not BITQUERY_API_KEY:
    raise ValueError("API key not found. Please set the BITQUERY_API_KEY environment variable.")

# Define the GraphQL subscription query
subscription_query = gql("""
subscription MyQuery {
  Solana {
    DEXTrades(
      where: {
        Trade: { Dex: { ProtocolName: { is: "pump" } } },
        Transaction: { Result: { Success: true } }
      }
    ) {
      Instruction {
        Program {
          Method
        }
      }
      Trade {
        Dex {
          ProtocolFamily
          ProtocolName
        }
        Buy {
          Amount
          Account {
            Address
          }
          Currency {
            Name
            Symbol
            MintAddress
            Decimals
            Fungible
            Uri
          }
        }
        Sell {
          Amount
          Account {
            Address
          }
          Currency {
            Name
            Symbol
            MintAddress
            Decimals
            Fungible
            Uri
          }
        }
      }
      Transaction {
        Signature
      }
    }
  }
}
""")

def save_data_to_json(data, folder_path):
    """
    Save the received data as a JSON file.

    Args:
        data (dict): The data to save.
        folder_path (str): The directory where the JSON file will be saved.
    """
    # Extract the transaction signature and current timestamp for a unique filename
    signature = data.get('Transaction', {}).get('Signature', 'unknown_signature')
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]  # Up to milliseconds
    filename = f"{signature}_{timestamp}.json"
    filepath = os.path.join(folder_path, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to '{filepath}'.")
    except Exception as e:
        print(f"Error saving data: {e}")

async def subscribe_and_save(folder_path):
    """
    Subscribe to the Bitquery WebSocket and save incoming data as JSON files.

    Args:
        folder_path (str): The directory where JSON files will be saved.
    """
    # Set up the WebSocket transport with the provided API key
    transport = WebsocketsTransport(
        url='wss://streaming.bitquery.io/eap',
        headers={
            'X-API-KEY': BITQUERY_API_KEY
        }
    )

    # Create the GraphQL client
    async with Client(
        transport=transport,
        fetch_schema_from_transport=False,
    ) as client:
        try:
            # Execute the subscription
            async for result in client.subscribe(subscription_query):
                # Print the received data
                print("New DEX trade detected:")
                print(result)

                # Save the data as a JSON file
                save_data_to_json(result, folder_path)
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    """
    Main function to initiate the subscription and data saving process.
    """
    # Define the folder where JSON files will be saved
    DATA_FOLDER = 'data'  # Change this to your desired subfolder

    # Check if the specified folder exists
    if not os.path.exists(DATA_FOLDER):
        print(f"The data folder '{DATA_FOLDER}' does not exist. Please create it before running the script.")
        return

    # Start the asynchronous subscription
    asyncio.run(subscribe_and_save(DATA_FOLDER))

if __name__ == "__main__":
    main()
