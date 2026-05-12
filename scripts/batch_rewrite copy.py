#!/usr/bin/env python3
"""
Batch Rewriting Script
Process large texts (like entire novels) in Mary Shelley's style.
Handles chunking, context management, and output assembly.
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re
from tqdm import tqdm


class BatchRewriter:
    """
    Rewrite large texts in batches while maintaining narrative coherence.
    """
    
    def __init__(self, model_path="./mary_shelley_model", base_model="meta-llama/Llama-3.1-8B"):
        self.model_path = model_path
        self.base_model = base_model
        
        print("=" * 60)
        print("Mary Shelley Batch Rewriter")
        print("=" * 60)
        print(f"Loading model from: {model_path}")
        print()
        
        self.load_model()
    
    def load_model(self):
        """Load the fine-tuned model."""
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print("Loading base model...")
        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )
        
        print("Loading LoRA weights...")
        self.model = PeftModel.from_pretrained(base_model, self.model_path)
        self.model = self.model.merge_and_unload()
        
        print("✓ Model loaded successfully!")
        print()
    
    def split_into_chunks(self, text, max_words=300):
        """
        Split text into manageable chunks at paragraph or sentence boundaries.
        """
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = []
        current_words = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_words = len(para.split())
            
            # If single paragraph is too long, split by sentences
            if para_words > max_words:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sent in sentences:
                    sent_words = len(sent.split())
                    if current_words + sent_words > max_words and current_chunk:
                        chunks.append(' '.join(current_chunk))
                        current_chunk = [sent]
                        current_words = sent_words
                    else:
                        current_chunk.append(sent)
                        current_words += sent_words
            else:
                if current_words + para_words > max_words and current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [para]
                    current_words = para_words
                else:
                    current_chunk.append(para)
                    current_words += para_words
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def rewrite_chunk(self, chunk, previous_context="", style_instruction=""):
        """
        Rewrite a single chunk with context awareness.
        """
        # Build prompt with context
        if style_instruction:
            instruction = style_instruction
        else:
            instruction = "Rewrite the following passage in the Gothic literary style of Mary Shelley, with elaborate descriptions, philosophical depth, and emotional intensity"
        
        if previous_context:
            prompt = f"""{instruction}.

Previous context: {previous_context[-500:]}

Passage to rewrite:
{chunk}

Rewritten passage:"""
        else:
            prompt = f"""{instruction}.

Passage to rewrite:
{chunk}

Rewritten passage:"""
        
        # Generate
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=len(chunk.split()) * 3,  # Allow for expansion
                temperature=0.8,
                top_p=0.92,
                top_k=50,
                repetition_penalty=1.15,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        
        # Decode and extract only the rewritten part
        full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Try to extract just the rewritten portion
        if "Rewritten passage:" in full_output:
            rewritten = full_output.split("Rewritten passage:")[-1].strip()
        else:
            rewritten = full_output[len(prompt):].strip()
        
        return rewritten
    
    def rewrite_document(
        self,
        input_file,
        output_file,
        chunk_size=300,
        style_instruction="",
        maintain_context=True
    ):
        """
        Rewrite an entire document file.
        """
        print(f"Reading input file: {input_file}")
        
        # Read input
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        original_length = len(text.split())
        print(f"Original text: {original_length:,} words")
        
        # Split into chunks
        print(f"Splitting into chunks ({chunk_size} words each)...")
        chunks = self.split_into_chunks(text, max_words=chunk_size)
        print(f"Created {len(chunks)} chunks")
        print()
        
        # Process chunks
        print("Rewriting in Mary Shelley's style...")
        rewritten_chunks = []
        previous_context = ""
        
        for i, chunk in enumerate(tqdm(chunks, desc="Processing")):
            rewritten = self.rewrite_chunk(
                chunk,
                previous_context=previous_context if maintain_context else "",
                style_instruction=style_instruction
            )
            
            rewritten_chunks.append(rewritten)
            
            # Update context for next chunk
            if maintain_context:
                previous_context = rewritten
        
        # Combine chunks
        print("\nAssembling rewritten text...")
        final_text = "\n\n".join(rewritten_chunks)
        
        # Save output
        print(f"Saving to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_text)
        
        final_length = len(final_text.split())
        expansion = (final_length / original_length - 1) * 100
        
        print()
        print("=" * 60)
        print("REWRITING COMPLETE")
        print("=" * 60)
        print(f"Original:  {original_length:,} words")
        print(f"Rewritten: {final_length:,} words")
        print(f"Expansion: {expansion:+.1f}%")
        print(f"Output saved to: {output_file}")
        print()
        
        return final_text
    
    def rewrite_with_custom_plot(self, plot_file, output_file, chapter_summaries=None):
        """
        Generate a new story based on plot points in Shelley's style.
        """
        print(f"Reading plot outline: {plot_file}")
        
        with open(plot_file, 'r', encoding='utf-8') as f:
            plot = f.read()
        
        # If chapter summaries provided, process each separately
        if chapter_summaries:
            chapters = []
            for i, summary in enumerate(chapter_summaries, 1):
                print(f"\nGenerating Chapter {i}...")
                
                prompt = f"""Write Chapter {i} of a Gothic novel in the style of Mary Shelley.

Chapter summary: {summary}

Previous chapters context: {' '.join(chapters[-2:])[-1000:] if chapters else 'This is the beginning.'}

Chapter {i}:"""
                
                inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=2000,
                        temperature=0.85,
                        top_p=0.9,
                        do_sample=True,
                        pad_token_id=self.tokenizer.pad_token_id,
                    )
                
                chapter = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                chapter = chapter[len(prompt):].strip()
                chapters.append(chapter)
            
            final_text = "\n\n" + "\n\n".join(
                [f"CHAPTER {i}\n\n{ch}" for i, ch in enumerate(chapters, 1)]
            )
        else:
            # Generate full narrative from plot
            prompt = f"""Transform the following plot outline into a complete Gothic novel in the style of Mary Shelley, with rich descriptions, philosophical meditations, and emotional depth.

Plot outline:
{plot}

Novel:"""
            
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            print("Generating novel from plot...")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=5000,
                    temperature=0.85,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                )
            
            final_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            final_text = final_text[len(prompt):].strip()
        
        # Save output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_text)
        
        print(f"\n✓ Novel generated and saved to: {output_file}")
        return final_text


def main():
    """
    Main function with example usage.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch rewrite text in Mary Shelley's style")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("output", help="Output text file")
    parser.add_argument("--model", default="./mary_shelley_model", help="Model path")
    parser.add_argument("--chunk-size", type=int, default=300, help="Words per chunk")
    parser.add_argument("--no-context", action="store_true", help="Disable context between chunks")
    parser.add_argument("--instruction", default="", help="Custom style instruction")
    
    args = parser.parse_args()
    
    # Initialize rewriter
    rewriter = BatchRewriter(model_path=args.model)
    
    # Process document
    rewriter.rewrite_document(
        input_file=args.input,
        output_file=args.output,
        chunk_size=args.chunk_size,
        style_instruction=args.instruction,
        maintain_context=not args.no_context
    )


if __name__ == "__main__":
    main()
