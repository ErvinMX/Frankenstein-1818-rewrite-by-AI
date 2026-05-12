# Frankenstein-1818-rewrite-by-AI
This project demonstrates the capabilities of AI in terms of mimicking the style of a 19 century author.

**"To what extent can fine-tuned LLMs replicate the subconscious syntactic signature?"**

## Project Overview
This project utilizes a fine-tuned **Llama 3.1-8B** model to explore the literary expansion of Mary Shelley's 1818 *Frankenstein*. The primary goal was to reimagine the narrative by shifting the focus from Victor Frankenstein’s "flight response" to a trajectory of **sustained moral accountability**. This version, titled *The Accountability Cut*, introduces new narrative perspectives, including Elizabeth Lavenza’s first-person journal, to address themes of socioeconomic status and scientific responsibility.

## Technical Stack
* **Base Model:** Meta Llama-3.1-8B.
* **Optimization & Training:** Utilized the **Unsloth** library to implement **QLoRA** (4-bit quantization), significantly reducing VRAM overhead while maintaining model performance.
* **Infrastructure:** Python-based pipeline for data cleaning, batch inference, and narrative assembly.
* **Evaluation:** Stylometric analysis performed using the **'stylo' package in RStudio** to measure the 500 Most Frequent Words (MFWs).

## Core Engineering Features
* **Dataset Preprocessing:** A custom script identified and removed Project Gutenberg structural noise (legal markers, metadata, and non-prose text) to create a clean, training-ready corpus of Mary Shelley's collected works.
* **Algorithmic Chunking:** To bypass context window limitations, the inference engine constrained processing to 300-word blocks, ensuring plot coherence across a 70,000+ word manuscript.
* **Narrative Stitching:** Implemented a contextual memory mechanism that automatically fed previous AI outputs back into the model to maintain narrative flow during generation.
* **Hyperparameter Tuning:** Optimized generation using a temperature of 0.8–0.85 and a Top-p of 0.9–0.92 to balance creativity with narrative stability.

## Evaluation Results
The project employed **Principal Components Analysis (PCA)** and **Cluster Analysis** to validate the stylistic fidelity of the AI-generated prose.

* **Lexical Success:** The analysis confirmed the AI's effectiveness in mimicking Mary Shelley's gothic-style vocabulary.
* **Syntactic Bifurcation:** The results depicted a definitive structural separation between the original 19th-century prose and AI interventions along the PC2 axis, revealing the model's current limitations in replicating an author's subconscious syntactic "signature".
* **Anomaly Detection:** The software successfully identified a significant outlier (26.9% variance) in Chapter 1, correctly detecting the shift from third-person to first-person narrative.

## Repository Content
* **[/scripts](./scripts):** Includes Python logic for text cleaning, batch rewriting, and final manuscript assembly.
* **[/documentation](./documentation):** Contains the full academic report and the project's visual poster summary.
* **[Frankenstein_Accountability_Cut.txt](./Frankenstein_Accountability_Cut.txt):** The final hybrid manuscript.

## Documentation
For a deep dive into the methodology and results, please refer to:
* [Digital Humanities Final Report](./documentation/Digital_Hums_final_report.pdf)
* [Project Presentation Poster](./documentation/Digital_humanities_final_project_poster.pdf)
