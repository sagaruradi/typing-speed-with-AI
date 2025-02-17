import tkinter as tk
from tkinter import messagebox
import time
import random
import openai  # Install using: pip install openai

# Replace with your OpenAI API Key
API_KEY = "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"
openai.api_key = API_KEY


# Sample sentences
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing speed is important for programmers.",
    "Python is a great language for beginners.",
    "Machine learning is changing the world.",
    "Practice makes perfect in coding and typing.",
    "Artificial intelligence is transforming industries.",
    "Efficient typing improves productivity and workflow.",
    "Keyboard shortcuts can help you work faster.",
    "Consistent practice is key to mastering typing skills."
]

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Improver with AI Feedback")
        self.root.geometry("650x500")
        self.root.configure(bg="#f0f0f0")

        # Label
        self.label = tk.Label(root, text="Type the following sentences:", font=("Arial", 12), bg="#f0f0f0")
        self.label.pack(pady=10)

        # Select multiple random sentences
        self.selected_sentences = random.sample(sentences, 3)
        self.sentence_text = "\n".join(self.selected_sentences)

        self.sentence_label = tk.Label(root, text=self.sentence_text, font=("Arial", 12, "bold"), wraplength=600, bg="#f0f0f0", justify="left")
        self.sentence_label.pack(pady=5)

        # Input field
        self.entry = tk.Text(root, height=5, width=70, font=("Arial", 12))
        self.entry.pack(pady=10)

        # Start button
        self.start_button = tk.Button(root, text="Start Typing", font=("Arial", 12), command=self.start_typing)
        self.start_button.pack(pady=5)

        # Timer
        self.start_time = None

    def start_typing(self):
        """Start timer when user begins typing."""
        self.start_time = time.time()
        self.entry.delete("1.0", tk.END)
        self.entry.focus()
        self.root.bind("<Return>", self.check_typing)

    def check_typing(self, event=None):
        """Check typing speed and accuracy."""
        if self.start_time is None:
            messagebox.showwarning("Warning", "Click 'Start Typing' before beginning!")
            return

        end_time = time.time()
        time_taken = end_time - self.start_time

        typed_text = self.entry.get("1.0", tk.END).strip()
        typed_words = typed_text.split()
        word_count = len(typed_words)

        # Calculate WPM correctly
        if time_taken > 0:
            speed = (word_count / time_taken) * 60
        else:
            speed = 0

        # Calculate accuracy
        correct_chars = sum(1 for a, b in zip(" ".join(self.selected_sentences), typed_text) if a == b)
        total_chars = len(" ".join(self.selected_sentences))
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0

        # Get AI-generated feedback
        feedback = self.get_ai_feedback(speed, accuracy)

        # Show results
        messagebox.showinfo("Typing Test Results", f"Speed: {speed:.2f} WPM\nAccuracy: {accuracy:.2f}%\n\nAI Feedback:\n{feedback}")
        self.reset_test()

    def get_ai_feedback(self, speed, accuracy):
        """Get AI-generated feedback from OpenAI."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert typing coach providing feedback."},
                    {"role": "user", "content": f"My typing speed is {speed:.2f} WPM and accuracy is {accuracy:.2f}%. Please give feedback and tips."}
                ]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error generating AI feedback: {str(e)}"

    def reset_test(self):
        """Reset the test with new sentences."""
        self.selected_sentences = random.sample(sentences, 3)
        self.sentence_text = "\n".join(self.selected_sentences)
        self.sentence_label.config(text=self.sentence_text)
        self.entry.delete("1.0", tk.END)
        self.start_time = None

# Run Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
