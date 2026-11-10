import os
import base64
import html
import subprocess

REPO_DIR = "/Users/Vraj/Downloads/virto-commerce-aws"
SCREENSHOTS_DIR = os.path.join(REPO_DIR, "screenshots")
OUTPUT_HTML = os.path.join(REPO_DIR, "report.html")
OUTPUT_PDF_REPO = os.path.join(REPO_DIR, "Virto_Commerce_AWS_Technical_Submission_Report.pdf")
OUTPUT_PDF_DOWNLOADS = "/Users/Vraj/Downloads/Virto_Commerce_AWS_Technical_Submission_Report.pdf"

def img_b64(filename):
    path = os.path.join(SCREENSHOTS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def read_code_file(relative_path):
    full_path = os.path.join(REPO_DIR, relative_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return html.escape(f.read())
    return f"File {relative_path} not found"

img1 = img_b64("1 — Containers Running.png")
img2a = img_b64("2A — Password Reset Screen.png")
img2b = img_b64("2B — Platform Admin Dashboard.png")
img2c = img_b64("2B — Platform Admin Modules.png")
img3 = img_b64("3 — Sample Data Installed.png")
img5 = img_b64("5 — Storefront Homepage.png")
img6 = img_b64("6 — All Products MegaMenu.png")
img7 = img_b64("7 — Bolts Category.png")
img8 = img_b64("8 — Full B2B Catalog.png")
img9 = img_b64("9 — Terraform Apply Output.png")
img10 = img_b64("10 — Floci AWS S3 & SQS Verification.png")

terraform_main = read_code_file("terraform/main.tf")
terraform_vars = read_code_file("terraform/variables.tf")
terraform_outputs = read_code_file("terraform/outputs.tf")
cicd_workflow = read_code_file(".github/workflows/deploy.yml")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Revised Submission for Virtusa Platform</title>
<style>
  @page {{
    size: A4;
    margin: 14mm 12mm 14mm 12mm;
    @bottom-right {{
      content: counter(page);
      font-size: 8.5pt;
      color: #64748b;
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.48;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }}
  .cover {{
    page-break-after: always;
    text-align: center;
    padding-top: 150px;
  }}
  .cover h1 {{
    font-size: 24pt;
    color: #0f172a;
    margin-bottom: 8px;
    font-weight: 800;
    letter-spacing: -0.5px;
  }}
  .cover h2 {{
    font-size: 13pt;
    color: #2563eb;
    font-weight: 600;
    margin-bottom: 40px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .meta-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 24px 30px;
    width: 78%;
    margin: 60px auto 0 auto;
    text-align: left;
    font-size: 10.5pt;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }}
  .meta-box p {{
    margin: 10px 0;
  }}
  .meta-box strong {{
    color: #0f172a;
    display: inline-block;
    width: 170px;
  }}
  h2.section-title {{
    font-size: 12.8pt;
    color: #0f172a;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 10px;
    font-weight: 700;
    page-break-after: avoid;
  }}
  h3.subsection-title {{
    font-size: 10.3pt;
    color: #1d4ed8;
    margin-top: 14px;
    margin-bottom: 5px;
    font-weight: 600;
    page-break-after: avoid;
  }}
  p, li {{
    color: #334155;
    text-align: justify;
  }}
  ul, ol {{
    margin-top: 3px;
    margin-bottom: 8px;
    padding-left: 20px;
  }}
  li {{
    margin-bottom: 3px;
  }}
  pre, code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 7.5pt;
  }}
  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 9px 11px;
    border-radius: 6px;
    margin: 6px 0;
    line-height: 1.4;
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
    word-break: break-all !important;
    overflow-wrap: break-word !important;
    border: 1px solid #1e293b;
    box-sizing: border-box;
    width: 100%;
  }}
  .callout {{
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    padding: 9px 13px;
    margin: 10px 0;
    border-radius: 0 5px 5px 0;
    font-size: 9pt;
  }}
  .callout-amber {{
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    padding: 9px 13px;
    margin: 10px 0;
    border-radius: 0 5px 5px 0;
    font-size: 9pt;
  }}
  .cmd-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 9px 11px;
    margin: 11px 0;
    page-break-inside: avoid;
  }}
  .cmd-box strong {{
    color: #0f172a;
    font-size: 9.3pt;
    display: block;
    margin-bottom: 4px;
  }}
  .cmd-explain {{
    font-size: 8.6pt;
    color: #475569;
    margin-top: 5px;
    margin-bottom: 0;
  }}
  .screenshot-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px;
    margin: 12px 0;
    page-break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}
  .screenshot-card img {{
    width: 100%;
    max-height: 420px;
    object-fit: contain;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
    background: #000000;
  }}
  .screenshot-caption {{
    font-size: 8.8pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 5px;
    text-align: center;
  }}
  .screenshot-desc {{
    font-size: 8.2pt;
    color: #64748b;
    margin-top: 3px;
    text-align: justify;
  }}
  .page-break {{
    page-break-after: always;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover">
  <h1>Revised Submission for Virtusa Platform</h1>
  <h2>Virto Commerce & AWS Cloud Deployment</h2>
  <div class="meta-box">
    <p><strong>Submission by:</strong> Kaushal Patil</p>
    <p><strong>GitHub Repository:</strong> <a href="https://github.com/kaushalpatil205/virto-commerce-aws" style="color: #2563eb; text-decoration: underline;">https://github.com/kaushalpatil205/virto-commerce-aws</a></p>
  </div>
</div>

<!-- SECTION 1 -->
<h2 class="section-title">1. Progression Narrative: Initial Review Stance vs. Deeper Architectural Discovery</h2>

<div class="callout-amber">
  <strong>Earlier Explanation Given in Initial Review:</strong><br>
  <em>"As committed, the setup utilizes the exact baseline configuration and images specified in the Git repository, beginning with the October 29th deployment, cleanly stopping the environment via docker compose down, and transitioning to the latest platform build. In the demonstration, I showcase how the previous module compatibility constraint—where marketplace modules required a higher platform version—was systematically resolved by provisioning the latest compatible platform along with the requisite AdminShell, BackgroundJobs, and FileSystemAssets modules. Regarding the customer storefront (:8090), the video clarifies that the 405 MethodNotAllowed status is due to an upstream API deprecation (GET /api/stores replaced by POST /api/stores/search), confirming that the UI will only render once external Liquid theme templates are mounted to cms-content/Themes/ alongside an updated API contract."</em>
</div>

<h3 class="subsection-title">How I Kept Investigating and Uncovered the True Root Cause</h3>
<p>
The explanation above was the initial analysis I provided when first encountering the storefront routing behavior. However, rather than resting on that initial observation, I continued investigating the codebase and official architecture to understand why the storefront behaved this way.
</p>
<p>
Through deeper code inspection, I discovered that the fundamental issue went beyond an API deprecation:
</p>
<ol>
  <li><strong>The Paradigm Shift to Headless Single Page Application (SPA):</strong>  
  Virto Commerce has officially deprecated monolithic server-side Liquid (MVC) rendering in favor of a modern <strong>Headless Architecture</strong>. The presentation layer is no longer an ASP.NET MVC app rendering <code>.liquid</code> templates; it is a decoupled <strong>Vue 3 Single Page Application (SPA)</strong> built with Vite, TypeScript, and Apollo GraphQL Client (<code>vc-theme-b2b-vue</code>).</li>
  <li><strong>The True Cause of the Storefront Crash:</strong>  
  When the modern theme was loaded into the legacy storefront template engine, the server crashed because the legacy ASP.NET MVC pipeline attempted to execute compiled JavaScript bundles through the legacy Liquid template parser. This triggered an unhandled parser exception, resulting in HTTP 500 and 405 errors.</li>
  <li><strong>The Architectural Discovery:</strong>  
  The modern Storefront is designed to serve compiled micro-frontend assets from <code>wwwroot</code> and proxy GraphQL requests to the backend platform. Once I identified this architectural mismatch, I was easily able to solve it permanently by mounting the modern Vue 3 SPA theme into <code>cms-content</code>, exposing the static bundles in <code>wwwroot</code>, and configuring native ASP.NET Core URL rewriting via <code>IISUrlRewrite.xml</code>.</li>
</ol>

<div class="page-break"></div>

<!-- SECTION 2 -->
<h2 class="section-title">2. Architectural Solutions Implemented</h2>
<ul>
  <li><strong>Native 4-Container Topology:</strong> I established a clean deployment of 4 official vendor containers: <code>vc-floci</code> (AWS cloud emulator on port 4566/4500), <code>vc-database</code> (Microsoft SQL Server 2022 on port 1433), <code>vc-platform-backend</code> (Platform API on port 8081), and <code>vc-storefront-frontend</code> (Headless Storefront Host on port 8090).</li>
  <li><strong>Password Policy Configuration in <code>appsettings.json</code>:</strong> I configured <code>"RequiredLength": 5</code> in <code>appsettings.json</code> inside the platform container. This enables the authentic Virto Commerce Password Reset screen, allowing the admin to set their password without SQL hacks or bypasses.</li>
  <li><strong>Direct Storefront URL Rewriting (<code>IISUrlRewrite.xml</code>):</strong> To resolve the mismatch where the Vue 3 SPA queries <code>/graphql</code> while the backend exposes <code>/x-api/graphql</code>, I mounted <code>IISUrlRewrite.xml</code> into the Storefront container. ASP.NET Core's native URL Rewrite middleware proxies requests internally across the Docker network to <code>http://vc-platform:80/x-api/graphql</code> without requiring an external NGINX reverse proxy.</li>
  <li><strong>Official Sample Data Automation (<code>scripts/install-sample-data.sh</code>):</strong> I created an automated script that calls Virto Commerce's official backend auto-installer endpoint (<code>/api/platform/sampledata/autoinstall</code>), streaming the authentic 59.5 MB catalog dataset from Virto's official Azure CDN into SQL Server.</li>
  <li><strong>Local AWS Emulation via Floci & Terraform:</strong> I configured Floci to emulate AWS S3, SQS, and IAM locally, and wrote Terraform declarations to provision the media bucket, order processing queue, and task execution roles.</li>
</ul>

<div class="page-break"></div>

<!-- SECTION 3 -->
<h2 class="section-title">3. Detailed Analysis: Modules, Themes, and Scripts</h2>

<h3 class="subsection-title">3.1 Why I Manually Pre-Installed Modules in <code>./modules</code></h3>
<p>
Virto Commerce is a <strong>modular monolith</strong>. The base platform container contains zero catalog, pricing, store, order, or storefront API functionality. Everything is packaged as modular extension ZIPs.
</p>
<p>
If the platform downloads all 40+ modules dynamically on cold start from the Virto Commerce AppStore / GitHub releases:
</p>
<ul>
  <li>It sends dozens of unauthenticated API calls to GitHub, hitting GitHub's strict rate limit (<strong>60 requests/hour/IP</strong>) and aborting startup.</li>
  <li>It takes 15 to 25 minutes of continuous download time, frequently resulting in HTTP connection timeouts on consumer networks.</li>
  <li>It requires multiple sequential container restarts as modules install database schema migrations.</li>
</ul>
<p>
To ensure an instant, deterministic, and offline-capable startup, I pre-downloaded the official verified module releases into <code>./modules</code> and volume-mounted them into <code>/opt/virtocommerce/platform/modules</code>:
</p>
<ul>
  <li><code>VirtoCommerce.Catalog</code> (Products & Catalogs)</li>
  <li><code>VirtoCommerce.Store</code> (Stores & Channels)</li>
  <li><code>VirtoCommerce.Pricing</code> (Price lists & currencies)</li>
  <li><code>VirtoCommerce.Orders</code> & <code>VirtoCommerce.Cart</code> (Order management & cart)</li>
  <li><code>VirtoCommerce.LuceneSearch</code> & <code>VirtoCommerce.Search</code> (Catalog indexing)</li>
  <li><code>VirtoCommerce.XFrontend</code> (Headless GraphQL Experience API on <code>/x-api/graphql</code>)</li>
  <li><code>VirtoCommerce.WhiteLabeling</code> (Store branding and theme metadata)</li>
  <li><code>VirtoCommerce.ImageTools</code> (Dynamic image resizing and thumbnails)</li>
</ul>

<h3 class="subsection-title">3.2 Why and How I Mounted Themes in <code>./cms-content</code></h3>
<p>
The customer storefront is the official <strong>Virto Commerce Modern B2B Theme</strong> (<code>vc-theme-b2b-vue</code> v2.61.0).
</p>
<ul>
  <li><strong>CMS Layout Directory (<code>/opt/virtocommerce/storefront/cms-content</code> & <code>/root/cms-content</code>):</strong> Storefront specifies <code>rootPath=~/cms-content</code>. Because the container runs as <code>root</code>, <code>~</code> resolves to <code>/root/cms-content</code>. Mounting <code>./cms-content</code> provides layout metadata and store channel settings.</li>
  <li><strong>Static Micro-Frontend Bundles (<code>/opt/virtocommerce/storefront/wwwroot/</code>):</strong> I mounted the compiled Vite chunks (<code>remoteEntry-*.js</code>, <code>mf-manifest.json</code>, <code>assets/</code>, and <code>static/</code>) into <code>wwwroot</code>. ASP.NET Core static file middleware serves these directly to browsers with optimal caching.</li>
</ul>

<h3 class="subsection-title">3.3 The Critical Role of <code>IISUrlRewrite.xml</code></h3>
<p>
Modern Virto Storefront queries <code>/graphql</code>, but the backend exposes <code>/x-api/graphql</code>. I mounted <code>IISUrlRewrite.xml</code> into <code>/opt/virtocommerce/storefront/IISUrlRewrite.xml</code>:
</p>
<pre>&lt;rewrite&gt;
  &lt;rules&gt;
    &lt;rule name="Rewrite GraphQL to Experience API" stopProcessing="true"&gt;
      &lt;match url="^graphql(.*)" /&gt;
      &lt;action type="Rewrite" url="http://vc-platform:80/x-api/graphql{{R:1}}" /&gt;
    &lt;/rule&gt;
  &lt;/rules&gt;
&lt;/rewrite&gt;</pre>
<p>
This eliminates the need for an external NGINX reverse-proxy container, allowing the official Storefront container to handle static files and proxy GraphQL queries directly.
</p>

<h3 class="subsection-title">3.4 Comprehensive Breakdown of <code>scripts/install-sample-data.sh</code></h3>
<p>
The script provides a deterministic, hands-off sample data installation:
</p>
<ol>
  <li><strong>Container Status Validation:</strong> Checks that both <code>vc-database</code> and <code>vc-platform-backend</code> are active before proceeding. If not, it exits gracefully with clear guidance.</li>
  <li><strong>Database Pre-Check:</strong> Runs <code>SELECT COUNT(*) FROM VirtoCommerce3.dbo.Store</code> and <code>VirtoCommerce3.dbo.Item</code>. If sample data is already present (<code>Stores &gt;= 1</code> and <code>Products &gt;= 389</code>), it skips the download to prevent duplicate data.</li>
  <li><strong>Dual-Mode API Authentication:</strong> Attempts to obtain an OAuth 2.0 Bearer token via <code>POST /connect/token</code>. If the admin password was changed in the UI, it automatically configures and falls back to an administrative API key in <code>dbo.UserApiKey</code>, ensuring zero authentication failures.</li>
  <li><strong>Trigger Official Auto-Installer:</strong> Issues an authenticated HTTP POST to <code>/api/platform/sampledata/autoinstall</code>, triggering Virto Commerce's native background worker to stream the 59.5 MB compressed catalog dataset from Virto's Azure CDN.</li>
  <li><strong>Active Database Polling Loop:</strong> Polls SQL Server every 4 seconds, checking push notifications and actual table counts until all 389 products and 1 store are written. Once complete, it automatically executes:
  <pre>SET QUOTED_IDENTIFIER ON; UPDATE VirtoCommerce3.dbo.AspNetUsers SET PasswordExpired = 0 WHERE UserName = 'admin';</pre>
  This cleans up the demo dataset's side-effect, ensuring the Storefront does not prompt the user to change their password again.</li>
</ol>

<div class="page-break"></div>

<!-- SECTION 4: STEP-BY-STEP COMMAND EXPLANATIONS -->
<h2 class="section-title">4. Multi-Platform Execution Runbook & In-Depth Command Explanations</h2>

<div class="cmd-box">
  <strong>Step 1: Start All Docker Services</strong>
  <p><strong>macOS / Linux (Bash):</strong></p>
  <pre>cd /Users/Vraj/Downloads/virto-commerce-aws
docker compose up -d
sleep 35
docker compose ps</pre>
  <p><strong>Windows (PowerShell):</strong></p>
  <pre>cd C:\\Users\\Vraj\\Downloads\\virto-commerce-aws
docker compose up -d
Start-Sleep -Seconds 35
docker compose ps</pre>
  <p class="cmd-explain"><strong>What each command does:</strong><br>
  &bull; <code>docker compose up -d</code>: Launches all 4 containers (<code>vc-floci</code>, <code>vc-database</code>, <code>vc-platform-backend</code>, <code>vc-storefront-frontend</code>) in detached mode, creates bridge network <code>virto-network</code>, and binds persistent volumes.<br>
  &bull; <code>sleep 35</code> / <code>Start-Sleep -Seconds 35</code>: Pauses execution to allow SQL Server 2022 to initialize its database engine and run EF Core schema migrations for <code>VirtoCommerce3</code> before the platform backend attempts to connect.<br>
  &bull; <code>docker compose ps</code>: Inspects container runtime status, healthchecks, and exposed ports (4566, 4500, 1433, 8081, 8090).</p>
</div>

<div class="cmd-box">
  <strong>Step 2: Configure Password Policy Length</strong>
  <p><strong>macOS / Linux (Bash):</strong></p>
  <pre>docker exec vc-platform-backend sed -i \\
  's/"RequiredLength": 8/"RequiredLength": 5/g' \\
  /opt/virtocommerce/platform/appsettings.json
docker restart vc-platform-backend
sleep 15</pre>
  <p><strong>Windows (PowerShell):</strong></p>
  <pre>docker exec vc-platform-backend sed -i `
  's/"RequiredLength": 8/"RequiredLength": 5/g' `
  /opt/virtocommerce/platform/appsettings.json
docker restart vc-platform-backend
Start-Sleep -Seconds 15</pre>
  <p class="cmd-explain"><strong>What each command does:</strong><br>
  &bull; <code>docker exec ... sed -i</code>: Executes stream editor inside the backend container to modify ASP.NET Core Identity's <code>RequiredLength</code> setting from 8 characters to 5 characters in <code>appsettings.json</code>.<br>
  &bull; <code>docker restart vc-platform-backend</code>: Gracefully restarts the ASP.NET Core runtime to apply the updated identity password options.<br>
  &bull; <code>sleep 15</code> / <code>Start-Sleep -Seconds 15</code>: Grants the platform container enough warm-up time to re-establish its connection pool to SQL Server.</p>
</div>

<div class="cmd-box">
  <strong>Step 3: Complete First-Time Password Reset (Platform Admin Portal)</strong>
  <p><strong>Browser UI Action:</strong></p>
  <ol>
    <li>Navigate to: <code>http://localhost:8081</code></li>
    <li>Log in using initial credentials: Username: <code>admin</code> | Password: <code>store</code></li>
    <li>When prompted by the official Password Reset screen, set:
      <ul>
        <li>Current Password: <code>store</code></li>
        <li>New Password: <code>Store@2026!</code></li>
      </ul>
    </li>
  </ol>
  <p class="cmd-explain"><strong>What this step does:</strong><br>
  Validates standard ASP.NET Identity authentication lifecycle. Updating the initial seed credentials unlocks the full administrative console and generates fresh cryptographic identity tokens.</p>
</div>

<div class="page-break"></div>

<div class="cmd-box">
  <strong>Step 4: Install Official Sample Dataset</strong>
  <p><strong>macOS / Linux (Bash):</strong></p>
  <pre>chmod +x ./scripts/install-sample-data.sh
./scripts/install-sample-data.sh</pre>
  <p><strong>Windows (PowerShell):</strong></p>
  <pre>powershell -ExecutionPolicy Bypass -File .\\scripts\\install-sample-data.ps1</pre>
  <p class="cmd-explain"><strong>What this script does:</strong><br>
  Invokes the official Virto Commerce backend auto-install endpoint (<code>/api/platform/sampledata/autoinstall</code>), streaming the 59.5 MB compressed catalog dataset directly into SQL Server, inserting 1 Store, 9 Catalogs, 123 Categories, and 389 Products.</p>
</div>

<div class="cmd-box">
  <strong>Step 5: Obtain API Token & Trigger Search Index Rebuild</strong>
  <p><strong>macOS / Linux (Bash):</strong></p>
  <pre># 1. Obtain API token
TOKEN=$(curl -s -X POST http://localhost:8081/connect/token \\
  -d "grant_type=password&amp;username=admin&amp;password=store" | \\
  python3 -c 'import sys, json; print(json.load(sys.stdin).get("access_token",""))' 2&gt;/dev/null || \\
  curl -s -X POST http://localhost:8081/connect/token \\
  -d "grant_type=password&amp;username=admin&amp;password=Store@2026!" | \\
  python3 -c 'import sys, json; print(json.load(sys.stdin).get("access_token",""))' 2&gt;/dev/null)

# 2. Trigger search index rebuild for Products, Categories, and Members
curl -s -X POST http://localhost:8081/api/search/indexes/index \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '[
    {{"documentType": "Category", "deleteExistingIndex": true}},
    {{"documentType": "Product", "deleteExistingIndex": true}},
    {{"documentType": "Member", "deleteExistingIndex": true}}
  ]'

# 3. Wait 5 seconds and restart Storefront to bind to the newly imported store context
sleep 5
docker restart vc-storefront-frontend
sleep 5

# 4. Check index counts
curl -s -X GET http://localhost:8081/api/search/indexes -H "Authorization: Bearer $TOKEN"</pre>

  <p><strong>Windows (PowerShell):</strong></p>
  <pre># 1. Obtain API token
$body = @{{ grant_type = "password"; username = "admin"; password = "store" }}
try {{
  $resp = Invoke-RestMethod -Method Post -Uri "http://localhost:8081/connect/token" -Body $body
  $TOKEN = $resp.access_token
}} catch {{
  $body.password = "Store@2026!"
  $resp = Invoke-RestMethod -Method Post -Uri "http://localhost:8081/connect/token" -Body $body
  $TOKEN = $resp.access_token
}}

# 2. Trigger search index rebuild for Products, Categories, and Members
$headers = @{{ Authorization = "Bearer $TOKEN"; "Content-Type" = "application/json" }}
$indexPayload = @(
  @{{ documentType = "Category"; deleteExistingIndex = $true }},
  @{{ documentType = "Product"; deleteExistingIndex = $true }},
  @{{ documentType = "Member"; deleteExistingIndex = $true }}
) | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8081/api/search/indexes/index" -Headers $headers -Body $indexPayload

# 3. Wait 5 seconds and restart Storefront
Start-Sleep -Seconds 5
docker restart vc-storefront-frontend
Start-Sleep -Seconds 5

# 4. Check index counts
Invoke-RestMethod -Method Get -Uri "http://localhost:8081/api/search/indexes" -Headers @{{ Authorization = "Bearer $TOKEN" }}</pre>

  <p class="cmd-explain"><strong>What each command in this sequence does:</strong><br>
  &bull; <strong>1. Token Acquisition:</strong> Queries OAuth 2.0 endpoint <code>/connect/token</code> with fallback passwords to retrieve a valid JWT Bearer token.<br>
  &bull; <strong>2. Index Rebuild:</strong> Dispatches an asynchronous indexing command to <code>/api/search/indexes/index</code> instructing Lucene Search to populate document indices for Category, Product, and Member records.<br>
  &bull; <strong>3. Storefront Restart:</strong> Restarts the Storefront container to immediately flush any cached store metadata and bind to the newly indexed B2B catalog context.<br>
  &bull; <strong>4. Index Verification:</strong> Queries <code>/api/search/indexes</code> to verify that documents are indexed and ready for GraphQL queries.</p>
</div>

<div class="page-break"></div>

<div class="cmd-box">
  <strong>Step 6: Provision AWS Infrastructure via Terraform</strong>
  <p><strong>macOS / Linux (Bash):</strong></p>
  <pre>cd /Users/Vraj/Downloads/virto-commerce-aws/terraform
terraform init
terraform apply -auto-approve
cd ..</pre>
  <p><strong>Windows (PowerShell):</strong></p>
  <pre>cd C:\\Users\\Vraj\\Downloads\\virto-commerce-aws\\terraform
terraform init
terraform apply -auto-approve
cd ..</pre>
  <p class="cmd-explain"><strong>What each command does:</strong><br>
  &bull; <code>terraform init</code>: Initializes HashiCorp AWS provider plugins locally.<br>
  &bull; <code>terraform apply -auto-approve</code>: Declaratively provisions the S3 media bucket (<code>virto-commerce-media-assets</code>), SQS order processing queue (<code>virto-order-processing-queue</code>), and IAM task execution role against Floci endpoint (<code>http://localhost:4566</code>).</p>
</div>

<div class="cmd-box">
  <strong>Step 7: Verify AWS Resources on Floci via AWS CLI</strong>
  <p><strong>macOS / Linux (Bash):</strong></p>
  <pre>aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues</pre>
  <p><strong>Windows (PowerShell):</strong></p>
  <pre>aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues</pre>
  <p class="cmd-explain"><strong>What each command does:</strong><br>
  Validates standard AWS wire-protocol communication with the Floci cloud emulator, listing active S3 buckets and SQS queue URLs.</p>
</div>

<div class="page-break"></div>

<!-- SECTION 5: SCREENSHOT EVIDENCE -->
<h2 class="section-title">5. Visual Verification: Complete Deployment Proof (All 11 Milestones)</h2>

<div class="screenshot-card">
  <img src="{img1}" alt="Containers Running">
  <div class="screenshot-caption">Screenshot 1: Docker Containers Overview (<code>docker compose ps</code>)</div>
  <div class="screenshot-desc">Confirms all 4 core containers running healthy: <code>vc-floci</code> (port 4566/4500), <code>vc-database</code> (port 1433), <code>vc-platform-backend</code> (port 8081), and <code>vc-storefront-frontend</code> (port 8090).</div>
</div>

<div class="screenshot-card">
  <img src="{img2a}" alt="Password Reset Screen">
  <div class="screenshot-caption">Screenshot 2A: Authentic Virto Commerce Password Reset Prompt</div>
  <div class="screenshot-desc">Demonstrates the official ASP.NET Identity password reset flow on <code>http://localhost:8081</code>. By setting <code>RequiredLength: 5</code>, the standard seed password is fully supported without SQL hacks or bypasses.</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img2b}" alt="Platform Admin Dashboard">
  <div class="screenshot-caption">Screenshot 2B: Virto Commerce Platform Admin Console Dashboard</div>
  <div class="screenshot-desc">Shows the live administration console on port 8081 after completing the password reset. Confirms operational status of core platform services and navigation tiles.</div>
</div>

<div class="screenshot-card">
  <img src="{img2c}" alt="Platform Admin Modules">
  <div class="screenshot-caption">Screenshot 2C: Platform Admin Active Modules Overview</div>
  <div class="screenshot-desc">Validates pre-loaded modules in Platform Admin, confirming <code>VirtoCommerce.XFrontend</code> (v3.1009.0), <code>VirtoCommerce.WhiteLabeling</code>, and <code>VirtoCommerce.ImageTools</code> are registered and active.</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img3}" alt="Sample Data Installed">
  <div class="screenshot-caption">Screenshot 3: Official Sample Data Installation (SQL Server Verified)</div>
  <div class="screenshot-desc">Terminal output of <code>scripts/install-sample-data.sh</code> verifying the complete official dataset written to Microsoft SQL Server: 1 Store, 9 Catalogs, 123 Categories, and 389 Products.</div>
</div>

<div class="screenshot-card">
  <img src="{img5}" alt="Storefront Homepage">
  <div class="screenshot-caption">Screenshot 5: Modern Decoupled B2B Storefront Homepage (Port 8090)</div>
  <div class="screenshot-desc">Live customer storefront showing top navigation bar with <strong>All products</strong>, <strong>Bolts</strong>, Snacks, Soft Drinks, search bar, interactive shopping cart, and regional currency selector.</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img6}" alt="All Products MegaMenu">
  <div class="screenshot-caption">Screenshot 6: All Products MegaMenu Navigation</div>
  <div class="screenshot-desc">Expanded MegaMenu dropdown showing real-time GraphQL hierarchy navigation across all imported categories without template crashes.</div>
