## Usage

To generate datasets using this library, follow these steps:

1. **Set up your environment**:
   Ensure you have Python installed on your system. This library requires Python 3.6 or later.

2. **Install the dependencies**:
  ```
   pip install -r requirements.txt
   ```

3. **Prepare your API key**:
   The library uses OpenAI's GPT models for generating datasets. You need to have an OpenAI API key. Set your API key as an environment variable:
   ```
   export OPENAI_API_KEY='your_api_key_here'
   ```

4. **Generate datasets**:
   Use the `create_dataset.py` script to generate datasets. This script supports generating datasets from PDF documents or directly from SEC filings using a ticker symbol and year.

   **Available Variables**:
   - `--model_name`: The model name to use for generating the dataset. Default is 'gpt-3.5-turbo'.
   - `--pdf_path`: The path to the PDF document you want to generate the dataset from.
   - `--ticker`: The stock ticker symbol for generating a dataset from a 10-K filing.
   - `--year`: The year of the 10-K filing to generate from.
   - `--max_questions`: The maximum number of questions to generate from the document or filing.

   **Example command to generate a dataset from a PDF document**:
   ```
   python create_dataset.py --model_name 'gpt-3.5-turbo' --pdf_path '/path/to/your/document.pdf' --max_questions 100
   ```

   **Example command to generate a dataset from a 10-K filing**:
   ```
   python create_dataset.py --model_name 'gpt-3.5-turbo' --ticker 'AAPL' --year 2021 --max_questions 100
   ```

   The script will generate a dataset and save it as a JSON file in the `data` directory.

**Note**: Replace `'gpt-3.5-turbo'` with the model of your choice supported by OpenAI. Adjust the `--max_questions` parameter based on how many questions you want to generate from the document or filing.

Based on:

<a href="https://github.com/virattt/financial-datasets/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=virattt/financial-datasets" />
</a>
