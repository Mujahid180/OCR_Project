import google.generativeai as genai

genai.configure(api_key="AIzaSyBCuS6N-Rfgleo3WurTfdG35BCb7yRK1O8")
models = genai.list_models()
for model in models:
    print(model.name)
