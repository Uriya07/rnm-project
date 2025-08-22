# Rick & Morty Characters Filter

## Project Goal
This project connects to the public [Rick & Morty API](https://rickandmortyapi.com/), 
fetches all characters, filters them based on specific conditions, 
and outputs the result into a CSV file.

### Filter Conditions
- `species == "Human"`
- `status == "Alive"`
- `origin` contains `"Earth"`

### Output
A CSV file (`out.csv`) with the following columns:
- **Name**
- **Location**
- **Image**

---

## Steps Completed
1. **Setup**  
   - Installed Python and virtual environment (venv).  
   - Installed the `requests` library.  

2. **API Connection**  
   - Fetched the first page of characters.  
   - Inspected the structure of the JSON response.  

3. **Pagination**  
   - Implemented `fetch_all_characters()` to follow `info.next` until no more pages remain.  

4. **Filtering**  
   - Implemented `filter_human_alive_earth()`.  
   - Returned only Human + Alive characters with origin containing Earth.  

5. **CSV Export**  
   - Implemented `write_csv()`.  
   - Generated `out.csv` with the selected data.  

---

## Current Status
✔️ Core logic complete (Fetch → Pagination → Filter → CSV).  

➡️ Next steps:
- Build a REST API with **FastAPI**.  
- Containerize with **Docker**.  
- Deploy with **Kubernetes** and **AWS EKS**.  

---

## How to Run
```bash
# Activate virtual environment (example)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python app.py

# Result will be in out.csv
```
