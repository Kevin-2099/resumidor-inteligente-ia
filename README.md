# Resumidor Inteligente con IA ✨📝

Asistente inteligente basado en IA que genera resúmenes estructurados de textos en español o inglés, organizados en Pros, Contras, Recomendaciones y Conclusión.

## ✨ Características principales

📝 Resúmenes automáticos en español o inglés.

✅ Estructura en viñetas: Pros, Contras, Recomendaciones, Conclusión.

🔍 Análisis de texto completo, segmentando en frases para mejor legibilidad.

🌐 Interfaz web accesible con Gradio.

⚡ Resumen rápido usando el modelo DistilBART de Hugging Face (sshleifer/distilbart-cnn-12-6).

🧠 Detección automática del idioma con langdetect.

💡 Extrae automáticamente frases de conclusión del texto original si están presentes.

🔄 Filtra frases redundantes para entregar bullets únicos y coherentes.

## 🛠️ Tecnologías usadas

Python 3.x

Gradio (interfaz de usuario)

Transformers (Hugging Face, modelo DistilBART)

Langdetect (detección automática de idioma)

## 🚀 Uso

Instalar dependencias:

pip install -r requirements.txt


Ejecutar la aplicación:

python app.py


Abre la interfaz web de Gradio en tu navegador.

Pega un artículo o texto largo en español o inglés y haz clic en "Generar Resumen".

Obtén un resumen en viñetas automáticamente.

## 🎯 Ideal para

Investigadores y estudiantes que necesitan resúmenes rápidos de textos largos.

Profesionales que quieren analizar documentos y extraer información clave.

Cualquier persona que quiera un resumen estructurado de artículos o informes.
