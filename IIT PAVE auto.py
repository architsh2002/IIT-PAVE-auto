import subprocess
import re
from openpyxl import Workbook

# --- Constants (Renamed for clarity) ---
MOD_GRANULAR = 240.2
MOD_SUBGRADE = 76.8
THK_GRANULAR = 450
THK_BASE = 100
POISSON = 0.35
TYRE_RADIUS_M = 0.56
AXLE_LOAD = 20000

# --- Parameter Ranges ---
mod_surface_options = [2000, 2500, 3000, 3500, 4000]
mod_base_options = [300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
surf_thickness_options = [float(x) for x in range(40, 160, 10)]

# --- File paths ---
EXECUTABLE = "IITPFILE.exe"
OUTPUT_FILE = "iitpave.out"
INPUT_FILE = "IITPAVE.in"
EXCEL_FILE = "IITPAVE_Results_Tabular.xlsx"

# --- Initialize Workbook ---
wb = Workbook()
wb.remove(wb.active)

# --- Helper: Create IITPAVE input file ---
def write_input_file(mod_surf, mod_base, thk_surf):
    with open(INPUT_FILE, "w") as inp:
        inp.write("4\n")
        inp.write(f"{mod_surf} {mod_base} {MOD_GRANULAR} {MOD_SUBGRADE}\n")
        inp.write(f"{POISSON} {POISSON} {POISSON} {POISSON}\n")
        inp.write(f"{thk_surf} {THK_BASE} {THK_GRANULAR}\n")
        inp.write(f"{AXLE_LOAD} {TYRE_RADIUS_M}\n")
        inp.write("2\n")
        inp.write(f"{thk_surf} 0\n")
        inp.write(f"{thk_surf / 2} 0\n")
        inp.write("2\n")

# --- Helper: Parse IITPAVE output file ---
def extract_stresses(thk_surf):
    stress_data = {"full": {}, "half": {}}
    with open(OUTPUT_FILE, "r") as file:
        for line in file:
            matches = re.findall(r'[-+]?\d*\.\d+(?:[Ee][-+]?\d+)?', line)
            if len(matches) >= 10:
                try:
                    depth = float(matches[0].replace("L", ""))
                    radius = float(matches[1])
                    if radius != 0:
                        continue
                    values = {
                        "sigz": matches[2],
                        "sigt": matches[3],
                        "sigr": matches[4],
                        "tau":  matches[5],
                        "epz":  matches[7],
                        "ept":  matches[8],
                        "epr":  matches[9],
                    }
                    if abs(depth - thk_surf) < 1e-3:
                        stress_data["full"] = values
                    elif abs(depth - thk_surf / 2) < 1e-3:
                        stress_data["half"] = values
                except:
                    continue
    return stress_data

# --- Main Execution ---
for mod_base in mod_base_options:
    sheet = wb.create_sheet(title=f"Base_{mod_base}")
    sheet.append([
        "SurfMod", "ModRatio", "Thickness",
        "σz_h1", "σt_h1", "σr_h1", "τ_h1", "εz_h1", "εt_h1", "εr_h1",
        "σz_h1/2", "σt_h1/2", "σr_h1/2", "τ_h1/2", "εz_h1/2", "εt_h1/2", "εr_h1/2",
    ])
    
    for mod_surf in mod_surface_options:
        for thk_surf in surf_thickness_options:
            # Prepare input for IITPAVE
            write_input_file(mod_surf, mod_base, thk_surf)

            # Execute IITPAVE externally
            subprocess.run([EXECUTABLE], check=True)

            # Read output values
            results = extract_stresses(thk_surf)

            # Assemble row
            data_row = [mod_surf, round(mod_surf / mod_base, 2), thk_surf]
            for param in ["sigz", "sigt", "sigr", "tau", "epz", "ept", "epr"]:
                data_row.append(results["full"].get(param, ""))
            for param in ["sigz", "sigt", "sigr", "tau", "epz", "ept", "epr"]:
                data_row.append(results["half"].get(param, ""))

            sheet.append(data_row)

# --- Save workbook ---
wb.save(EXCEL_FILE)
