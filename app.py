import gradio as gr
import re
from transformers import pipeline
from langdetect import detect

# Pipeline de resumen
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Regex para detectar frases de conclusión
patron_conclusion = re.compile(r'\b(in conclusion|en conclusión|en general|overall)\b', re.IGNORECASE)

def es_conclusion(frase: str) -> bool:
    return bool(patron_conclusion.search(frase))

def buscar_conclusion_original(texto: str):
    m = re.search(r'(?i)\b(in conclusion|en conclusión|en general|overall)\b.*?(?:[.!?]|$)', texto, flags=re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0).strip().rstrip('.') + '.'
    return None

def unique_preserve_order(lst):
    seen = set()
    out = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def resumir_texto(texto):
    try:
        idioma = detect(texto)
        lang = "es" if idioma == "es" else "en"

        # Conclusión desde el texto original
        conclusion_original = buscar_conclusion_original(texto)

        resumen = summarizer(texto, max_length=300, min_length=120, do_sample=False)
        resumen_text = resumen[0]['summary_text']

        # Dividir en frases principales
        frases = []
        for f in re.split(r'\.\s+|\.\n+', resumen_text):
            f_strip = f.strip()
            if not f_strip:
                continue

            if es_conclusion(f_strip):
                frases.append(f_strip)
                continue

            if conclusion_original and conclusion_original.lower().split()[0] in f_strip.lower():
                frases.append(f_strip)
                continue

            subfrases = re.split(r', | and |; | but | however | such as ', f_strip)
            frases.extend([s.strip() for s in subfrases if s.strip()])

        pros, cons, recomendaciones, conclusion = [], [], [], []

        # Clasificación según idioma
        if lang == "es":
            for s in frases:
                s_low = s.lower()

                # Conclusión
                if es_conclusion(s):
                    conclusion.append(s)
                    continue

                # Recomendaciones primero
                if any(word in s_low for word in ["recomienda", "sugerencia", "aconseja", "debe", 
                                                  "es recomendable", "es aconsejable", "fundamental", 
                                                  "es fundamental", "necesario", "es necesario"]):
                    recomendaciones.append(s)
                    continue

                # Pros
                if any(word in s_low for word in ["mejora", "beneficio", "ventaja", "eficiente", 
                                                  "facilita", "permit", "permitir", "optimiza", 
                                                  "colaboración", "transformando", "adoptando", "ofrecer", "colaboración"]):
                    pros.append(s)
                    continue

                # Contras
                if any(word in s_low for word in ["problema", "limitación", "desventaja", 
                                                  "pérdida", "inconveniente", "desafíos", "desafío","limitaciones"]):
                    cons.append(s)
                    continue

        else:
            for s in frases:
                s_low = s.lower()

                # Conclusión
                if es_conclusion(s):
                    conclusion.append(s)
                    continue

                # Recomendaciones en inglés
                if any(word in s_low for word in ["to fully leverage", "it is critical", "should", "must", 
                                                  "recommend", "invest", "train", "educat", "policy"]):
                    recomendaciones.append(s)
                    continue

                # Contras en inglés
                if any(word in s_low for word in ["risk", "risks", "challenge", "problem", "loss", "issue", 
                                                  "concern", "concerns", "lack", "limitation", "desventaja", 
                                                  "riesgo", "problema", "pérdida", "threat", "danger", 
                                                  "displace", "side effect", "ethical"]):
                    cons.append(s)
                    continue

                # Pros en inglés
                if any(word in s_low for word in ["improve", "benefit", "advantage", "allow", "efficient", 
                                                  "productivity", "personalized", "leverage", "permit", 
                                                  "facilita", "mejora", "adopt", "transform", "deliver", 
                                                  "opportunity","collaboration"]):
                    pros.append(s)
                    continue

        # Usar conclusión original si existe
        if conclusion_original:
            conclusion = [conclusion_original]
            cons = [c for c in cons if conclusion_original.lower() not in c.lower()]

        pros = unique_preserve_order(pros)
        cons = unique_preserve_order(cons)
        recomendaciones = unique_preserve_order(recomendaciones)
        conclusion = unique_preserve_order(conclusion)

        # Mensajes por defecto
        if not pros:
            pros = ["No clear pros found." if lang == "en" else "No se identificaron pros claros."]
        if not cons:
            cons = ["No clear cons found." if lang == "en" else "No hay contras importantes identificadas."]
        if not recomendaciones:
            recomendaciones = ["No recommendations found." if lang == "en" else "No se encontraron recomendaciones específicas."]
        if not conclusion:
            conclusion = ["No clear conclusion found." if lang == "en" else "No se pudo determinar una conclusión clara."]

        # Construcción de bullets
        if lang == "es":
            bullets = [
                "✅ **Pros**: " + "; ".join(pros),
                "⚠️ **Contras**: " + "; ".join(cons),
                "🔧 **Recomendaciones**: " + "; ".join(recomendaciones),
                "📌 **Conclusión**: " + "; ".join(conclusion),
            ]
        else:
            bullets = [
                "✅ **Pros**: " + "; ".join(pros),
                "⚠️ **Cons**: " + "; ".join(cons),
                "🔧 **Recommendations**: " + "; ".join(recomendaciones),
                "📌 **Conclusion**: " + "; ".join(conclusion),
            ]

        return "\n".join(bullets)

    except Exception as e:
        return f"No se pudo generar el resumen. Error: {str(e)}"

# Interfaz Gradio
with gr.Blocks() as demo:
    gr.Markdown("## ✨ Resumidor Inteligente (Pros / Cons / Recommendations / Conclusion)")
    gr.Markdown("Pega un artículo en español o inglés y obtén un resumen 🚀")

    input_text = gr.Textbox(label="Texto de entrada", placeholder="Pega aquí un artículo largo en español o inglés...", lines=12)
    output_text = gr.Textbox(label="Resumen generado en bullets", lines=12)
    boton = gr.Button("Generar Resumen")

    boton.click(fn=resumir_texto, inputs=input_text, outputs=output_text)

demo.launch()
