# Google Play Store Dashboard

An interactive data visualization dashboard analyzing Google Play Store applications, focusing on app categories, content ratings, installs, reviews, and user ratings.

This project uses Python and Altair to generate linked, interactive charts for exploratory data analysis of Google Play Store data.

---
## Dashboard Preview

### Dashboard 1
<img width="1100" height="804" alt="visualization (3) copy" src="https://github.com/user-attachments/assets/78f03154-91a4-48b5-9842-225a53b6d035" />

### Dashboard 2
<img width="1473" height="849" alt="visualization (3) copy 2" src="https://github.com/user-attachments/assets/8ccbca63-7a8d-46b5-a0e9-a2efd820b311" />

---
## Dashboard Overview

The dashboard allows users to explore:

* App distribution across categories
* Install counts and popularity patterns
* User ratings and review volume
* Content rating composition
* Relationships between installs, reviews, and ratings

The final output is an interactive HTML dashboard generated programmatically.

---

## Key Features

* Category-level breakdown of Google Play Store apps
* Install distribution and popularity trends
* Ratings vs. review count scatter plots
* Content rating analysis across categories
* Interactive filtering and linked charts using Altair

---

## Tech Stack

* Python 3.12+
* Pandas
* NumPy
* Altair

---


## Setup Instructions

### 1) Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python google_play_dashboard.py or google_play_heatmap_dashboard.py
```

After the script finishes, open the generated dashboard:

```
visuals/google_play_dashboard.html
```

in your web browser.

---



