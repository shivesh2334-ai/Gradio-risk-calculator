%%writefile app.py
import gradio as gr
from utils_risk_calculator import RiskCalculator
from utils_data_validator import DataValidator
from utils_claude_integration import ClaudeIntegration
import config

def assess_patient_risk(
    age: int,
    gender: str,
    height: float,
    weight: float,
    smoking: str,
    alcohol: str,
    exercise: str,
    diet: str,
    diabetes_history: bool,
    depression_history: bool,
    family_diabetes: bool,
    family_hypertension: bool,
    family_cancer: str,
    systolic_bp: int,
    diastolic_bp: int,
    heart_rate: int,
    fasting_glucose: float,
    hba1c: float,
    total_cholesterol: float,
    ldl_cholesterol: float,
    hdl_cholesterol: float
):
    """
    Calculates patient risk and gets AI insights.

    Args:
        age: Patient's age.
        gender: Patient's gender.
        height: Patient's height in cm.
        weight: Patient's weight in kg.
        smoking: Smoking status.
        alcohol: Alcohol consumption level.
        exercise: Exercise level.
        diet: Diet pattern.
        diabetes_history: History of gestational diabetes.
        depression_history: History of depression/mental health issues.
        family_diabetes: Family history of diabetes.
        family_hypertension: Family history of hypertension.
        family_cancer: Family history of cancer type.
        systolic_bp: Systolic blood pressure.
        diastolic_bp: Diastolic blood pressure.
        heart_rate: Heart rate.
        fasting_glucose: Fasting glucose level.
        hba1c: HbA1c level.
        total_cholesterol: Total cholesterol level.
        ldl_cholesterol: LDL cholesterol level.
        hdl_cholesterol: HDL cholesterol level.

    Returns:
        A formatted string containing risk assessment and AI insights.
    """
    patient_data = {
        'age': age,
        'gender': gender,
        'height': height,
        'weight': weight,
        'bmi': weight / ((height/100)**2),
        'smoking': smoking,
        'alcohol': alcohol,
        'exercise': exercise,
        'diet': diet,
        'diabetes_history': diabetes_history,
        'depression_history': depression_history,
        'family_diabetes': family_diabetes,
        'family_hypertension': family_hypertension,
        'family_cancer': family_cancer,
        'systolic_bp': systolic_bp,
        'diastolic_bp': diastolic_bp,
        'heart_rate': heart_rate,
        'fasting_glucose': fasting_glucose,
        'hba1c': hba1c,
        'total_cholesterol': total_cholesterol,
        'ldl_cholesterol': ldl_cholesterol,
        'hdl_cholesterol': hdl_cholesterol
    }

    risk_calculator = RiskCalculator()
    claude_integration = ClaudeIntegration(config.CLAUDE_API_KEY)

    risk_results = risk_calculator.calculate_all_risks(patient_data)
    ai_insights = claude_integration.get_risk_insights(patient_data, risk_results)

    formatted_output = "## Risk Assessment Results\n\n"
    for condition, result in risk_results.items():
        formatted_output += f"- **{condition.replace('_', ' ').title()}:** {result['risk_percentage']:.1f}% (Key Factors: {', '.join(result['key_factors'])})\n"

    formatted_output += "\n## AI-Powered Clinical Insights\n\n"
    formatted_output += ai_insights

    return formatted_output

# Define input components within a Blocks context
with gr.Blocks() as demo:
    gr.Markdown("### Basic Information")
    age_input = gr.Slider(minimum=18, maximum=100, value=45, label="Age")
    gender_input = gr.Radio(["Female", "Male", "Other"], label="Gender", value="Female")
    height_input = gr.Number(minimum=100, maximum=250, value=165, label="Height (cm)")
    weight_input = gr.Number(minimum=30, maximum=200, value=70, label="Weight (kg)")

    gr.Markdown("### Lifestyle Factors")
    smoking_input = gr.Radio(["Never", "Former", "Current"], label="Smoking Status", value="Never")
    alcohol_input = gr.Radio(["None", "Occasional", "Moderate", "Heavy"], label="Alcohol Consumption", value="None")
    exercise_input = gr.Radio(["Sedentary", "Light", "Moderate", "Active", "Very Active"], label="Exercise Level", value="Sedentary")
    diet_input = gr.Radio(["Standard", "Mediterranean", "Plant-based", "Low-carb", "Other"], label="Diet Pattern", value="Standard")

    gr.Markdown("### Medical History")
    diabetes_history_input = gr.Checkbox(label="History of Gestational Diabetes")
    depression_history_input = gr.Checkbox(label="History of Depression/Mental Health Issues")

    gr.Markdown("### Family History")
    family_diabetes_input = gr.Checkbox(label="Family History - Diabetes")
    family_hypertension_input = gr.Checkbox(label="Family History - Hypertension")
    family_cancer_input = gr.Radio(["None", "Breast", "Prostate", "Lung", "Colorectal", "Other"], label="Family Cancer History", value="None")

    gr.Markdown("### Vital Signs")
    systolic_bp_input = gr.Number(minimum=70, maximum=200, value=128, label="Systolic BP (mmHg)")
    diastolic_bp_input = gr.Number(minimum=40, maximum=120, value=82, label="Diastolic BP (mmHg)")
    heart_rate_input = gr.Number(minimum=40, maximum=150, value=72, label="Heart Rate (bpm)")

    gr.Markdown("### Laboratory Results")
    fasting_glucose_input = gr.Number(minimum=50, maximum=300, value=97, label="Fasting Glucose (mg/dL)")
    hba1c_input = gr.Number(minimum=3.0, maximum=15.0, value=5.7, step=0.1, label="HbA1c (%)")
    total_cholesterol_input = gr.Number(minimum=100, maximum=400, value=201, label="Total Cholesterol (mg/dL)")
    ldl_cholesterol_input = gr.Number(minimum=50, maximum=300, value=120, label="LDL Cholesterol (mg/dL)")
    hdl_cholesterol_input = gr.Number(minimum=20, maximum=100, value=54, label="HDL Cholesterol (mg/dL)")


    # Define output component
    output_text = gr.Markdown(label="Risk Assessment and Insights")

    # Create a button to trigger the risk assessment
    submit_button = gr.Button("Assess Risk")

    # Link the button click to the function and outputs
    submit_button.click(
        fn=assess_patient_risk,
        inputs=[
            age_input,
            gender_input,
            height_input,
            weight_input,
            smoking_input,
            alcohol_input,
            exercise_input,
            diet_input,
            diabetes_history_input,
            depression_history_input,
            family_diabetes_input,
            family_hypertension_input,
            family_cancer_input,
            systolic_bp_input,
            diastolic_bp_input,
            heart_rate_input,
            fasting_glucose_input,
            hba1c_input,
            total_cholesterol_input,
            ldl_cholesterol_input,
            hdl_cholesterol_input
        ],
        outputs=output_text
    )


if __name__ == "__main__":
    demo.launch()
