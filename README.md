# cardio-vo2
Estimate and compare energy expenditure on treadmill incline walking and StairMaster using ACSM metabolic equations and Apple Watch readings.

Estimate and compare calorie expenditure on treadmill incline walking and StairMaster workouts
using ACSM metabolic equations and Apple Watch readings with uncertainty modeling.

## Why this project?
Most wearables misestimate energy expenditure. This repo builds a transparent,
reproducible pipeline that derives **theoretical kcal·min⁻¹** from ACSM equations and
compares them to **Apple Watch “active calories”** with a conservative ±28% error band.

## Key features
- **ACSM treadmill & stepping equations** (gross VO₂)
- **Reproducible kcal·min⁻¹** conversion at subject mass (80.3 kg)
- **Polished tables & plots** (exported HTML for one-click review)
- **Tested core functions** (PyTest) to ensure monotonic/units sanity

## Skills demonstrated
Python • NumPy/Pandas • Matplotlib • scientific computing • uncertainty modeling •
reproducible notebooks (nbconvert) • testing • documentation

## Repo structure
