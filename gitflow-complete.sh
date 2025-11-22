#!/bin/bash

echo "🚀 INICIANDO CONFIGURACIÓN COMPLETA DE GIT FLOW"

# Configuración inicial
echo "📝 Configurando usuario Git..."
git config user.name "elfhotel24"
git config user.email "tu-email@gmail.com"

# Crear ramas base
echo "🌿 Creando ramas base..."
git checkout -b develop
git push -u origin develop

git checkout -b qa
git push -u origin qa

# Volver a develop
git checkout develop

# Crear directorios para las features
mkdir -p templates utils services hotfixes

# Lista de features a crear
features=(
    "feature/login-form"
    "feature/validate-user-input" 
    "feature/payment-api-integration"
    "feature/user-dashboard"
    "hotfix/fix-date-format"
)

echo "🎯 Creando ${#features[@]} ramas de features..."

for feature in "${features[@]}"; do
    echo "📝 Creando: $feature"
    
    # Crear rama desde develop
    git checkout develop
    git checkout -b "$feature"
    
    # Crear un archivo específico para cada feature
    case $feature in
        "feature/login-form")
            echo "<!-- Login Form Feature -->" > templates/login.html
            ;;
        "feature/validate-user-input")
            echo "# Validaciones" > utils/validators.py
            ;;
        "feature/payment-api-integration")
            echo "# Servicio de Pagos" > services/payment_service.py
            ;;
        "feature/user-dashboard")
            echo "<!-- Dashboard -->" > templates/dashboard.html
            ;;
        "hotfix/fix-date-format")
            echo "# Fix para fechas" > hotfixes/date_fix.py
            ;;
    esac
    
    # Commit y push
    git add .
    git commit -m "feat: Implement $feature"
    git push -u origin "$feature"
    
    echo "✅ $feature creada exitosamente"
done

echo "🎉 Todas las ramas features creadas!"
