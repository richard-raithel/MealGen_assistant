import os
import base64
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI

# Load environment variables
load_dotenv()

# Your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ingredients list
ingredients = {
    "proteins": ["Beef", "Bison", "Chicken", "Turkey", "Duck", "Pork", "Seafood", "Whole Milk", "Cheese", "Eggs", "Beans", "Chia Seeds", "Lentils", "Edamame", "Quinoa", "Greek Yogurt"],
    "healthy_fats": ["Almonds", "Avocado", "Avocado Oil", "Brazil Nuts", "Cashew", "Chia Seeds", "Coconut Oil", "Flax Seeds", "Ghee", "Hazelnuts", "Hemp Seeds", "Macadamia", "Macadamia Oil", "Nut Butters", "Pecans", "Pine Nuts", "Pistachios", "Pumpkin Seeds", "Sesame Seeds", "Sunflower Seeds", "Tahini", "Walnuts", "Walnut Oil", "Peanut Butter", "Almond Butter"],
    "carbohydrates": ["Apples", "Artichokes", "Asparagus", "Bananas", "Beets", "Bell Peppers", "Blackberries", "Blueberries", "Bok choy", "Broccoli", "Brussel Sprouts", "Cabbage", "Cantaloupe", "Carrots", "Cauliflower", "Cherries", "Cranberries", "Figs", "Grapefruit", "Grapes", "Honeydew", "Kiwi", "Mangos", "Oranges", "Parsnips", "Peaches", "Pears", "Peas", "Plantain", "Potatoes", "Pumpkin", "Radishes", "Snow Peas", "Squash", "Sweet Potatoes", "Turnip Greens", "Turnips", "Yams", "Zucchini", "Quinoa", "Brown Rice", "Wild Rice", "Oats", "Barley", "Millet", "Buckwheat (whole groats)", "Farro", "Rice Cakes"]
}

def format_ingredients(ingredients):
    formatted = "\n".join(
        [
            f"{category.capitalize()}: {', '.join(items)}"
            for category, items in ingredients.items()
        ]
    )
    return f"The available ingredients are:\n{formatted}\n"

def generate_meal_idea(user_message, history):

    # Construct the system prompt
    # system_prompt = (
    #     "You are a creative meal idea generator. "
    #     "Your task is to provide meal ideas using only the given ingredients:\n"
    #     f"{format_ingredients(ingredients)}"
    #     "\nOnly herbs and spices are allowed other than the ingredients listed above. Bread is not allowed.\n"
    #     "For each meal, include:\n"
    #     "1) The recipe\n"
    #     "2) Preparation instructions\n"
    #     "3) Number of servings\n"
    #     "4) Grams of each ingredient per serving for input into the MyFitnessPal app\n"
    #     # "Finally, include a shopping list that covers all recipes.\n"
    # )

    system_prompt = (
        "You are an expert culinary assistant with extensive knowledge of global cuisines, innovative cooking techniques, and a passion for creating diverse and unique meal ideas. "
        "Your task is to generate creative and varied meal ideas using only the provided ingredients:\n"
        f"{format_ingredients(ingredients)}"
        "\nYou may use any herbs and spices to enhance the flavors, but bread and other non-listed ingredients are not allowed.\n"
        "For each meal, please provide the following details:\n"
        "1) **Recipe Name**: A unique and appealing name for the dish.\n"
        "2) **Description**: A brief description of the dish, highlighting its cultural or regional inspiration and any dietary benefits or considerations, such as being high in protein, low in carbohydrates, or suitable for specific diets like ketogenic or vegetarian.\n"
        "3) **Cooking Time**: Include the estimated time required to prepare the meal, from start to finish.\n"
        "4) **Ingredients**: Provide a comprehensive list of all ingredients needed for the recipe, including both raw and prepared (cooked) weights where applicable. Present the information in a structured format, such as a Markdown table, specifying each ingredient alongside its exact quantity and unit of measurement. Use american units of measurement for this setion. For example:\n\n"
        "| Ingredient        | Quantity |\n"
        "|-------------------|----------|\n"
        "| Cooked Chicken    | 2 cups   |\n"
        "| Cooked Rice       | 1/2 cup  |\n"
        "| Steamed Broccoli  | 1 cup    |\n"
        "| Olive Oil         | 2 tbsp   |\n"
        "\n"
        "5) **Preparation Instructions**: Step-by-step instructions to prepare the meal, ensuring clarity and ease of understanding.\n"
        "6) **Number of Servings**: Indicate how many servings the recipe yields.\n"
        "7) **Ingredients per Serving (for input into MyFitnessPal)**: List the grams of each prepared (cooked) ingredient per serving, ensuring accurate measurements for input into the MyFitnessPal app.\n"
        "8) **Nutritional Information Per Serving**: Provide a summary of key nutritional values per serving, such as calories, protein, carbohydrates, and fats.\n"
        "\nPlease ensure that the recipes are balanced, nutritious, and cater to a variety of tastes and preferences. Use vivid and descriptive language to make the recipes appealing and engaging. Maintain a consistent formatting style for all sections to ensure clarity and ease of use."
    )

    # Initialize messages with the system prompt if history is empty
    if not history:
        messages = [{"role": "system", "content": system_prompt}]
    else:
        messages = history

    # Call OpenAI to get the assistant's response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}] + messages + [{"role": "user", "content": user_message}]
    )

    # Extract the assistant's reply
    assistant_reply = response.choices[0].message.content.strip()

    return assistant_reply

# # Encode the image in base64
# with open("SOMA_logo_white-removebg.png", "rb") as image_file:
#     encoded_image = base64.b64encode(image_file.read()).decode()
#
# img_data = f"data:image/png;base64,{encoded_image}"

# title = f"""
# <div style="display: flex;">
#     <img src="{img_data}" alt="Logo" style="height: 40px; margin-right: 10px;">
#     <div style="text-align: left;">
#         <h5 style="font-size: 16px; margin: 0;">SOMA Nutrition Assistant</h5>
#         <h5 style="font-size: 14px; margin: 0;">
#             <a href="https://docs.google.com/document/d/10uyxdAbwJ2k6c5WhYtxTuD60s6tPYKCS9yrCMu4tjio/edit?tab=t.0" target="_blank" style="text-decoration: none; color: #007BFF;">
#                 Instructions
#             </a>
#         </h5>
#     </div>
# </div>
# """

description = f"""
    <h5 style="font-size: 14px; margin: 0;">
        <a href="https://docs.google.com/document/d/10uyxdAbwJ2k6c5WhYtxTuD60s6tPYKCS9yrCMu4tjio/edit?tab=t.0" target="_blank" style="text-decoration: none; color: #007BFF;">
            Instructions
        </a>
    </h5>
"""


# Create and launch the app
gr.ChatInterface(
    fn=generate_meal_idea,
    type="messages",
    description=description,
    autoscroll=True,
    concurrency_limit=None
).launch()

# share=True
# server_name="0.0.0.0", server_port=7860
