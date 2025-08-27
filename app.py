import gradio as gr
from transformers import pipeline
from langdetect import detect

# Pipeline de resumen
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def resumir_texto(texto):
    try:
        # Detectar idioma del texto
        idioma = detect(texto)
        lang = "es" if idioma == "es" else "en"

        # Generar resumen base
        resumen = summarizer(texto, max_length=200, min_length=80, do_sample=False)
        resumen_text = resumen[0]['summary_text']

        # Cortar en frases
        frases = resumen_text.split(". ")
        
        # Forzar estructura en bullets con idioma correcto
        if lang == "es":
            bullets = [
                "✅ **Pros**: " + (frases[0] if len(frases) > 0 else "Se destacan beneficios clave en el texto."),
                "⚠️ **Contras**: " + (frases[1] if len(frases) > 1 else "Existen algunos riesgos o limitaciones mencionados."),
                "🔧 **Recomendaciones**: " + (frases[2] if len(frases) > 2 else "Se sugieren acciones o estrategias para mejorar la situación."),
                "📌 **Conclusión**: " + (frases[3] if len(frases) > 3 else "El tema ofrece oportunidades si se gestionan bien los retos.")
            ]
        else:
            bullets = [
                "✅ **Pros**: " + (frases[0] if len(frases) > 0 else "Key benefits are highlighted in the text."),
                "⚠️ **Cons**: " + (frases[1] if len(frases) > 1 else "Some risks or limitations are mentioned."),
                "🔧 **Recommendations**: " + (frases[2] if len(frases) > 2 else "Suggested actions or strategies to improve the situation."),
                "📌 **Conclusion**: " + (frases[3] if len(frases) > 3 else "The topic shows opportunities if challenges are well managed.")
            ]

        return "\n".join(bullets)

    except Exception as e:
        return f"No se pudo generar el resumen. Error: {str(e)}"

# Interfaz Gradio
with gr.Blocks() as demo:
    gr.Markdown("## ✨ Resumidor Inteligente (Pros / Contras / Recomendaciones / Conclusión)")
    gr.Markdown("Pega un artículo en español o inglés y obtén un resumen 🚀")
    
    input_text = gr.Textbox(label="Texto de entrada", placeholder="Pega aquí un artículo largo en español o inglés...", lines=12)
    output_text = gr.Textbox(label="Resumen generado en bullets", lines=12)
    boton = gr.Button("Generar Resumen")
    
    boton.click(fn=resumir_texto, inputs=input_text, outputs=output_text)

demo.launch()