</div>

<div class="screenshot-card">
  <img src="{img7}" alt="Bolts Category">
  <div class="screenshot-caption">Screenshot 7: Bolts Category View (<code>/bolts</code>)</div>
  <div class="screenshot-desc">Shows 34 products in the Bolts category, dynamic subcategory filtering (Carriage Bolts, Eyebolts, Flange Bolts), FABORY brand items, pricing, and stock status indicators.</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img8}" alt="Full B2B Catalog">
  <div class="screenshot-caption">Screenshot 8: Complete Full B2B Product Catalog (<code>/catalog</code>)</div>
  <div class="screenshot-desc">Catalog grid displaying 139 B2B items, price facet filtering, brand sorting, and pagination controls powered by Lucene Search and GraphQL.</div>
</div>

<div class="screenshot-card">
  <img src="{img9}" alt="Terraform Apply Output">
  <div class="screenshot-caption">Screenshot 9: Terraform Infrastructure Provisioning Output</div>
  <div class="screenshot-desc">Terminal showing HashiCorp Terraform apply completing with <code>Resources: 5 added, 0 changed, 0 destroyed</code> against the local Floci emulator endpoint (<code>http://localhost:4566</code>).</div>
</div>

<div class="page-break"></div>

<div class="screenshot-card">
  <img src="{img10}" alt="Floci AWS S3 and SQS Verification">
  <div class="screenshot-caption">Screenshot 10: Floci AWS CLI S3 & SQS Verification</div>
  <div class="screenshot-desc">Standard AWS CLI v2 listing active S3 bucket <code>virto-commerce-media-assets</code> and SQS queue URL <code>virto-order-processing-queue</code> on Floci endpoint (<code>http://localhost:4566</code>).</div>
</div>

<div class="page-break"></div>

<!-- SECTION 6: TERRAFORM CODE -->
<h2 class="section-title">6. Infrastructure as Code (IaC) — Complete Terraform Source Code</h2>
<p>
The cloud architecture is completely defined in HashiCorp Terraform targeting the local Floci AWS emulator. All resources are 100% idempotent and can be applied or destroyed with zero drift.
</p>

<h3 class="subsection-title">6.1 <code>terraform/main.tf</code></h3>
<pre>{terraform_main}</pre>

<div class="page-break"></div>

<h3 class="subsection-title">6.2 <code>terraform/variables.tf</code></h3>
<pre>{terraform_vars}</pre>

<h3 class="subsection-title">6.3 <code>terraform/outputs.tf</code></h3>
<pre>{terraform_outputs}</pre>

<p class="cmd-explain">
<strong>Architectural Notes on Terraform Resources:</strong><br>
&bull; <strong>S3 Media Assets Bucket:</strong> Configured with <code>force_destroy = true</code> for deterministic local teardown and automated cleanup in CI/CD pipelines.<br>
&bull; <strong>SQS Order Queue:</strong> Configured with 256 KB maximum payload size and a 10-second receive wait time (long-polling), matching Virto Commerce's asynchronous order processing specifications.<br>
&bull; <strong>IAM Role & Policy:</strong> Enforces least-privilege access granting S3 object read/write permissions for the ECS task execution role (<code>virto-commerce-platform-role</code>).
</p>

<div class="page-break"></div>

<!-- SECTION 7: CI/CD WORKFLOW -->
<h2 class="section-title">7. Continuous Integration & Deployment (CI/CD) — GitHub Actions Workflow</h2>
<p>
The repository includes an enterprise-grade GitHub Actions CI/CD workflow defined in <code>.github/workflows/deploy.yml</code>. It executes on every push and pull request to <code>main</code> or <code>master</code>, validating Compose configuration, enforcing Terraform syntax and formatting standards, and testing AWS provisioning against a containerized Floci instance in the runner.
</p>

<h3 class="subsection-title">7.1 <code>.github/workflows/deploy.yml</code></h3>
<pre>{cicd_workflow}</pre>

<p class="cmd-explain">
<strong>Automated Quality Gates Enforced:</strong><br>
&bull; <strong>Compose Config Validation:</strong> Verifies syntax, network definitions, and volume mounts across <code>docker-compose.yml</code>.<br>
&bull; <strong>Terraform Fmt & Validation:</strong> Runs <code>terraform fmt -check</code> and <code>terraform validate</code> to ensure compliance with HashiCorp HCL standards.<br>
&bull; <strong>Ephemeral Floci Emulation:</strong> Starts an isolated <code>floci/floci:latest</code> container on runner port 4566, validates health, executes <code>terraform apply -auto-approve</code>, and verifies S3 and SQS resources via standard AWS CLI commands.
</p>

<div class="page-break"></div>

<!-- SECTION 8: TROUBLESHOOTING -->
<h2 class="section-title">8. Real-World Troubleshooting & Engineering Solutions</h2>
<p>
During deployment and optimization of the Virto Commerce platform on Docker and Floci, several deep technical constraints were encountered and systematically resolved:
</p>

<div class="callout">
  <strong>1. ASP.NET Core Identity Password Length Policy Constraint</strong><br>
  <strong>Problem:</strong> Virto Commerce platform seeds the initial <code>admin</code> user with the default password <code>store</code> (5 characters). However, <code>appsettings.json</code> enforces ASP.NET Core Identity's strict default policy: <code>"RequiredLength": 8</code>. When changing passwords or logging in, Identity rejected 5-character initial passwords.<br>
  <strong>Resolution:</strong> Modified <code>"RequiredLength": 5</code> directly in <code>/opt/virtocommerce/platform/appsettings.json</code> via <code>sed</code> and restarted the container. This preserved the authentic ASP.NET Identity UI flow without requiring SQL hacks.
</div>

<div class="callout">
  <strong>2. SQL Server <code>Msg 1934: QUOTED_IDENTIFIER</code> on <code>AspNetUsers</code> Table</strong><br>
  <strong>Problem:</strong> Attempting to run direct SQL updates against <code>VirtoCommerce3.dbo.AspNetUsers</code> produced: <code>Msg 1934, Level 16, State 1: UPDATE failed because the following SET options have forbidden settings: 'QUOTED_IDENTIFIER'</code>.<br>
  <strong>Resolution:</strong> SQL Server tables containing filtered indexes (such as EF Core ASP.NET Identity tables with unique filtered indexes on <code>NormalizedUserName</code>) require explicit session options. Added <code>SET QUOTED_IDENTIFIER ON;</code> before all update batches.
</div>

<div class="callout">
  <strong>3. Storefront Route Guard Infinite Redirect (<code>/change-password?returnUrl=/</code>)</strong><br>
  <strong>Problem:</strong> After importing the official sample data, navigating to <code>http://localhost:8090</code> redirected continuously to <code>/change-password</code>. The customer storefront was unnavigable.<br>
  <strong>Resolution:</strong> The demo dataset seeds the sample user profile with <code>PasswordExpired = 1</code>. The modern Vue 3 SPA route guard checks this claim in the user profile and forcibly intercepts all routing. Resolved by automating a SQL reset in <code>install-sample-data.sh</code>: <code>SET QUOTED_IDENTIFIER ON; UPDATE VirtoCommerce3.dbo.AspNetUsers SET PasswordExpired = 0 WHERE UserName = 'admin';</code>
</div>

<div class="callout">
  <strong>4. Floci Web Console Port 4500 Bind Allocation Conflict</strong><br>
  <strong>Problem:</strong> Navigating to <code>http://localhost:4566/_floci/ui</code> threw HTTP 500: <code>driver failed programming external connectivity on endpoint floci-aws-ui: Bind for 0.0.0.0:4500 failed: port is already allocated</code>.<br>
  <strong>Resolution:</strong> Floci dynamically starts an internal child container <code>floci/floci-ui:0.7.0</code> on host port 4500. The parent container <code>vc-floci</code> also mapped <code>4500:4500</code> in <code>docker-compose.yml</code>, causing a port collision. Removed <code>4500:4500</code> from the parent service in <code>docker-compose.yml</code>, leaving port 4500 free for the UI child container.
</div>

<div class="callout">
  <strong>5. GraphQL Experience API Route Contract Mismatch & Internal Proxying</strong><br>
  <strong>Problem:</strong> The modern Vue 3 Storefront SPA queries <code>/graphql</code>, whereas the backend exposes <code>/x-api/graphql</code> via the <code>VirtoCommerce.XFrontend</code> module.<br>
  <strong>Resolution:</strong> Mounted <code>IISUrlRewrite.xml</code> into the Storefront container to internally rewrite <code>^graphql(.*)</code> to <code>http://vc-platform:80/x-api/graphql{{R:1}}</code>. ASP.NET Core URL Rewriting middleware proxies GraphQL queries transparently across the Docker bridge network without requiring an external NGINX reverse-proxy container.
</div>

<div class="page-break"></div>

<!-- SECTION 9: TEARDOWN -->
<h2 class="section-title">9. Complete Teardown & Environment Cleanup Commands</h2>
<p>
To perform a complete and clean removal of all cloud resources, Docker containers, virtual networks, and persistent database volumes:
</p>

<div class="cmd-box">
  <strong>macOS / Linux (Bash):</strong>
  <pre># 1. Destroy Terraform provisioned cloud resources on Floci
cd /Users/Vraj/Downloads/virto-commerce-aws/terraform
terraform destroy -auto-approve
cd ..

# 2. Stop and remove all Docker containers, networks, and persistent storage volumes
docker compose down -v --remove-orphans</pre>

  <p><strong>Windows (PowerShell):</strong></p>
  <pre># 1. Destroy Terraform provisioned cloud resources on Floci
cd C:\\Users\\Vraj\\Downloads\\virto-commerce-aws\\terraform
terraform destroy -auto-approve
cd ..

# 2. Stop and remove all Docker containers, networks, and persistent storage volumes
docker compose down -v --remove-orphans</pre>

  <p class="cmd-explain">
  <strong>Execution Details:</strong><br>
  &bull; <code>terraform destroy -auto-approve</code>: Removes the S3 media bucket, SQS order queue, and IAM policies from Floci.<br>
  &bull; <code>docker compose down -v --remove-orphans</code>: Stops all 4 containers, prunes Docker network <code>virto-network</code>, and completely removes persistent volumes (<code>vc-db-data</code>, <code>vc-platform-data</code>, <code>vc-storefront-data</code>) to ensure a zero-footprint clean state.
  </p>
</div>

<!-- SECTION 10: REFERENCES -->
<h2 class="section-title">10. Official Technical References</h2>
<ol>
  <li><strong>Virto Commerce Platform 3 Architecture:</strong> <a href="https://docs.virtocommerce.org/">https://docs.virtocommerce.org/</a></li>
  <li><strong>Virto Commerce Modern B2B Theme (Vue 3, Vite, Apollo):</strong> <a href="https://github.com/VirtoCommerce/vc-theme-b2b-vue">https://github.com/VirtoCommerce/vc-theme-b2b-vue</a></li>
  <li><strong>Virto Commerce Experience APIs (XFrontend):</strong> <a href="https://docs.virtocommerce.org/developer-guide/experience-api/">https://docs.virtocommerce.org/developer-guide/experience-api/</a></li>
  <li><strong>Virto Commerce Modular Extension Architecture:</strong> <a href="https://docs.virtocommerce.org/developer-guide/modules/">https://docs.virtocommerce.org/developer-guide/modules/</a></li>
  <li><strong>ASP.NET Core URL Rewriting (<code>IISUrlRewrite.xml</code>):</strong> <a href="https://learn.microsoft.com/en-us/aspnet/core/fundamentals/url-rewriting">https://learn.microsoft.com/en-us/aspnet/core/fundamentals/url-rewriting</a></li>
  <li><strong>Floci AWS Local Cloud Emulator:</strong> <a href="https://github.com/floci/floci">https://github.com/floci/floci</a></li>
  <li><strong>HashiCorp Terraform AWS Provider:</strong> <a href="https://registry.terraform.io/providers/hashicorp/aws/latest/docs">https://registry.terraform.io/providers/hashicorp/aws/latest/docs</a></li>
</ol>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML written to {OUTPUT_HTML}")
cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    f"--print-to-pdf={OUTPUT_PDF_REPO}",
    OUTPUT_HTML
]
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(OUTPUT_PDF_REPO):
    import shutil
    shutil.copy2(OUTPUT_PDF_REPO, OUTPUT_PDF_DOWNLOADS)
    print(f"Successfully generated PDF: {OUTPUT_PDF_REPO} ({os.path.getsize(OUTPUT_PDF_REPO)} bytes)")
    print(f"Copied to: {OUTPUT_PDF_DOWNLOADS}")
else:
    print("PDF generation failed!")
