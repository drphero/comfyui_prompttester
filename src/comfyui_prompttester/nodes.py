class PromptTester:
    """
    A node to analyze the impact of different phrases in a prompt.
    It takes a full prompt, splits it into phrases, and generates
    a batch of prompts, each omitting one phrase. It also provides labels
    for each generated image for easy comparison.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "delimiter": ("STRING", {"default": ","}),
                "include_baseline": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompts", "labels")
    OUTPUT_IS_LIST= (True, True)
    FUNCTION = "test_prompt"
    CATEGORY = "utils/prompting"

    def test_prompt(self, prompt, delimiter, include_baseline):
        # Clean up phrases: split by delimiter, strip whitespace, and remove empty strings
        phrases = [p.strip() for p in prompt.split(delimiter) if p.strip()]

        if not phrases:
            return ([""], ["Empty Prompt"])

        output_prompts = []
        output_labels = []

        # Add the baseline (original full prompt) if requested
        if include_baseline:
            output_prompts.append(prompt)
            output_labels.append("Baseline Full Prompt")

        # Generate a version for each phrase being omitted
        for i, phrase_to_omit in enumerate(phrases):
            # Create a new list of phrases excluding the current one
            remaining_phrases = phrases[:i] + phrases[i+1:]
            
            # Join the remaining phrases back into a string
            new_prompt = delimiter.join(remaining_phrases)
            
            if len(phrase_to_omit) > 30: # Truncate long phrases for filename
                phrase_to_omit = phrase_to_omit[:30]

            output_prompts.append(new_prompt)
            output_labels.append(phrase_to_omit)

        return (output_prompts, output_labels)

NODE_CLASS_MAPPINGS = {
    "PromptTester": PromptTester,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptTester": "Prompt Tester",
}