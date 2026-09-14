import os
import shutil
import zipfile

desktop = r"C:\Users\joaov\Desktop"
target_dir = os.path.join(desktop, "ENTREGA_SPRINT3_DISRUPTIVE_ARCHITECTURES")
zip_path = os.path.join(desktop, "ENTREGA_SPRINT3_DISRUPTIVE_ARCHITECTURES.zip")

# Recreate target_dir
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
os.makedirs(target_dir, exist_ok=True)

# 1. PDF técnico (6 páginas, com diagrama arquitetural de alta resolução incorporado na pág 3)
src_pdf = os.path.join(desktop, "DOCUMENTACAO_TECNICA_IA_CLYVO_VET.pdf")
dst_pdf = os.path.join(target_dir, "DOCUMENTACAO_TECNICA_IA_CLYVO_VET.pdf")
shutil.copy2(src_pdf, dst_pdf)

# 2. Arquivo com links e instruções de execução
src_txt = os.path.join(desktop, "ENTREGA_SPRINT3_DISRUPTIVE_ARCHITECTURES_IOT.txt")
dst_txt = os.path.join(target_dir, "ENTREGA_SPRINT3_DISRUPTIVE_ARCHITECTURES_IOT.txt")
shutil.copy2(src_txt, dst_txt)

# Remove old zip if exists
if os.path.exists(zip_path):
    os.remove(zip_path)

# Create zip with only the files directly in root
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for filename in sorted(os.listdir(target_dir)):
        filepath = os.path.join(target_dir, filename)
        if os.path.isfile(filepath):
            zf.write(filepath, arcname=filename)
            print(f"Added to ZIP: {filename} ({os.path.getsize(filepath)} bytes)")

print(f"\nZIP final gerado com sucesso: {zip_path} ({os.path.getsize(zip_path)} bytes)")

# Também copia para a pasta do projeto challenge-sprint-3
challenge_dir = r"C:\Users\joaov\Desktop\challenge-sprint-3"
shutil.copy2(zip_path, os.path.join(challenge_dir, "ENTREGA_SPRINT3_DISRUPTIVE_ARCHITECTURES.zip"))
shutil.copy2(dst_pdf, os.path.join(challenge_dir, "DOCUMENTACAO_TECNICA_IA_CLYVO_VET.pdf"))
print("Copiado para challenge-sprint-3 com sucesso.")
