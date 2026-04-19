import base64

# Lire le fichier session
with open('fingerbot_session.session', 'rb') as f:
    session_bytes = f.read()

# Encoder en base64
session_base64 = base64.b64encode(session_bytes).decode('utf-8')

# Afficher
print("\n" + "="*60)
print("SESSION_BASE64 (copie tout entre les lignes)")
print("="*60)
print(session_base64)
print("="*60)
print(f"\nLongueur: {len(session_base64)} caractères")
print(f"Valide: {len(session_base64) % 4 == 0}")

# Sauvegarder
with open('session_base64.txt', 'w') as f:
    f.write(session_base64)

print("\n✅ Sauvegardé dans session_base64.txt")