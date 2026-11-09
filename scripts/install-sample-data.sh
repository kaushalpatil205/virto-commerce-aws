#!/bin/bash
set -e

PLATFORM_URL="http://localhost:8081"

echo "=========================================================="
echo "Virto Commerce Sample Data Installation & Verification"
echo "=========================================================="

# Check current count in database
STORE_COUNT=$(docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -h -1 -W -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM VirtoCommerce3.dbo.Store" 2>/dev/null | tr -d '[:space:]' || echo "0")
PRODUCT_COUNT=$(docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -h -1 -W -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM VirtoCommerce3.dbo.Item" 2>/dev/null | tr -d '[:space:]' || echo "0")

if [ "$STORE_COUNT" -ge 1 ] && [ "$PRODUCT_COUNT" -ge 389 ]; then
    echo "  ✓ Sample data is already fully populated in the database!"
else
    echo -e "\n[1/3] Authenticating as admin to trigger sample data import..."
    TOKEN=$(curl -s -X POST "${PLATFORM_URL}/connect/token" -d "grant_type=password&username=admin&password=store" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || true)
    
    if [ -z "$TOKEN" ]; then
        echo "  [Error] Could not obtain bearer token from ${PLATFORM_URL}/connect/token."
        echo "  Ensure vc-platform-backend is running and healthy."
        exit 1
    fi
    echo "  ✓ Authenticated successfully with Virto Commerce API."

    echo -e "\n[2/3] Checking if auto-installation is already active or triggering it..."
    curl -s -X POST "${PLATFORM_URL}/api/platform/sampledata/autoinstall" -H "Authorization: Bearer ${TOKEN}" > /dev/null 2>&1 || true

    echo -e "\n[3/3] Waiting for download (59.5 MB) and database import to complete..."
    for i in $(seq 1 60); do
        sleep 4
        # Check push notification description if available
        STATUS_DESC=$(curl -s -X POST "${PLATFORM_URL}/api/platform/pushnotifications" -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" -d '{"take": 1}' | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('notifyEvents', [{}])[0].get('description') or '')" 2>/dev/null || echo "")
        
        STORES=$(docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -h -1 -W -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM VirtoCommerce3.dbo.Store" 2>/dev/null | tr -d '[:space:]' || echo "0")
        PRODUCTS=$(docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -h -1 -W -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM VirtoCommerce3.dbo.Item" 2>/dev/null | tr -d '[:space:]' || echo "0")

        if [ -n "$STATUS_DESC" ]; then
            echo "  [Wait $((i*4))s] $STATUS_DESC (DB: Stores=${STORES}, Products=${PRODUCTS})"
        else
            echo "  [Wait $((i*4))s] Importing... (DB: Stores=${STORES}, Products=${PRODUCTS})"
        fi

        if [ "$STORES" -ge 1 ] && [ "$PRODUCTS" -ge 389 ]; then
            echo -e "\n  ✓ Import successfully completed!"
            break
        fi
    done
fi

echo -e "\nFinal Verified Entity Counts in Database:"
docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -Q "SELECT (SELECT COUNT(*) FROM VirtoCommerce3.dbo.Store) as Stores, (SELECT COUNT(*) FROM VirtoCommerce3.dbo.Catalog) as Catalogs, (SELECT COUNT(*) FROM VirtoCommerce3.dbo.Category) as Categories, (SELECT COUNT(*) FROM VirtoCommerce3.dbo.Item) as Products"
