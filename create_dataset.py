import os
import fitz  # PyMuPDF
import argparse
import json

from financial_datasets.generator import DatasetGenerator
from langchain_text_splitters import TokenTextSplitter

def main(model_name, pdf_path, max_questions, ticker, year):
    # Set default values
    api_key = os.getenv('OPENAI_API_KEY', 'your_api_key')  # Get API key from environment variable or use default

    # Instantiate the DatasetGenerator
    generator = DatasetGenerator(model=model_name, api_key=api_key)

    if pdf_path:
        # Load and extract text from PDF
        pdf_text = []
        chunk_size = 8192  # Define the desired chunk size in terms of token count

        with fitz.open(pdf_path) as doc:
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            
            token_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=0)  # Assuming no overlap is needed
            pdf_text = token_splitter.split_text(full_text)

        # Generate the dataset from the extracted PDF text
        dataset = generator.generate_from_texts(document_name=os.path.basename(pdf_path), texts=pdf_text, max_questions=max_questions)
        document_name = os.path.basename(pdf_path)
    elif ticker and year:
        # Generate the dataset from a 10-K filing
        dataset = generator.generate_from_filings(ticker=ticker, year=year, max_questions=max_questions, form_types=['DEF 14A'])
        document_name = f"{ticker}_{year}_10k"
    else:
        raise ValueError("Either a PDF path or a ticker and year must be provided.")

    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)  # Add this line

    # Save the generated dataset to a JSON file
    dataset_file_name = f"data/{document_name.split('.')[0]}_dataset.json"
    with open(dataset_file_name, 'w') as f:
        # Add document name to each dataset item before saving
        for item in dataset.items:
            item.__dict__['document_name'] = document_name
        json.dump([item.__dict__ for item in dataset.items], f, indent=4)
    
    print(f"Dataset saved to {dataset_file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a dataset from a PDF document or a 10-K filing.")
    parser.add_argument("--model_name", type=str, default='gpt-3.5-turbo', help="The model name to use for generating the dataset. Default is 'gpt-3.5-turbo'.")
    parser.add_argument("--pdf_path", type=str, default=None, help="The path to the PDF document.")
    parser.add_argument("--ticker", type=str, default=None, help="The stock ticker symbol for generating from a 10-K filing.")
    parser.add_argument("--year", type=int, default=None, help="The year of the 10-K filing to generate from.")
    parser.add_argument("--max_questions", type=int, default=2, help="The maximum number of questions to generate.")

    args = parser.parse_args()

    main(args.model_name, args.pdf_path, args.max_questions, args.ticker, args.year)
