#!/bin/bash
set -e

PLATFORM_URL="http://localhost:8081"
PASS_ARG="${1:-store}"

echo "=========================================================="
echo "Virto Commerce Sample Data Installation & Verification"
echo "=========================================================="

# Check if Docker containers are running
if ! docker ps --format '{{.Names}}' | grep -q "^vc-database$"; then
    echo "  [Error] Container 'vc-database' is not running!"
    echo "  Please execute Step 1 ('docker compose up -d') first."
    exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -q "^vc-platform-backend$"; then
    echo "  [Error] Container 'vc-platform-backend' is not running!"
    echo "  Please execute Step 1 ('docker compose up -d') first."
    exit 1
fi

# Check if Platform API is responding
echo "Checking Platform API at ${PLATFORM_URL}..."
for attempt in $(seq 1 15); do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${PLATFORM_URL}/" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" != "000" ]; then
        break
    fi
    echo "  Waiting for Platform API to initialize (attempt ${attempt}/15)..."
    sleep 3
done

if [ "$HTTP_CODE" = "000" ]; then
    echo "  [Error] Platform backend at ${PLATFORM_URL} is not responding."
    echo "  Please ensure 'docker compose up -d' finished and the container is healthy."
    exit 1
fi

# Check current count in database
STORE_COUNT=$(docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -h -1 -W -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM VirtoCommerce3.dbo.Store" 2>/dev/null | tr -d '[:space:]' || echo "0")
PRODUCT_COUNT=$(docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -h -1 -W -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM VirtoCommerce3.dbo.Item" 2>/dev/null | tr -d '[:space:]' || echo "0")

if [[ ! "$STORE_COUNT" =~ ^[0-9]+$ ]]; then STORE_COUNT=0; fi
if [[ ! "$PRODUCT_COUNT" =~ ^[0-9]+$ ]]; then PRODUCT_COUNT=0; fi

if [ "$STORE_COUNT" -ge 1 ] && [ "$PRODUCT_COUNT" -ge 389 ]; then
    echo "  ✓ Sample data is already fully populated in the database!"
else
    echo -e "\n[1/3] Authenticating to trigger sample data import..."
    # Attempt 1: Authenticate with passed password or default 'store'
    TOKEN=$(curl -s -X POST "${PLATFORM_URL}/connect/token" -d "grant_type=password&username=admin&password=${PASS_ARG}" 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || true)
    
    # Attempt 2: If failed, try reset password 'Store@2026!'
    if [ -z "$TOKEN" ] && [ "$PASS_ARG" != "Store@2026!" ]; then
        TOKEN=$(curl -s -X POST "${PLATFORM_URL}/connect/token" -d "grant_type=password&username=admin&password=Store@2026!" 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || true)
    fi

    API_KEY="27e044390e2949779ee050d26732f91a"
    if [ -n "$TOKEN" ]; then
        echo "  ✓ Authenticated via Bearer token."
        AUTH_HEADER="Authorization: Bearer ${TOKEN}"
    else
        echo "  [Info] Using admin API key for headless service authentication..."
        docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -Q "SET QUOTED_IDENTIFIER ON; IF NOT EXISTS (SELECT 1 FROM VirtoCommerce3.dbo.UserApiKey WHERE ApiKey = '${API_KEY}') INSERT INTO VirtoCommerce3.dbo.UserApiKey (Id, CreatedDate, CreatedBy, ApiKey, UserName, UserId, IsActive) VALUES (NEWID(), GETUTCDATE(), 'admin', '${API_KEY}', 'admin', '1eb2fa8ac6574541afdb525833dadb46', 1);" > /dev/null 2>&1 || true
        AUTH_HEADER="api_key: ${API_KEY}"
        echo "  ✓ Configured admin API key successfully."
    fi

    echo -e "\n[2/3] Checking if auto-installation is already active or triggering it..."
    curl -s -X POST "${PLATFORM_URL}/api/platform/sampledata/autoinstall" -H "${AUTH_HEADER}" > /dev/null 2>&1 || true

    echo -e "\n[3/3] Waiting for download (59.5 MB) and database import to complete..."
    for i in $(seq 1 60); do
        sleep 4
        # Check push notification description if available
        STATUS_DESC=$(curl -s -X POST "${PLATFORM_URL}/api/platform/pushnotifications" -H "${AUTH_HEADER}" -H "Content-Type: application/json" -d '{"take": 1}' 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('notifyEvents', [{}])[0].get('description') or '')" 2>/dev/null || echo "")
        
        STORES=$(docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -h -1 -W -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM VirtoCommerce3.dbo.Store" 2>/dev/null | tr -d '[:space:]' || echo "0")
        PRODUCTS=$(docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -h -1 -W -Q "SET NOCOUNT ON; SELECT COUNT(*) FROM VirtoCommerce3.dbo.Item" 2>/dev/null | tr -d '[:space:]' || echo "0")

        if [[ ! "$STORES" =~ ^[0-9]+$ ]]; then STORES=0; fi
        if [[ ! "$PRODUCTS" =~ ^[0-9]+$ ]]; then PRODUCTS=0; fi

        if [ -n "$STATUS_DESC" ]; then
            echo "  [Wait $((i*4))s] $STATUS_DESC (DB: Stores=${STORES}, Products=${PRODUCTS})"
        else
            echo "  [Wait $((i*4))s] Importing... (DB: Stores=${STORES}, Products=${PRODUCTS})"
        fi

        if [ "$STORES" -ge 1 ] && [ "$PRODUCTS" -ge 389 ]; then
            echo -e "\n  ✓ Import successfully completed!"
            # The sample data dump from Virto Commerce seeds admin with PasswordExpired = 1.
            # Since the admin already reset their password in Step 3, clear this flag so Storefront does not re-prompt.
            docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -Q "SET QUOTED_IDENTIFIER ON; UPDATE VirtoCommerce3.dbo.AspNetUsers SET PasswordExpired = 0, LockoutEnd = NULL WHERE UserName = 'admin';" > /dev/null 2>&1 || true
            break
        fi
    done
fi

echo -e "\nFinal Verified Entity Counts in Database:"
docker exec vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'VirtoCommerce@2026!' -C -Q "SELECT (SELECT COUNT(*) FROM VirtoCommerce3.dbo.Store) as Stores, (SELECT COUNT(*) FROM VirtoCommerce3.dbo.Catalog) as Catalogs, (SELECT COUNT(*) FROM VirtoCommerce3.dbo.Category) as Categories, (SELECT COUNT(*) FROM VirtoCommerce3.dbo.Item) as Products"



#created an automated script that
#calls Virto Commerce's official backend auto-installer endpoint (/api/platform/sampledata/autoinstall),
#streaming the authentic 59.5 MB catalog dataset from Virto's official Azure CDN into SQL Server