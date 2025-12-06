import json
import csv

# Data Visualization amd Processing Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Random Forest Modeling Imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

# Tree Visualisation (Not used currently :<)
# from sklearn.tree import export_graphviz
# from IPython.display import Image
# import graphviz

# ---------------------------------------------- Weapons ----------------------------------------------------------------
def loadWeaponData():
     # Step 1: Load weapon and spell data from JSON files
    weapons_items = []
    with open('weapons.json', 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                weapons_items.append(json.loads(line))
    # Step 2: Categorize weapons based on damage attributes
    WeaponDataDamage(weapons_items) # Categorize weapons based on damage values
    WeaponDataCrit(weapons_items) # Categorize weapons based on critical damage
    WeaponDataAttributes(weapons_items) # Categorize weapons based on damage attributes
    WeaponDataWeight(weapons_items) # Categorize weapons based on weight

def WeaponDataAttributes(weapons_items):
    # --------------------------------------------------------------
    NoStat = [] # List to hold No DMG items
    MagicStat = [] # List to hold Magic DMG items
    HolyStat = [] # List to hold Holy DMG items
    FireStat = [] # List to hold Fire DMG items
    LightningStat = [] # List to hold Lightning DMG items
    HybridStats = [] # List to hold Hybrid DMG items
    for i in weapons_items:
        if i["Magic_DMG"] == "0" and i["Holy_DMG"] == "0" and i["Fire_DMG"] == "0" and i["Lighting_DMG"] == "0":
            NoStat.append(i)
        elif i["Magic_DMG"] != "0" and i["Holy_DMG"] == "0" and i["Fire_DMG"] == "0" and i["Lighting_DMG"] == "0":
            MagicStat.append(i)
        elif i["Holy_DMG"] != "0" and i["Magic_DMG"] == "0" and i["Fire_DMG"] == "0" and i["Lighting_DMG"] == "0":
            HolyStat.append(i)
        elif i["Fire_DMG"] != "0" and i["Magic_DMG"] == "0" and i["Holy_DMG"] == "0" and i["Lighting_DMG"] == "0":
            FireStat.append(i)
        elif i["Lighting_DMG"] != "0" and i["Magic_DMG"] == "0" and i["Holy_DMG"] == "0" and i["Fire_DMG"] == "0":
            LightningStat.append(i)
        else:
            HybridStats.append(i)

    # Testing Outputs        
    print(NoStat)
    print("There are " + str(len(NoStat)) + " No DMG Stats Weapons")
    NoStatWeapons = len(NoStat)
    print("--------------------------------------------------------------\n")
    print(MagicStat)
    print("There are " + str(len(MagicStat)) + " Magic only Stats Weapons")
    MagicStatWeapons = len(MagicStat)
    print("--------------------------------------------------------------\n")
    print(HolyStat)
    print("There are " + str(len(HolyStat)) + " Holy only Stats Weapons")
    HolyStatWeapons = len(HolyStat)
    print("--------------------------------------------------------------\n")
    print(FireStat)
    print("There are " + str(len(FireStat)) + " Fire only Stats Weapons")
    FireStatWeapons = len(FireStat)
    print("--------------------------------------------------------------\n")
    print(LightningStat)
    print("There are " + str(len(LightningStat)) + " Lightning only Stats Weapons")
    LightningStatWeapons = len(LightningStat)
    print("--------------------------------------------------------------\n")
    print(HybridStats)
    print("There are " + str(len(HybridStats)) + " Hybrid Stats Weapons")
    HybridStatWeapons = len(HybridStats)
    AllWeapons = NoStatWeapons + MagicStatWeapons + HolyStatWeapons + FireStatWeapons + LightningStatWeapons + HybridStatWeapons
    # --------------------------------------------------------------
   # Step 2: We create a plot to visualize the distribution of weapons and spells based on their stat requirements
    xaxis = np.array(['No DMG', 'Magic DMG', 'Holy DMG', 'Fire DMG', 'Lightning DMG', 'Hybrid DMG'])
    yaxis = np.array([NoStatWeapons, MagicStatWeapons, HolyStatWeapons, FireStatWeapons, LightningStatWeapons, HybridStatWeapons])
    plt.bar(xaxis, yaxis, color='blue', edgecolor='black')
    plt.title("Distribution of Weapons by DMG Attribute")
    plt.xlabel("DMG Type")
    plt.ylabel("Number of Weapons")
    plt.show()

def WeaponDataDamage(weapons_items):
    AttDMG = []
    for i in weapons_items:
        AttDMG.append(int(i["AttDMG"]))
    plt.hist(AttDMG, bins=40, color='green', edgecolor='black')
    plt.title("Distribution of Weapons Flat Attack Damage")
    plt.xlabel("Attack Damage")
    plt.ylabel("Number of Weapons")
    plt.show()

def WeaponDataWeight(weapons_items):
    Weights = []
    for i in weapons_items:
        Weights.append(eval(i["Weight"]))
    plt.hist(Weights, bins=40, color='green', edgecolor='black')
    plt.title("Distribution of Weapons Based on Weight")
    plt.xlabel("Weight")
    plt.ylabel("Number of Weapons")
    plt.show()

def WeaponDataCrit(weapons_items):
    Crits = []
    for i in weapons_items:
        Crits.append(int(i["Crit"]))
    plt.hist(Crits, bins=4, range=(min(Crits), max(Crits)), color='green', edgecolor='black')
    plt.title("Distribution of Weapons Based on Critical Damage Multiplier")
    plt.xlabel("Critical Damage Multiplier")
    plt.ylabel("Number of Weapons")
    plt.show()
# ------------------------------------------------- Spells ----------------------------------------------------------------
def loadSpellData():
    spells_items = []
    with open('spells.json', 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                spells_items.append(json.loads(line))
    # Step 2: Grouping Spells based on stat requirements for visualization
    IntelligenceSpells = []
    FaithSpells = []
    ArcaneSpells = []
    HybridSpells = []
    for i in spells_items:
        if i["Required Intelligence"] != 0 and i["Required Faith"] == 0 and i["Required Arcane"] == 0:
            IntelligenceSpells.append(i)
        elif i["Required Faith"] != 0 and i["Required Intelligence"] == 0 and i["Required Arcane"] == 0 :
            FaithSpells.append(i)
        elif i["Required Arcane"] != 0 and i["Required Intelligence"] == 0 and i["Required Faith"] == 0:
            ArcaneSpells.append(i)
        else:
            HybridSpells.append(i)

    # Testing Outputs
    print("Total Spells: " + str(len(spells_items)) + "\n")
    print("--------------------------------------------------------------\n")
    print(IntelligenceSpells)
    print("There are " + str(len(IntelligenceSpells)) + " Intelligence only Spells")
    print("--------------------------------------------------------------\n")
    print(FaithSpells)
    print("There are " + str(len(FaithSpells)) + " Faith only Spells")
    print("--------------------------------------------------------------\n")
    print(ArcaneSpells)
    print("There are " + str(len(ArcaneSpells)) + " Arcane only Spells")
    print("--------------------------------------------------------------\n")
    print(HybridSpells)
    print("There are " + str(len(HybridSpells)) + " Hybrid Spells")
    print("--------------------------------------------------------------\n")

    # ---------------------------------------------- Plot Visualizations ------------------------------------------------
    # Inelligence Spells Only plot
    SpellDataIntelligence(IntelligenceSpells)

    # Faith Spells Only plot
    SpellDataFaith(FaithSpells)

    # Arcane Spells Only plot
    SpellDataArcane(ArcaneSpells)

    # Hybrid Spells Only plot
    SpellDataHybrid(HybridSpells, IntelligenceSpells, FaithSpells, ArcaneSpells) 

    # Total Stat Requirements for all Spells plot
    SpellDataTotalReqs(spells_items)

def SpellDataIntelligence(IntelligenceSpells):
    plt.hist([int(i["Required Intelligence"]) for i in IntelligenceSpells], bins=31, color='purple', edgecolor='black')
    plt.title("Distribution of Intelligence Only Spells Based on Intelligence Requirements")
    plt.xlabel("Total Intelligence Requirement")
    plt.ylabel("Number of Spells")
    plt.show()

def SpellDataFaith(FaithSpells):
    plt.hist([int(i["Required Faith"]) for i in FaithSpells], bins= 50, color='purple', edgecolor='black')
    plt.title("Distribution of Faith Only Spells Based on Faith Requirements")
    plt.xlabel("Faith Requirement")
    plt.ylabel("Number of Spells")
    plt.show()

def SpellDataArcane(ArcaneSpells):
    plt.hist([int(i["Required Arcane"]) for i in ArcaneSpells], bins=4, color='purple', edgecolor='black')
    plt.title("Distribution of Arcane Only Spells Based on Arcane Requirements")
    plt.xlabel("Total Arcane Requirement")
    plt.ylabel("Number of Spells")
    plt.show()

def SpellDataHybrid(HybridSpells, IntelligenceSpells=[], FaithSpells=[], ArcaneSpells=[]):
    xaxis = np.array(['Hybrid Stat Req', 'Single Stat Req'])
    yaxis = np.array([len(HybridSpells), len(IntelligenceSpells) + len(FaithSpells) + len(ArcaneSpells)])
    plt.bar(xaxis, yaxis, color='purple', edgecolor='black')
    plt.title("Distribution of Hybrid vs Single Stat Spells")
    plt.xlabel("Spell Type")
    plt.ylabel("Number of Spells")
    plt.show()

def SpellDataTotalReqs(spells_items):
    TotalReqs = []
    for i in spells_items:
        TotalReqs.append(int(i["TotalReq"]))
    plt.hist(TotalReqs, bins=51, color='purple', edgecolor='black')
    plt.title("Distribution of Spells Based on Total Stat Requirements")
    plt.xlabel("Total Stat Requirements (Intelligence + Faith + Arcane)")
    plt.ylabel("Number of Spells")
    plt.show()

# ---------------------------------------------- Random Forest Rare Sets Analysis ------------------------------------------------

def RandomForestRareSets():
    # ========================= Step 1: Merge Weapon and Spell Data =========================
    data = MergeData() # Weapon and Spell Data combined into "Sets"
    df = CreateLabels(data) # Create Rarity Labels

    # ========================= Step 2: Prepare feature matrix and target vector =========================
    feature_columns = [
        'AttDMG', 'Crit', 'Magic_DMG', 'Fire_DMG', 
        'Lighting_DMG', 'Holy_DMG', 'Weight',
        'TotalReq', 'Required Intelligence', 
        'Required Faith', 'Required Arcane']
    X = df[feature_columns].copy() # Feature matrix
    # Convert all to numeric and fill missing values
    for col in feature_columns:
        X[col] = pd.to_numeric(X[col], errors='coerce')
    X = X.fillna(0) # Fill NaN with 0
    y = df['Rarity'] # Target variable

    # Split into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {len(X_train)} items") # Training set size
    print(f"Testing set: {len(X_test)} items\n") # Testing set size

    print("Training set:\n" + str(X_train) + "\n")
    print("Testing set:\n" + str(X_test) + "\n")

    # ========================= Step 3: Create and train the Random Forest model =========================
    rf_model = RandomForestClassifier(
        n_estimators=100,      # Number of trees in the forest
        max_depth=10,          # Maximum depth of each tree
        min_samples_split=5,   # Minimum samples to split a node
        random_state=42,       # For reproducibility
        n_jobs=-1              # Use all CPU cores?
    )
    print("TRAINING THE MODEL...\n")
    rf_model.fit(X_train, y_train) # Train the Random Forest model
    
    # ========================= Step 4: Make predictions and evaluate the model =========================
    print("MAKING PREDICTIONS...\n")
    y_pred = rf_model.predict(X_test) # Predict on the test set
    accuracy = accuracy_score(y_test, y_pred) # Calculate accuracy
    print(f"=========== Model Accuracy: {accuracy:.2f} ===========\n") # Print accuracy
    print(classification_report(y_test, y_pred)) # Detailed classification report

    # ========================= Step 5: Confusion Matrix Visualization =========================
    print("\n+------------------ Confusion Matrix ------------------+")
    print("Random Forest Model Classifer results: " + "test: " + str(y_test.shape[0]) + ", correct: " + str((y_test == y_pred).sum()) + ", incorrect: " + str((y_test != y_pred).sum()) + "\n")
    cm = confusion_matrix(y_test, y_pred, labels=rf_model.classes_)
    print(f"  Correct Common predictions: {cm[0][0]}")
    print(f"  Common wrongly classified as Rare: {cm[0][1]}")
    print(f"  Rare wrongly classified as Common: {cm[1][0]}")
    print(f"  Correct Rare predictions: {cm[1][1]}")
    print("\n")
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=rf_model.classes_)
    disp.plot(cmap=plt.cm.Blues)
    disp.ax_.set_title("Random Forest Classifier Confusion Matrix")
    plt.show()

def classify_rarity(row):
    # Check if it's a rare set
    has_extra_dmg = row['NonZero_DMG_Count'] >= 1
    has_multiple_reqs = row['NonZero_Req_Count'] >= 2
    
    if has_extra_dmg and has_multiple_reqs:
        return 'Rare'
    else:
        return 'Common'

def CreateLabels(data):    
    df = data.copy()
    # Convert all relevant columns to numeric
    numeric_cols = ['AttDMG', 'Magic_DMG', 'Fire_DMG', 'Lighting_DMG', 'Holy_DMG',
                    'Required Intelligence', 'Required Faith', 'Required Arcane']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df[numeric_cols] = df[numeric_cols].fillna(0) # Fill NaN with 0

    # Count non-zero Weapon damage types (excluding AttDMG)
    # .astype(int) converts boolean to integer (True=1, False=0)
    df['NonZero_DMG_Count'] = (
        (df['Magic_DMG'] > 0).astype(int) +
        (df['Fire_DMG'] > 0).astype(int) +
        (df['Lighting_DMG'] > 0).astype(int) +
        (df['Holy_DMG'] > 0).astype(int)
    )
    
    # Count non-zero Spell requirements
    # .astype(int) converts boolean to integer (True=1, False=0)
    df['NonZero_Req_Count'] = (
        (df['Required Intelligence'] > 0).astype(int) +
        (df['Required Faith'] > 0).astype(int) +
        (df['Required Arcane'] > 0).astype(int)
    )

    df['Rarity'] = df.apply(classify_rarity, axis=1) # Apply classification to each row
    return df

def MergeData():
     # Combine weapon and spell data into a single DataFrame
    weapons = []
    with open('weapons.json', 'r') as f:
        for line in f:
            weapons.append(json.loads(line.strip()))
    
    spells = []
    with open('spells.json', 'r') as f:
        for line in f:
            spells.append(json.loads(line.strip()))

    combined = []
    for weapon, spell in zip(weapons, spells):
        # Merge the two dictionaries
        merged = {**weapon, **spell}
        combined.append(merged)

    with open('combined_horizontal.json', 'w') as f:
        for item in combined:
            f.write(json.dumps(item) + '\n')
    
    # Load into pandas DataFrame
    data = pd.read_json('combined_horizontal.json', lines=True) # Load combined data
     # Save combined data as CSV
    data.to_csv('combined_horizontal.csv', index=False) # Save as CSV 
    return data

def main():
   # Step 1: Load and process weapon and spell data
   print("Loading Weapon Data...\n")
   loadWeaponData()
   print("\n==============================================================\n")
   print("Loading Spell Data...\n")
   loadSpellData()

   # Step 2: Random Forest Rare Sets Analysis
   print("\n==============================================================\n")
   RandomForestRareSets()
   

if __name__ == "__main__":
    main()