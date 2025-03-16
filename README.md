## Project Overview  

This project involves building an **ETL (Extract, Transform, Load) pipeline** using **Apache NiFi** to collect and process cryptocurrency market data for six major coins:  

- **Ethereum (ETH)**  
- **Ripple (XRP)**  
- **Bitcoin (BTC)**  
- **Dogecoin (DOGE)**  
- **Tron (TRX)**  
- **Solana (SOL)**  

### ETL Flow in Apache NiFi  

1. **Extract:**  
   - The flow fetches historical market data for the last **120 days** for each coin.  
   - The extracted data includes:  
     - **Price (USD)**  
     - **Market Capitalization (USD)**  
     - **Trading Volume (USD)**  

2. **Transform:**  
   - The extracted data is structured and formatted to match the schema of the target database.  

3. **Load:**  
   - The processed data is inserted into a **PostgreSQL database** in the `crypto_details` table.  

### Dashboard Development  

After storing the data in PostgreSQL, a **Python-based dashboard** was developed to visualize the cryptocurrency trends. The dashboard allows users to:  

- Select a specific coin and view its **Price, Market Cap, Volume and RSI indicator** over time.  
- Analyze historical trends using interactive graphs.  

This solution provides a streamlined process for monitoring cryptocurrency market movements with automated data collection, storage, and visualization.

Sample images of the NiFi flow and dashboard are saved in the `images` folder.

-----------------------------------------------------

## 1- Setting Up PostgreSQL

1. **Set up PostgreSQL and create the database**  
   ```sh
   CREATE DATABASE Crypto;
2. **Create the crypto_details table for storing data**
   ```sh
   CREATE TABLE crypto_details (
    id SERIAL PRIMARY KEY,
    coin_name TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    price DECIMAL(18,8) NOT NULL,
    market_cap DECIMAL(18,2),
    volume DECIMAL(18,2)
   );
## 2- Setting Up Apache NiFi

1. **Download and install Apache NiFi 2.3.0**

2. **Access the NiFi UI.**
   - Start NiFi and open the browser at http://localhost:8080/nifi.

3. **Load `Crypto_Flow.json`**
   - Create a new process group and load the flow definition from the JSON file.

4. **Check parameter contexts and update them if necessary.**
5. **Start the flow and wait for data to be inserted into PostgreSQL.**

## 3- Setting Up Python Environment

1. **Download and install python 3.9 or above**

2. **Create virtual environment**

3. **Install `requirements.txt`**

4. **Check `.env` file and update them if necessary.**

5. **Run `dashboard.py` and visit http://127.0.0.1:8050/ for dynamic dashboard.**

