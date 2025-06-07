# DamnedStatistics  

## Introduction  
*"There are 3 kinds of lies: lies, damned lies, and statistics."* —Mark Twain  

DamnedStatistics is a CSV editor with extended functionality that enables multiple records from multiple datasets to be easily entered into a prompt, generating AI responses that can be exported for further analysis.  

## Installation Prerequisites  
### General Requirements  
1. Ensure you have Python installed: [Download Python](https://www.python.org/downloads/)  
2. Set up your workspace and navigate to it in VSCode or another preferred code editor.  
3. Open the terminal and run:  
   ```
   pip install -r requirements.txt
   ```

### Gemini API Key Setup  
1. Visit the [Google Gemini API documentation](https://ai.google.dev/gemini-api/docs/api-key).  
2. Create a project at [Google Cloud Console](https://console.cloud.google.com/projectcreate?pli=1&inv=1&invt=AbzgOw).  
3. Select **Create API Key**, then **Project** from the dashboard.  
4. Copy your API key for use in DamnedStatistics.  

---

## This software currently follows the UK governments Stndard for CSV
https://www.gov.uk/government/publications/recommended-open-standards-for-government/tabular-data-standard

## Getting Started  
To run DamnedStatistics, execute the `UI.py` file located in the `frontend` folder.  

> **Note:** A Gemini API key is required for AI-generated responses.  

1. Select data cells to include.
2. Click **"Add selected data to prompt"** to transfer rows into the AI input.  
3. Rows with selected data are added to the prompt, with column headers, and "NI" marking unselected data in included rows.  

> **Note:** If the dataset contains significant missing data, Gemini AI will generate lower-quality responses.  

Upon prompt submission, the software waits for a response from the Gemini API and then displays the generated response in a pop-up window.  

---

Citation and Terms of Use
- Scope of License As defined by https://creativecommons.org/share-your-work/cclicenses/
CC BY-NC-SA

This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format for noncommercial purposes only, and only so long as attribution is given to the creator. If you remix, adapt, or build upon the material, you must license the modified material under identical terms. CC BY-NC-SA.
- Restrictions
- Users agree not to employ automated systems, algorithms, or processes—including but not limited to web crawlers, data scraping tools, or AI models—to extract or analyse any part of this software or its associated data.
- The software or its contents shall not be integrated into training datasets for machine learning or AI systems. The outputted data may be used in non-commercial AI training.
- Users agree not to attempt reverse engineering, decompiling, disassembling, or modifying any part of the software, unless the altered software is made available as open source
- Acceptance By downloading, installing, or using the software, users acknowledge that they have read, understood, and agreed to these terms of use.
