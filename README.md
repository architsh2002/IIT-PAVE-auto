# IIT-PAVE-auto

# IITPAVE Batch Automation – Pavement Stress-Strain Analysis Tool

This project automates the simulation of flexible pavement responses using the IITPAVE software. The program systematically generates multiple combinations of pavement parameters, executes simulations via IITPAVE’s executable, extracts stress-strain results from the output file, and compiles the findings into a well-structured Excel workbook.

---

##  Objective

Performing iterative pavement response analyses manually in IITPAVE is inefficient when evaluating numerous material and geometric combinations. This tool provides a way to:

- Auto-generate input files for multiple cases
- Batch-run IITPAVE simulations
- Parse output stress-strain data at two key depths
- Export results in a tabular Excel format for comparison and plotting

---

##  How the Script Works

1. **Parameter Sweep**:  
   The code iterates over:
   - `mod_surf` (surface layer modulus),
   - `mod_base` (base layer modulus),
   - `thk_surf` (surface layer thickness)

2. **Input File Generation**:  
   For each combination, the script creates an `IITPAVE.in` file with layer properties and loading conditions.

3. **Execution of IITPAVE**:  
   The program automatically runs the IITPAVE analysis by invoking `IITPFILE.exe` using Python's `subprocess` module.

4. **Output Parsing**:  
   The output file `iitpave.out` is scanned using regular expressions. The script extracts:
   - Vertical stress (σz)
   - Tangential stress (σt)
   - Radial stress (σr)
   - Shear stress (τ)
   - Vertical strain (εz)
   - Tangential strain (εt)
   - Radial strain (εr)

   These are extracted at:
   - **Full depth of the surface layer (`z = h1`)**
   - **Half depth (`z = h1/2`)**

5. **Excel Compilation**:  
   Using the `openpyxl` library, results are recorded in an Excel workbook. A separate worksheet is created for each value of `mod_base`, storing results across all cases for easy filtering and visualization.

---

##  Output

- **Excel file**: `IITPAVE_Results_Tabular.xlsx`  
  Contains all stress and strain values across simulations, categorized by base modulus.

---

##  Technologies Used

- **Python 3** – scripting and automation
- **openpyxl** – for Excel workbook generation
- **subprocess** – to execute `.exe` files from within Python
- **re (regex)** – to parse floating-point and scientific notation output from IITPAVE
- **IITPFILE.exe** – pavement response calculator from the IITPAVE suite

---

##  Notes

- Ensure `IITPFILE.exe` is in the same directory as the script or update the path accordingly.
- The output assumes circular tire loading and a 3-layer pavement structure.
- Modify parameter ranges at the top of the script if you want to simulate different configurations.

---

##  Getting Started

Place the following files in the same folder:
- The Python script
- `IITPFILE.exe` (IITPAVE executable)

Then run:
```bash
python run_iitpave_batch.py

