"""
AI Rule-Based Clinical Decision Support Engine
Maps diseases to clinical suggestions, drug warnings, and care protocols.
"""

DISEASE_PROTOCOLS = {
    "diabetes": {
        "severity": "chronic",
        "suggestions": [
            "Monitor fasting blood glucose daily (target: 80–130 mg/dL)",
            "HbA1c test every 3 months; target < 7%",
            "Prescribe Metformin 500mg as first-line therapy if not contraindicated",
            "Refer to dietitian for low-GI dietary planning",
            "Annual dilated eye exam and foot inspection",
            "Screen for nephropathy: urine albumin-creatinine ratio",
        ],
        "drug_alerts": ["Avoid NSAIDs — risk of renal impairment", "Caution with contrast dye (CT/MRI) — hold Metformin 48h before"],
        "follow_up": "Every 3 months",
        "badge": "chronic",
    },
    "hypertension": {
        "severity": "moderate",
        "suggestions": [
            "Target BP < 130/80 mmHg; monitor twice daily at home",
            "First-line: ACE inhibitor (Lisinopril 10mg) or ARB",
            "Advise DASH diet: reduce sodium < 2.3g/day",
            "Encourage 150 min/week moderate aerobic exercise",
            "Check renal function and electrolytes every 6 months",
            "ECG to rule out left ventricular hypertrophy",
        ],
        "drug_alerts": ["Avoid Pseudoephedrine (decongestants) — raises BP", "Monitor potassium with ACE inhibitors"],
        "follow_up": "Every 1 month until stable, then every 6 months",
        "badge": "moderate",
    },
    "pneumonia": {
        "severity": "acute",
        "suggestions": [
            "Chest X-ray (PA view) to confirm consolidation",
            "Sputum culture and sensitivity before starting antibiotics",
            "Empiric therapy: Amoxicillin-Clavulanate + Azithromycin (community-acquired)",
            "SpO₂ monitoring; supplement O₂ if < 94%",
            "Adequate hydration — IV fluids if oral intake is poor",
            "Reassess at 48–72h; escalate to ICU if CURB-65 score ≥ 3",
        ],
        "drug_alerts": ["Avoid fluoroquinolones in children", "Check penicillin allergy before Amoxicillin"],
        "follow_up": "48–72 hour review; chest X-ray in 6 weeks post-recovery",
        "badge": "acute",
    },
    "asthma": {
        "severity": "moderate",
        "suggestions": [
            "Prescribe short-acting beta₂-agonist (Salbutamol) as reliever",
            "Add inhaled corticosteroid (Budesonide) for persistent symptoms",
            "Assess inhaler technique at every visit",
            "Peak flow monitoring: record twice daily",
            "Identify and avoid triggers (dust, pollen, smoke, cold air)",
            "Provide written Asthma Action Plan",
        ],
        "drug_alerts": ["Avoid beta-blockers — may precipitate bronchospasm", "NSAIDs can worsen asthma in aspirin-sensitive patients"],
        "follow_up": "Every 1–3 months until stable",
        "badge": "moderate",
    },
    "depression": {
        "severity": "mental",
        "suggestions": [
            "Administer PHQ-9 scale; score ≥ 10 indicates moderate depression",
            "First-line pharmacotherapy: SSRI (Sertraline 50mg or Escitalopram 10mg)",
            "Refer to psychologist for Cognitive Behavioral Therapy (CBT)",
            "Screen for suicidal ideation at every visit",
            "Lifestyle interventions: regular exercise, sleep hygiene, social support",
            "Review medication response at 4–6 weeks; titrate dose if needed",
        ],
        "drug_alerts": ["Risk of serotonin syndrome with MAOIs — do not combine", "Monitor for increased suicidality in patients < 25 years on SSRIs"],
        "follow_up": "Weekly for first month, then monthly",
        "badge": "mental",
    },
    "heart failure": {
        "severity": "critical",
        "suggestions": [
            "Echocardiogram to assess ejection fraction (EF)",
            "Prescribe ACE inhibitor + beta-blocker + diuretic (HFrEF protocol)",
            "Strict fluid restriction: < 1.5L/day",
            "Daily weight monitoring; alert if gain > 2kg in 2 days",
            "Sodium restriction < 2g/day",
            "Refer to cardiologist for device therapy evaluation (ICD/CRT) if EF < 35%",
        ],
        "drug_alerts": ["Avoid NSAIDs — worsen fluid retention and renal function", "Avoid calcium channel blockers (Verapamil/Diltiazem) in HFrEF"],
        "follow_up": "Weekly until stable, then monthly",
        "badge": "critical",
    },
    "tuberculosis": {
        "severity": "infectious",
        "suggestions": [
            "Confirm with sputum AFB smear, GeneXpert, and chest X-ray",
            "Initiate DOTS therapy: RHEZ (Rifampicin, Isoniazid, Ethambutol, Pyrazinamide) for 2 months",
            "Continuation phase: RH for 4 months (total 6-month regimen)",
            "Notify to public health authorities — TB is a notifiable disease",
            "Contact tracing for household members",
            "Pyridoxine (Vit B6) 25mg daily with Isoniazid to prevent neuropathy",
        ],
        "drug_alerts": ["Rifampicin reduces efficacy of OCP, warfarin, and many antiretrovirals", "Monitor liver enzymes monthly — hepatotoxicity risk"],
        "follow_up": "Monthly sputum smear; end-of-treatment evaluation",
        "badge": "infectious",
    },
    "anemia": {
        "severity": "moderate",
        "suggestions": [
            "CBC, peripheral blood smear, serum ferritin, B12, folate levels",
            "Iron deficiency: Ferrous Sulfate 325mg three times daily with Vitamin C",
            "B12 deficiency: Cyanocobalamin 1000 mcg IM monthly",
            "Identify and treat underlying cause (GI bleed, menorrhagia, poor diet)",
            "Dietary counseling: red meat, leafy greens, legumes, fortified cereals",
            "Transfuse if Hb < 7 g/dL or symptomatic",
        ],
        "drug_alerts": ["Iron supplements reduce absorption of fluoroquinolones and levothyroxine — space by 2h", "Antacids reduce iron absorption — avoid concurrent use"],
        "follow_up": "Recheck CBC in 4–6 weeks",
        "badge": "moderate",
    },
}

DEFAULT_PROTOCOL = {
    "severity": "general",
    "suggestions": [
        "Conduct a thorough clinical history and physical examination",
        "Order relevant baseline investigations (CBC, CMP, urinalysis)",
        "Establish a differential diagnosis and document findings",
        "Review current medications for interactions or contraindications",
        "Educate patient on red-flag symptoms requiring urgent review",
        "Schedule follow-up within 1–2 weeks",
    ],
    "drug_alerts": ["Review all current medications for potential interactions"],
    "follow_up": "Within 1–2 weeks",
    "badge": "general",
}


def get_suggestions(disease: str) -> dict:
    """Return clinical decision support data for a given disease."""
    key = disease.strip().lower()
    for disease_key, protocol in DISEASE_PROTOCOLS.items():
        if disease_key in key or key in disease_key:
            return {"disease": disease, **protocol}
    return {"disease": disease, **DEFAULT_PROTOCOL}