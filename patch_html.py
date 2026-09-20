import os

html_path = r"Medical AI Agent using groq\static\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add ID to symptoms textarea
content = content.replace(
    '<textarea class="w-full bg-surface-container-lowest',
    '<textarea id="symptoms-input" class="w-full bg-surface-container-lowest'
)

# Add ID to extract symptoms button
content = content.replace(
    'Extract &amp; Structure Symptoms with NLP',
    'Extract &amp; Structure Symptoms with NLP</button>'
).replace(
    '<button class="w-full py-2.5 px-4 rounded-lg bg-surface-container-high hover:bg-surface-container-highest text-on-surface font-label font-semibold text-xs tracking-wide transition-all flex items-center justify-center gap-2" type="button">\n<span class="material-symbols-outlined text-primary text-[18px]">auto_fix_high</span>\n          Extract &amp; Structure Symptoms with NLP</button>',
    '<button id="extract-symptoms-btn" class="w-full py-2.5 px-4 rounded-lg bg-surface-container-high hover:bg-surface-container-highest text-on-surface font-label font-semibold text-xs tracking-wide transition-all flex items-center justify-center gap-2" type="button">\n<span class="material-symbols-outlined text-primary text-[18px]">auto_fix_high</span>\n          Extract &amp; Structure Symptoms with NLP</button>'
)

# Add ID to prescription file input (replace the upload button with a file input)
content = content.replace(
    '<button class="py-2.5 px-3 rounded-lg bg-surface-container hover:bg-surface-container-high text-secondary hover:text-on-surface text-xs font-label transition-all flex items-center justify-center" title="Upload New File" type="button">\n<span class="material-symbols-outlined text-[18px]">cloud_upload</span>\n</button>',
    '<input type="file" id="prescription-upload" class="py-2.5 px-3 rounded-lg bg-surface-container text-secondary text-xs font-label" accept="image/*" />'
)

# Add ID to analyze prescription button
content = content.replace(
    '<button class="flex-1 py-2.5 px-4 rounded-lg bg-surface-container-high hover:bg-surface-container-highest text-on-surface font-label font-semibold text-xs tracking-wide transition-all flex items-center justify-center gap-2" type="button">\n<span class="material-symbols-outlined text-primary text-[18px]">document_scanner</span>\n          Re-Analyze Prescription OCR\n        </button>',
    '<button id="analyze-prescription-btn" class="flex-1 py-2.5 px-4 rounded-lg bg-surface-container-high hover:bg-surface-container-highest text-on-surface font-label font-semibold text-xs tracking-wide transition-all flex items-center justify-center gap-2" type="button">\n<span class="material-symbols-outlined text-primary text-[18px]">document_scanner</span>\n          Re-Analyze Prescription OCR\n        </button>'
)

# Add ID to synthesize button
content = content.replace(
    '<button class="w-full py-4 px-8 rounded-xl bg-primary hover:opacity-95 text-on-primary font-label font-bold text-base tracking-wide transition-all shadow-md flex items-center justify-center gap-3 group" type="button">\n<span class="material-symbols-outlined text-[22px] group-hover:rotate-12 transition-transform">bolt</span>\n<span>Synthesize Multimodal Symptoms &amp; Prescription Interaction</span>\n<span class="material-symbols-outlined text-[20px] group-hover:translate-x-1 transition-transform">arrow_forward</span>\n</button>',
    '<button id="synthesize-btn" class="w-full py-4 px-8 rounded-xl bg-primary hover:opacity-95 text-on-primary font-label font-bold text-base tracking-wide transition-all shadow-md flex items-center justify-center gap-3 group" type="button">\n<span class="material-symbols-outlined text-[22px] group-hover:rotate-12 transition-transform">bolt</span>\n<span>Synthesize Multimodal Symptoms &amp; Prescription Interaction</span>\n<span class="material-symbols-outlined text-[20px] group-hover:translate-x-1 transition-transform">arrow_forward</span>\n</button>'
)

# Add elements to display the dynamic text (replacing static text)
content = content.replace(
    '<span class="font-semibold text-on-surface">Acute Migraine w/o Aura</span>',
    '<span id="extracted-symptoms-display" class="font-semibold text-on-surface">...</span>'
)
content = content.replace(
    '<span class="font-semibold text-tertiary">Moderate–Severe (7 / 10)</span>',
    '<span id="prescription-ocr-display" class="font-semibold text-tertiary">...</span>'
)

# Add a div to display the final analysis
content = content.replace(
    '<h2 class="font-headline text-3xl font-bold text-on-surface tracking-tight">Clinical Synthesis &amp; Diagnostic Hypothesis</h2>',
    '<h2 class="font-headline text-3xl font-bold text-on-surface tracking-tight">Clinical Synthesis &amp; Diagnostic Hypothesis</h2>\n<div id="final-analysis-display" class="mt-4 p-4 bg-surface-container-lowest rounded-xl text-sm font-body whitespace-pre-wrap">Waiting for synthesis...</div>'
)

# Add Marked.js
content = content.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>\n</head>')

# Add JS logic
js_code = """
<script>
    let prescriptionJsonData = "{}";

    document.getElementById('extract-symptoms-btn').addEventListener('click', async () => {
        const text = document.getElementById('symptoms-input').value;
        document.getElementById('extracted-symptoms-display').innerText = "Extracting...";
        
        const formData = new FormData();
        formData.append('type', 'Text');
        formData.append('text', text);

        try {
            const response = await fetch('/api/symptoms', { method: 'POST', body: formData });
            const data = await response.json();
            document.getElementById('extracted-symptoms-display').innerText = data.text.substring(0, 50) + "...";
        } catch (e) {
            document.getElementById('extracted-symptoms-display').innerText = "Error extracting.";
        }
    });

    document.getElementById('analyze-prescription-btn').addEventListener('click', async () => {
        const fileInput = document.getElementById('prescription-upload');
        if (!fileInput.files.length) {
            alert("Please upload an image first.");
            return;
        }

        document.getElementById('prescription-ocr-display').innerText = "Analyzing...";
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/api/prescription', { method: 'POST', body: formData });
            const data = await response.json();
            document.getElementById('prescription-ocr-display').innerText = "Analyzed!";
            prescriptionJsonData = JSON.stringify(data.data);
        } catch (e) {
            document.getElementById('prescription-ocr-display').innerText = "Error analyzing.";
        }
    });

    document.getElementById('synthesize-btn').addEventListener('click', async () => {
        const symptoms = document.getElementById('symptoms-input').value;
        const analysisDisplay = document.getElementById('final-analysis-display');
        analysisDisplay.innerHTML = "<em>Generating synthesis...</em>";

        const formData = new FormData();
        formData.append('symptoms', symptoms);
        formData.append('prescription_data', prescriptionJsonData);

        try {
            const response = await fetch('/api/analyze', { method: 'POST', body: formData });
            const data = await response.json();
            analysisDisplay.innerHTML = marked.parse(data.analysis);
        } catch (e) {
            analysisDisplay.innerHTML = `<span class="text-error">Error: ${e}</span>`;
        }
    });
</script>
"""
content = content.replace('</body>', js_code + '</body>')

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched index.html!")
