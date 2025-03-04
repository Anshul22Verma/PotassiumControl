prompt = """
Generate a dataset of 10 patient meal logs, nutrition diagnoses, diet goals, and follow-up recommendations for end-stage heart failure patients on MRAs, so the dietitian recommendations need to limit patients potassium intake mainly, alongside potassium intake dietitian also need to make sure that patients are eating and drinking healthy as they need to manage their fluid, salt "Eat less than 2,000 mg of salt (sodium) per day", fat and nutrients intake. Use end-stage heart failure patients diet requirements as whats ideal, and because these patients are on Mineralocorticoid Receptor Antagonists (MRA), so managing patients potassium becomes even more important. Each entry should be in JSON format.

Follow these guidelines:
1. **Patient Data:** Include a "patient_id" (e.g., "P00001") and "ethnicity" (e.g., "Caucasian", "African American", "Hispanic", "Asian", "Mediterranean").
2. **Total Daily Fluid Intake:** Include a "total_drinks" string field with the total daily fluid intake in liters. Include a note that the patient should not exceed 4 liters per day.
2. **Detailed Meal Log (String):**
* The "meal_log" field should be a single string representing the patient's meals.
* Include specific food items, cooking methods, and details (e.g., "whole-wheat toast with butter," "Greek yogurt with honey," "grilled chicken breast").
* Include meal times.
* Example: "8:30 AM - Whole-wheat toast with butter, Greek yogurt with honey. 1:00 PM - Turkey sandwich (whole wheat), Mixed green salad with vinaigrette. 7:00 PM - Grilled chicken breast, Steamed broccoli."
3. **Dietary Preferences:** Include an "example_guide_other_diet" field with a short description of the patient's food preferences.
4. **Nutrition Diagnosis:** Include a "nutrition_diagnosis" field with a diagnosis related to potassium, sodium, or fat intake.
5. **Diet Goals:** Include "diet_goals" with specific goals related to the diagnosis.
6. **Follow-Up Recommendations:** Include "follow_up_recommendations" with specific dietary recommendations. Needs to be a single string with all the recommendations bulleted "1. 2. 3."

Here is an example output format:
json
{
"patient_id": "P00001",
"ethnicity": "Caucasian",
"total_drinks": "2.5 litres",
"meal_log": "9 am-gluten free bagel with peanut butter or salted butter or plain or frozen waffles/pancake-mix with real maple syrup or gluten-free oatmeal made with water plus brown sugar (1 TBSP) and berries 1300 hrs- cheese (2 slices of cheddar) or tuna sandwich plus dry apricots and 1 apple or gluten-free crackers with cheese or leftovers 5:50 pm-Fish with 2 cups rice with asparagus (6) and green beans (1 cup) or hamburger patty no bun and salad with prepared or homemade dressing or chicken breast (5 oz) with rice and vegs-1.5 cups (peppers, mushrooms, carrot, turnip, cabbage, tomatoes" (need be detailed have cooking method, weight and different contents in each dish etc.),
"example_guide_other_diet": "loves tomato and pesto sauce; mushrooms. (can be empty sometimes as well, infact is empty a lot of times in the dataset or is none if patient has no preference some patients like juices some like meat each is different)",
"nutrition_diagnosis": "excessive fat intake related to food and nutrition-related knowledge gap re: appropriate amount of dietary fat as evidenced by patient's diet hx (cheese, butter)",
"diet_goals": "1. Identified high potassium and high total and SFA foods in patient'
diet history 2. Reviewed low potassium fruits and vegetables",
"follow_up_recommendations": "Each recommendation need to have bullet points. Like 1. Limit butter to 3 servings/day and use unsalted butter 2. Limit low potassium vegs to 3 servings/day 3. Limit milk/yogurt/ice cream to 1 cup per day 4. Limit mushrooms to 1/2 cup 1 time per week 5. Limit tomato sauce to 1/4 cup per week 6. Limit tomatoes to 1/2 small tomato or 5 cherry tomatoes per day 7. Read the nutrition facts table to optimize choices (present in most of the recommendations)"
}

Have more empty fields "example_guide_other_diet" or "none" in this generation, generate different examples everytime for people with different dietary preferences and restrictions. Do try to cover all high potassium, high sodium, high fat, and low potassium, low sodium, low fat foods in the meal logs and recommendations.
"""



if __name__ == "__main__":
    import json

    data = []  # will have the generations from the API of different LLMs
    data_json = {}
    for idx, sample in enumerate(data):
        sample["patient_id"] = f"P{str(idx+1).zfill(5)}"
        sample["total_drinks"] = sample["total_drinks"].replace("  (Do not exceed 4 litres daily)", "").replace(" (max 4 liters/day)", "")
        data_json[f"sample_{idx+1}"] = sample

    with open('gmdt_synthetic_data.json', 'w') as fp:
        json.dump(data_json, fp, indent=4)
