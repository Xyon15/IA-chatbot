#!/usr/bin/env python3
"""
Diagnostic approfondi du fichier .env et du token Discord
"""

import os
import sys
from pathlib import Path

def diagnose_env_file():
    """Diagnostique complet du fichier .env"""
    print("🔍 Diagnostic Approfondi du Fichier .env")
    print("=" * 50)
    
    env_path = Path("../.env")
    
    if not env_path.exists():
        print("❌ Fichier .env introuvable!")
        return False
    
    print(f"✅ Fichier .env trouvé: {env_path.absolute()}")
    
    # Lire le fichier en mode binaire pour voir l'encodage
    with open(env_path, 'rb') as f:
        raw_content = f.read()
    
    print(f"📏 Taille du fichier: {len(raw_content)} bytes")
    
    # Détecter l'encodage
    try:
        content_utf8 = raw_content.decode('utf-8')
        print("✅ Encodage: UTF-8")
    except UnicodeDecodeError:
        try:
            content_utf8 = raw_content.decode('latin-1')
            print("⚠️ Encodage: Latin-1 (peut causer des problèmes)")
        except UnicodeDecodeError:
            print("❌ Encodage non reconnu")
            return False
    
    # Analyser chaque ligne
    print("\n📋 Contenu ligne par ligne:")
    lines = content_utf8.split('\n')
    
    for i, line in enumerate(lines, 1):
        print(f"Ligne {i}: '{line}'")
        if line.strip() == '':
            print(f"  → Ligne vide")
        elif line.startswith('#'):
            print(f"  → Commentaire")
        elif '=' in line:
            key, value = line.split('=', 1)
            print(f"  → Variable: '{key}' = '{value}'")
            
            # Vérifications spécifiques
            if key == 'DISCORD_TOKEN':
                print(f"    🔍 Token trouvé, longueur: {len(value)}")
                if value.strip() != value:
                    print(f"    ⚠️ PROBLÈME: Espaces détectés autour du token!")
                    print(f"    📝 Token avec espaces: '{value}'")
                    print(f"    ✂️ Token nettoyé: '{value.strip()}'")
                
                # Vérifier le format du token
                clean_token = value.strip()
                if len(clean_token) < 50:
                    print(f"    ❌ Token trop court (< 50 caractères)")
                elif '.' not in clean_token:
                    print(f"    ❌ Format de token invalide (pas de points)")
                else:
                    parts = clean_token.split('.')
                    print(f"    🔍 Token en {len(parts)} parties: {[len(p) for p in parts]}")
                    if len(parts) == 3:
                        print(f"    ✅ Format de token correct (3 parties)")
                    else:
                        print(f"    ❌ Format de token incorrect ({len(parts)} parties)")
    
    return True

def test_env_loading():
    """Teste le chargement des variables d'environnement"""
    print("\n🧪 Test de Chargement des Variables")
    print("=" * 40)
    
    try:
        # Changer vers le répertoire parent pour charger .env
        original_cwd = os.getcwd()
        parent_dir = Path("..").absolute()
        os.chdir(parent_dir)
        
        from dotenv import load_dotenv
        
        print(f"📂 Répertoire de travail: {os.getcwd()}")
        
        # Charger .env
        result = load_dotenv()
        print(f"🔄 load_dotenv() résultat: {result}")
        
        # Vérifier les variables
        discord_token = os.getenv("DISCORD_TOKEN")
        auth_secret = os.getenv("AUTH_SECRET")
        
        print("\n📋 Variables chargées:")
        if discord_token:
            print(f"✅ DISCORD_TOKEN: longueur {len(discord_token)}")
            print(f"   Début: {discord_token[:20]}...")
            print(f"   Fin: ...{discord_token[-10:]}")
            
            # Test de caractères invisibles
            if discord_token != discord_token.strip():
                print(f"   ⚠️ PROBLÈME: Espaces détectés!")
                print(f"   📏 Longueur avant strip: {len(discord_token)}")
                print(f"   📏 Longueur après strip: {len(discord_token.strip())}")
        else:
            print("❌ DISCORD_TOKEN: Non trouvé")
        
        if auth_secret:
            print(f"✅ AUTH_SECRET: longueur {len(auth_secret)}")
            if auth_secret != auth_secret.strip():
                print(f"   ⚠️ PROBLÈME: Espaces détectés dans AUTH_SECRET!")
        else:
            print("❌ AUTH_SECRET: Non trouvé")
        
        # Restaurer le répertoire
        os.chdir(original_cwd)
        
        return discord_token, auth_secret
        
    except Exception as e:
        os.chdir(original_cwd)
        print(f"❌ Erreur lors du chargement: {e}")
        return None, None

def fix_env_file():
    """Propose une correction automatique du fichier .env"""
    print("\n🔧 Correction Automatique")
    print("=" * 30)
    
    env_path = Path("../.env")
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        changes_made = False
        
        for line in lines:
            original_line = line
            
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.split('=', 1)
                clean_key = key.strip()
                clean_value = value.rstrip('\n\r').rstrip()  # Supprimer seulement les espaces de fin
                
                if key != clean_key or value.rstrip('\n\r') != clean_value:
                    fixed_line = f"{clean_key}={clean_value}\n"
                    fixed_lines.append(fixed_line)
                    changes_made = True
                    print(f"🔄 Corrigé: {clean_key}")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        if changes_made:
            # Sauvegarder une copie
            backup_path = env_path.with_suffix('.env.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"💾 Sauvegarde créée: {backup_path}")
            
            # Écrire le fichier corrigé
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            print("✅ Fichier .env corrigé!")
            
            return True
        else:
            print("✅ Aucune correction nécessaire")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

if __name__ == "__main__":
    success = diagnose_env_file()
    
    if success:
        discord_token, auth_secret = test_env_loading()
        
        if discord_token and auth_secret:
            print("\n🎯 Résumé:")
            if (discord_token.strip() != discord_token or 
                auth_secret.strip() != auth_secret):
                print("⚠️ PROBLÈME TROUVÉ: Espaces parasites détectés")
                
                if input("\n🔧 Corriger automatiquement? (y/n): ").lower() == 'y':
                    if fix_env_file():
                        print("✅ Correction effectuée!")
                        print("🚀 Relancez maintenant: python start_bot.py")
            else:
                print("✅ Variables d'environnement correctes")
                print("🤔 Le problème peut venir d'ailleurs...")
                print("💡 Vérifiez que le token Discord n'a pas expiré")