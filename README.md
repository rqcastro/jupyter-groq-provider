# 🚀 Groq Provider for Jupyter AI

This project adds support for **Groq models** inside **Jupyter AI**, allowing you to use LLaMA 3, DeepSeek-R1, and other high-performance models directly from the JupyterLab interface or through the `%%ai` magic commands.

The provider integrates Groq’s API with the Jupyter AI ecosystem using the official *custom model provider* mechanism.

---

## ⚙️ Features

- Support for Groq models (LLaMA 3.3, LLaMA 3.1, DeepSeek-R1, etc.)
- Authentication via **Jupyter AI UI field** (`GROQ_API_KEY`)
- Configurable parameters such as `temperature` and `max_tokens`
- Compatible with both Jupyter AI chat UI and `%%ai` magics
- Implemented with the official `EnvAuthStrategy` used by Jupyter AI

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/jupyter-groq-provider.git
cd jupyter-groq-provider
```

Install in development/editable mode:

```bash
pip install -e .
```

### ✔️ Supported Python Versions

This provider supports:

- **Python 3.10**
- **Python 3.11**
- **Python 3.12**

❌ **Python 3.13 is not supported**, because Jupyter AI is not yet compatible with it.

---

## 🔑 API Key Configuration (via Jupyter AI UI)

1. Open **JupyterLab**
2. Open the **AI Chat** panel  
3. Click **Settings** (gear icon)  
4. Select the **Groq** provider  
5. Paste your API key in the **GROQ_API_KEY** field  
6. Save and close  

No environment variables are required — Jupyter AI handles the key storage automatically.

---

## 🧪 Usage

### 📌 Using the Jupyter AI UI

In the JupyterLab sidebar:

1. Select **Groq** as the provider  
2. Choose a model  
3. Prompt normally  

### 📌 Using magic commands

```python
%%ai groq --model llama-3.3-70b-versatile
Explain what a Large Language Model is.
```

---

## 📁 Project Structure

```
jupyter-groq-provider/
├─ src/
│  └─ jupyter_groq_provider/
│     ├─ __init__.py
│     └─ groq_provider.py
├─ README.md
└─ pyproject.toml
```

The project follows the modern **src-layout** structure recommended for Python packages.

---

## 🧩 Entry Point

The provider is automatically registered with Jupyter AI via:

```toml
[project.entry-points."jupyter_ai.model_providers"]
groq = "jupyter_groq_provider:GroqProvider"
```

---

## 🔧 Improvements for Future Versions

Although this is the initial version, a few enhancements are planned:

### **1. Make Groq’s base URL configurable**
Currently, the provider uses a hardcoded API base URL from the Groq SDK.  
A future version will allow overriding this URL through:

- Jupyter AI settings field  
- environment variable  
- or both  

This will improve flexibility for testing, proxies, and custom endpoints.

### **2. Maintain Python compatibility guard (`<3.13`)**
The package intentionally requires:

```
requires-python = ">=3.10, <3.13"
```

to avoid environments where Jupyter AI is not yet supported.
