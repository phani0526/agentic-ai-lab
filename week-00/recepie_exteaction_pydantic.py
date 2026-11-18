import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

# 1. Define your desired schema using Pydantic
class RecipeExtraction(BaseModel):
    dish_name: str = Field(description="The name of the dish")
    prep_time_minutes: int = Field(description="Total preparation time in minutes")
    ingredients: list[str] = Field(description="List of ingredients with quantities")

    # You can even put your own convenience properties right inside your Pydantic model!
    @property
    def is_quick_meal(self) -> bool:
        return self.prep_time_minutes <= 30


# 2. Initialize the client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTER_API_KEY")
)

# 3. Call the model using standard chat completions with structured outputs
completion = client.beta.chat.completions.parse(
    model="openrouter/free",  # Or any other model supporting structured outputs
    messages=[
        {"role": "system", "content": "Extract recipe details from the text."},
        {
            "role": "user",
            "content": "To make crispy Masala Dosa, start with 2 cups of fermented rice and urad dal batter. For the potato filling, boil 4 medium potatoes and mash them. Temper 1 tsp mustard seeds, 1 tsp chana dal, curry leaves, 2 chopped green chilies, and 1 sliced onion in 2 tbsp oil, then add 1/2 tsp turmeric and the mashed potatoes. Spread a ladle of batter onto a hot tawa, drizzle ghee, stuff with the potato masala, and fold. Active cooking and assembly takes about 25 minutes."  # noqa: E501
        },
    ],
    response_format=RecipeExtraction,
)

# 4. Extract the parsed Pydantic object
# 1. Get the parsed result (which might be None)
recipe = completion.choices[0].message.parsed

# 2. Check if parsing was successful before using it
if recipe is not None:
    print(f"Dish: {recipe.dish_name}")
    print(f"Ingredients: {recipe.ingredients}")
    print(f"Prep Time: {recipe.prep_time_minutes} minutes")
    print(f"Is Quick Meal?: {recipe.is_quick_meal}")
else:
    # Handle the failure case (e.g., model refusal or parsing error)
    refusal = completion.choices[0].message.refusal
    print(f"Failed to parse response. Refusal reason: {refusal}")

#recipe: RecipeExtraction = completion.choices[0].message.parsed

