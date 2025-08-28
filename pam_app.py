from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template
HTML = """
<!doctype html>
<title>PAM Sequence Finder</title>
<h2>PAM Sequence Finder (CRISPR-Cas9)</h2>
<form method="POST">
  Enter nucleotide sequence:<br>
  <textarea name="sequence" rows="4" cols="50">{{ sequence }}</textarea><br><br>
  <input type="submit" value="Find PAMs">
</form>
{% if pams %}
  <h3>Found PAM sequences (NGG):</h3>
  <ul>
    {% for pam in pams %}
      <li>{{ pam }}</li>
    {% endfor %}
  </ul>
{% endif %}
"""

# PAM finder logic
def find_pam_sites(seq):
    seq = seq.upper()
    pams = []
    for i in range(len(seq) - 2):
        if seq[i+1:i+3] == "GG":
            pam = seq[i:i+3]
            pams.append(f"{pam} at position {i}")
    return pams

@app.route("/", methods=["GET", "POST"])
def index():
    sequence = ""
    pams = []
    if request.method == "POST":
        sequence = request.form["sequence"]
        pams = find_pam_sites(sequence)
    return render_template_string(HTML, sequence=sequence, pams=pams)

if __name__ == "__main__":
    app.run(debug=True)
