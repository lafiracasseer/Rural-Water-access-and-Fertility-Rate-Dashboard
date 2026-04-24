# How does access to safe drinking water in rural areas effect fertility rates? 

This dashboard explores how access to safe drinking water in rural areas correlates with national fertility rates. Using global data from 2000 to 2021, it visualizes whether improving basic infrastructure in rural communities leads to a decline in births per woman.

https://rural-water-access-and-fertility-rate-dashboard.streamlit.app/

## Key Features
- **Interactive Global Map:** Visualization of rural water access levels across 85+ countries.
- **Correlation Analysis:** Statistical breakdown of how water utility access impacts fertility trends.
- **Regional Deep-Dives:** Comparative analysis of Sub-Saharan Africa, South Asia, and other key global regions.
- **Dynamic Filtering:** Users can filter the entire dataset by year (2000–2021) and geographic region.

## Tech Stack
- **Language:** Python 3.x
- **Framework:** Streamlit
- **Visualizations:** Plotly Express & Graph Objects
- **Data Source:** World Bank (SP.DYN.TFRT.IN) and FAO AQUASTAT.
  
 See [requirements.txt](requirements.txt) for complete list.

## Data Source and Datasets
- **WorldBank** https://data.worldbank.org/
- **Rural population with access to safe drinking-water (JMP)** https://data360.worldbank.org/en/indicator/FAO_AS_4115
- **Fertility rate, total (births per woman)** https://data360.worldbank.org/en/indicator/WB_GS_SP_DYN_TFRT_IN
