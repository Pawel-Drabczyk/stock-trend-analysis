#!/bin/bash
IFS=' ' read -ra CMD <<< "$@"

echo "${CMD[@]}"
"${CMD[@]}"
