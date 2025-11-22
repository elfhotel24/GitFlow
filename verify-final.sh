#!/bin/bash

echo "🔍 VERIFICACIÓN FINAL DEL GIT FLOW"

echo "🌿 RAMAS EXISTENTES:"
git branch -a

echo ""
echo "📊 COMMITS EN MAIN:"
git log main --oneline -10

echo ""
echo "📊 COMMITS EN DEVELOP:"
git log develop --oneline -5

echo ""
echo "📊 COMMITS EN QA:"
git log qa --oneline -5

echo ""
echo "🔄 TOTAL DE MERGES:"
git log --oneline --merges | wc -l

echo ""
echo "📈 GRÁFICO DEL HISTORIAL:"
git log --oneline --graph --all -15

echo ""
echo "✅ VERIFICACIÓN COMPLETADA"
