neo4j-admin import \
    --id-type=STRING \
    --skip-duplicate-nodes=true \
    --ignore-empty-strings=true \
    --nodes=import/company.csv \
    --nodes=import/concept.csv \
    --relationships=import/company_concept.csv