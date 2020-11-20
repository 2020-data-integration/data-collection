./neo4j-admin import \
    --id-type=STRING \
    --skip-duplicate-nodes=true \
    --ignore-empty-strings=true \
    --nodes=new_import/company.csv \
    --nodes=new_import/industry.csv \
    --relationships=new_import/industry_company.csv \
    --relationships=new_import/company_company.csv