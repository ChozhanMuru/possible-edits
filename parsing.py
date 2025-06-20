class ParsingAgent:
    def __init__(self):
        pass

    def parse(self, text: str) -> dict:
        """
        Parses text to extract numbers, percentages, finance-related words,
        and provides context sentences for each number found.
        """
        import re
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        from nltk.tokenize import sent_tokenize

        # Extract numbers (integers and decimals)
        numbers = re.findall(r"\b\d+\.?\d*\b", text)

        # Extract percentages (e.g., 12%, 3.5 percent)
        percentages = re.findall(r"\b\d+\.?\d*\s*%|\b\d+\.?\d*\s*percent", text, re.IGNORECASE)

        # Extract finance-related words
        finance_keywords = [
            "revenue", "profit", "loss", "income", "expense", "cost", "earnings",
            "margin", "growth", "investment", "dividend", "debt", "asset", "liability",
            "equity", "cash", "capital", "tax", "interest", "valuation", "return"
        ]
        found_finance_words = set()
        for word in finance_keywords:
            if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                found_finance_words.add(word)

        # Extract context for each number (sentence containing the number)
        sentences = sent_tokenize(text)
        number_contexts = []
        for num in numbers:
            for sent in sentences:
                if num in sent:
                    number_contexts.append({"number": num, "context": sent.strip()})
                    break

        return {
            "numbers": numbers,
            "percentages": percentages,
            "finance_words": list(found_finance_words),
            "number_contexts": number_contexts,
            "original_text": text
        }