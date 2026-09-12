# AI Gold & Silver Assistant

AI Gold & Silver Assistant is a Streamlit-based chatbot that uses Large Language Model function calling to provide live gold and silver price information. The application connects a Hugging Face LLM with the OroPocket public price API to retrieve current metal rates and perform quantity-based calculations.

## About the Project

The application combines AI function calling with live external API data.

When a user asks for current gold or silver information, the LLM identifies that live data is required and calls the `get_live_metal_rates()` function. The Python function retrieves the latest gold and silver prices from the OroPocket API and returns the data to the LLM. The LLM then generates a clear natural-language response.

For general questions that do not require live metal data, the LLM can respond directly without calling the price function.

## Key Features

- Live gold price retrieval
- Live silver price retrieval
- Gold and silver buy and sell quotes
- 24-hour price change information
- Gold and silver price comparison
- Quantity-based price calculation
- AI-powered natural-language responses
- Function calling with Hugging Face
- External API integration
- General question handling without unnecessary API calls
- Interactive Streamlit chatbot interface
- Animated gold and silver visual elements using CSS
- Market snapshot for 10-gram values and GST information
- Quick question buttons
- API response caching to reduce unnecessary requests

## Function Calling Workflow

The application follows this workflow:

```text
User Question
      |
      v
Hugging Face LLM
      |
      v
Does the question require live metal data?
      |
   +--+--+
   |     |
  Yes    No
   |     |
   v     v
Function   LLM responds
Call       directly
   |
   v
get_live_metal_rates()
   |
   v
OroPocket Public API
   |
   v
Live Gold/Silver Data
   |
   v
Tool Result
   |
   v
Hugging Face LLM
   |
   v
Final Natural-Language Response
```
## Technologies Used

- Python
- Streamlit
- Hugging Face InferenceClient
- Hugging Face LLM
- OroPocket Public Price API
- Requests
- JSON
- python-dotenv
- HTML
- CSS

  ## Live Price Data

The application uses the OroPocket Public Price API to retrieve current gold and silver tradeable price data.

The API provides:

- Gold buy price
- Gold sell price
- Silver buy price
- Silver sell price
- 24-hour price changes
- GST information
- API timestamp

The prices are provided in Indian Rupees per gram.

The application uses the retrieved live data to display current market information and perform quantity-based calculations.

## AI Function Calling

The application uses Hugging Face LLM function calling to connect natural-language user questions with live external data.

A function named `get_live_metal_rates()` is provided to the LLM. When a user asks for current gold or silver prices, comparisons, 24-hour changes, or quantity-based values, the LLM can decide to call this function.

The function retrieves live data from the OroPocket API and returns the result to the LLM. The LLM then uses the returned data to generate the final response.

For general questions that do not require live metal data, the LLM can respond directly without calling the function.

### Function Calling Flow

```text
User Question
      |
      v
Hugging Face LLM
      |
      v
Function Call Decision
      |
      v
get_live_metal_rates()
      |
      v
OroPocket API
      |
      v
Live Gold/Silver Data
      |
      v
LLM
      |
      v
Final Response
```
## Application Interface

The application provides a simple and user-friendly Streamlit interface for interacting with the AI Gold & Silver Assistant.

The interface includes:

- Gold and silver live price cards
- Market snapshot information
- AI-powered chatbot
- Quick question options
- Gold and silver visual elements
- Current buy and sell price information
- 24-hour price change information
- Quantity-based metal value calculations

Users can ask questions in natural language, and the chatbot provides responses based on live metal price data when required.

## Error Handling

The application includes basic error handling to provide a reliable user experience.

The application handles:

- Missing Hugging Face API token
- API request failures
- Invalid or unavailable metal price data
- Network connection errors
- Invalid user inputs
- Function calling errors

If live price data cannot be retrieved, the application displays an appropriate error message instead of generating or assuming incorrect prices.

## Important Data Limitation

The application uses the OroPocket Public Price API to retrieve current gold and silver tradeable prices.

The displayed prices are provided in Indian Rupees per gram and represent the buy and sell prices returned by the API.

The application does not provide:

- Historical gold or silver prices
- City-specific prices such as Chennai market rates
- MCX official prices
- LBMA official prices
- Official spot market prices
- Guaranteed jeweller prices

Therefore, the displayed rates should be treated as API-provided market information and may differ from prices offered by individual jewellery stores or other financial platforms.

## Project Objective

The main objective of the project is to demonstrate how Large Language Models can use function calling to interact with real-time external data.

The project combines an AI chatbot with a live metal price API so that users can ask natural-language questions about gold and silver rates without manually checking the API.

It demonstrates how an LLM can:

- Understand the user's question
- Decide when external data is required
- Call a Python function
- Retrieve live data from an external API
- Use the returned data
- Generate a natural-language response

## Future Enhancements

The application can be further improved by adding:

- Historical gold and silver price tracking
- Price charts and trends
- Budget-based gold and silver calculations
- Support for different currencies
- Additional metal support
- Price alerts and notifications
- More detailed market analysis
- Jewellery price estimation including making charges and taxes
- Multiple data sources for price comparison
- Improved conversational memory
- Voice-based interaction

## Conclusion

The AI Gold & Silver Assistant demonstrates the practical use of function calling in an LLM-powered application.

By connecting a Hugging Face LLM with the OroPocket Public Price API, the chatbot can dynamically retrieve live gold and silver price information and use it to answer relevant user questions.

The project shows how function calling can extend the capabilities of an LLM by allowing it to interact with external APIs and real-time data sources instead of depending only on its internal knowledge.

