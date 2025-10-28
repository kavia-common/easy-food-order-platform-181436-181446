#!/bin/bash
cd /home/kavia/workspace/code-generation/easy-food-order-platform-181436-181446/food_ordering_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

