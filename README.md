# Hong Kong Tides Visualization

This project displays projected tidal data in Chek Lap Kok (E), Hong Kong for 2025.  
The data was collected from the Hong Kong Observatory site HKO Tidal Information (https://www.hko.gov.hk/tide/eCLKtext2025.html) and transformed into a graphical visualization in Python.   

The goal is to explore the boundary between data visualization and artistic expression, showing the natural trend of the tides through a clean and minimal graph design

## Features
- Acquisition of tidal data from HKO (scraping/parsing).
- Cleaning and organization of data in manageable format (lists / pandas dataframe).
- Tide cycle display as a line graph.
- Possibility of extending the project with:
- animations (GIF with tidal pattern),

## How to use in VS Code
1. Open the folder `PROJECT_HKO` in VS Code.
2. Install requirements once:
   ```
   pip install -r requirements.txt
   ```
3. Press Run  in VS Code to execute `src/main.py`.
4. The result `hkotide.gif` will appear in the `output/` folder.

