# 🚒 Autonomous Raspberry Pi Fire Brigade System

An autonomous, thermal-guided emergency response vehicle powered by a Raspberry Pi. Utilizing an MLX90614 non-contact infrared sensor mounted on a 2-axis pan/tilt gimbal, the system scans hazardous environments for thermal anomalies in real time. Upon detecting temperatures exceeding preset safety thresholds, the vehicle halts chassis movement, locks onto the heat source, and deploys a high-flow water pump via relay to execute targeted suppression sweeps until safe ambient levels are restored.

---

## 📁 Repository Structure

```text
.
├── .github/
│   └── copilot-instructions.md   # Hardware rules & context for GitHub Copilot
├── main.py                       # Main autonomous state machine script
├── schematic.txt                 # Circuit diagram and pinout reference
├── .gitignore                    # Git tracking exclusion list
└── README.md                     # Project documentation
