#!/bin/bash

# Verifica se o nome do componente foi passado
if [ -z "$1" ]; then
  echo "Uso: ./create_component.sh NomeDoComponente"
  exit 1
fi

COMPONENT_NAME=$1
COMPONENT_NAME_LOWER=$(echo "$COMPONENT_NAME" | tr '[:upper:]' '[:lower:]')

# Diretórios
CONTROLLER_DIR="src/controllers"
MODEL_DIR="src/models"
VIEW_DIR="src/views"

# Cria diretórios se não existirem
mkdir -p $CONTROLLER_DIR $MODEL_DIR $VIEW_DIR

# Arquivos
CONTROLLER_FILE="$CONTROLLER_DIR/${COMPONENT_NAME_LOWER}_controller.py"
MODEL_FILE="$MODEL_DIR/${COMPONENT_NAME_LOWER}_model.py"
VIEW_FILE="$VIEW_DIR/${COMPONENT_NAME_LOWER}_view.py"

# Controller
cat <<EOF > $CONTROLLER_FILE
class ${COMPONENT_NAME}Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
EOF

# Model
cat <<EOF > $MODEL_FILE
class ${COMPONENT_NAME}Model:
    def __init__(self):
        pass
EOF

# View
cat <<EOF > $VIEW_FILE
class ${COMPONENT_NAME}View:
    def __init__(self):
        pass
EOF

echo "Componente '$COMPONENT_NAME' criado com sucesso!"
echo " - $CONTROLLER_FILE"
echo " - $MODEL_FILE"
echo " - $VIEW_FILE"
