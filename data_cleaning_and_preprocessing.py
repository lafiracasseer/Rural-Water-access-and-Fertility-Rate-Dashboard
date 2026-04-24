import pandas as pd

#LOADING DATASET FILES
RW= pd.read_csv("data/FAO_AS_4115.csv")
FR = pd.read_csv(data/WB_GS_SP_DYN_TFRT_IN.csv") 

print(f"Fertiltiy_rate raw shape:  {FR.shape}")
print(f"Rural_water  raw shape:  {RW.shape}")

#CLEANING RW(Rural Water Access)
#Keeping only needed columns and renaming column names
RW_clean = RW[["REF_AREA_LABEL", "TIME_PERIOD", "OBS_VALUE"]].copy()
RW_clean.columns = ["country", "year", "rural_water_access_pct"]

#Filtering years 2000-2022
RW_clean = RW_clean[RW_clean["year"].between(2000, 2022)]

#Converting to numeric and dropping non-numeric rows
RW_clean["rural_water_access_pct"] = pd.to_numeric(
    RW_clean["rural_water_access_pct"], errors="coerce"
)
RW_clean = RW_clean.dropna(subset=["rural_water_access_pct"])

print(f"\nRural_water clean shape: {RW_clean.shape}")
print(f"Rural_water countries:   {RW_clean['country'].nunique()}")

#CLEANING FR (Fertility Rate)
RW_countries = set(RW_clean["country"].unique())

FR_clean = FR[["REF_AREA_LABEL", "TIME_PERIOD", "OBS_VALUE"]].copy()
FR_clean.columns = ["country", "year", "fertility_rate"]

#Filtering years 2000-2022
FR_clean = FR_clean[FR_clean["year"].between(2000, 2022)]

#Removing aggregate/regional rows - keep only countries that exist in RW dataset
FR_clean = FR_clean[FR_clean["country"].isin(RW_countries)]

#Converting to numeric and dropping missing values
FR_clean["fertility_rate"] = pd.to_numeric(FR_clean["fertility_rate"], errors="coerce")
FR_clean = FR_clean.dropna(subset=["fertility_rate"])

print(f"\nFertility_rate  clean shape: {FR_clean.shape}")
print(f"Fertility_rate  countries:   {FR_clean['country'].nunique()}")

#MERGING BOTH THE DATASETS 
merged = pd.merge(FR_clean, RW_clean, on=["country", "year"], how="inner")

#ADDING REGION COLUMN
region_map = {
    #South Asia
    "Afghanistan":"South Asia","Bangladesh":"South Asia","India":"South Asia",
    "Nepal":"South Asia","Pakistan":"South Asia","Sri Lanka":"South Asia",
    "Bhutan":"South Asia","Maldives":"South Asia",
    #East Asia & Pacific
    "China":"East Asia & Pacific","Indonesia":"East Asia & Pacific",
    "Vietnam":"East Asia & Pacific","Philippines":"East Asia & Pacific",
    "Thailand":"East Asia & Pacific","Myanmar":"East Asia & Pacific",
    "Cambodia":"East Asia & Pacific","Malaysia":"East Asia & Pacific",
    "Papua New Guinea":"East Asia & Pacific","Mongolia":"East Asia & Pacific",
    "Lao PDR":"East Asia & Pacific","Timor-Leste":"East Asia & Pacific",
    #Latin America & Caribbean
    "Brazil":"Latin America & Caribbean","Colombia":"Latin America & Caribbean",
    "Mexico":"Latin America & Caribbean","Peru":"Latin America & Caribbean",
    "Bolivia":"Latin America & Caribbean","Ecuador":"Latin America & Caribbean",
    "Guatemala":"Latin America & Caribbean","Honduras":"Latin America & Caribbean",
    "Nicaragua":"Latin America & Caribbean","Paraguay":"Latin America & Caribbean",
    "El Salvador":"Latin America & Caribbean","Haiti":"Latin America & Caribbean",
    "Dominican Republic":"Latin America & Caribbean","Cuba":"Latin America & Caribbean",
    #Sub-Saharan Africa
    "Nigeria":"Sub-Saharan Africa","Ethiopia":"Sub-Saharan Africa",
    "Tanzania":"Sub-Saharan Africa","Kenya":"Sub-Saharan Africa",
    "Uganda":"Sub-Saharan Africa","Ghana":"Sub-Saharan Africa",
    "Mozambique":"Sub-Saharan Africa","Madagascar":"Sub-Saharan Africa",
    "Cameroon":"Sub-Saharan Africa","Zambia":"Sub-Saharan Africa",
    "Zimbabwe":"Sub-Saharan Africa","Malawi":"Sub-Saharan Africa",
    "Niger":"Sub-Saharan Africa","Mali":"Sub-Saharan Africa",
    "Burkina Faso":"Sub-Saharan Africa","Chad":"Sub-Saharan Africa",
    "Guinea":"Sub-Saharan Africa","Rwanda":"Sub-Saharan Africa",
    "Senegal":"Sub-Saharan Africa","Somalia":"Sub-Saharan Africa",
    "South Sudan":"Sub-Saharan Africa","Angola":"Sub-Saharan Africa",
    "Congo, Dem. Rep.":"Sub-Saharan Africa","Sierra Leone":"Sub-Saharan Africa",
    "Benin":"Sub-Saharan Africa","Togo":"Sub-Saharan Africa",
    "Eritrea":"Sub-Saharan Africa","Liberia":"Sub-Saharan Africa",
    "South Africa":"Sub-Saharan Africa","Namibia":"Sub-Saharan Africa",
    "Botswana":"Sub-Saharan Africa","Lesotho":"Sub-Saharan Africa",
    "Eswatini":"Sub-Saharan Africa","Central African Republic":"Sub-Saharan Africa",
    #Middle East & North Africa
    "Egypt":"Middle East & North Africa","Morocco":"Middle East & North Africa",
    "Algeria":"Middle East & North Africa","Tunisia":"Middle East & North Africa",
    "Sudan":"Middle East & North Africa","Yemen":"Middle East & North Africa",
    "Iraq":"Middle East & North Africa","Syria":"Middle East & North Africa",
    "Jordan":"Middle East & North Africa","Iran, Islamic Rep.":"Middle East & North Africa",
    "Libya":"Middle East & North Africa",
    #Europe & Central Asia
    "Turkey":"Europe & Central Asia","Ukraine":"Europe & Central Asia",
    "Uzbekistan":"Europe & Central Asia","Kazakhstan":"Europe & Central Asia",
    "Tajikistan":"Europe & Central Asia","Kyrgyz Republic":"Europe & Central Asia",
    "Turkmenistan":"Europe & Central Asia","Azerbaijan":"Europe & Central Asia",
    "Georgia":"Europe & Central Asia","Armenia":"Europe & Central Asia",
    "Moldova":"Europe & Central Asia",
}

merged["region"] = merged["country"].map(region_map).fillna("Other")

#Removing unmapped countries
merged = merged[merged["region"] != "Other"]

#FINAL CLEANING
merged["year"] = merged["year"].astype(int)
merged["fertility_rate"] = merged["fertility_rate"].round(3)
merged["rural_water_access_pct"] = merged["rural_water_access_pct"].round(2)
merged = merged.sort_values(["country", "year"]).reset_index(drop=True)

#Reordering columns
merged = merged[["country", "year", "region", "fertility_rate", "rural_water_access_pct"]]

#SAVING THE MERGED DATASET
merged.to_csv("data/merged_dataset.csv", index=False)

print(f"\nCLEANED DATASET SAVED")
print(f"   Rows:      {len(merged)}")
print(f"   Countries: {merged['country'].nunique()}")
print(f"   Years:     {merged['year'].min()} - {merged['year'].max()}")
print(f"   Regions:   {list(merged['region'].unique())}")
print(f"   Columns:   {list(merged.columns)}")
print(f"   Missing:   {merged.isna().sum().sum()} values")
